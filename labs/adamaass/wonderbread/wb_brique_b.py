"""Brique B sans `claude -p` : même consigne, même entrée, même post-traitement que labs/phamphamh/resume/resume.py.
  prompt  <moments.json>                 → écrit prompt.txt à côté (CONSIGNE + moments, exactement comme resume.py)
  finir   <moments.json> <reponse.json> <pseudo> → écrit resume.json à côté (preuves → horaires, stats, comme resume.py)
"""
import json, os, re, sys

DEPOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(DEPOT, "labs", "phamphamh", "resume"))
import resume as B  # noqa: E402  (CONSIGNE et ligne() d'origine, main() n'est pas lancé)

def moments_retenus(chemin):
    d = json.load(open(chemin))
    return d, [m for m in d["moments"] if not m["hors_travail"] and m["minutes"] >= 0.2]

mode, chemin = sys.argv[1], sys.argv[2]
d, ms = moments_retenus(chemin)
if mode == "prompt":
    entree = "\n".join(B.ligne(i, m) for i, m in enumerate(ms))
    open(os.path.join(os.path.dirname(chemin), "prompt.txt"), "w").write(B.CONSIGNE + "\n\nLES MOMENTS :\n" + entree)
    print(os.path.basename(os.path.dirname(chemin)), len(ms), "moments,", len(entree), "caractères")
else:
    st = d["stats"]
    bloc = re.search(r"\{.*\}", open(sys.argv[3]).read(), re.S)
    ia = json.loads(bloc.group(0))
    for t in ia.get("taches", []):
        t["preuves"] = [{"debut": ms[i]["debut"], "fin": ms[i]["fin"], "app": ms[i]["app"]} for i in t.get("preuves", []) if isinstance(i, int) and 0 <= i < len(ms)]
    resume = {"personne": sys.argv[4], "periode": st["periode"], "heures_captees": round(st["minutes_travail"] / 60, 1),
              "temps_par_app": [{"app": k, "minutes": v} for k, v in st["minutes_par_app"].items() if v >= 1],
              **ia, "tri_80_20": {"captures_regardees": st["captures_regardees"], "captures_gardees": st["captures_cles"], "part": st["part_gardee"]},
              "valide_par_la_personne": False}
    json.dump(resume, open(os.path.join(os.path.dirname(chemin), "resume.json"), "w"), ensure_ascii=False, indent=1)
    print(sys.argv[4], len(resume.get("taches", [])), "tâches")
