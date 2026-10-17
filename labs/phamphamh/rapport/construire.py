"""Construit un rapport d'audit par méthode : données d'audit + méthodes → donnees/rapport/<id>.html.

Méthodes : labs/phamphamh/recherche/methodes.json si le fichier existe et se lit (la vraie version, écrite par la
recherche), sinon labs/phamphamh/rapport/methodes-defaut.json. Même schéma :
  [{"id","nom","inspire_de","promesse","ton","chapitres":[{"id","titre","question","viz","metriques":[],"lecture"}],
    "visuels_signature":[],"sources":[]}]
Dans titre, question et lecture, {id} est remplacé par la valeur calculée (catalogue MET et ALIAS dans rapport.html).
Une valeur suivie de son unité (« {part_ia} % », « {actif_h} h ») s'écrit en nombre brut. Un morceau de phrase dont la
donnée manque est retiré, et l'écran dit ce qu'il faudrait capter.

Données :
- par défaut : donnees/audit/audit.json (sortie de labs/phamphamh/audit/construire.py, nos vraies données) ;
- --demo : les résumés validés de la démo Maison Corvo (labs/phamphamh/demo/resumes/*.json + onboarding.json),
  données fictives, avec décisions, reprises, coût horaire et liste des outils fournis.

Sortie : donnees/rapport/<id>.html (ou donnees/rapport/demo/<id>.html) et index.json à côté. Chaque fichier embarque
toutes les méthodes : ?methode=<id> en change, ?pause coupe la lecture automatique. Le dossier donnees/ est ignoré par git.
Usage : python3 labs/phamphamh/rapport/construire.py [--demo] [--methodes chemin.json] [--cout-horaire 45]
"""
import argparse, glob, json, os, re, sys
from collections import Counter, defaultdict
from datetime import datetime

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(os.path.join(ICI, "..", "..", ".."))
DEMO = os.path.join(RACINE, "labs", "phamphamh", "demo")
VIZ_CONNUES = {"chiffre-cle", "barres-empilees", "frise", "reseau", "anneau", "liste-classee", "matrice-2x2", "cascade",
               "arbre", "vsm", "carte-chaleur", "course", "bureau-3d", "plan"}
# mêmes règles que categorieApp() dans rapport.html, pour que l'arbre retombe juste
RE_CAT = [("ia", r"orca|claude|chatgpt|codex|cursor|gemini|copilot|mistral|perplexity|opencode"),
          ("pause", r"musique|music|spotify|deezer|youtube|netflix"), ("reunion", r"meet|zoom|teams"),
          ("comm", r"discord|slack|whatsapp|gmail|outlook|messages|mail|zendesk"), ("admin", r"agenda|calendar|drive"),
          ("systeme", r"finder|réglages|usernotificationcenter|securityagent|loginwindow|app store"),
          ("veille", r"chrome|firefox|safari|edge|arc|brave")]


def categorie(app):
    a = app.lower()
    return next((c for c, r in RE_CAT if re.search(r, a)), "projet")


def js(x):
    """JSON sûr dans une balise <script>."""
    return json.dumps(x, ensure_ascii=False).replace("</", "<\\/")


def charger_methodes(chemin_force=None):
    candidats = [chemin_force] if chemin_force else [os.path.join(RACINE, "labs", "phamphamh", "recherche", "methodes.json"),
                                                      os.path.join(ICI, "methodes-defaut.json")]
    for chemin in candidats:
        if not chemin or not os.path.exists(chemin):
            continue
        try:
            m = json.load(open(chemin, encoding="utf-8"))
            if isinstance(m, dict):
                m = m.get("methodes", [])
            m = [x for x in m if isinstance(x, dict) and x.get("id") and x.get("chapitres")]
            if m:
                return m, chemin
            print(f"⚠ {chemin} : aucune méthode exploitable, on passe au suivant", file=sys.stderr)
        except (ValueError, OSError) as e:
            print(f"⚠ {chemin} illisible ({e}), on passe au suivant", file=sys.stderr)
    sys.exit("Aucun fichier de méthodes exploitable.")


def ids_connus(gabarit):
    """Les {id} que le moteur sait remplir, lus dans rapport.html (catalogue, alias, contexte)."""
    ids = set(re.findall(r'(?:met|txt)\("([a-z0-9_]+)"', gabarit)) | set(re.findall(r"ctx\.([a-z0-9_]+)\s*=", gabarit))
    alias = re.search(r"const ALIAS = \{(.*?)\};", gabarit, re.S)
    if alias:
        ids |= set(re.findall(r"([a-z0-9_]+):", alias.group(1)))
    ids |= {f"{p}{k}" for p in ("tache_", "euros_", "h_gain_", "action_h") for k in (1, 2, 3)} | {"tache", "h_tache_1"}
    return ids


def verifier(m, connus):
    """Avertit sur ce que le moteur ne sait pas dessiner ou remplir ; le rapport se construit quand même."""
    for ch in m["chapitres"]:
        if ch.get("viz") not in VIZ_CONNUES:
            print(f"  ⚠ {m['id']}/{ch.get('id')} : viz « {ch.get('viz')} » inconnue, l'écran le dira")
        inconnus = sorted({c for champ in ("titre", "question", "lecture") for c in re.findall(r"\{([a-z0-9_]+)\}", ch.get(champ) or "")} - connus)
        if inconnus:
            print(f"  · {m['id']}/{ch.get('id')} : pas de calcul pour {', '.join(inconnus)} → « pas encore observé »")


def audit_demo():
    """Les résumés validés de la démo Maison Corvo, au format de donnees/audit/audit.json."""
    onb = json.load(open(os.path.join(DEMO, "onboarding.json"), encoding="utf-8"))
    postes, taches, outils, ecartes, periode = [], [], defaultdict(dict), [], None
    for chemin in sorted(glob.glob(os.path.join(DEMO, "resumes", "*.json"))):
        r = json.load(open(chemin, encoding="utf-8"))
        if not r.get("valide_par_la_personne"):
            ecartes.append(r.get("personne"))
            continue
        pid = f"P{len(postes) + 1:02d}"
        periode = periode or r.get("periode")
        agr = Counter()
        for x in r.get("temps_par_app", []):
            agr[categorie(x["app"])] += x["minutes"]
            outils[x["app"]][pid] = outils[x["app"]].get(pid, 0) + x["minutes"]
        # l'IA est vue dans d'autres fenêtres (navigateur, Excel) : on la retire au prorata pour ne pas compter deux fois
        ia = sum(u.get("minutes", 0) for u in r.get("usage_ia", []))
        tot = sum(agr.values())
        if tot and ia:
            for c in list(agr):
                agr[c] -= agr[c] * min(1, ia / tot)
            agr["ia"] += ia
        for u in r.get("usage_ia", []):
            outils[u["outil"]][pid] = outils[u["outil"]].get(pid, 0) + u.get("minutes", 0)
        postes.append({"id": pid, "qui": r.get("personne", pid), "source": "résumé validé (démo)", "segments": [], "mesures": None,
                       "agregats_min": {k: round(v, 1) for k, v in agr.items() if v > 0}})
        for t in r.get("taches", []):
            taches.append({"poste": r.get("personne"), "titre": t["titre"], "frequence_par_semaine": t.get("frequence_par_semaine"),
                           "duree_moyenne_min": t.get("duree_moyenne_min"), "apps": t.get("apps", []),
                           "etapes": [{k: e.get(k) for k in ("type", "texte", "app", "statut")} for e in t.get("etapes", [])],
                           "goulots": [g.get("type") if isinstance(g, dict) else g for g in t.get("goulots", [])],
                           "automatisable": t.get("automatisable"), "confiance": t.get("confiance")})
    deb, fin = periode["debut"][:16], periode["fin"][:16]
    hmin = lambda s: int(s[11:13]) * 60 + int(s[14:16])
    return {"genere_le": datetime.now().astimezone().isoformat(timespec="seconds"),
            "periode": {"debut": deb, "fin": fin, "debut_min": hmin(deb), "fin_min": hmin(fin)},
            "regles": {"note": f"démo Maison Corvo, données fictives ; résumés non validés écartés : {', '.join(ecartes) or 'aucun'}"},
            "postes": postes, "parallele": {"ensemble_min": [], "meme_sujet_min": []},
            "outils": {k: {p: round(m, 1) for p, m in v.items()} for k, v in sorted(outils.items(), key=lambda kv: -sum(kv[1].values())) if sum(v.values()) >= 3},
            "taches": taches, "libelles": {"projet": "Outils métier"},
            "parametres": {"entreprise": onb.get("entreprise"), "cout_horaire": onb.get("cout_horaire"), "outils_fournis": onb.get("outils", [])}}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--audit", default=os.path.join(RACINE, "donnees", "audit", "audit.json"))
    p.add_argument("--demo", action="store_true", help="données de la démo Maison Corvo au lieu de nos vraies données")
    p.add_argument("--methodes", default=None)
    p.add_argument("--cout-horaire", type=float, default=None, help="coût horaire chargé en euros (sinon : pas de montant)")
    p.add_argument("--sortie", default=None)
    a = p.parse_args()

    if a.demo:
        audit = audit_demo()
        sortie = a.sortie or os.path.join(RACINE, "donnees", "rapport", "demo")
        os.makedirs(sortie, exist_ok=True)
        json.dump(audit, open(os.path.join(sortie, "audit-demo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    else:
        if not os.path.exists(a.audit):
            sys.exit(f"Pas de données d'audit : {a.audit}. Lancer d'abord labs/phamphamh/audit/construire.py")
        audit = json.load(open(a.audit, encoding="utf-8"))
        sortie = a.sortie or os.path.join(RACINE, "donnees", "rapport")
    if a.cout_horaire:
        audit.setdefault("parametres", {})["cout_horaire"] = a.cout_horaire

    methodes, source = charger_methodes(a.methodes)
    gabarit = open(os.path.join(ICI, "rapport.html"), encoding="utf-8").read()
    connus = ids_connus(gabarit)
    os.makedirs(sortie, exist_ok=True)

    print(f"données : {'démo Maison Corvo' if a.demo else os.path.relpath(a.audit, RACINE)} · {len(audit['postes'])} postes, {len(audit.get('taches', []))} tâches")
    print(f"méthodes : {os.path.relpath(source, RACINE)} ({len(methodes)})")
    index = []
    for m in methodes:
        verifier(m, connus)
        page = (gabarit.replace("__DATA__", js(audit))
                       .replace("__METHODES__", js(methodes))
                       .replace("__METHODE__", js(m)))
        fichier = os.path.join(sortie, f"{m['id']}.html")
        open(fichier, "w", encoding="utf-8").write(page)
        index.append({"id": m["id"], "nom": m.get("nom"), "inspire_de": m.get("inspire_de"), "promesse": m.get("promesse"),
                      "fichier": f"{m['id']}.html", "chapitres": [{"id": c.get("id"), "viz": c.get("viz")} for c in m["chapitres"]]})
        print(f"  {m['id']:<10} {len(m['chapitres'])} chapitres → {os.path.relpath(fichier, RACINE)}")
    json.dump({"genere_le": datetime.now().astimezone().isoformat(timespec="seconds"), "demo": a.demo,
               "methodes_source": os.path.relpath(source, RACINE), "rapports": index},
              open(os.path.join(sortie, "index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"index → {os.path.relpath(os.path.join(sortie, 'index.json'), RACINE)}")


if __name__ == "__main__":
    main()
