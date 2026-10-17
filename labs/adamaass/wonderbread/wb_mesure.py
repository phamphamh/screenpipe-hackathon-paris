"""Mesure simple vs la vérité terrain WONDERBREAD : pour chaque tâche trouvée par la brique B, on prend les SOP
humains des démos que couvrent ses preuves, on extrait les éléments d'interface cités entre guillemets
(« Reports », « Show Report »…, sans les valeurs saisies), et on compte ceux que nos étapes nomment aussi.
Usage : python3 -I wb_mesure.py <dossier nova> pseudo1,pseudo2,..."""
import json, os, re, sys
from collections import Counter
from datetime import datetime

base = sys.argv[1]
def termes(sop):
    out = set()
    for t in re.findall(r'"([^"]{2,40})"', sop):
        t = t.strip().lower()
        if re.search(r"\d", t) or len(t.split()) > 4:  # valeurs saisies, dates, phrases : pas des éléments d'interface
            continue
        out.add(t)
    return out

lignes, tot_t, tot_ok, par_tache = [], 0, 0, []
for p in sys.argv[2].split(","):
    r = json.load(open(os.path.join(base, p, "resume.json")))
    v = json.load(open(os.path.join(base, p, "verite.json")))
    iv = [(datetime.fromisoformat(x["debut"]), datetime.fromisoformat(x["fin"]), x) for x in v]
    for t in r["taches"]:
        demos = {}
        for pr in t["preuves"]:
            d = datetime.fromisoformat(pr["debut"])
            for a, b, x in iv:
                if a <= d <= b:
                    demos[x["debut"]] = x
        if not demos:
            continue
        nos = " ".join(e["texte"] for e in t.get("etapes", [])).lower()
        ref = set().union(*(termes(x["sop"]) for x in demos.values()))
        if not ref:
            continue
        ok = {x for x in ref if x in nos}
        tot_t += len(ref); tot_ok += len(ok)
        modeles = Counter(x["modele"] for x in demos.values())
        par_tache.append((p, t["titre"], len(demos), len(ok), len(ref), modeles.most_common(1)[0]))
print(f"Éléments d'interface des SOP humains retrouvés dans nos étapes : {tot_ok}/{tot_t} = {tot_ok / max(tot_t, 1):.0%}")
par_tache.sort(key=lambda x: -x[2])
for p, titre, n, ok, ref, (mod, k) in par_tache[:12]:
    print(f"  {p:7s} {ok:2d}/{ref:2d} ({ok / ref:.0%}) · {n:2d} démos · {titre[:48]}  ← « {mod[:55]} » ×{k}")
pures = [x for x in par_tache if x[5][1] / x[2] >= 0.8]
print(f"Tâches dont ≥ 80 % des démos ont le même modèle d'intention (bien isolées) : {len(pures)}/{len(par_tache)}")
