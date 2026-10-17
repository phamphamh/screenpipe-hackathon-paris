#!/usr/bin/env python3
"""Tests du garde-fou : python3 test_approbations.py  (aucun appel à Claude, quelques secondes)."""
import json, os, shutil, subprocess, sys, tempfile, unittest

ICI = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
LIGNES = json.dumps([{"ref": "REF-1042", "qte": 24, "prix": 3.10}])


class Garde(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="test-approb-")
        self.addCleanup(shutil.rmtree, self.tmp)
        shutil.copy(os.path.join(ICI, "bac_a_sable.py"), self.tmp)  # comme le fait tester_en_vrai.py : rien d'autre
        with open(os.path.join(ICI, "scenarios", "saisie-commande.json"), encoding="utf-8") as f:
            self.etat = json.load(f)["cas"][0]["etat"]

    def ecrire_etat(self, garde):
        if garde:
            self.etat["politique"] = {"approbation_requise": ["gmail envoyer", "sage valider-commande"]}
        with open(os.path.join(self.tmp, "etat.json"), "w", encoding="utf-8") as f:
            json.dump(self.etat, f)

    def agent(self, *args):
        return subprocess.run([PY, "bac_a_sable.py", *args], cwd=self.tmp, capture_output=True, text=True)

    def humain(self, *args):
        return subprocess.run([PY, os.path.join(ICI, "approbations.py"), "-d", self.tmp, *args], capture_output=True, text=True)

    def etat_final(self):
        with open(os.path.join(self.tmp, "etat.json"), encoding="utf-8") as f:
            return json.load(f)

    def audit(self):
        with open(os.path.join(self.tmp, "audit.jsonl"), encoding="utf-8") as f:
            return [json.loads(l) for l in f]

    def test_sans_politique_rien_ne_change(self):
        self.ecrire_etat(garde=False)
        self.agent("sage", "creer-commande", "Bistrot", LIGNES)
        self.agent("sage", "valider-commande", "CV-1001")
        self.agent("gmail", "envoyer", "a@b.fr", "objet", "corps")
        e = self.etat_final()
        self.assertEqual(e["sage"]["commandes"][0]["statut"], "validee")
        self.assertEqual(len(e["gmail"]["envoyes"]), 1)
        self.assertNotIn("approbations", e)

    def test_avec_garde_les_actions_sensibles_attendent(self):
        self.ecrire_etat(garde=True)
        self.agent("sage", "creer-commande", "Bistrot", LIGNES)
        sortie = self.agent("sage", "valider-commande", "CV-1001").stdout
        self.agent("gmail", "envoyer", "a@b.fr", "objet", "corps")
        self.agent("gmail", "brouillon", "a@b.fr", "objet", "corps")
        e = self.etat_final()
        self.assertIn("PAS été exécuté", sortie)
        self.assertEqual(e["sage"]["commandes"][0]["statut"], "brouillon")  # créer = autorisé, valider = en attente
        self.assertEqual(e["gmail"]["envoyes"], [])
        self.assertEqual(len(e["gmail"]["brouillons"]), 1)
        self.assertEqual([d["statut"] for d in e["approbations"]], ["en_attente", "en_attente"])

    def test_l_agent_ne_peut_pas_s_approuver(self):
        self.ecrire_etat(garde=True)
        self.agent("gmail", "envoyer", "a@b.fr", "objet", "corps")
        for appel in (["approbations", "approuver", "A-1"], ["approuver", "A-1"], ["gmail", "approuver", "A-1"]):
            r = self.agent(*appel)
            self.assertEqual(r.returncode, 1, appel)
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "approbations.py")))
        self.assertEqual(self.etat_final()["gmail"]["envoyes"], [])

    def test_approuver_execute_et_trace_qui(self):
        self.ecrire_etat(garde=True)
        self.agent("sage", "creer-commande", "Bistrot", LIGNES)
        self.agent("sage", "valider-commande", "CV-1001")
        r = self.humain("approuver", "A-1", "--par", "Marie")
        self.assertEqual(r.returncode, 0, r.stdout)
        e = self.etat_final()
        self.assertEqual(e["sage"]["commandes"][0]["statut"], "validee")
        self.assertEqual((e["approbations"][0]["statut"], e["approbations"][0]["par"]), ("approuvee", "Marie"))
        dernier = self.audit()[-1]
        self.assertEqual((dernier["acteur"], dernier["statut"], dernier["par"], dernier["demande"]),
                         ("humain", "approuvee", "Marie", "A-1"))

    def test_refuser_n_execute_rien_et_garde_le_motif(self):
        self.ecrire_etat(garde=True)
        self.agent("gmail", "envoyer", "a@b.fr", "objet", "corps")
        self.humain("refuser", "A-1", "--par", "Marie", "--motif", "mauvais destinataire")
        self.assertEqual(self.etat_final()["gmail"]["envoyes"], [])
        dernier = self.audit()[-1]
        self.assertEqual((dernier["statut"], dernier["motif"]), ("refusee", "mauvais destinataire"))

    def test_pas_de_decision_sans_nom_ni_deux_fois(self):
        self.ecrire_etat(garde=True)
        self.agent("gmail", "envoyer", "a@b.fr", "objet", "corps")
        self.assertNotEqual(self.humain("approuver", "A-1").returncode, 0)          # --par obligatoire
        self.assertNotEqual(self.humain("approuver", "A-1", "--par", " ").returncode, 0)
        self.assertEqual(self.humain("approuver", "A-1", "--par", "Marie").returncode, 0)
        r = self.humain("approuver", "A-1", "--par", "Paul")
        self.assertEqual(r.returncode, 1)
        self.assertIn("déjà tranchée", r.stdout)
        self.assertEqual(len(self.etat_final()["gmail"]["envoyes"]), 1)

    def test_journal_lisible_et_bilan_juste(self):
        self.ecrire_etat(garde=True)
        self.agent("gmail", "recus")
        self.agent("sage", "creer-commande", "Bistrot", LIGNES)
        self.agent("sage", "valider-commande", "CV-1001")
        self.agent("gmail", "envoyer", "a@b.fr", "objet", "corps")
        self.humain("approuver", "A-1", "--par", "Marie")
        j = self.humain("journal").stdout
        self.assertIn("**Marie** (humain)", j)
        self.assertNotIn("gmail recus", j)                       # les lectures sont masquées par défaut
        self.assertIn("gmail recus", self.humain("journal", "--tout").stdout)
        self.assertIn("1 action(s) de l'agent exécutée(s) directement, 2 mise(s) en attente → 1 approuvée(s), 0 refusée(s), "
                      "1 encore en attente (A-2)", j)


if __name__ == "__main__":
    unittest.main(verbosity=1)
