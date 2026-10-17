#!/usr/bin/env python3
"""Export complet de tout ce que screenpipe a capté chez une personne, pour l'analyser sur une autre machine.

Usage : python3 -I equipe/export_complet.py [prenom] [--depuis 2026-10-16T00:00:00Z]

Passe par l'API locale (localhost:3030) : texte des écrans, apps, fenêtres, URL, événements
d'interface, transcriptions, sans les images. La clé est trouvée toute seule (CLI screenpipe),
ou lue dans SCREENPIPE_API_KEY. Sortie : ~/Desktop/screenpipe-<prenom>-<date>.jsonl.gz,
une capture par ligne. Ce fichier ne va jamais dans le dépôt.
"""
import argparse, glob, gzip, json, os, subprocess, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

API = os.environ.get("SCREENPIPE_URL", "http://localhost:3030")
PAGE = 100
TRANCHE = timedelta(minutes=10)  # screenpipe refuse les offsets profonds (« payload budget exceeded ») : on avance par tranches de temps


def cle():
    if os.environ.get("SCREENPIPE_API_KEY"):
        return os.environ["SCREENPIPE_API_KEY"]
    clis = glob.glob(os.path.expanduser("~/.screenpipe/cli/*/screenpipe*"))
    clis += glob.glob("/mnt/c/Users/*/.screenpipe/cli/*/screenpipe.exe")
    for cli in sorted(clis, key=os.path.getmtime, reverse=True):
        try:
            sortie = subprocess.run([cli, "auth", "token"], capture_output=True, text=True, timeout=20).stdout
        except (OSError, subprocess.TimeoutExpired):
            continue
        if sortie.strip():
            return sortie.strip().splitlines()[-1]
    raise SystemExit("Clé screenpipe introuvable : copie-la depuis screenpipe > Settings > Privacy dans SCREENPIPE_API_KEY")


def get(chemin, params, jeton):
    req = urllib.request.Request(f"{API}{chemin}?{urllib.parse.urlencode(params)}")
    req.add_header("Authorization", f"Bearer {jeton}")
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def bureau():
    for d in [os.path.expanduser("~/Desktop")] + glob.glob("/mnt/c/Users/*/Desktop"):
        if os.path.isdir(d):
            return d
    return os.getcwd()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("prenom", nargs="?")
    p.add_argument("--depuis", default="2026-10-16T00:00:00Z")
    args = p.parse_args()
    prenom = (args.prenom or input("Ton prénom : ")).strip().lower().replace(" ", "-") or "anonyme"
    jeton = cle()
    depuis = datetime.fromisoformat(args.depuis.replace("Z", "+00:00"))
    fin = datetime.now(timezone.utc)
    iso = lambda t: t.strftime("%Y-%m-%dT%H:%M:%SZ")

    def tranche(a, b):
        """Toutes les captures entre a et b ; si screenpipe refuse, on coupe la tranche en deux."""
        out, offset = [], 0
        while True:
            try:
                d = get("/search", {"content_type": "all", "start_time": iso(a), "end_time": iso(b),
                                    "limit": PAGE, "offset": offset}, jeton)
            except urllib.error.HTTPError as e:
                if e.code != 500 or b - a <= timedelta(seconds=5):
                    erreurs.append(iso(a))
                    return out
                m = a + (b - a) / 2
                return tranche(a, m) + tranche(m, b)
            lignes = d.get("data", [])
            out += lignes
            offset += len(lignes)
            if not lignes or offset >= d.get("pagination", {}).get("total", 0):
                return out

    sortie = os.path.join(bureau(), f"screenpipe-{prenom}-{datetime.now():%Y%m%d-%H%M}.jsonl.gz")
    vus, types, erreurs, t = set(), {}, [], depuis
    with gzip.open(sortie, "wt", encoding="utf-8") as f:
        while t < fin:
            for x in tranche(t, min(t + TRANCHE, fin)):
                ligne = json.dumps(x, ensure_ascii=False, sort_keys=True)
                if ligne in vus:
                    continue  # screenpipe renvoie parfois deux fois la même capture
                vus.add(ligne)
                types[x.get("type")] = types.get(x.get("type"), 0) + 1
                f.write(ligne + "\n")
            t += TRANCHE
            print(f"\r{t.astimezone():%d/%m %H:%M} : {len(vus)} captures", end="", flush=True)
        resume = get("/activity-summary", {"start_time": iso(depuis), "end_time": iso(fin)}, jeton)
        f.write(json.dumps({"type": "ActivitySummary", "content": resume}, ensure_ascii=False) + "\n")

    taille = os.path.getsize(sortie) / 1e6
    print(f"\n\nFait : {sortie}\n{len(vus)} captures ({types}), {taille:.1f} Mo.")
    if erreurs:
        print(f"{len(erreurs)} passages illisibles sautés (premier : {erreurs[0]}).")
    print("Envoie ce fichier à Youssef (AirDrop, Drive ou WeTransfer).")


if __name__ == "__main__":
    main()
