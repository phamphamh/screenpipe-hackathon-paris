#!/usr/bin/env python3
"""Exporte l'activité screenpipe d'une personne, sans le bruit, pour la vue d'équipe.

Usage : python3 -I equipe/export.py <prenom> [--db chemin/index.sqlite] [--depuis 2026-10-16T16:00]

Lit une COPIE de la base (l'originale est en cours d'écriture), et sort equipe/<prenom>.json.
Ce qui est retiré :
- l'audio (transcriptions vides ou inventées sur nos machines) ;
- les captures non actives (focused=0 : écrans secondaires, aucune app) ;
- browser_url (faux sous Windows : l'URL d'un onglet reste collée aux autres fenêtres) ;
- le perso : mails, DM, connexions/2FA, trading, achats ; adresses mail masquées partout ;
- le détail Discord (salons, contacts) et les termes de recherche Google ;
- les passages éclair (bloc de moins de 5 s).
Relis le fichier avant de le commiter.
"""
import argparse, glob, json, os, re, shutil, sqlite3, tempfile
from collections import defaultdict
from datetime import datetime

PERSO = re.compile(
    r"gmail|boîte de réception|inbox|outlook|connexion|sign in|log in|two-factor|2fa|"
    r"mot de passe|password|tradingview|forex|npc-traders|vous avez vendu|leboncoin|banque|bank|"
    r"\$\s?[\d,]+\.\d{2}",  # cours de bourse dans le titre
    re.I,
)
DM_DISCORD = re.compile(r"Discord \| @")
MAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
NAVIGATEURS = re.compile(r"\s+[—-]\s+(Mozilla Firefox|Google Chrome|Microsoft​? Edge|Brave)$")
NOMS_APPS = {
    "firefox.exe": "Firefox", "msedge.exe": "Edge", "chrome.exe": "Chrome",
    "WindowsTerminal.exe": "Terminal", "claude.exe": "Claude", "explorer.exe": "Explorateur",
}
ECART_MAX_S = 60  # deux captures de la même fenêtre à moins d'1 min = même bloc
DUREE_MIN_S = 5  # en dessous, c'est un passage éclair


def trouver_base():
    candidats = glob.glob("/mnt/c/Users/*/.screenpipe/storage/*/index.sqlite")
    candidats += glob.glob(os.path.expanduser("~/.screenpipe/storage/*/index.sqlite"))
    candidats += glob.glob(os.path.expanduser("~/.screenpipe/db.sqlite"))
    if not candidats:
        raise SystemExit("Base screenpipe introuvable, passe --db")
    return max(candidats, key=os.path.getmtime)


def copier(base):
    dossier = tempfile.mkdtemp(prefix="sp-export-")
    for suffixe in ("", "-wal"):
        if os.path.exists(base + suffixe):
            shutil.copy(base + suffixe, os.path.join(dossier, "index.sqlite" + suffixe))
    return os.path.join(dossier, "index.sqlite"), dossier


def nettoyer_titre(app, titre):
    titre = MAIL.sub("<mail>", titre or "")
    titre = NAVIGATEURS.sub("", titre)
    titre = re.sub(r"^\(\d+\)\s*", "", titre)  # compteur de non-lus
    if app == "WindowsTerminal.exe" and titre.startswith("Ubuntu"):
        titre = "WSL (Claude Code)"
    # noms de salons, contacts et termes de recherche : on garde le service, pas le détail
    if titre.startswith("Discord"):
        titre = "Discord"
    if re.search(r" - Recherche Google$| - Google Search$", titre):
        titre = "Recherche Google"
    return titre.strip() or "(sans titre)"


def lire_ts(ts):
    return datetime.fromisoformat(re.sub(r"(\.\d{6})\d+", r"\1", ts))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("prenom")
    p.add_argument("--db")
    p.add_argument("--depuis", default="")
    args = p.parse_args()

    copie, dossier = copier(args.db or trouver_base())
    try:
        c = sqlite3.connect(copie)
        lignes = c.execute(
            "select timestamp, app_name, window_name from frames "
            "where focused = 1 and app_name is not null and timestamp >= ? order by timestamp",
            (args.depuis,),
        ).fetchall()
    finally:
        shutil.rmtree(dossier, ignore_errors=True)

    blocs, retirees_perso = [], 0
    for ts, app, titre in lignes:
        brut = titre or ""
        if PERSO.search(brut) or PERSO.search(app) or DM_DISCORD.search(brut):
            retirees_perso += 1
            continue
        t = lire_ts(ts)
        cle = (NOMS_APPS.get(app, app.removesuffix(".exe")), nettoyer_titre(app, brut))
        dernier = blocs[-1] if blocs else None
        if dernier and dernier["cle"] == cle and (t - dernier["fin"]).total_seconds() <= ECART_MAX_S:
            dernier["fin"], dernier["captures"] = t, dernier["captures"] + 1
        else:
            blocs.append({"cle": cle, "debut": t, "fin": t, "captures": 1})

    gardes = [b for b in blocs if (b["fin"] - b["debut"]).total_seconds() >= DUREE_MIN_S]
    totaux = defaultdict(int)
    sortie = []
    for b in gardes:
        duree = int((b["fin"] - b["debut"]).total_seconds())
        totaux[b["cle"][0]] += duree
        sortie.append({
            "debut": b["debut"].isoformat(timespec="seconds"),
            "fin": b["fin"].isoformat(timespec="seconds"),
            "duree_s": duree,
            "app": b["cle"][0],
            "fenetre": b["cle"][1],
            "captures": b["captures"],
        })

    resultat = {
        "personne": args.prenom,
        "genere_le": datetime.now().astimezone().isoformat(timespec="seconds"),
        "fuseau": "UTC",
        "periode": {"debut": sortie[0]["debut"] if sortie else None, "fin": sortie[-1]["fin"] if sortie else None},
        "filtrage": {
            "captures_lues": len(lignes),
            "retirees_perso": retirees_perso,
            "blocs_eclair_retires": len(blocs) - len(gardes),
            "blocs_gardes": len(gardes),
            "regles": "focused=1 seulement ; pas d'audio ; pas d'URL ; perso/DM/mails retirés ; Discord et recherches Google sans détail ; blocs de moins de 5 s retirés",
        },
        "temps_par_app_s": dict(sorted(totaux.items(), key=lambda kv: -kv[1])),
        "blocs": sortie,
    }
    chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{args.prenom}.json")
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(resultat, f, ensure_ascii=False, indent=2)
    print(f"{chemin} : {len(gardes)} blocs, {retirees_perso} captures perso retirées")


if __name__ == "__main__":
    main()
