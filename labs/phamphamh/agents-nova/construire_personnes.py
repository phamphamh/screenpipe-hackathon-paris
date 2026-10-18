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
PERSONNES = [("lea", "Léa", "Responsable e-commerce", "E-commerce manager"),
             ("karim", "Karim", "Gestionnaire catalogue", "Catalog manager"),
             ("sophie", "Sophie", "Analyste ventes", "Sales analyst"),
             ("nadia", "Nadia", "Service client (back-office)", "Customer service (back office)"),
             ("julien", "Julien", "Commandes et logistique", "Orders and logistics"),
             ("emma", "Emma", "Marketing et promotions", "Marketing and promotions")]
# versions anglaises (démo devant le jury) : nom du workflow et étapes observées, dans l'ordre de nova-backoffice.json
EN = {
    "prix-produit": ("Product pricing", [
        "Open the Products catalog and search the product by keyword",
        "Pick the variant to change in the results (size/color)",
        "Type the new value (price or quantity) in the product form",
        "Save the product",
        "Go back to the list and repeat for each variant",
        "Check that every variant is saved"]),
    "rapport-ventes": ("Sales report", [
        "Open a report (Bestsellers, Orders or Order Count) in the Reports menu",
        "Enter the start and end dates and pick the granularity (day)",
        "For the Orders report, pick an order status (e.g. Payment Review)",
        "Run the report (Show Report or Refresh)",
        "Scroll through the results to read them",
        "Run it again with another period or report if needed"]),
    "commandes-annulees": ("Cancelled orders", [
        "Open Sales > Orders",
        "Open Filters and select the Canceled status",
        "Apply the filters",
        "Sort by Purchase Date",
        "Browse the list of cancelled orders (scrolling)",
        "Open an order's details or go to the customer page"]),
}
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


CATEGORIES_EN = {"prix-produit": "Product price", "rapport-ventes": "Sales report", "commandes-annulees": "Cancelled orders"}
ECRANS = [("reports", "Reports"), ("sales/order", "Orders"), ("sales/", "Sales"), ("catalog/product", "Catalog"),
          ("catalog", "Catalog"), ("customer", "Customers"), ("review", "Reviews"), ("dashboard", "Dashboard"),
          ("sales_rule", "Promotions"), ("catalog_rule", "Promotions"), ("cms", "Content")]


def ecran(m):
    """Écran du back-office d'après l'URL (sinon le titre de la fenêtre)."""
    chemin = (m.get("url") or "").split("/admin/", 1)[-1]
    for motif, nom in ECRANS:
        if chemin.startswith(motif) or f"/{motif}" in chemin:
            return nom
    titre = [t.strip() for t in (m.get("fenetre") or "").split("/") if t.strip() and t.strip() != "Magento Admin"]
    return titre[-1] if titre else "Other"


def activite(pid, verite):
    """L'activité réelle de la semaine (moments.json), chaque moment classé par la démo qui le contient (verite.json)."""
    moments = json.load(open(os.path.join(RACINE, "donnees", "nova", pid, "moments.json")))["moments"]
    demos = []
    for v in verite:
        cat = next((CATEGORIES_EN[a] for a, (_, _, motif) in AGENTS.items()
                    if re.search(motif, v["intention"], re.I) and not v["intention"].startswith("Cancel order")),
                   "Other back-office work")
        demos.append((datetime.fromisoformat(v["debut"]), datetime.fromisoformat(v["fin"]), cat))
    jours, rep, fois, ecrans = {}, {}, {}, {}
    for _, _, cat in demos:
        fois[cat] = fois.get(cat, 0) + 1
    for m in moments:
        t = datetime.fromisoformat(m["debut"])
        cat = next((c for d, f, c in demos if d <= t < f), "Other back-office work")
        jour = t.strftime("%a")
        jours[jour] = jours.get(jour, 0) + m["minutes"]
        rep[cat] = rep.get(cat, 0) + m["minutes"]
        e = ecran(m)
        ecrans[e] = ecrans.get(e, 0) + m["minutes"]
    ordre = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return {
        "minutes": round(sum(m["minutes"] for m in moments), 1), "captures": sum(m.get("captures", 0) for m in moments),
        "moments": len(moments),
        "jours": [{"jour": j, "minutes": round(jours[j], 1)} for j in ordre if j in jours],
        "repartition": sorted([{"nom_en": c, "minutes": round(rep.get(c, 0), 1), "fois": fois.get(c, 0)}
                               for c in set(rep) | set(fois)], key=lambda x: -x["minutes"]),
        "ecrans_top": [{"ecran": e, "minutes": round(mn, 1)} for e, mn in sorted(ecrans.items(), key=lambda x: -x[1])[:4]],
    }


def main():
    demandes = json.load(open(os.path.join(ICI, "demandes.json")))["agents"]
    taches = {t["id"]: t for t in json.load(open(os.path.join(RACINE, "labs", "adamaass", "exemples", "nova-backoffice.json")))["taches"]}
    sortie = []
    for pid, prenom, role, role_en in PERSONNES:
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
            workflows.append({"agent": agent, "nom": nom, "nom_en": EN[agent][0], "fois": len(siennes), "minutes": round(secondes / 60, 1),
                              "etapes": [e["texte"] for e in taches[tache]["etapes"]][:6], "etapes_en": EN[agent][1],
                              "demande": {"en": en, "fr": fr, "sienne": bool(choix)}})
        workflows.sort(key=lambda w: -w["fois"])
        sortie.append({"id": pid, "prenom": prenom, "role": role, "role_en": role_en, "workflows": workflows,
                       "activite": activite(pid, verite)})
    json.dump(sortie, open(os.path.join(ICI, "personnes.json"), "w"), ensure_ascii=False, indent=1)
    return sortie


if __name__ == "__main__":
    for p in main():
        print(p["prenom"], [(w["agent"], w["fois"], w["minutes"], w["demande"]["en"][:50]) for w in p["workflows"]])
