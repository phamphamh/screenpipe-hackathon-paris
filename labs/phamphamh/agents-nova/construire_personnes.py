#!/usr/bin/env python3
"""Les 6 salariés du back-office et LEURS workflows, calculés sur les vraies données → personnes.json.

Pour chaque personne (donnees/nova/<p>/verite.json : les intentions réelles de ses démos WONDERBREAD, cf.
labs/adamaass/wonderbread/wb_salaries.py), on classe chaque intention dans un des 3 agents déployés (mêmes motifs
que demandes.json) : nombre de fois sur la semaine, minutes passées, étapes observées (nova-backoffice.json) et une
vraie demande de CETTE personne faisable avec boutique.py (sinon une de demandes.json).
Usage : python3 labs/phamphamh/agents-nova/construire_personnes.py
"""
import json, os, re
from datetime import datetime

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(ICI)))
# prénoms et rôles inventés (wb_salaries.py) : les vrais annotateurs ne sortent jamais
PERSONNES = [("lea", "Léa", "Responsable e-commerce"), ("karim", "Karim", "Gestionnaire catalogue"),
             ("sophie", "Sophie", "Analyste ventes"), ("nadia", "Nadia", "Service client (back-office)"),
             ("julien", "Julien", "Commandes et logistique"), ("emma", "Emma", "Marketing et promotions")]
AGENTS = {  # agent → (nom, tâche observée, motif qui classe une intention)
    "prix-produit": ("Prix produit", "t1", r"(reduce|increase) the price of"),
    "rapport-ventes": ("Rapport de ventes", "t2", r"report|best-selling"),
    "commandes-annulees": ("Commandes annulées", "t5", r"(?<!non-)cancell?ed|canlled|cancellations"),
}
# demandes faisables avec boutique.py qui ne sont pas dans demandes.json (traduction pour l'écran)
EN_PLUS = {
    "What is the top-1 best-selling product in 2022": "Quel est le produit le plus vendu en 2022 ?",
    "What are the top-5 best-selling product in 2023": "Quels sont les 5 produits les plus vendus en 2023 ?",
    "What are the top-2 best-selling product in 2022": "Quels sont les 2 produits les plus vendus en 2022 ?",
    "Lookup orders that are canceled": "Retrouver les commandes annulées",
    "Get the customer name of the most recent cancelled order": "Quel client a passé la commande annulée la plus récente ?",
}


def main():
    demandes = json.load(open(os.path.join(ICI, "demandes.json")))["agents"]
    taches = {t["id"]: t for t in json.load(open(os.path.join(RACINE, "labs", "adamaass", "exemples", "nova-backoffice.json")))["taches"]}
    sortie = []
    for pid, prenom, role in PERSONNES:
        verite = json.load(open(os.path.join(RACINE, "donnees", "nova", pid, "verite.json")))
        workflows = []
        for agent, (nom, tache, motif) in AGENTS.items():
            siennes = [v for v in verite if re.search(motif, v["intention"], re.I) and not v["intention"].startswith("Cancel order")]
            if not siennes:
                continue
            secondes = sum((datetime.fromisoformat(v["fin"]) - datetime.fromisoformat(v["debut"])).total_seconds() for v in siennes)
            intentions = {v["intention"] for v in siennes}
            connues = {d["intention"]: d["fr"] for d in demandes[agent]} | EN_PLUS
            choix = next(((i, connues[i]) for i in list(connues) if i in intentions), None)  # la sienne, faisable
            en, fr = choix or (demandes[agent][0]["intention"], demandes[agent][0]["fr"])
            workflows.append({"agent": agent, "nom": nom, "fois": len(siennes), "minutes": round(secondes / 60, 1),
                              "etapes": [e["texte"] for e in taches[tache]["etapes"]][:6],
                              "demande": {"en": en, "fr": fr, "sienne": bool(choix)}})
        workflows.sort(key=lambda w: -w["fois"])
        sortie.append({"id": pid, "prenom": prenom, "role": role, "workflows": workflows})
    json.dump(sortie, open(os.path.join(ICI, "personnes.json"), "w"), ensure_ascii=False, indent=1)
    return sortie


if __name__ == "__main__":
    for p in main():
        print(p["prenom"], [(w["agent"], w["fois"], w["minutes"], w["demande"]["en"][:50]) for w in p["workflows"]])
