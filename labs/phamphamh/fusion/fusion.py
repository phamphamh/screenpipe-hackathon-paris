"""Brique D du Wrapped : fusionne les résumés VALIDÉS de plusieurs personnes en insights d'entreprise.

Règles de confidentialité appliquées ici, pas dans le site :
- seuls les résumés où "valide_par_la_personne" vaut true comptent ;
- moins de 3 participants → pas de Wrapped du tout ;
- une app, une catégorie ou un outil d'IA utilisé par moins de 3 personnes est fondu dans « Autres » ;
- le nombre de personnes d'une tâche est donné en tranche (« moins de 3 ») sous 3 ; aucun nom n'apparaît.
Usage : python3 fusion.py <dossier ou fichiers de résumés> --onboarding onboarding.json [-o insights.json] [--ia]
Uniquement la bibliothèque standard de Python.
"""
import argparse, ast, glob, hashlib, json, os, re, subprocess, sys, tempfile, unicodedata
from collections import defaultdict
from datetime import datetime

MIN_PERSONNES = 3
SEMAINES_PAR_MOIS = 4.33
MOTS_VIDES = set("a au aux avec d de des du en et l la le les pour par sur un une dans son sa ses leur leurs ou a au plus sans chaque est qui que".split())


def normaliser(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9 ]+", " ", s)


def mots(s):
    return {m[:6] for m in normaliser(s).split() if m not in MOTS_VIDES and len(m) > 2}  # racine grossière : « relancer » ≈ « relance »


def app_propre(a):
    return re.sub(r"[‎‏​]", "", a or "").strip() or "Inconnue"


def texte_limite(l):
    """Une limite arrive en texte — ou en objet {"texte": …}, ou en texte d'objet (nos générateurs hésitent).
    La fusion ne garde que du texte : un objet casserait dict.fromkeys (non hachable) et s'afficherait mal."""
    if isinstance(l, dict):
        l = l.get("texte") or l.get("text") or next((v for v in l.values() if isinstance(v, str)), "")
    t = str(l or "").strip()
    if t.startswith("{"):
        try:
            d = ast.literal_eval(t)
            if isinstance(d, dict):
                t = str(d.get("texte") or d.get("text") or "").strip() or t
        except (ValueError, SyntaxError):
            pass
    return t


def jours(resume):
    """Nombre de jours calendaires couverts par la période (une journée = 1, du lundi au vendredi = 5)."""
    p = resume.get("periode") or {}
    try:
        return (datetime.fromisoformat(p["fin"]).date() - datetime.fromisoformat(p["debut"]).date()).days + 1
    except (KeyError, ValueError, TypeError):
        return 1


# ---------- regroupement des tâches, catégories et outils entre personnes ----------

def regrouper_heuristique(taches, categories, outils):
    """Tâches : mêmes mots-clés (Jaccard) ou mêmes apps avec des mots en commun. Catégories et outils : premier mot-clé commun."""
    n = len(taches); parent = list(range(n))
    def racine(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    qui = {i: {t["_personne"]} for i, t in enumerate(taches)}  # personnes présentes dans chaque groupe
    mt = [mots(t["titre"]) for t in taches]
    ap = [set(t.get("apps") or []) for t in taches]
    for i in range(n):
        for j in range(i + 1, n):
            ri, rj = racine(i), racine(j)
            if ri == rj or qui[ri] & qui[rj]:  # jamais deux tâches d'une même personne dans un groupe
                continue
            inter = len(mt[i] & mt[j]); union = len(mt[i] | mt[j]) or 1
            apps = len(ap[i] & ap[j]) / (len(ap[i] | ap[j]) or 1)
            if inter / union >= 0.34 or (inter >= 1 and apps >= 0.5 and inter / union >= 0.2):
                parent[rj] = ri; qui[ri] |= qui.pop(rj)
    groupes = defaultdict(list)
    for i in range(n):
        groupes[racine(i)].append(i)
    return {"taches": [{"titre": None, "membres": m} for m in groupes.values()],
            "categories": {c: c for c in categories}, "outils": {o: outil_heuristique(o) for o in outils}}


def outil_heuristique(o):
    n = normaliser(o)
    for cle, nom in (("chatgpt", "ChatGPT"), ("openai", "ChatGPT"), ("codex", "Codex"), ("claude", "Claude"), ("orca", "Claude"),
                     ("copilot", "Copilot"), ("gemini", "Gemini"), ("mistral", "Le Chat"), ("perplexity", "Perplexity"), ("cursor", "Cursor")):
        if cle in n:
            return nom
    return o.strip()


CONSIGNE_IA = """Tu regroupes les résultats de plusieurs salariés d'une même entreprise.
1. TÂCHES : regroupe les tâches qui sont LA MÊME activité malgré des libellés différents (ex. « Relancer un devis » et « Relance clients sans réponse »).
   Ne regroupe jamais deux tâches de la même personne (même lettre). Donne à chaque groupe un titre court, concret, en français, sans nom propre.
2. CATÉGORIES : ramène chaque catégorie à une catégorie générale parmi 5 à 8 au total (ex. « Relation client », « Administratif et finance », « Réunions », « Production », « Veille »).
3. OUTILS D'IA : ramène chaque libellé à un nom d'outil simple (ex. « Orca (agent Claude Code) » → « Claude »).
Réponds UNIQUEMENT avec ce JSON :
{"taches":[{"titre":str,"membres":[int]}],"categories":{"libellé d'origine":"catégorie générale"},"outils":{"libellé d'origine":"outil"}}
Chaque numéro de tâche apparaît dans exactement un groupe."""


def regrouper_ia(taches, categories, outils, modele="sonnet"):
    entree = "TÂCHES (numéro | personne | titre | apps | étapes) :\n" + "\n".join(
        f"#{i} | {chr(65 + t['_rang'])} | {t['titre']} | {', '.join(t.get('apps') or [])} | {' / '.join(e.get('texte', '') for e in (t.get('etapes') or [])[:5])}"
        for i, t in enumerate(taches))
    entree += "\n\nCATÉGORIES :\n" + "\n".join(categories) + "\n\nOUTILS D'IA :\n" + "\n".join(outils)
    cache = os.path.join(tempfile.gettempdir(), "wrapped-fusion-" + hashlib.sha1(entree.encode()).hexdigest()[:16] + ".json")
    if os.path.exists(cache):
        return json.load(open(cache))
    r = subprocess.run(["claude", "-p", "--model", modele, "--no-session-persistence"], input=CONSIGNE_IA + "\n\n" + entree,
                       capture_output=True, text=True, timeout=600, cwd=tempfile.gettempdir())
    bloc = re.search(r"\{.*\}", r.stdout, re.S)
    if r.returncode or not bloc:
        raise RuntimeError(f"Claude n'a pas rendu de JSON : {(r.stderr or r.stdout)[:300]}")
    g = json.loads(bloc.group(0))
    # garde-fous : chaque tâche dans un seul groupe, jamais deux tâches d'une même personne ensemble
    vus, propres = set(), []
    for grp in g.get("taches", []):
        par_personne, m = set(), []
        for i in grp.get("membres", []):
            if isinstance(i, int) and 0 <= i < len(taches) and i not in vus and taches[i]["_personne"] not in par_personne:
                m.append(i); vus.add(i); par_personne.add(taches[i]["_personne"])
        if m:
            propres.append({"titre": grp.get("titre"), "membres": m})
    propres += [{"titre": None, "membres": [i]} for i in range(len(taches)) if i not in vus]
    g["taches"] = propres
    g["categories"] = {c: g.get("categories", {}).get(c, c) for c in categories}
    g["outils"] = {o: g.get("outils", {}).get(o) or outil_heuristique(o) for o in outils}
    json.dump(g, open(cache, "w"), ensure_ascii=False)
    return g


# ---------- la fusion ----------

def tranche(n):
    return str(n) if n >= MIN_PERSONNES else f"moins de {MIN_PERSONNES}"


def agreger_lignes(lignes, cle):
    """lignes = [(personne, libellé, minutes)] → [{cle, minutes, personnes}], les libellés à moins de 3 personnes fondus dans « Autres »."""
    minutes, qui = defaultdict(float), defaultdict(set)
    for p, lib, m in lignes:
        minutes[lib] += m; qui[lib].add(p)
    out, autres, autres_qui = [], 0.0, set()
    for lib in sorted(minutes, key=minutes.get, reverse=True):
        if len(qui[lib]) >= MIN_PERSONNES:
            out.append({cle: lib, "minutes": round(minutes[lib]), "personnes": len(qui[lib])})
        else:
            autres += minutes[lib]; autres_qui |= qui[lib]
    if autres >= 1:
        out.append({cle: "Autres", "minutes": round(autres), "personnes": tranche(len(autres_qui)), "regroupe": True})
    return out


def fusionner(resumes, onboarding, regroupement="heuristique", modele="sonnet"):
    tous = len(resumes)
    valides = [r for r in resumes if r.get("valide_par_la_personne") is True]
    base = {"entreprise": onboarding.get("entreprise", "Votre entreprise"), "onboarding": onboarding,
            "participants": len(valides), "invites": tous, "non_valides": tous - len(valides), "minimum": MIN_PERSONNES}
    if len(valides) < MIN_PERSONNES:
        return {**base, "statut": "pas_assez",
                "message": f"{len(valides)} résumé(s) validé(s) sur {tous}. Il en faut au moins {MIN_PERSONNES} pour qu'aucun chiffre ne désigne une personne."}

    cout_h = float(onboarding.get("cout_horaire") or 40)
    taches, categories, outils = [], set(), set()
    for rang, r in enumerate(valides):
        pid = f"p{rang}"
        jrs = jours(r)
        for t in r.get("taches") or []:
            if not t.get("titre"):
                continue
            taches.append({**t, "_personne": pid, "_rang": rang, "_extrapole": jrs < 5})
        categories |= {c["categorie"] for c in r.get("temps_par_categorie") or []}
        outils |= {u["outil"] for u in r.get("usage_ia") or []}
    categories, outils = sorted(categories), sorted(outils)

    methode = "heuristique"
    if regroupement == "ia" and taches:
        try:
            g = regrouper_ia(taches, categories, outils, modele); methode = "ia"
        except Exception as e:  # pas de Claude sur la machine, ou réponse illisible : on ne bloque pas le Wrapped
            print(f"Regroupement IA impossible ({e}) : regroupement par mots-clés.", file=sys.stderr)
            g = regrouper_heuristique(taches, categories, outils)
    else:
        g = regrouper_heuristique(taches, categories, outils)

    # --- temps observé ---
    heures = sum(float(r.get("heures_captees") or 0) for r in valides)
    jours_total = sum(jours(r) for r in valides)
    lignes_app = [(f"p{k}", app_propre(a["app"]), a["minutes"]) for k, r in enumerate(valides) for a in r.get("temps_par_app") or []]
    lignes_cat = [(f"p{k}", g["categories"].get(c["categorie"], c["categorie"]), c["minutes"]) for k, r in enumerate(valides) for c in r.get("temps_par_categorie") or []]
    apps_distinctes = len({a for _, a, _ in lignes_app})

    # --- IA ---
    ia_min, ia_qui, ia_usages = defaultdict(float), defaultdict(set), defaultdict(list)
    for k, r in enumerate(valides):
        for u in r.get("usage_ia") or []:
            o = g["outils"].get(u["outil"], u["outil"])
            ia_min[o] += u.get("minutes") or 0; ia_qui[o].add(k); ia_usages[o] += u.get("usages") or []
    utilisateurs_ia = len(set().union(*ia_qui.values())) if ia_qui else 0
    for o in [o for o in ia_qui if len(ia_qui[o]) < MIN_PERSONNES]:  # outils trop rares : fondus dans « Autres outils d'IA »
        a = "Autres outils d'IA"
        ia_min[a] += ia_min.pop(o); ia_qui[a] |= ia_qui.pop(o); ia_usages[a] += ia_usages.pop(o)
    ia = [{"outil": o, "minutes": round(ia_min[o]), "personnes": tranche(len(ia_qui[o])), "usages": list(dict.fromkeys(ia_usages[o]))[:5]}
          for o in sorted(ia_min, key=lambda o: (o == "Autres outils d'IA", -ia_min[o]))]

    # --- tâches communes ---
    groupes = []
    for grp in g["taches"]:
        membres = [taches[i] for i in grp["membres"]]
        personnes = {m["_personne"] for m in membres}
        h_sem = sum((m.get("frequence_par_semaine") or 0) * (m.get("duree_moyenne_min") or 0) for m in membres) / 60
        if h_sem <= 0:
            continue
        poids = [(m.get("frequence_par_semaine") or 0) * (m.get("duree_moyenne_min") or 0) or 1 for m in membres]
        score_ia = sum((m.get("automatisable") or {}).get("score", 50) * p for m, p in zip(membres, poids)) / sum(poids)
        ref = max(membres, key=lambda m: (m.get("confiance") or 0, len(m.get("etapes") or [])))
        etapes = ref.get("etapes") or []
        part_decision = sum(e.get("type") == "decision" for e in etapes) / (len(etapes) or 1)
        goulots = list({(x.get("type"), x.get("detail")): x for m in membres for x in (m.get("goulots") or [])}.values())
        copier_coller = any(x.get("type") == "switching" for x in goulots)
        corrige = [m["automatisable"].get("corrige_par_la_personne") for m in membres if (m.get("automatisable") or {}).get("corrige_par_la_personne")]
        score = max(0, min(100, round(score_ia + (10 if copier_coller else 0) - 30 * part_decision)))
        cout_mois = h_sem * SEMAINES_PAR_MOIS * cout_h
        groupes.append({
            "titre": grp.get("titre") or ref["titre"],
            "libelles": list(dict.fromkeys(m["titre"] for m in membres)),
            "personnes": tranche(len(personnes)), "nb_personnes": len(personnes) if len(personnes) >= MIN_PERSONNES else None,
            "frequence_par_semaine": round(sum(m.get("frequence_par_semaine") or 0 for m in membres), 1),
            "duree_moyenne_min": round(sum(m.get("duree_moyenne_min") or 0 for m in membres) / len(membres)),
            "heures_par_semaine": round(h_sem, 1), "heures_par_mois": round(h_sem * SEMAINES_PAR_MOIS, 1),
            "cout_par_mois": round(cout_mois), "statut": "estimé" if any(m["_extrapole"] for m in membres) else "observé",
            "apps": list(dict.fromkeys(app_propre(a) for m in membres for a in m.get("apps") or [])),
            "etapes": etapes, "exceptions": list(dict.fromkeys(e for m in membres for e in m.get("exceptions") or []))[:5],
            "goulots": goulots[:6],
            "automatisable": {"score": score, "score_ia": round(score_ia), "copier_coller": copier_coller,
                              "part_decision": round(part_decision, 2), "corrections": corrige,
                              "pourquoi": [(m.get("automatisable") or {}).get("pourquoi") for m in membres if (m.get("automatisable") or {}).get("pourquoi")][:3]},
            "gain_par_mois": round(cout_mois * score / 100), "heures_gagnees_par_mois": round(h_sem * SEMAINES_PAR_MOIS * score / 100, 1),
            "confiance": round(sum(m.get("confiance") or 0.5 for m in membres) / len(membres), 2),
            "preuves": sorted(({"debut": p.get("debut"), "fin": p.get("fin"), "app": app_propre(p.get("app"))} for m in membres for p in m.get("preuves") or [] if isinstance(p, dict)),
                              key=lambda p: p["debut"] or "")[:30],
        })
    groupes.sort(key=lambda t: t["cout_par_mois"], reverse=True)
    for i, t in enumerate(groupes):
        t["rang_cout"] = i + 1
    a_automatiser = sorted(groupes, key=lambda t: t["gain_par_mois"], reverse=True)

    # --- goulots ---
    gl = defaultdict(lambda: {"taches": [], "heures_par_semaine": 0.0, "exemples": []})
    for t in groupes:
        for typ in {x.get("type") for x in t["goulots"]}:
            if not typ or typ == "unclear":
                continue
            d = gl[typ]; d["taches"].append(t["titre"]); d["heures_par_semaine"] += t["heures_par_semaine"]
            d["exemples"] += [x["detail"] for x in t["goulots"] if x.get("type") == typ and x.get("detail")][:2]
    goulots = sorted(({"type": k, "taches": v["taches"], "nb_taches": len(v["taches"]), "heures_par_semaine": round(v["heures_par_semaine"], 1),
                       "exemples": v["exemples"][:4]} for k, v in gl.items()), key=lambda x: x["heures_par_semaine"], reverse=True)

    # --- ce qu'on ne sait pas ---
    limites = list(dict.fromkeys(t for r in valides for t in (texte_limite(l) for l in r.get("limites") or []) if t))
    peu_surs = [t["titre"] for t in groupes if t["confiance"] < 0.6]
    supposes = sum(e.get("statut") == "supposé" for t in groupes for e in t["etapes"])

    h_taches = sum(t["heures_par_semaine"] for t in groupes)
    return {**base, "statut": "ok", "regroupement": methode, "cout_horaire": cout_h,
            "periode": {"debut": min((r.get("periode") or {}).get("debut", "") for r in valides),
                        "fin": max((r.get("periode") or {}).get("fin", "") for r in valides)},
            "chiffres": {"heures_captees": round(heures, 1), "jours_personne": round(jours_total, 1), "apps": apps_distinctes,
                         "taches_repetees": len(groupes), "taches_communes": sum(1 for t in groupes if t["nb_personnes"]),
                         "heures_taches_par_semaine": round(h_taches, 1),
                         "cout_taches_par_mois": round(sum(t["cout_par_mois"] for t in groupes)),
                         "gain_top3_par_mois": round(sum(t["gain_par_mois"] for t in a_automatiser[:3])),
                         "heures_gagnees_top3_par_mois": round(sum(t["heures_gagnees_par_mois"] for t in a_automatiser[:3]), 1),
                         "utilisateurs_ia": tranche(utilisateurs_ia), "part_ia": round(sum(ia_min.values()) / (heures * 60), 2) if heures else 0,
                         "captures_regardees": sum((r.get("tri_80_20") or {}).get("captures_regardees", 0) for r in valides),
                         "captures_gardees": sum((r.get("tri_80_20") or {}).get("captures_gardees", 0) for r in valides)},
            "temps_par_categorie": agreger_lignes(lignes_cat, "categorie"),
            "temps_par_app": agreger_lignes(lignes_app, "app"),
            "usage_ia": ia, "taches": groupes, "a_automatiser": [t["titre"] for t in a_automatiser[:5]],
            "goulots": goulots,
            "inconnues": {"limites": limites[:6], "taches_peu_sures": peu_surs, "etapes_supposees": supposes}}


def vers_front_adamaass(ins, fictif=False):
    """Même résultat, au format attendu par le site de labs/adamaass (heures par semaine, « personnes » en nombre)."""
    o = ins.get("onboarding") or {}
    base = {"fictif": fictif, "entreprise": {"nom": ins["entreprise"], "secteur": o.get("activite", ""), "cout_horaire_eur": ins.get("cout_horaire") or o.get("cout_horaire", 40)},
            "personnes": {"invitees": ins["invites"], "participantes": ins["invites"], "validees": ins["participants"]}}
    if ins["statut"] != "ok":
        return {**base, "erreur": ins["message"]}
    c = ins["chiffres"]
    sem = max(1.0, c["jours_personne"] / ins["participants"] / 5)  # semaines couvertes en moyenne par personne
    hs = lambda m: round(m / 60 / sem, 1)
    nb = lambda p: p if isinstance(p, int) else (int(p) if str(p).isdigit() else 0)
    return {**base,
            "campagne": {"nom": ins.get("campagne") or "Campagne", "debut": ins["periode"]["debut"][:10], "fin": ins["periode"]["fin"][:10], "suppression_prevue": ""},
            "heures_captees": c["heures_captees"], "nb_apps": c["apps"],
            "tri_80_20": {"captures_regardees": c["captures_regardees"], "captures_gardees": c["captures_gardees"]},
            "temps_par_categorie": [{"categorie": x["categorie"], "heures_semaine": hs(x["minutes"])} for x in ins["temps_par_categorie"]],
            "temps_par_app": [{"app": x["app"], "heures_semaine": hs(x["minutes"])} for x in ins["temps_par_app"]],
            "taches": [{"id": f"t{i + 1}", "titre": t["titre"], "personnes": t["nb_personnes"] or 0, "frequence_par_semaine": t["frequence_par_semaine"],
                        "duree_moyenne_min": t["duree_moyenne_min"], "apps": t["apps"], "etapes": t["etapes"], "exceptions": t["exceptions"],
                        "goulots": t["goulots"], "score_automatisation": t["automatisable"]["score"], "pourquoi": " ".join(t["automatisable"]["pourquoi"]),
                        "confiance": t["confiance"], "statut": t["statut"], "preuves": t["preuves"]} for i, t in enumerate(ins["taches"])],
            "goulots": [{"type": g["type"], "detail": (g["exemples"] or [""])[0], "heures_semaine": g["heures_par_semaine"]} for g in ins["goulots"]],
            "usage_ia": [{"outil": u["outil"], "personnes": nb(u["personnes"]), "heures_semaine": hs(u["minutes"]), "usages": u["usages"]} for u in ins["usage_ia"]],
            "questions_ouvertes": ins["inconnues"]["limites"] + [f"Tâche peu sûre : {t}" for t in ins["inconnues"]["taches_peu_sures"]]}


def charger(chemins):
    fichiers = []
    for c in chemins:
        fichiers += sorted(glob.glob(os.path.join(c, "*.json"))) if os.path.isdir(c) else [c]
    return [json.load(open(f)) for f in fichiers]


def main():
    a = argparse.ArgumentParser()
    a.add_argument("resumes", nargs="+"); a.add_argument("--onboarding", required=True); a.add_argument("-o", "--sortie")
    a.add_argument("--ia", action="store_true", help="regrouper les tâches avec Claude plutôt que par mots-clés")
    a.add_argument("--format", choices=["complet", "adamaass"], default="complet", help="adamaass : le format du site de labs/adamaass")
    a.add_argument("--modele", default="sonnet"); args = a.parse_args()
    ins = fusionner(charger(args.resumes), json.load(open(args.onboarding)), "ia" if args.ia else "heuristique", args.modele)
    s = json.dumps(vers_front_adamaass(ins) if args.format == "adamaass" else ins, ensure_ascii=False, indent=1)
    if args.sortie:
        open(args.sortie, "w").write(s)
    if ins["statut"] != "ok":
        print(ins["message"]); return
    c = ins["chiffres"]
    print(f"{ins['participants']} participants ({ins['non_valides']} sans validation), {c['heures_captees']} h captées, regroupement {ins['regroupement']}")
    print(f"{c['taches_repetees']} tâches répétées ({c['taches_communes']} communes à 3 personnes ou plus), {c['cout_taches_par_mois']} €/mois")
    for t in ins["taches"][:5]:
        print(f"- {t['titre']} : {t['heures_par_mois']} h/mois, {t['cout_par_mois']} €/mois, {t['personnes']} pers., automatisable {t['automatisable']['score']}/100 → gain {t['gain_par_mois']} €/mois")


if __name__ == "__main__":
    main()
