"""Brique A du Wrapped : découpe une période screenpipe en « moments » et ne garde que les 20 % de captures utiles.

Tout reste sur la machine : le résultat est écrit dans donnees/ (ignoré par git).
Usage : python3 collecte.py [--depuis 2026-10-16T08:00] [--jusqua 2026-10-16T23:00] [--sortie donnees/moi]
La clé de l'API locale est lue dans SCREENPIPE_API_KEY (screenpipe > Settings > Privacy), si l'API en demande une.
Uniquement la bibliothèque standard de Python, pour tourner partout sans rien installer.
"""
import argparse, json, os, re, sys, urllib.parse, urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone

API = os.environ.get("SCREENPIPE_URL", "http://localhost:3030")
HORS_TRAVAIL = {"music", "musique", "spotify", "deezer", "loginwindow", "screensaverengine", "netflix", "tv"}
GARDE_MAX = 300      # une capture « couvre » au plus 5 min ; au-delà c'est de l'inactivité
COUPURE = 120        # plus de 2 min sans capture ou changement de fenêtre = nouveau moment

def get(path, params):
    req = urllib.request.Request(f"{API}{path}?{urllib.parse.urlencode(params)}")
    if os.environ.get("SCREENPIPE_API_KEY"):
        req.add_header("Authorization", f"Bearer {os.environ['SCREENPIPE_API_KEY']}")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def captures(depuis, jusqua):
    out, offset = [], 0
    while True:
        d = get("/search", {"content_type": "ocr", "start_time": depuis, "end_time": jusqua, "limit": 500, "offset": offset})
        rows = d.get("data", [])
        for x in rows:
            c = x["content"]
            if str(c.get("focused")).lower() != "true" or not c.get("app_name"):
                continue  # l'écran que la personne ne regarde pas ne compte pas
            out.append({"id": int(c["frame_id"]), "t": datetime.fromisoformat(c["timestamp"]), "app": c["app_name"],
                        "fenetre": c.get("window_name") or "", "url": c.get("browser_url") or "", "texte": c.get("text") or ""})
        offset += len(rows)
        if not rows or offset >= d.get("pagination", {}).get("total", 0):
            break
    out.sort(key=lambda r: r["t"])
    return out

def lignes(texte):
    return {re.sub(r"\s+", " ", l).strip().lower() for l in texte.splitlines() if len(l.strip()) >= 4}

def decouper(caps):
    vues, moments = set(), []
    for i, c in enumerate(caps):
        suiv = caps[i + 1]["t"] if i + 1 < len(caps) else c["t"] + timedelta(seconds=5)
        c["couvre"] = min((suiv - c["t"]).total_seconds(), GARDE_MAX)
        ls = lignes(c["texte"]); neuves = ls - vues; vues |= ls
        c["nouveaute"] = len(neuves) / len(ls) if ls else 0.0
        c["neuf"] = sorted(neuves)
        m = moments[-1] if moments else None
        if m and m["app"] == c["app"] and m["fenetre"] == c["fenetre"] and (c["t"] - m["caps"][-1]["t"]).total_seconds() <= COUPURE:
            m["caps"].append(c)
        else:
            moments.append({"app": c["app"], "fenetre": c["fenetre"], "caps": [c]})
    return moments

def resumer(m):
    caps = m["caps"]; secondes = sum(c["couvre"] for c in caps)
    cles = sorted(caps, key=lambda c: -c["nouveaute"])[:3]
    texte_neuf = " | ".join(l for c in caps for l in c["neuf"])[:600]
    return {"debut": caps[0]["t"].isoformat(), "fin": (caps[-1]["t"] + timedelta(seconds=caps[-1]["couvre"])).isoformat(),
            "minutes": round(secondes / 60, 1), "app": m["app"], "fenetre": m["fenetre"],
            "url": Counter(c["url"] for c in caps).most_common(1)[0][0], "captures": len(caps),
            "captures_cles": [c["id"] for c in cles if c["nouveaute"] > 0] or [caps[0]["id"]],
            "texte_nouveau": texte_neuf, "hors_travail": m["app"].lower() in HORS_TRAVAIL}

def main():
    a = argparse.ArgumentParser()
    now = datetime.now(timezone.utc)
    a.add_argument("--depuis", default=(now - timedelta(hours=24)).isoformat())
    a.add_argument("--jusqua", default=now.isoformat())
    a.add_argument("--sortie", default=os.path.join(os.path.dirname(__file__), "..", "..", "..", "donnees", "moi"))
    args = a.parse_args()
    utc = lambda s: datetime.fromisoformat(s).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        caps = captures(utc(args.depuis), utc(args.jusqua))
    except Exception as e:
        sys.exit(f"screenpipe ne répond pas sur {API} ({e}). Est-il lancé ? Faut-il SCREENPIPE_API_KEY ?")
    if not caps:
        sys.exit("Aucune capture sur cette période : pas assez de données, rien n'est inventé.")
    moments = [resumer(m) for m in decouper(caps)]
    travail = [m for m in moments if not m["hors_travail"]]
    cles = sum(len(m["captures_cles"]) for m in travail)
    par_app = defaultdict(float)
    for m in travail: par_app[m["app"]] += m["minutes"]
    stats = {"periode": {"debut": caps[0]["t"].isoformat(), "fin": caps[-1]["t"].isoformat()},
             "captures_regardees": len(caps), "moments": len(moments), "moments_travail": len(travail),
             "captures_cles": cles, "part_gardee": round(cles / len(caps), 3),
             "minutes_travail": round(sum(m["minutes"] for m in travail)), "minutes_hors_travail": round(sum(m["minutes"] for m in moments if m["hors_travail"])),
             "minutes_par_app": {k: round(v) for k, v in sorted(par_app.items(), key=lambda kv: -kv[1])}}
    os.makedirs(args.sortie, exist_ok=True)
    json.dump({"stats": stats, "moments": moments}, open(os.path.join(args.sortie, "moments.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(stats, ensure_ascii=False, indent=1))
    print(f"→ {os.path.normpath(os.path.join(args.sortie, 'moments.json'))} (reste sur cette machine)")

if __name__ == "__main__":
    main()
