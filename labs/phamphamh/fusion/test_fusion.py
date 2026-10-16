"""Les cas de la section 6 du découpage, côté fusion. Lancer : python3 -m unittest test_fusion (depuis ce dossier)."""
import copy, json, os, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fusion import fusionner, charger, regrouper_heuristique  # noqa: E402

DEMO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "demo")
RESUMES = charger([os.path.join(DEMO, "resumes")])
ONB = json.load(open(os.path.join(DEMO, "onboarding.json")))


def texte(ins):
    return json.dumps(ins, ensure_ascii=False)


class Fusion(unittest.TestCase):
    def test_cas_normal(self):
        ins = fusionner(RESUMES, ONB)
        self.assertEqual(ins["statut"], "ok")
        self.assertEqual(ins["participants"], 5)
        self.assertGreaterEqual(len(ins["taches"]), 3)
        top = ins["taches"][0]
        self.assertGreater(top["cout_par_mois"], 0)
        self.assertTrue(top["preuves"])

    def test_non_valide_absent(self):
        ins = fusionner(RESUMES, ONB)
        self.assertEqual(ins["non_valides"], 1)
        self.assertNotIn("tournées", texte(ins))  # tâche du salarié qui n'a pas validé
        self.assertNotIn("Google Maps", texte(ins))

    def test_moins_de_3_validations(self):
        r = copy.deepcopy(RESUMES)
        for x in r[2:]:
            x["valide_par_la_personne"] = False
        ins = fusionner(r, ONB)
        self.assertEqual(ins["statut"], "pas_assez")
        self.assertNotIn("taches", ins)

    def test_aucun_identifiant_de_personne(self):
        t = texte(fusionner(RESUMES, ONB))
        for r in RESUMES:
            self.assertNotIn(r["personne"], t)

    def test_agregats_sous_3_personnes_fondus(self):
        ins = fusionner(RESUMES, ONB)
        for ligne in ins["temps_par_app"] + ins["temps_par_categorie"]:
            if not ligne.get("regroupe"):
                self.assertGreaterEqual(ligne["personnes"], 3)
        self.assertNotIn("Zendesk", [l["app"] for l in ins["temps_par_app"]])  # une seule personne l'utilise
        for o in ins["usage_ia"]:
            if o["outil"] != "Autres outils d'IA":
                self.assertNotEqual(o["personnes"], "moins de 3")
        for t in ins["taches"]:
            if t["nb_personnes"] is None:
                self.assertEqual(t["personnes"], "moins de 3")

    def test_resume_sans_tache(self):
        r = copy.deepcopy(RESUMES)
        r[0]["taches"] = []
        r[0]["heures_captees"] = 0.3
        ins = fusionner(r, ONB)
        self.assertEqual(ins["statut"], "ok")

    def test_tout_le_monde_sans_tache(self):
        r = copy.deepcopy(RESUMES)
        for x in r:
            x["taches"] = []
        ins = fusionner(r, ONB)
        self.assertEqual(ins["taches"], [])
        self.assertEqual(ins["chiffres"]["gain_top3_par_mois"], 0)

    def test_correction_du_salarie_change_le_classement(self):
        avant = fusionner(RESUMES, ONB)
        r = copy.deepcopy(RESUMES)
        for x in r:
            for t in x["taches"]:
                if "commande" in t["titre"].lower():
                    t["automatisable"] = {"score": 10, "pourquoi": "il faut connaître les clients", "corrige_par_la_personne": "Pas automatisable"}
        apres = fusionner(r, ONB)
        self.assertIn("commande", avant["a_automatiser"][0].lower())
        self.assertNotIn("commande", apres["a_automatiser"][0].lower())

    def test_jamais_deux_taches_dune_meme_personne_ensemble(self):
        taches = [{"titre": "Relancer un devis", "apps": ["Gmail"], "_personne": "p0"},
                  {"titre": "Relancer les devis", "apps": ["Gmail"], "_personne": "p0"},
                  {"titre": "Relance devis", "apps": ["Gmail"], "_personne": "p1"}]
        g = regrouper_heuristique(taches, [], [])
        for grp in g["taches"]:
            self.assertEqual(len({taches[i]["_personne"] for i in grp["membres"]}), len(grp["membres"]))

    def test_vrai_resume_produit_par_la_brique_B(self):
        """Le format de resume.py (preuves en horaires, apps avec caractères invisibles) passe sans erreur."""
        r = copy.deepcopy(RESUMES[:3])
        r[0]["temps_par_app"].append({"app": "‎WhatsApp", "minutes": 4})
        ins = fusionner(r, ONB)
        self.assertNotIn("‎", texte(ins))


if __name__ == "__main__":
    unittest.main()
