"""Après la brique B (salariés fictifs Nova) : fréquence = occurrences observées dans la semaine,
écrans visités par tâche (routes d'URL sans identifiants), puis résumé « validé pour la démo ».
Usage : python3 -I wb_post.py <dossier nova> pseudo1,pseudo2,..."""
import json, os, re, sys
from collections import Counter
from datetime import datetime
from urllib.parse import urlparse

def route(u):
    p = urlparse(u).path
    p = re.sub(r"/(key|id|order_id|product_id|customer_id)/[^/]+", r"/\1/:x", p)
    p = re.sub(r"/\d+(?=/|$)", "/:n", p)
    p = re.sub(r"/[0-9a-f]{20,}(?=/|$)", "/:h", p)
    return p.rstrip("/") or "/"

base = sys.argv[1]
for p in sys.argv[2].split(","):
    d = os.path.join(base, p)
    r = json.load(open(os.path.join(d, "resume.json")))
    v = json.load(open(os.path.join(d, "verite.json")))
    ms = {m["debut"]: m for m in json.load(open(os.path.join(d, "moments.json")))["moments"]}
    iv = [(datetime.fromisoformat(x["debut"]), datetime.fromisoformat(x["fin"]), i) for i, x in enumerate(v)]
    for t in r["taches"]:
        occ = set()
        for pr in t["preuves"]:
            x = datetime.fromisoformat(pr["debut"])
            occ |= {i for a, b, i in iv if a <= x <= b}
        t.setdefault("frequence_par_semaine_modele", t.get("frequence_par_semaine"))
        t["frequence_par_semaine"] = len(occ)
        t["ecrans"] = [k for k, _ in Counter(route(ms[pr["debut"]]["url"]) for pr in t["preuves"] if pr["debut"] in ms).most_common(5)]
    lim = [l if isinstance(l, str) else l.get("texte", str(l)) for l in r.get("limites", [])]
    for ajout in ("Fréquence = nombre de fois où la tâche a été observée sur la semaine (preuves), recalculée : la brique B ne voit que l'heure des moments, pas la date.",
                  "Salarié fictif construit à partir de WONDERBREAD (Stanford, CC-BY-4.0)."):
        if ajout not in lim:
            lim.append(ajout)
    r["limites"] = lim
    json.dump(r, open(os.path.join(d, "resume.json"), "w"), ensure_ascii=False, indent=1)
    val = dict(r, valide_par_la_personne=True, relecture={"note": "salarié fictif : validé pour la démo, sans relecture humaine"})
    json.dump(val, open(os.path.join(d, "resume-valide.json"), "w"), ensure_ascii=False, indent=1)
    print(p, len(r["taches"]), "tâches ·", [(t["titre"][:32], t["frequence_par_semaine"]) for t in r["taches"]][:4])
