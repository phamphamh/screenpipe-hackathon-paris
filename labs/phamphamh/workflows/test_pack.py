"""Tests du moteur de pack de workflows.  Lancer : cd labs/phamphamh/workflows && python3 -m unittest test_pack -v"""
import json, os, shutil, tempfile, unittest
from unittest import mock

import pack as P

THESE = {"id": "test", "nom": "Test", "autonomie": 2, "humain": "valide avant envoi",
         "tests_avant": ["rejouer sur la 2e entrée"], "suivi_apres": ["temps gagné mesuré"]}
THESE_SIMPLE = {**THESE, "tests_avant": ["relire le SKILL.md"]}  # n'exige pas de 2e entrée


def etape(type_, texte, app="Gmail", statut="observé"):
    return {"type": type_, "texte": texte, "app": app, "statut": statut}


COMMANDE = {
    "titre": "Saisir une commande reçue par mail dans l'ERP", "frequence_par_semaine": 6, "duree_moyenne_min": 12,
    "apps": ["Gmail", "Sage"],
    "etapes": [etape("input", "Ouvrir le bon de commande PDF reçu par mail"),
               etape("action", "Créer la commande et saisir les lignes article par article", "Sage"),
               etape("check", "Vérifier le stock et le prix négocié", "Sage"),
               etape("output", "Répondre au client avec le numéro de commande")],
    "exceptions": ["référence inconnue → appel au commercial"],
    "goulots": [{"type": "switching", "detail": "recopier chaque ligne du PDF dans Sage"}],
    "preuves": [{"debut": "2026-10-13T09:00:00+02:00", "fin": "2026-10-13T09:12:00+02:00", "app": "Gmail"}],
}
RELANCE = {
    "titre": "Relancer les devis sans réponse", "frequence_par_semaine": 10, "duree_moyenne_min": 8, "apps": ["HubSpot", "Gmail"],
    "etapes": [etape("input", "Filtrer les devis envoyés il y a plus de 7 jours", "HubSpot"),
               etape("output", "Envoyer le mail de relance depuis un modèle"),
               etape("decision", "Ne pas relancer si le client a déjà répondu", statut="supposé")],
    "exceptions": ["client sans email → appel"],
    "preuves": [{"debut": "2026-10-12T10:00:00+02:00", "fin": "2026-10-12T10:08:00+02:00", "app": "HubSpot"}],
}


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def gen(self, tache, these=THESE_SIMPLE, **kw):
        return P.generer(tache, these, sortie=self.tmp, **kw)

    def skill(self, d):
        return P.lire_txt(os.path.join(d, "SKILL.md"))


class Generer(Base):
    def test_tache_normale(self):
        d = self.gen(COMMANDE)
        md = self.skill(d)
        self.assertTrue(md.startswith("---\nname: saisir-une-commande-recue-par-mail-dans-l-erp\ndescription: "))
        for s in ("## Déclencheur", "## Outils et apps", "## Étapes", "## Exceptions", "## Garde-fous", "## Ne jamais faire", "Sage", "Gmail"):
            self.assertIn(s, md)
        self.assertEqual(len(P.lignes_etapes(md)), 4)
        tests = P.lire_json(os.path.join(d, "tests.json"))
        self.assertGreaterEqual(len(tests["cas"]), 3)  # référence + preuves + exception
        r = P.tester(d)
        self.assertEqual(r["verdict"], "pret", r["echecs"])
        self.assertEqual(r["couverture_etapes"], 1.0)

    def test_tache_sans_decision(self):
        md = self.skill(self.gen(COMMANDE))
        # niveau 2 : seule la sortie (l'envoi) porte un point humain, pas de « décision »
        self.assertNotIn("— décision :", md)
        self.assertEqual(sum(P.MARQUE_HUMAIN in l for l in P.lignes_etapes(md)), 1)

    def test_decisions_point_humain_selon_autonomie(self):
        for a in (1, 2, 3):
            d = P.generer(RELANCE, {**THESE_SIMPLE, "autonomie": a}, sortie=os.path.join(self.tmp, str(a)))
            ligne = [l for l in P.lignes_etapes(self.skill(d)) if "déjà répondu" in l][0]
            self.assertIn(P.MARQUE_HUMAIN, ligne, f"autonomie {a}")
            self.assertEqual(P.tester(d)["verdict"], "pret")
        d4 = P.generer(RELANCE, {**THESE_SIMPLE, "autonomie": 4}, sortie=os.path.join(self.tmp, "4"))
        ligne = [l for l in P.lignes_etapes(self.skill(d4)) if "déjà répondu" in l][0]
        self.assertNotIn(P.MARQUE_HUMAIN, ligne)

    def test_decision_sans_point_humain_detectee(self):
        d = self.gen(RELANCE)  # autonomie 2
        md = self.skill(d).replace(P.MARQUE_HUMAIN, "Point")  # quelqu'un (ou l'IA) a retiré le point humain
        P.ecrire_txt(os.path.join(d, "SKILL.md"), md)
        r = P.tester(d)
        self.assertEqual(r["verdict"], "a_revoir")
        self.assertTrue(any("sans point de validation humaine" in e["raison"] for e in r["echecs"]))

    def test_tache_une_etape(self):
        t = {"titre": "Préparer les tournées de livraison", "frequence_par_semaine": 5, "duree_moyenne_min": 30,
             "apps": ["Excel"], "etapes": [etape("action", "Répartir les livraisons par zone", "Excel")]}
        d = self.gen(t)
        self.assertEqual(len(P.lignes_etapes(self.skill(d))), 1)
        r = P.tester(d, [{"etapes": t["etapes"], "apps": ["Excel"]}])
        self.assertEqual(r["verdict"], "pret", r["echecs"])

    def test_etapes_supposees_signalees(self):
        d = self.gen(RELANCE)
        md = self.skill(d)
        self.assertIn("## À confirmer avant d'automatiser", md)
        self.assertIn("supposé, à confirmer", md)
        self.assertEqual(P.lire_json(os.path.join(d, "workflow.json"))["etapes_supposees"], ["Ne pas relancer si le client a déjà répondu"])

    def test_tache_sans_etape_refusee(self):
        with self.assertRaises(ValueError) as c:
            self.gen({"titre": "Vide", "etapes": []})
        self.assertIn("pas assez de données", str(c.exception))

    def test_these_invalide(self):
        with self.assertRaises(ValueError):
            self.gen(COMMANDE, {**THESE, "autonomie": 7})

    def test_ia_degrade_sans_claude(self):
        with mock.patch.object(P.shutil, "which", return_value=None):
            d = self.gen(COMMANDE, ia=True)
        ia = P.lire_json(os.path.join(d, "workflow.json"))["ia"]
        self.assertFalse(ia["utilise"])
        self.assertIn("introuvable", ia["raison"])
        self.assertTrue(os.path.exists(os.path.join(d, "SKILL.md")))


class Tester(Base):
    def test_deuxieme_entree_couvre(self):
        d = self.gen(COMMANDE, THESE)
        autre = {**COMMANDE, "titre": "Saisie des commandes mail dans Sage"}
        r = P.tester(d, [autre])
        self.assertEqual(r["verdict"], "pret", r["echecs"])
        self.assertTrue(r["deuxieme_entree"])

    def test_deuxieme_entree_ne_couvre_pas(self):
        d = self.gen(COMMANDE, THESE)
        autre = {"titre": "Saisie des commandes", "apps": ["Gmail", "Pennylane"],
                 "etapes": COMMANDE["etapes"] + [etape("action", "Archiver le bon de commande dans Pennylane", "Pennylane")],
                 "exceptions": ["client bloqué pour impayé → refus"]}
        r = P.tester(d, [autre])
        raisons = " | ".join(e["raison"] for e in r["echecs"])
        self.assertEqual(r["verdict"], "a_revoir")
        self.assertIn("Archiver le bon de commande", raisons)
        self.assertIn("Pennylane", raisons)
        self.assertIn("client bloqué", raisons)
        self.assertLess(r["couverture_etapes"], 1.0)

    def test_these_exige_2e_entree(self):
        d = self.gen(COMMANDE, THESE)
        r = P.tester(d)  # seulement les preuves de la personne elle-même
        self.assertEqual(r["verdict"], "a_revoir")
        self.assertTrue(any("2e entrée" in e["raison"] for e in r["echecs"]))

    def test_entree_vide_pas_assez_de_donnees(self):
        sans_preuve = {k: v for k, v in COMMANDE.items() if k != "preuves"}
        d = self.gen(sans_preuve)
        for entrees in ([], [{}], None):
            r = P.tester(d, entrees)
            self.assertEqual(r["verdict"], "a_revoir")
            self.assertEqual(r["message"], "pas assez de données")

    def test_app_pas_confondue_avec_un_mot(self):
        # « Sage » ne doit pas être trouvée dans « message »
        t = {**COMMANDE, "apps": ["Gmail"], "goulots": [], "etapes": [etape("output", "Envoyer le message au client")]}
        d = self.gen(t)
        r = P.tester(d, [{"etapes": t["etapes"], "apps": ["Sage"]}])
        self.assertTrue(any("« Sage »" in e["raison"] for e in r["echecs"]))


class Deployer(Base):
    def test_refus_si_a_revoir(self):
        d = self.gen(COMMANDE, THESE)
        P.tester(d)  # a_revoir : pas de 2e entrée
        r = P.deployer(d, "equipe", racine=self.tmp)
        self.assertFalse(r["deploye"])
        self.assertIn("refusé", r["raison"])
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "labs")))

    def test_refus_si_jamais_teste(self):
        r = P.deployer(self.gen(COMMANDE), "local-demo", racine=self.tmp, poste="x")
        self.assertFalse(r["deploye"])
        self.assertIn("jamais testée", r["raison"])

    def test_forcer(self):
        d = self.gen(COMMANDE, THESE)
        P.tester(d)
        r = P.deployer(d, "equipe", forcer=True, racine=self.tmp)
        self.assertTrue(r["deploye"])
        self.assertTrue(r["force"])

    def test_cibles_equipe_et_local_demo(self):
        d = self.gen(COMMANDE)
        P.tester(d)
        eq = P.deployer(d, "equipe", racine=self.tmp)
        lo = P.deployer(d, "local-demo", racine=self.tmp, poste="Poste Démo")
        nom = "saisir-une-commande-recue-par-mail-dans-l-erp"
        dest_eq = os.path.join(self.tmp, "labs", "phamphamh", "workflows", "deployes", nom)
        dest_lo = os.path.join(self.tmp, "donnees", "deploiement", "poste-demo", "skills", nom)
        for dest, r in ((dest_eq, eq), (dest_lo, lo)):
            self.assertTrue(r["deploye"], r)
            self.assertTrue(os.path.isfile(os.path.join(dest, "SKILL.md")))
            recu = P.lire_json(os.path.join(dest, "deploiement.json"))
            self.assertEqual(recu["these"]["id"], "test")
            self.assertEqual(recu["autonomie"], 2)
            self.assertEqual(recu["tests"]["verdict"], "pret")
            self.assertFalse(recu["force"])
        self.assertEqual(lo["poste"], "poste-demo")
        self.assertFalse(P.deployer(d, "prod", racine=self.tmp)["deploye"])

    def test_jamais_dans_dot_claude(self):
        d = self.gen(COMMANDE)
        P.tester(d)
        faux_home = os.path.join(self.tmp, "home")
        with mock.patch.object(P.os.path, "expanduser", return_value=os.path.join(faux_home, ".claude")):
            r = P.deployer(d, "local-demo", racine=faux_home.replace("home", "home/.claude/x"), poste="p")
        self.assertFalse(r["deploye"])
        self.assertIn("~/.claude", r["raison"])


class Pack(Base):
    def resume(self, personne, taches, valide=True):
        return {"personne": personne, "taches": taches, "valide_par_la_personne": valide}

    def test_pack_trie_par_gain_et_2e_entree(self):
        autre = {**COMMANDE, "titre": "Saisie des commandes mail dans Sage", "frequence_par_semaine": 25, "duree_moyenne_min": 10}
        res = P.pack([self.resume("a", [COMMANDE, RELANCE]), self.resume("b", [autre]),
                      self.resume("c", [RELANCE], valide=False)], THESE, sortie=self.tmp)
        self.assertEqual([l["titre"] for l in res][0], "Saisir une commande reçue par mail dans l'ERP")
        top = res[0]
        for k in ("id", "titre", "heures_semaine", "gain_estime_h", "autonomie", "verdict", "couverture", "chemin_skill"):
            self.assertIn(k, top)
        self.assertEqual(top["personnes"], 2)  # le résumé non validé de « c » est ignoré
        self.assertEqual(top["verdict"], "pret", top["echecs"])
        self.assertAlmostEqual(top["heures_semaine"], (6 * 12 + 25 * 10) / 60, places=2)
        self.assertAlmostEqual(top["gain_estime_h"], top["heures_semaine"] * 0.5, places=2)
        relance = [l for l in res if l["titre"].startswith("Relancer")][0]
        self.assertEqual(relance["verdict"], "a_revoir")  # personne d'autre (validée) ne la fait

    def test_pack_vide(self):
        self.assertEqual(P.pack([], THESE, sortie=self.tmp), [])


if __name__ == "__main__":
    unittest.main()
