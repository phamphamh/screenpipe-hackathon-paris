"""Fabrique une entreprise FICTIVE (Maison Corvo, 48 salariés) pour montrer le Wrapped sans les données de personne.

6 salariés invités : 5 ont validé leur résumé, 1 non (il ne doit pas apparaître). Les résumés suivent le contrat commun
(produit/decoupage.md, section 5), comme s'ils sortaient de la brique B puis de la relecture.
Usage : python3 generer.py   → écrit demo/resumes/*.json et demo/onboarding.json
"""
import json, os
from datetime import datetime, timedelta

ICI = os.path.dirname(os.path.abspath(__file__))
DEBUT = datetime.fromisoformat("2026-10-12T09:00:00+02:00")  # lundi


def e(typ, texte, app, statut="observé"):
    return {"type": typ, "texte": texte, "app": app, "statut": statut}


def tache(titre, freq, duree, apps, etapes, score, pourquoi, goulots=(), exceptions=(), confiance=0.8, jour=0, heure=9):
    preuves = []
    for k in range(min(4, max(1, round(freq / 3)))):  # quelques horaires vérifiables, répartis sur la semaine
        d = DEBUT + timedelta(days=(jour + k) % 5, hours=heure - 9 + (k * 2) % 7, minutes=(k * 17) % 50)
        preuves.append({"debut": d.isoformat(), "fin": (d + timedelta(minutes=duree)).isoformat(), "app": apps[k % len(apps)]})
    return {"titre": titre, "frequence_par_semaine": freq, "duree_moyenne_min": duree, "apps": apps, "etapes": etapes,
            "exceptions": list(exceptions), "goulots": [{"type": t, "detail": d} for t, d in goulots],
            "automatisable": {"score": score, "pourquoi": pourquoi}, "confiance": confiance, "preuves": preuves}


RELANCE = lambda freq, duree, j: tache(
    "Relancer les devis sans réponse", freq, duree, ["HubSpot", "Gmail"],
    [e("input", "Filtrer les devis envoyés il y a plus de 7 jours", "HubSpot"), e("action", "Copier le contact et le numéro du devis", "HubSpot"),
     e("output", "Envoyer le mail de relance depuis un modèle", "Gmail"), e("decision", "Ne pas relancer si le client a déjà répondu", "Gmail", "supposé")],
    82, "Mêmes étapes à chaque fois, une seule décision simple.", [("switching", "copier-coller HubSpot → Gmail à chaque relance")],
    ["client sans email → appel"], 0.85, j, 10)

COMMANDE = lambda titre, freq, duree, j: tache(
    titre, freq, duree, ["Gmail", "Sage"],
    [e("input", "Ouvrir le bon de commande PDF reçu par mail", "Gmail"), e("action", "Créer la commande et saisir les lignes article par article", "Sage"),
     e("check", "Vérifier le stock et le prix négocié", "Sage"), e("output", "Répondre au client avec le numéro de commande", "Gmail")],
    78, "Le PDF a toujours la même structure ; la saisie ligne à ligne est mécanique.",
    [("switching", "recopier chaque ligne du PDF dans Sage"), ("rework", "erreurs de référence corrigées après coup")],
    ["référence inconnue → appel au commercial"], 0.8, j, 9)

FICHE = lambda freq, j: tache(
    "Chercher la fiche technique d'un produit", freq, 4, ["Google Drive", "Google Chrome"],
    [e("input", "Recevoir une question client sur un produit", "Gmail"), e("action", "Chercher la fiche dans le Drive ou sur le site du fabricant", "Google Drive"),
     e("output", "Envoyer la fiche ou la réponse au client", "Gmail")],
    70, "Une base de fiches interrogeable répondrait à la place.", [("waiting", "fiches rangées dans 3 dossiers différents")], (), 0.75, j, 11)

REPORTING = lambda titre, duree, apps, j: tache(
    titre, 1, duree, apps,
    [e("input", "Exporter les chiffres de la semaine", apps[0]), e("action", "Coller dans le tableau et recalculer les totaux", "Excel"),
     e("output", "Envoyer le tableau à la direction", apps[-1])],
    74, "Export et calculs identiques chaque semaine ; seul le commentaire est humain.",
    [("rework", "formules cassées après le collage, refaites à la main")], (), 0.8, 4, 16)

DELAI = lambda freq, apps, j: tache(
    "Répondre aux demandes de délai de livraison", freq, 6, apps,
    [e("input", "Lire la demande du client", apps[0]), e("action", "Chercher la commande puis le suivi transporteur", "Sage"),
     e("output", "Répondre avec la date estimée", apps[0])],
    68, "Le suivi transporteur est consultable automatiquement.", [("switching", "Sage → site du transporteur → mail")], (), 0.75, j, 14)

PERSONNES = [
    ("anonyme-1", 5, 31.5, True,
     [RELANCE(10, 8, 0), COMMANDE("Saisir une commande reçue par mail dans l'ERP", 6, 12, 1), FICHE(15, 0),
      REPORTING("Préparer le reporting hebdo des ventes", 50, ["HubSpot", "Excel", "Gmail"], 4)],
     {"Relation client": 600, "Commandes et devis": 520, "Reporting": 50, "Réunions": 410, "Mails internes": 310},
     {"Gmail": 640, "HubSpot": 520, "Sage": 160, "Google Chrome": 330, "Excel": 70, "Google Meet": 170},
     [("ChatGPT", 70, ["reformuler des mails", "traduire une fiche produit"])]),
    ("anonyme-2", 5, 33.0, True,
     [RELANCE(14, 7, 1),
      tache("Créer un devis à partir d'une demande mail", 8, 18, ["Gmail", "Sage", "Excel"],
            [e("input", "Lire la demande du client", "Gmail"), e("action", "Chercher les prix et les remises du client", "Excel"),
             e("decision", "Choisir la remise à proposer", "Excel", "supposé"), e("output", "Créer le devis dans Sage et l'envoyer", "Sage")],
            76, "Les champs du devis se remplissent à partir du mail.", [("switching", "Gmail → Excel → Sage")], ["demande floue → appel"], 0.7, 0, 10),
      FICHE(12, 2), REPORTING("Reporting hebdo des ventes", 40, ["HubSpot", "Excel", "Slack"], 4)],
     {"Relation client": 720, "Commandes et devis": 640, "Reporting": 40, "Réunions": 300, "Mails internes": 280},
     {"Gmail": 700, "HubSpot": 450, "Sage": 300, "Excel": 220, "Slack": 140, "Google Chrome": 170},
     [("ChatGPT", 95, ["rédiger des devis", "reformuler des mails"]), ("Claude", 20, ["résumer un appel d'offres"])]),
    ("anonyme-3", 5, 34.5, True,
     [COMMANDE("Saisie des commandes mail dans Sage", 25, 10, 0), DELAI(20, ["Gmail", "Sage", "Site transporteur"], 1),
      RELANCE(5, 6, 3), REPORTING("Mettre à jour le reporting hebdo", 60, ["Sage", "Excel", "Gmail"], 4)],
     {"Commandes et devis": 1020, "Relation client": 480, "Reporting": 60, "Réunions": 150, "Mails internes": 360},
     {"Sage": 920, "Gmail": 760, "Excel": 160, "Site transporteur": 120, "HubSpot": 50, "Google Chrome": 60},
     [("ChatGPT", 25, ["corriger l'orthographe"])]),
    ("anonyme-4", 3, 19.5, True,
     [tache("Rapprocher les factures fournisseurs des bons de commande", 30, 6, ["Pennylane", "Sage"],
            [e("input", "Ouvrir la facture fournisseur", "Pennylane"), e("check", "Retrouver le bon de commande et comparer les montants", "Sage"),
             e("decision", "Valider ou signaler un écart", "Pennylane")],
            72, "La comparaison des montants est mécanique ; seuls les écarts demandent un humain.",
            [("switching", "Pennylane ↔ Sage pour chaque facture")], ["écart de prix → mail au fournisseur"], 0.8, 0, 9),
      tache("Relancer les factures impayées", 10, 10, ["Pennylane", "Gmail"],
            [e("input", "Lister les factures échues", "Pennylane"), e("output", "Envoyer la relance", "Gmail"),
             e("decision", "Appeler les clients importants plutôt que d'écrire", "Gmail", "supposé")],
            65, "Relance écrite automatisable ; le choix d'appeler reste humain.", [("waiting", "attente des retours clients")], (), 0.55, 1, 15),
      REPORTING("Préparer le reporting hebdo de trésorerie", 45, ["Pennylane", "Excel", "Gmail"], 2)],
     {"Comptabilité": 760, "Reporting": 45, "Réunions": 150, "Mails internes": 210},
     {"Pennylane": 610, "Sage": 230, "Excel": 160, "Gmail": 170},
     [("Copilot", 30, ["formules Excel"]), ("ChatGPT", 15, ["rédiger une relance"])]),
    ("anonyme-5", 5, 30.0, True,
     [tache("Traiter une demande de retour produit", 12, 15, ["Zendesk", "Sage", "Gmail"],
            [e("input", "Lire le ticket et les photos du client", "Zendesk"), e("check", "Vérifier la garantie dans Sage", "Sage"),
             e("decision", "Accepter ou refuser le retour", "Zendesk"), e("output", "Créer le bon de retour et prévenir le client", "Gmail")],
            45, "La décision d'accepter demande du jugement ; la préparation peut être automatisée.",
            [("handoff", "validation du responsable pour les retours de plus de 500 €")], ["produit hors garantie → devis de réparation"], 0.7, 0, 10),
      DELAI(15, ["Zendesk", "Sage", "Site transporteur"], 1), FICHE(10, 3)],
     {"Relation client": 1050, "Commandes et devis": 120, "Réunions": 200, "Mails internes": 250},
     {"Zendesk": 820, "Sage": 380, "Gmail": 260, "Site transporteur": 140, "Google Drive": 90},
     [("ChatGPT", 40, ["rédiger des réponses clients"])]),
    ("anonyme-6", 5, 28.0, False,  # n'a pas validé : ne doit apparaître nulle part
     [tache("Préparer les tournées de livraison", 5, 40, ["Excel", "Google Maps"], [e("action", "Placer les livraisons sur la carte", "Google Maps")],
            80, "Optimisation de tournée classique.", (), (), 0.7)],
     {"Logistique": 900}, {"Excel": 500, "Google Maps": 400}, [("ChatGPT", 10, ["calcul"])]),
]


def main():
    os.makedirs(os.path.join(ICI, "resumes"), exist_ok=True)
    for pid, nb_jours, heures, valide, taches, cats, apps, ia in PERSONNES:
        r = {"campagne": "demo-maison-corvo", "personne": pid,
             "periode": {"debut": DEBUT.isoformat(), "fin": (DEBUT + timedelta(days=nb_jours - 1, hours=9)).isoformat()},
             "heures_captees": heures,
             "temps_par_app": [{"app": a, "minutes": m} for a, m in apps.items()],
             "temps_par_categorie": [{"categorie": c, "minutes": m} for c, m in cats.items()],
             "usage_ia": [{"outil": o, "minutes": m, "usages": u} for o, m, u in ia],
             "taches": taches,
             "limites": (["Seulement 3 jours captés : les fréquences hebdomadaires sont extrapolées."] if nb_jours < 5 else [])
                        + ["Données fictives : entreprise de démonstration."],
             "tri_80_20": {"captures_regardees": int(heures * 360), "captures_gardees": int(heures * 360 * 0.24), "part": 0.24},
             "valide_par_la_personne": valide}
        json.dump(r, open(os.path.join(ICI, "resumes", f"{pid}.json"), "w"), ensure_ascii=False, indent=1)
    onboarding = {"entreprise": "Maison Corvo", "activite": "Distribution de matériel de cuisine professionnelle, 48 salariés",
                  "priorites": ["Répondre plus vite aux clients", "Moins de saisie manuelle", "Fiabiliser le reporting"],
                  "cout_horaire": 42, "outils": ["Gmail", "HubSpot", "Sage", "Pennylane", "Zendesk", "Excel"],
                  "irritants": "On passe nos journées à recopier des commandes et à relancer des devis."}
    json.dump(onboarding, open(os.path.join(ICI, "onboarding.json"), "w"), ensure_ascii=False, indent=1)
    print(f"{len(PERSONNES)} résumés fictifs + onboarding écrits dans {ICI}")


if __name__ == "__main__":
    main()
