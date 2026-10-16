"""Brique B du Wrapped : transforme les moments d'une personne (brique A) en résumé « tâches répétées » au format commun.

Un seul appel à Claude, via Claude Code (`claude -p`) : pas de clé API à gérer, chacun a déjà Claude.
Seuls les moments triés partent dans le prompt, jamais les captures. Le résultat reste dans donnees/ jusqu'à la relecture.
Usage : python3 resume.py donnees/moi/moments.json [--pseudo anonyme-1] [--modele sonnet]
"""
import argparse, json, os, re, subprocess, sys, tempfile
from urllib.parse import urlparse

CONSIGNE = """Tu analyses les moments de travail d'UNE personne, captés par screenpipe (une ligne par moment :
début-fin | minutes | app | fenêtre | site | texte nouveau apparu à l'écran).
Trouve ses TÂCHES RÉPÉTÉES : des activités qui reviennent (plusieurs moments, souvent plusieurs apps), pas juste « utilise Chrome ».
Règles strictes :
- N'invente rien. Chaque tâche cite ses moments sources (numéros #) dans "preuves". Si c'est une déduction, mets "statut": "supposé".
- Une tâche = au moins 2 moments distincts. Sinon, ne la mets pas.
- Des libellés concrets et courts, en français. Pas de nom de client, d'email ou de montant dans les libellés.
- "frequence_par_semaine" : extrapole seulement si la période fait moins d'une semaine, et dis-le dans "limites".
- Les étapes utilisent les types action, input, output, decision et check (vocabulaire screenpipe).
Réponds UNIQUEMENT avec ce JSON, sans texte autour :
{"temps_par_categorie":[{"categorie":str,"minutes":num}],
 "usage_ia":[{"outil":str,"minutes":num,"usages":[str]}],
 "taches":[{"titre":str,"frequence_par_semaine":num,"duree_moyenne_min":num,"apps":[str],
   "etapes":[{"type":"action|input|output|decision|check","texte":str,"app":str,"statut":"observé|supposé"}],
   "exceptions":[str],"goulots":[{"type":"waiting|switching|rework|handoff|unclear","detail":str}],
   "automatisable":{"score":0-100,"pourquoi":str},"confiance":0-1,"preuves":[int]}],
 "limites":[str]}"""

def ligne(i, m):
    site = urlparse(m["url"]).netloc if m["url"] else ""
    return f"#{i} {m['debut'][11:16]}-{m['fin'][11:16]} | {m['minutes']} | {m['app']} | {m['fenetre'][:80]} | {site} | {m['texte_nouveau'][:300]}"

def main():
    a = argparse.ArgumentParser(); a.add_argument("moments"); a.add_argument("--pseudo", default="anonyme")
    a.add_argument("--modele", default="sonnet"); args = a.parse_args()
    d = json.load(open(args.moments)); st = d["stats"]
    ms = [m for m in d["moments"] if not m["hors_travail"] and m["minutes"] >= 0.2]
    if st["minutes_travail"] < 30:
        sys.exit("Moins de 30 min de travail capté : pas assez de données, aucune tâche n'est inventée.")
    entree = "\n".join(ligne(i, m) for i, m in enumerate(ms))
    r = subprocess.run(["claude", "-p", "--model", args.modele, "--no-session-persistence"],
                       input=CONSIGNE + "\n\nLES MOMENTS :\n" + entree, capture_output=True, text=True, timeout=900,
                       cwd=tempfile.gettempdir())  # hors du dépôt : sinon les hooks et consignes de l'équipe se déclenchent
    bloc = re.search(r"\{.*\}", r.stdout, re.S)
    if r.returncode or not bloc:
        sys.exit(f"Claude n'a pas rendu de JSON : {r.stderr[:500] or r.stdout[:500]}")
    ia = json.loads(bloc.group(0))
    for t in ia.get("taches", []):  # les preuves deviennent des horaires vérifiables, plus des numéros
        t["preuves"] = [{"debut": ms[i]["debut"], "fin": ms[i]["fin"], "app": ms[i]["app"]} for i in t.get("preuves", []) if isinstance(i, int) and 0 <= i < len(ms)]
    resume = {"personne": args.pseudo, "periode": st["periode"], "heures_captees": round(st["minutes_travail"] / 60, 1),
              "temps_par_app": [{"app": k, "minutes": v} for k, v in st["minutes_par_app"].items() if v >= 1],
              **ia, "tri_80_20": {"captures_regardees": st["captures_regardees"], "captures_gardees": st["captures_cles"], "part": st["part_gardee"]},
              "valide_par_la_personne": False}
    out = os.path.join(os.path.dirname(args.moments), "resume.json")
    json.dump(resume, open(out, "w"), ensure_ascii=False, indent=1)
    print(f"{len(resume.get('taches', []))} tâches répétées → {out} (à relire avant tout partage)")
    for t in resume.get("taches", []):
        print(f"- {t['titre']} : {t.get('frequence_par_semaine')}×/sem, ~{t.get('duree_moyenne_min')} min, automatisable {t.get('automatisable', {}).get('score')}/100, {len(t['preuves'])} preuves")

if __name__ == "__main__":
    main()
