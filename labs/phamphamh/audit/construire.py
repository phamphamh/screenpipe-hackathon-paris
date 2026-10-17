"""Assemble les données de l'équipe en un seul jeu « fin d'audit » pour la visualisation.

Sources (toutes facultatives, on prend ce qui existe) :
- donnees/equipe/screenpipe-<prenom>-*.jsonl.gz : export complet (equipe/export_complet.py)
- equipe/<prenom>.json : export par blocs (equipe/export.py, format de Mickael)
- labs/<pseudo>/campagne/resume-valide.json : résumé validé (pas de frise, des agrégats et des tâches)

Sortie : donnees/audit/audit.json et donnees/audit/audit.html, la story (ignorés par git). Aucun titre de fenêtre n'y figure :
seulement des catégories, des sujets génériques, des noms d'apps et des horaires.
Usage : python3 labs/phamphamh/audit/construire.py [--debut 2026-10-16T18:00] [--fin 2026-10-16T23:00]
"""
import argparse, glob, gzip, json, os, re
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone

RACINE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PARIS = timezone(timedelta(hours=2))
FUSION_S = 60    # même règle que equipe/export.py : deux captures de la même fenêtre à moins d'1 min = même bloc
ECLAIR_S = 5     # un bloc de moins de 5 s est un passage éclair

AGENTS = ("orca", "claude code", "codex", "opencode", "cursor", "wsl (claude code)")
CHAT_IA = ("claude", "chatgpt", "gemini", "mistral", "perplexity", "copilot")
REGLES = [  # (catégorie, mots dans l'app ou le titre), dans l'ordre
    ("pause", ("musique", "music", "spotify", "deezer", "youtube", "netflix")),
    ("reunion", ("meet -", "google meet", "zoom", "teams", "webinaire", "webinar")),
    ("comm", ("discord", "slack", "whatsapp", "gmail", "boîte de réception", "outlook", "messages", "mail")),
    ("projet", ("github", "screenpipe-hackathon", "linear", "notion", "submission", "decoupage", "visual studio", "code -", "terminal", "figma")),
    ("admin", ("agenda", "calendar", "inscription", "connexion", "manage access", "sign in", "drive")),
    ("systeme", ("finder", "explorateur", "réglages", "usernotificationcenter", "securityagent", "eaptlstrust", "loginwindow", "informations système", "app store")),
]
NAVIGATEURS = ("chrome", "firefox", "safari", "edge", "arc", "brave")
SUJETS = [
    ("le dépôt du projet", ("screenpipe-hackathon", "submission.md", "decoupage")),
    ("screenpipe", ("screenpipe",)),
    ("les concurrents", ("godhands", "granola", "composio", "opencode")),
    ("Discord", ("discord",)),
]


def classer(app, titre):
    a, t = (app or "").lower().strip("‎ "), (titre or "").lower()
    if any(k in a or k in t for k in AGENTS):
        return "ia", "agent"
    if any(re.search(rf"\b{k}\b", a) or re.search(rf"\b{k}\b", t) for k in CHAT_IA):
        return "ia", "chat"
    for cat, mots in REGLES:
        if any(m in a or m in t for m in mots):
            return cat, None
    if any(n in a for n in NAVIGATEURS):
        return "veille", None
    return "systeme", None


def sujet(app, titre):
    t = f"{app} {titre}".lower()
    for nom, mots in SUJETS:
        if any(m in t for m in mots):
            return nom
    return None


def minutes(dt):
    dt = dt.astimezone(PARIS)
    return dt.hour * 60 + dt.minute + dt.second / 60


def blocs(captures):
    """captures = [(datetime, app, titre)] triées → blocs fusionnés, même règle pour tout le monde."""
    out = []
    for t, app, titre in captures:
        d = out[-1] if out else None
        if d and d["cle"] == (app, titre) and (t - d["fin"]).total_seconds() <= FUSION_S:
            d["fin"] = t
        else:
            out.append({"cle": (app, titre), "debut": t, "fin": t})
    return [b for b in out if (b["fin"] - b["debut"]).total_seconds() >= ECLAIR_S]


def depuis_export_complet(chemin):
    caps = []
    with gzip.open(chemin, "rt", encoding="utf-8") as f:
        for ligne in f:
            x = json.loads(ligne)
            c = x.get("content") or {}
            if x.get("type") != "OCR" or str(c.get("focused")).lower() != "true" or not c.get("app_name"):
                continue
            caps.append((datetime.fromisoformat(c["timestamp"]), c["app_name"].strip("‎"), c.get("window_name") or ""))
    caps.sort(key=lambda c: c[0])
    return blocs(caps)


def depuis_blocs(chemin):
    d = json.load(open(chemin, encoding="utf-8"))
    return [{"cle": (b["app"], b["fenetre"]), "debut": datetime.fromisoformat(b["debut"]), "fin": datetime.fromisoformat(b["fin"])} for b in d["blocs"]]


def segments(bs, debut, fin):
    out = []
    for b in bs:
        a, z = max(b["debut"], debut), min(b["fin"], fin)
        if z <= a:
            continue
        app, titre = b["cle"]
        cat, mode = classer(app, titre)
        out.append([round(minutes(a), 2), round(minutes(z), 2), cat, mode, sujet(app, titre), app])
    return out


def mesures(segs):
    actif = sum(s[1] - s[0] for s in segs)
    par_cat = Counter()
    for s in segs:
        par_cat[s[2]] += s[1] - s[0]
    agent = sum(s[1] - s[0] for s in segs if s[3] == "agent")
    chat = sum(s[1] - s[0] for s in segs if s[3] == "chat")
    bascules = sum(1 for a, b in zip(segs, segs[1:]) if a[5] != b[5])
    durees = sorted((s[1] - s[0]) * 60 for s in segs)
    # plongée : suite de blocs dans la même catégorie de travail, trous de moins de 2 min tolérés
    plongee, cour = (0, None), None
    for s in segs:
        if s[2] in ("pause", "systeme"):
            cour = None
            continue
        if cour and cour[2] == s[2] and s[0] - cour[1] <= 2:
            cour[1] = s[1]
        else:
            cour = [s[0], s[1], s[2]]
        if cour[1] - cour[0] > plongee[0]:
            plongee = (cour[1] - cour[0], list(cour))
    paires = Counter((a[5], b[5]) for a, b in zip(segs, segs[1:]) if a[5] != b[5])
    return {
        "actif_min": round(actif, 1),
        "par_categorie_min": {k: round(v, 1) for k, v in par_cat.most_common()},
        "ia_agent_min": round(agent, 1), "ia_chat_min": round(chat, 1),
        "part_ia": round((agent + chat) / actif, 3) if actif else 0,
        "bascules": bascules,
        "bascules_par_heure": round(bascules / (actif / 60), 1) if actif else 0,
        "ecran_median_s": round(durees[len(durees) // 2]) if durees else None,
        "plongee": {"minutes": round(plongee[0], 1), "debut": plongee[1][0], "categorie": plongee[1][2]} if plongee[1] else None,
        "paires": [[a, b, n] for (a, b), n in paires.most_common(6)],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--debut", default="2026-10-16T18:00")
    p.add_argument("--fin", default="2026-10-16T23:00")
    p.add_argument("--sortie", default=os.path.join(RACINE, "donnees", "audit", "audit.json"))
    args = p.parse_args()
    debut = datetime.fromisoformat(args.debut).replace(tzinfo=PARIS)
    fin = datetime.fromisoformat(args.fin).replace(tzinfo=PARIS)

    postes = []
    for chemin in sorted(glob.glob(os.path.join(RACINE, "donnees", "equipe", "screenpipe-*.jsonl.gz"))):
        qui = os.path.basename(chemin).split("-")[1]
        if any(p["qui"] == qui for p in postes):
            continue  # on garde l'export le plus ancien trouvé ; un seul par personne
        postes.append({"qui": qui, "source": "export complet", "segments": segments(depuis_export_complet(chemin), debut, fin)})
    for chemin in sorted(glob.glob(os.path.join(RACINE, "equipe", "*.json"))):
        qui = os.path.splitext(os.path.basename(chemin))[0]
        if not any(p["qui"] == qui for p in postes):
            postes.append({"qui": qui, "source": "export par blocs", "segments": segments(depuis_blocs(chemin), debut, fin)})
    taches = []
    for chemin in sorted(glob.glob(os.path.join(RACINE, "labs", "*", "campagne", "resume-valide.json"))):
        r = json.load(open(chemin, encoding="utf-8"))
        qui = chemin.split(os.sep)[-3]
        par_cat = Counter()
        for x in r.get("temps_par_app", []):
            par_cat[classer(x["app"], "")[0]] += x["minutes"]
        postes.append({"qui": qui, "source": "résumé validé", "segments": [], "agregats_min": dict(par_cat)})
        for t in r.get("taches", []):
            taches.append({"poste": qui, "titre": t["titre"], "frequence_par_semaine": t.get("frequence_par_semaine"),
                           "duree_moyenne_min": t.get("duree_moyenne_min"), "apps": t.get("apps", []),
                           "etapes": [{"type": e.get("type"), "texte": e.get("texte"), "app": e.get("app"), "statut": e.get("statut")} for e in t.get("etapes", [])],
                           "goulots": [g.get("type") for g in t.get("goulots", [])], "confiance": t.get("confiance")})

    for i, p in enumerate(postes):
        p["id"] = f"P{i + 1:02d}"
        p["mesures"] = mesures(p["segments"]) if p["segments"] else None

    # travail en parallèle : minute par minute, qui est sur quoi
    frises = [p for p in postes if p["segments"]]
    ensemble, meme_sujet = Counter(), Counter()
    for m in range(int(minutes(debut)), int(minutes(fin))):
        etats = []
        for p in frises:
            s = next((s for s in p["segments"] if s[0] <= m + .5 < s[1]), None)
            if s:
                etats.append((p["id"], s))
        for i in range(len(etats)):
            for j in range(i + 1, len(etats)):
                (a, sa), (b, sb) = etats[i], etats[j]
                ensemble[(a, b)] += 1
                if sa[4] and sa[4] == sb[4]:
                    meme_sujet[(a, b, sa[4])] += 1
    outils = defaultdict(dict)
    for p in postes:
        if p["segments"]:
            for s in p["segments"]:
                outils[s[5]][p["id"]] = round(outils[s[5]].get(p["id"], 0) + s[1] - s[0], 1)
    r_valides = [p for p in postes if p["source"] == "résumé validé"]
    for p, chemin in zip(r_valides, sorted(glob.glob(os.path.join(RACINE, "labs", "*", "campagne", "resume-valide.json")))):
        for x in json.load(open(chemin, encoding="utf-8")).get("temps_par_app", []):
            outils[x["app"]][p["id"]] = x["minutes"]

    sortie = {
        "genere_le": datetime.now(PARIS).isoformat(timespec="seconds"),
        "periode": {"debut": args.debut, "fin": args.fin, "debut_min": int(minutes(debut)), "fin_min": int(minutes(fin))},
        "regles": {"fusion_s": FUSION_S, "eclair_s": ECLAIR_S, "note": "écran regardé seulement ; aucun titre de fenêtre conservé"},
        "postes": [{k: v for k, v in p.items() if k != "qui"} | {"qui": p["qui"]} for p in postes],
        "parallele": {"ensemble_min": [[a, b, n] for (a, b), n in ensemble.items()],
                      "meme_sujet_min": [[a, b, s, n] for (a, b, s), n in meme_sujet.most_common()]},
        "outils": {k: v for k, v in sorted(outils.items(), key=lambda kv: -sum(kv[1].values())) if sum(v.values()) >= 3},
        "taches": taches,
    }
    os.makedirs(os.path.dirname(args.sortie), exist_ok=True)
    json.dump(sortie, open(args.sortie, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # la story : le gabarit avec les données dedans, à ouvrir tel quel ou à publier
    gabarit = open(os.path.join(os.path.dirname(__file__), "gabarit.html"), encoding="utf-8").read()
    page = os.path.join(os.path.dirname(args.sortie), "audit.html")
    open(page, "w", encoding="utf-8").write(gabarit.replace("__DATA__", json.dumps(sortie, ensure_ascii=False)))
    for p in postes:
        m = p["mesures"]
        print(p["id"], p["qui"], p["source"], f"{m['actif_min']} min actives, IA {m['part_ia']:.0%}, {m['bascules']} bascules, écran médian {m['ecran_median_s']} s" if m else p.get("agregats_min"))
    print("en parallèle :", sortie["parallele"])
    print(sortie["genere_le"], "→", args.sortie, "+", page)


if __name__ == "__main__":
    main()
