#!/usr/bin/env python3
"""Écrit donnees.json pour l'écran « D'où viennent les données » : les 6 salariés du back-office d'Atelier Nova
(prénoms inventés, rôle, volumes) et un extrait brut de ce que l'IA a lu. Aucun nom d'annotateur réel.
Usage : python3 -I construire_donnees.py   (lit donnees/nova/, généré par labs/adamaass/wonderbread/wb_salaries.py)"""
import json, os
ICI = os.path.dirname(os.path.abspath(__file__))
NOVA = os.path.join(ICI, "..", "..", "..", "donnees", "nova")
EQUIPE = ["lea", "karim", "sophie", "nadia", "julien", "emma"]  # le back-office d'adamaass (fusion nova-backoffice.json)
personnes, extrait = [], []
for p in EQUIPE:
    d = json.load(open(os.path.join(NOVA, p, "moments.json")))
    s = d["stats"]
    personnes.append({"prenom": p.capitalize().replace("Lea", "Léa"), "role": s["role"], "minutes": s["minutes_travail"],
                      "captures": s["captures_regardees"], "moments": s["moments"]})
    if p == "sophie":
        ms = d["moments"]
        i = next(k for k, m in enumerate(ms) if "REPORTS" in (m.get("texte_nouveau") or ""))
        extrait = [{"heure": m["debut"][11:19], "fenetre": m["fenetre"], "action": m["texte_nouveau"]} for m in ms[i:i + 7]]
out = {"source": {"nom": "WONDERBREAD", "qui": "Stanford (NeurIPS 2024)", "licence": "CC-BY-4.0", "demos": 2929,
                  "lien": "https://hazyresearch.stanford.edu/wonderbread-website"},
       "boutique": "back-office Magento de WebArena (Carnegie Mellon)", "echelle": 10, "personnes": personnes,
       "captures": sum(p["captures"] for p in personnes), "minutes": sum(p["minutes"] for p in personnes), "extrait": extrait}
json.dump(out, open(os.path.join(ICI, "donnees.json"), "w"), ensure_ascii=False, indent=1)
print(out["captures"], "captures,", out["minutes"], "min ;", len(extrait), "lignes d'extrait")
