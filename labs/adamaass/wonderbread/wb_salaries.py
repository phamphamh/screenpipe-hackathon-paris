"""WONDERBREAD -> salariés fictifs d'« Atelier Nova », au format de sortie de la brique A (moments.json).

Chaque salarié = les démos d'UN annotateur réel sur UN site, posées sur la semaine du 13 au 17/10/2026.
Ce que voit la brique B : titre d'onglet, chemin d'URL, actions (clic sur tel texte, saisie de telle valeur).
Ce qu'elle ne voit PAS : l'intention ni le SOP (gardés à part dans verite.json, pour mesurer après).
Usage : python3 -I wb_salaries.py <dossier wonderbread> <dossier de sortie>
"""
import glob, json, os, random, re, sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

base, sortie = sys.argv[1], sys.argv[2]
PARIS = timezone(timedelta(hours=2))
RACINE = os.path.join(base, "traces", "demos_sop_and_trace_only")
APPS = {"shopping_admin": "Magento (back-office)", "gitlab": "GitLab", "reddit": "Forum Nova", "shopping": "Boutique en ligne"}
# (pseudo, rôle, annotateur réel — préfixe, site) ; les vrais noms ne sortent jamais de ce script
SALARIES = [
    ("lea", "Responsable e-commerce", "Sud", "shopping_admin"),
    ("karim", "Gestionnaire catalogue", "Krr", "shopping_admin"),
    ("sophie", "Analyste ventes", "Ish", "shopping_admin"),
    ("hugo", "Développeur", "Mig", "gitlab"),
    ("ines", "Développeuse", "Tib", "gitlab"),
    ("theo", "Développeur", "Jos", "gitlab"),
    ("malik", "Community manager", "Jus", "reddit"),
    ("camille", "Service client", "Var", "shopping"),
    ("nadia", "Service client (back-office)", "Mig", "shopping_admin"),
    ("julien", "Commandes et logistique", "Tat", "shopping_admin"),
    ("emma", "Marketing et promotions", "Tib", "shopping_admin"),
]
if len(sys.argv) > 3:  # ne construire que les pseudos demandés
    SALARIES = [s for s in SALARIES if s[0] in sys.argv[3].split(",")]

idx = json.load(open(os.path.join(base, "index.json")))

def trace(dossier):
    f = [x for x in glob.glob(os.path.join(RACINE, dossier, "*.json")) if "[raw]" not in x]
    return json.load(open(f[0]))["trace"] if f else None

def sop(dossier):
    f = [x for x in glob.glob(os.path.join(RACINE, dossier, "SOP - *.txt"))]
    return open(f[0], encoding="utf-8", errors="replace").read() if f else ""

def touches(k):
    return "".join(re.findall(r"'(.*?)'", k or "")) or (k or "")

def action_txt(a):
    el = (a.get("element_attributes") or {}).get("element") or {}
    cible = (el.get("text") or el.get("label") or el.get("placeholder") or el.get("role") or el.get("tag") or "").strip().split("\n")[0][:60]
    if a["type"] == "keystroke":
        return f"saisie « {touches(a.get('key'))[:60]} »" + (f" dans « {cible} »" if cible else "")
    if a["type"] == "scroll":
        return "défilement"
    return f"clic « {cible} »" if cible else "clic"

def moments_de(tr, t0, app):
    """Un moment = une suite d'états sur le même onglet ; texte nouveau = les actions faites dessus."""
    ms, cur = [], None
    fin_demo = max((e["data"].get("secs_from_start", 0) for e in tr), default=0) + 3
    for e in tr:
        d = e["data"]
        s = d.get("secs_from_start", 0)
        if e["type"] == "state":
            fen = d.get("tab") or ""
            if not cur or cur["fenetre"] != fen:
                cur = {"s0": s, "fenetre": fen, "url": d.get("url", ""), "actions": [], "etats": 0}
                ms.append(cur)
            cur["etats"] += 1
        elif e["type"] == "action" and cur:
            txt = action_txt(d)
            if not (cur["actions"] and cur["actions"][-1] == txt and txt == "défilement"):
                cur["actions"].append(txt)
    out = []
    for i, m in enumerate(ms):
        s1 = ms[i + 1]["s0"] if i + 1 < len(ms) else fin_demo
        u = urlparse(m["url"])
        out.append({"debut": (t0 + timedelta(seconds=m["s0"])).isoformat(), "fin": (t0 + timedelta(seconds=s1)).isoformat(),
                    "minutes": round(max(s1 - m["s0"], 1) / 60, 2), "app": app, "fenetre": m["fenetre"],
                    "url": "https://nova.example" + u.path, "captures": m["etats"], "captures_cles": [],
                    "texte_nouveau": " · ".join(m["actions"])[:600], "hors_travail": False})
    return out, fin_demo

os.makedirs(sortie, exist_ok=True)
for pseudo, role, prefixe, site in SALARIES:
    demos = sorted((d for d in idx["demos"] if d["personne"].startswith(prefixe) and d["site"] == site),
                   key=lambda d: d["dossier"].split(" @ ")[1])
    rnd = random.Random(pseudo)
    t = datetime(2026, 10, 13, 9, 0, tzinfo=PARIS)
    moments, verite, etats, actions = [], [], 0, 0
    for d in demos:
        tr = trace(d["dossier"])
        if not tr:
            continue
        ms, duree = moments_de(tr, t, APPS[site])
        if not ms:
            continue
        moments += ms
        etats += sum(m["captures"] for m in ms)
        actions += sum(1 for e in tr if e["type"] == "action")
        verite.append({"debut": ms[0]["debut"], "fin": ms[-1]["fin"], "task_id": d["task_id"], "modele": d["modele"],
                       "intention": d["intention"], "sop": sop(d["dossier"]), "variation": idx["variations"].get(d["task_id"])})
        # les tâches observées sont réparties sur 5 jours de 8 h 30 : entre deux, le reste du travail (non observé ici)
        ecart = 5 * 8.5 * 3600 / max(len(demos), 1)
        t += timedelta(seconds=duree + ecart * rnd.uniform(0.4, 1.15))
        if t.hour >= 17 and t.minute >= 30 or t.hour >= 18:  # fin de journée : lendemain 9h
            t = (t + timedelta(days=1)).replace(hour=9, minute=rnd.randint(0, 20))
            if t.weekday() >= 5:
                t += timedelta(days=7 - t.weekday())
    minutes = round(sum(m["minutes"] for m in moments))
    stats = {"periode": {"debut": moments[0]["debut"], "fin": moments[-1]["fin"]}, "captures_regardees": etats,
             "moments": len(moments), "moments_travail": len(moments), "captures_cles": actions,
             "part_gardee": round(actions / max(etats, 1), 3), "minutes_travail": minutes, "minutes_hors_travail": 0,
             "minutes_par_app": {APPS[site]: minutes}, "source": "WONDERBREAD (Stanford, CC-BY-4.0), réarrangé en semaine fictive",
             "role": role}
    dossier = os.path.join(sortie, pseudo)
    os.makedirs(dossier, exist_ok=True)
    json.dump({"stats": stats, "moments": moments}, open(os.path.join(dossier, "moments.json"), "w"), ensure_ascii=False, indent=1)
    json.dump(verite, open(os.path.join(dossier, "verite.json"), "w"), ensure_ascii=False, indent=1)
    rep = Counter(v["modele"] for v in verite)
    print(f"{pseudo:8s} {role:24s} {len(verite):3d} démos · {len(moments):4d} moments · {minutes:4d} min · "
          f"{sum(1 for n in rep.values() if n >= 2)} types de tâche répétés · jusqu'au {moments[-1]['fin'][:16]}")
