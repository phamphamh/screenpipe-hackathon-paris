#!/usr/bin/env python3
"""« Dès que… » — détecte, pour chaque tâche d'une campagne, les déclencheurs :

- l'événement qui doit **lancer l'action** (étape d'entrée de la tâche relue) ;
- la **voie technique** pour y accéder (connecteur entre les apps, appel API) ;
- le **cas d'arrêt** (exception observée : rien d'automatique, quelqu'un est prévenu) ;
- l'info à **partager** aux personnes concernées (étape de sortie : qui doit savoir).

Les tâches viennent de la **fusion officielle** (labs/phamphamh/fusion/fusion.py) — mêmes
chiffres et mêmes masquages que le Wrapped (moins de 3 personnes → masqué). Les règles
ne font que reformuler les étapes relues ; chaque déclencheur garde sa preuve
(étape, app, observé/supposé). Si moins de 3 résumés sont validés (fusion « pas_assez »),
les tâches sont regroupées à part, personne par personne.

    python3 detecter.py                          # démo Maison Corvo (6 salariés)
    python3 detecter.py --resumes labs/09125o/campagne/resume-valide.json \
        labs/adamaass/campagne/resume-valide.json --sortie resultat-equipe.html

Sorties : <sortie>.html, RESULTAT.md (ou RESULTAT-EQUIPE.md), declencheurs.json.
"""
import argparse, html, json, os, re, sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(ICI)))
sys.path.insert(0, os.path.join(RACINE, "labs", "phamphamh", "fusion"))
import fusion  # noqa: E402

TYPES = {"action": "Action", "input": "Entrée", "output": "Sortie", "decision": "Décision", "check": "Vérification"}
ARTICLES = {"le": "un", "la": "une", "les": "des", "l'": "un"}
ROLES = ["client", "commercial", "direction", "fournisseur", "transporteur", "adv", "équipe", "dirigeant"]
ROLES_AFFICHE = {"adv": "ADV", "équipe": "l'équipe", "dirigeant": "le dirigeant"}
LOCAUX = {"Excel"}  # pas un service : fichier local


def e(s):
    return html.escape(str(s if s is not None else ""))


def est_api(app):
    return bool(app) and app not in LOCAUX


def texte_personnes(n, brut=None):
    if isinstance(brut, str):
        return f"{brut} personnes" if not brut.endswith("personnes") else brut  # masque de la fusion (« moins de 3 »)
    if not n:
        return "un profil"
    return f"{n} personnes" if n >= fusion.MIN_PERSONNES else f"moins de {fusion.MIN_PERSONNES} personnes"


def roles_dans(texte):
    trouves = []
    bas = (texte or "").lower()
    for role in ROLES:
        if re.search(rf"\b{role}\b", bas) and role not in trouves:
            trouves.append(role)
    return [ROLES_AFFICHE.get(r, r) for r in trouves]


def reformuler_entree(texte):
    """Reformule une étape d'entrée en phrase « dès que… ». Retourne (phrase, genre)."""
    t = texte.strip()
    m = re.match(r"^(?:Ouvrir|Lire|Consulter)\s+(le|la|les|l['’])\s*(.+)$", t, re.I)
    if m:
        art = m.group(1).lower().replace("’", "'")
        reste = m.group(2).strip()
        par_mail = bool(re.search(r"re[çc]u[e]?s?\s+par\s+mail", reste, re.I))
        reste = re.sub(r"\s*re[çc]u[e]?s?\s+par\s+mail\s*$", "", reste, flags=re.I)
        fin = "arrive par mail" if par_mail else ("arrivent" if " et " in reste else "arrive")
        return f"{ARTICLES.get(art, 'un')} {reste} {fin}", "événement"
    m = re.match(r"^Recevoir\s+(.+)$", t, re.I)
    if m:
        return f"{m.group(1)} arrive", "événement"
    m = re.match(r"^(?:Lister|Filtrer|Exporter|Parcourir)\s+(?:les?\s+)?(.+)$", t, re.I)
    if m:
        return f"le balayage tourne — {m.group(1)}", "balayage"
    return f"« {t} »", "à préciser"


def app_cible(tache, app_source):
    """L'app sur laquelle l'action a lieu (première étape « action »), sinon la 2e app."""
    for et in tache.get("etapes") or []:
        if et.get("type") == "action" and et.get("app") and et.get("app") != app_source:
            return et["app"]
    for a in tache.get("apps") or []:
        if a != app_source:
            return a
    return app_source


def voie_connecteur(src, dst):
    if not est_api(src):
        return "à préciser"
    if not dst or dst == src:
        return f"API {src}"
    if not est_api(dst):
        return f"connecteur {src} → {dst} (API {src}, fichier local)"
    return f"connecteur {src} → {dst} (API {src}, API {dst})"


def declencheurs_de(tache):
    decl = []

    # 1) Événements d'entrée → lancent la tâche
    for et in tache.get("etapes") or []:
        if et.get("type") != "input":
            continue
        phrase, genre = reformuler_entree(et.get("texte", ""))
        src = et.get("app")
        dst = app_cible(tache, src)
        decl.append({
            "genre": genre,
            "dès_que": phrase,
            "preuve": {"texte": et.get("texte"), "app": src, "statut": et.get("statut", "observé"),
                       "type_etape": TYPES.get(et.get("type"), et.get("type"))},
            "lancer": {"genre": "action", "texte": "démarrer la tâche (la skill) sans attendre"},
            "voie": voie_connecteur(src, dst),
            "partager": None,
        })

    # 2) Exceptions → cas d'arrêt, quelqu'un est prévenu
    for ex in tache.get("exceptions") or []:
        morceaux = re.split(r"\s*→\s*", ex, maxsplit=1)
        condition = morceaux[0].strip()
        action = morceaux[1].strip() if len(morceaux) > 1 else "s'arrêter et demander"
        decl.append({
            "genre": "exception",
            "dès_que": condition,
            "preuve": {"texte": ex, "app": None, "statut": "observé", "type_etape": "Exception"},
            "lancer": {"genre": "humain", "texte": f"{action} (rien d'automatique)"},
            "voie": "notification",
            "partager": {"info": action, "qui": roles_dans(condition + " " + action)},
        })

    # 3) Sorties → infos à partager aux concernés
    for et in tache.get("etapes") or []:
        if et.get("type") != "output":
            continue
        decl.append({
            "genre": "sortie",
            "dès_que": "la tâche est finie",
            "preuve": {"texte": et.get("texte"), "app": et.get("app"), "statut": et.get("statut", "observé"),
                       "type_etape": TYPES.get(et.get("type"), et.get("type"))},
            "lancer": {"genre": "partage", "texte": et.get("texte", "")},
            "voie": f"API {et.get('app')}" if est_api(et.get("app")) else "local",
            "partager": {"info": et.get("texte", ""), "qui": roles_dans(et.get("texte", ""))},
        })
    return decl


def _concerne(t):
    qui = []
    for x in t["declencheurs"]:
        for q in (x.get("partager") or {}).get("qui") or []:
            if q not in qui:
                qui.append(q)
    return qui


def tache_finale(titre, freq, duree, personnes, apps, exceptions, etapes):
    tache = {"titre": titre, "frequence_par_semaine": freq, "duree_moyenne_min": duree,
             "apps": apps, "exceptions": exceptions, "etapes": etapes}
    decl = declencheurs_de(tache)
    return {"titre": titre,
            "freq_texte": f"{freq:.0f}×/sem",
            "duree_texte": f"{duree} min",
            "personnes_texte": personnes,
            "apps": apps,
            "libelles": [titre],
            "declencheurs": decl}


def construire(dossiers, onboarding_chemin=None):
    resumes = fusion.charger(list(dossiers))
    valides = [r for r in resumes if r.get("valide_par_la_personne") is True]
    ins = None
    if onboarding_chemin and os.path.exists(onboarding_chemin):
        ins = fusion.fusionner(resumes, json.load(open(onboarding_chemin)))
    taches = []

    if ins and ins.get("taches"):
        # Chemin officiel : mêmes tâches, mêmes chiffres, mêmes masquages que le Wrapped.
        for t in ins["taches"]:
            tf = tache_finale(t["titre"], t.get("frequence_par_semaine") or 0, t.get("duree_moyenne_min") or 0,
                              texte_personnes(t.get("nb_personnes"), t.get("personnes")),
                              t.get("apps") or [], t.get("exceptions") or [], t.get("etapes") or [])
            if tf["declencheurs"]:
                taches.append(tf)
    else:
        # Moins de 3 résumés validés (fusion « pas_assez ») : regroupement local, personne par personne.
        brutes = []
        for r in valides:
            for t in r.get("taches") or []:
                if t.get("titre"):
                    brutes.append({**t, "_personne": r["personne"]})
        cats = sorted({c["categorie"] for r in valides for c in r.get("temps_par_categorie") or []})
        outils = sorted({u["outil"] for r in valides for u in r.get("usage_ia") or []})
        g = fusion.regrouper_heuristique(brutes, cats, outils)
        for grp in g["taches"]:
            membres = [brutes[i] for i in grp["membres"]]
            ref = max(membres, key=lambda m: (m.get("confiance") or 0, len(m.get("etapes") or [])))
            personnes = sorted({m["_personne"] for m in membres})
            freqs = [m.get("frequence_par_semaine") or 0 for m in membres] or [0]
            durees = [m.get("duree_moyenne_min") or 0 for m in membres] or [0]
            exceptions = list(dict.fromkeys(ex.strip() for m in membres for ex in (m.get("exceptions") or []) if ex.strip()))
            freq = f"{min(freqs):.0f}–{max(freqs):.0f}" if min(freqs) != max(freqs) else f"{min(freqs):.0f}"
            duree = f"{min(durees):.0f}–{max(durees):.0f}" if min(durees) != max(durees) else f"{min(durees):.0f}"
            tf = tache_finale(ref.get("titre", ""), float(min(freqs)), 0,
                              texte_personnes(len(personnes)), list(dict.fromkeys(a for m in membres for a in (m.get("apps") or []))),
                              exceptions, ref.get("etapes") or [])
            tf["freq_texte"] = f"{freq}×/sem"
            tf["duree_texte"] = f"{duree} min"
            if tf["declencheurs"]:
                taches.append(tf)

    taches.sort(key=lambda x: len(x["declencheurs"]), reverse=True)
    return {"dossiers": [os.path.relpath(os.path.abspath(p), RACINE) for p in dossiers],
            "nb_valides": len(valides), "officiel": bool(ins and ins.get("taches")), "taches": taches}


GENRES = {"événement": "entrée", "balayage": "balayage", "exception": "exception", "sortie": "sortie", "à préciser": "à confirmer"}


def cellule_declencheur(d):
    genre = GENRES.get(d["genre"], d["genre"])
    p = d["preuve"]
    preuve = f'<div class="preuve">preuve : « {e(p["texte"])} »'
    if p.get("app"):
        preuve += f' — {e(p["app"])}'
    preuve += f' — {e(p["statut"])}</div>'
    return f'<span class="chip {genre.replace("é", "e").replace(" ", "-")}">{e(genre)}</span><b>{e(d["dès_que"])}</b>{preuve}'


def cellule_lancer(d):
    g = d["lancer"]["genre"]
    libelle = {"action": "action", "humain": "humain", "partage": "partage"}.get(g, g)
    return f'<span class="chip l-{libelle}">{e(libelle)}</span><span class="lancer">{e(d["lancer"]["texte"])}</span>'


def cellule_partager(d):
    if not d.get("partager"):
        return '<span class="absent">—</span>'
    qui = d["partager"].get("qui") or []
    chips = "".join(f"<span>{e(q)}</span>" for q in qui) or '<span class="absent">à définir</span>'
    return f'<div class="qui">{chips}</div><div class="preuve">{e(d["partager"]["info"])}</div>'


def page_html(d):
    nb_decl = sum(len(t["declencheurs"]) for t in d["taches"])
    nb_conn = sum(1 for t in d["taches"] for x in t["declencheurs"] if "connecteur" in x["voie"])
    nb_api = sum(1 for t in d["taches"] for x in t["declencheurs"] if x["voie"].startswith("API"))
    nb_ext = sum(1 for t in d["taches"] for x in t["declencheurs"] if x["genre"] == "exception")
    demo = all("demo" in p for p in d["dossiers"])
    c = []
    c.append(f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dès que… — les déclencheurs de la campagne</title>
<style>
:root {{ --encre:#17141f; --encre-2:#4a4556; --encre-3:#8a8496; --papier:#f6f3ec; --carte:#fff;
  --trait:#e6e1d6; --violet:#5b3df5; --violet-pale:#ece8ff; --ambre:#b7791f; --ambre-pale:#fbf0dc;
  --vert:#1e6b35; --vert-pale:#e7f3e9; --bleu:#44506b; --bleu-pale:#eef1f6;
  --serif: Georgia, "Times New Roman", serif; }}
* {{ box-sizing: border-box; }}
body {{ margin:0; background:var(--papier); color:var(--encre);
  font: 15px/1.55 -apple-system, "Segoe UI", system-ui, sans-serif; }}
header.bandeau {{ display:flex; align-items:center; justify-content:space-between; padding:14px 28px;
  background:var(--carte); border-bottom:1px solid var(--trait); }}
.marque {{ display:flex; align-items:center; gap:9px; font-weight:700; letter-spacing:-.01em; }}
.marque i {{ width:22px; height:22px; border-radius:7px;
  background: conic-gradient(from 200deg, var(--violet), #ff5fa2, #d4f53c, var(--violet)); display:inline-block; }}
.etiquette {{ display:inline-flex; align-items:center; font-size:12px; font-weight:600; padding:3px 10px;
  border-radius:999px; background:#efebe2; color:var(--encre-2); }}
main {{ max-width:1080px; margin:0 auto; padding:28px 24px 60px; }}
h1 {{ font-size:34px; letter-spacing:-.02em; margin:14px 0 4px; }}
h1 em {{ font-family:var(--serif); font-style:italic; font-weight:400; color:var(--violet); }}
.sous {{ color:var(--encre-2); max-width:780px; }}
.legende {{ color:var(--encre-3); font-size:13px; margin:2px 0 10px; max-width:820px; }}
.bandeau-chiffres {{ display:flex; gap:10px; flex-wrap:wrap; margin:18px 0 8px; }}
.chiffre {{ background:var(--carte); border:1px solid var(--trait); border-radius:12px; padding:10px 14px; }}
.chiffre b {{ display:block; font-size:20px; }}
.chiffre span {{ color:var(--encre-3); font-size:12.5px; }}
.carte {{ background:var(--carte); border:1px solid var(--trait); border-radius:14px; padding:20px 22px;
  margin:16px 0; box-shadow:0 1px 2px rgba(23,20,31,.05); }}
.carte h2 {{ margin:0 0 2px; font-size:19px; letter-spacing:-.01em; }}
.carte .meta {{ color:var(--encre-3); font-size:13px; margin-bottom:14px; }}
table {{ border-collapse:collapse; width:100%; }}
th, td {{ text-align:left; vertical-align:top; padding:9px 10px; border-top:1px solid var(--trait); }}
th {{ font-size:12.5px; color:var(--encre-3); font-weight:600; border-top:0; }}
td {{ font-size:14px; }}
.chip {{ display:inline-block; font-size:10.5px; font-weight:700; text-transform:uppercase; letter-spacing:.04em;
  border-radius:6px; padding:2px 7px; margin:0 6px 4px 0; vertical-align:1px; }}
.chip.entree {{ background:var(--vert-pale); color:var(--vert); }}
.chip.balayage {{ background:var(--bleu-pale); color:var(--bleu); }}
.chip.exception {{ background:var(--ambre-pale); color:var(--ambre); }}
.chip.sortie {{ background:var(--violet-pale); color:var(--violet); }}
.chip.a-confirmer {{ background:#efebe2; color:var(--encre-2); }}
.chip.l-action {{ background:var(--vert-pale); color:var(--vert); }}
.chip.l-humain {{ background:var(--ambre-pale); color:var(--ambre); }}
.chip.l-partage {{ background:var(--violet-pale); color:var(--violet); }}
.preuve {{ color:var(--encre-3); font-size:12.5px; margin-top:4px; }}
.lancer {{ font-weight:600; }}
.voie {{ color:var(--encre-2); font-size:13px; }}
.qui span {{ display:inline-block; font-size:12px; background:#efebe2; border-radius:999px; padding:2px 8px; margin:1px 3px 1px 0; }}
.absent {{ color:var(--encre-3); }}
footer {{ margin-top:28px; color:var(--encre-3); font-size:13px; }}
footer code {{ background:#efebe2; border-radius:5px; padding:1px 5px; }}
</style></head><body>
<header class="bandeau"><div class="marque"><i></i> Wrapped — les déclencheurs</div>
<span class="etiquette">{'Démo · Maison Corvo' if demo else 'Campagne équipe'}</span></header>
<main>
<h1>Dès que… <em>la liste à brancher</em></h1>
<p class="sous">Le produit ne s'arrête pas à « voici vos tâches répétées ». Pour chaque tâche relue et validée,
il détecte <b>l'événement qui doit la lancer</b>, la <b>voie technique</b> pour y accéder (connecteur entre apps, appel API),
et <b>l'info à partager aux personnes concernées</b>. Rien d'inventé : chaque déclencheur affiche sa preuve
(l'étape observée, son app, observé ou supposé).</p>
<p class="legende"><b>entrée</b> = l'événement qui déclenche · <b>balayage</b> = la vérification qui revient ·
<b>exception</b> = le cas qui doit tout arrêter (quelqu'un est prévenu) · <b>sortie</b> = l'info à partager.</p>
<div class="bandeau-chiffres">
  <div class="chiffre"><b>{len(d['taches'])}</b><span>tâches relues</span></div>
  <div class="chiffre"><b>{nb_decl}</b><span>déclencheurs détectés</span></div>
  <div class="chiffre"><b>{nb_conn}</b><span>connecteurs apps → apps</span></div>
  <div class="chiffre"><b>{nb_api}</b><span>appels API directs</span></div>
  <div class="chiffre"><b>{nb_ext}</b><span>cas d'arrêt (exceptions)</span></div>
</div>""")
    for t in d["taches"]:
        concerne = _concerne(t)
        ligne_concerne = f" · à tenir au courant : {', '.join(concerne)}" if concerne else ""
        c.append(f"""<div class="carte">
<h2>{e(t['titre'])}</h2>
<div class="meta">{e(t['freq_texte'])} · {e(t['duree_texte'])} · chez {e(t['personnes_texte'])} ·
apps : {e(', '.join(t['apps']))}{e(ligne_concerne)}</div>
<table><thead><tr><th style="width:38%">Dès que…</th><th>Lancer</th><th>Voie</th><th>Partager aux concernés</th></tr></thead><tbody>""")
        for x in t["declencheurs"]:
            c.append(f"""<tr><td>{cellule_declencheur(x)}</td>
<td>{cellule_lancer(x)}</td>
<td><span class="voie">{e(x['voie'])}</span></td>
<td>{cellule_partager(x)}</td></tr>""")
        c.append("</tbody></table></div>")
    c.append(f"""<footer>Généré par <code>labs/09125o/declencheurs/detecter.py</code> — les tâches et les chiffres viennent
de la fusion officielle (<code>labs/phamphamh/fusion/fusion.py</code>, « moins de 3 personnes » masqué). Les formulations
sont proposées par règles à partir des étapes relues ; chaque ligne garde sa preuve. Pour brancher pour de vrai :
un connecteur par app (MCP Gmail, API de l'ERP…) — c'est la liste à passer au déploiement.</footer>
</main></body></html>""")
    return "".join(c)


def resultat_md(d):
    lignes = [f"# Dès que… — les déclencheurs ({', '.join(d['dossiers'])})", "",
              f"{len(d['taches'])} tâches relues, {sum(len(t['declencheurs']) for t in d['taches'])} déclencheurs détectés.",
              f"({'tâches et chiffres de la fusion officielle' if d.get('officiel') else 'moins de 3 validations — regroupement local, personne par personne'})", ""]
    for t in d["taches"]:
        lignes.append(f"## {t['titre']}")
        lignes.append(f"*{t['freq_texte']} · {t['duree_texte']} · chez {t['personnes_texte']} · apps : {', '.join(t['apps'])}*")
        lignes.append("")
        lignes.append("| Dès que… | Lancer | Voie | Partager | Preuve |")
        lignes.append("|---|---|---|---|---|")
        for x in t["declencheurs"]:
            p = x["preuve"]
            preuve = f"« {p['texte']} »" + (f" — {p['app']}" if p.get("app") else "")
            partager = ""
            if x.get("partager"):
                qui = ", ".join(x["partager"].get("qui") or []) or "à définir"
                partager = f"{x['partager']['info']} → {qui}"
            lignes.append(f"| {x['dès_que']} | {x['lancer']['texte']} | {x['voie']} | {partager} | {preuve} |")
        lignes.append("")
    lignes.append("*Formulations par règles à partir des étapes relues ; chaque ligne garde sa preuve. Tâches et chiffres : fusion officielle.*")
    return "\n".join(lignes)


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--resumes", nargs="+", default=[os.path.join(RACINE, "labs", "phamphamh", "demo", "resumes")])
    a.add_argument("--onboarding", default=None, help="le json du dirigeant (défaut : celui de la démo si on lit la démo)")
    a.add_argument("--sortie", default=os.path.join(ICI, "resultat.html"))
    args = a.parse_args()

    onboarding = args.onboarding
    if onboarding is None and all("demo" in p for p in args.resumes):
        onboarding = os.path.join(RACINE, "labs", "phamphamh", "demo", "onboarding.json")
    d = construire(args.resumes, onboarding)
    base = os.path.basename(args.sortie)
    open(args.sortie, "w").write(page_html(d))
    md_nom = "RESULTAT.md" if base.lower() == "resultat.html" else base.rsplit(".", 1)[0].upper() + ".md"
    open(os.path.join(os.path.dirname(args.sortie), md_nom), "w").write(resultat_md(d) + "\n")
    json_nom = "declencheurs.json" if base.lower() == "resultat.html" else base.rsplit(".", 1)[0] + ".json"
    open(os.path.join(os.path.dirname(args.sortie), json_nom), "w").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
    mode = "fusion officielle" if d["officiel"] else "regroupement local (< 3 validations)"
    print(f"{len(d['taches'])} tâches, {sum(len(t['declencheurs']) for t in d['taches'])} déclencheurs [{mode}] → {args.sortie} + {md_nom} + {json_nom}")


if __name__ == "__main__":
    main()
