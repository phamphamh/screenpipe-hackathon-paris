"""Fusion minimale (brique D) : plusieurs résumés validés (brique C) → insights.json pour le Wrapped (brique E).

Version de départ pour brancher le front sur de vrais résumés. Les tâches de personnes différentes sont regroupées
quand leurs libellés se ressemblent (mots communs), pas encore par leurs étapes.
Usage : python3 fusion.py resume-a.json resume-b.json ... [--entreprise "Nom"] [--cout-horaire 45] [--sortie insights.json]
Bibliothèque standard uniquement.
"""
import argparse, json, re, sys, unicodedata
from collections import defaultdict

MOTS_VIDES = set("le la les un une des de du d l a au aux et ou en sur pour par avec sans dans son sa ses mon ma mes ce cette".split())

def mots(titre):
    t = unicodedata.normalize("NFD", titre.lower()).encode("ascii", "ignore").decode()
    # 5 premières lettres : « relance », « relancer », « relances » comptent comme le même mot
    return {m[:5] for m in re.findall(r"[a-z0-9]+", t) if m not in MOTS_VIDES and len(m) > 2}

def proches(a, b):
    return len(a & b) / max(1, len(a | b)) >= 0.5

def main():
    p = argparse.ArgumentParser()
    p.add_argument("resumes", nargs="+"); p.add_argument("--entreprise", default="Votre entreprise")
    p.add_argument("--cout-horaire", type=float, default=45); p.add_argument("--sortie", default="insights.json")
    p.add_argument("--invitees", type=int, default=0)
    a = p.parse_args()

    rs = [json.load(open(f)) for f in a.resumes]
    refuses = [r.get("personne", f) for r, f in zip(rs, a.resumes) if not r.get("valide_par_la_personne")]
    if refuses:
        sys.exit(f"Résumés non validés par la personne, refusés : {', '.join(map(str, refuses))}")
    personnes = sorted({r["personne"] for r in rs})
    if len(personnes) < len(rs):
        print(f"Attention : {len(rs)} fichiers mais seulement {len(personnes)} personnes distinctes (champ « personne »).", file=sys.stderr)
    # Toutes les fréquences sont ramenées à une semaine de 5 jours par personne : le résumé les extrapole déjà.

    cat, app, ia = defaultdict(float), defaultdict(float), defaultdict(lambda: {"minutes": 0, "personnes": set(), "usages": set()})
    groupes = []  # [{mots, taches:[(personne, tache)]}]
    for r in rs:
        for c in r.get("temps_par_categorie", []): cat[c["categorie"]] += c["minutes"]
        for x in r.get("temps_par_app", []): app[x["app"]] += x["minutes"]
        for u in r.get("usage_ia", []):
            ia[u["outil"]]["minutes"] += u["minutes"]; ia[u["outil"]]["personnes"].add(r["personne"]); ia[u["outil"]]["usages"].update(u.get("usages", []))
        for t in r.get("taches", []):
            m = mots(t["titre"])
            g = next((g for g in groupes if proches(g["mots"], m)), None)
            if g: g["taches"].append((r["personne"], t)); g["mots"] |= m
            else: groupes.append({"mots": m, "taches": [(r["personne"], t)]})

    taches, goulots, qui_goulot = [], defaultdict(float), defaultdict(set)
    for i, g in enumerate(groupes):
        ts = [t for _, t in g["taches"]]
        ref = max(ts, key=lambda t: len(t.get("etapes", [])))  # la description la plus détaillée sert de modèle
        freq = sum(t.get("frequence_par_semaine", 0) for t in ts)
        duree = sum(t.get("duree_moyenne_min", 0) * t.get("frequence_par_semaine", 0) for t in ts) / max(1, freq)
        score = round(sum(t.get("automatisable", {}).get("score", 0) for t in ts) / len(ts))
        conf = round(sum(t.get("confiance", 0.5) for t in ts) / len(ts), 2)
        for p_, t in g["taches"]:
            for gl in t.get("goulots", []):
                qui_goulot[(gl["type"], gl["detail"])].add(p_)
                goulots[(gl["type"], gl["detail"])] += t.get("frequence_par_semaine", 0) * t.get("duree_moyenne_min", 0) / 60 / max(1, len(t.get("goulots", [])))
        observe = all(e.get("statut") == "observé" for e in ref.get("etapes", [])) and len(ts) > 1
        taches.append({
            "id": f"t{i + 1}", "titre": ref["titre"], "personnes": len({p for p, _ in g["taches"]}),
            "frequence_par_semaine": round(freq, 1), "duree_moyenne_min": round(duree, 1),
            "apps": sorted({x for t in ts for x in t.get("apps", [])}),
            "etapes": ref.get("etapes", []), "exceptions": sorted({x for t in ts for x in t.get("exceptions", [])}),
            "goulots": ref.get("goulots", []),
            "score_automatisation": score, "pourquoi": ref.get("automatisable", {}).get("pourquoi", ""),
            "confiance": conf, "statut": "observé" if observe else "estimé",
            "preuves": [{**pr, "personne": p} for p, t in g["taches"] for pr in t.get("preuves", [])],
        })

    debuts = sorted(r["periode"]["debut"] for r in rs); fins = sorted(r["periode"]["fin"] for r in rs)
    tri = [r.get("tri_80_20") for r in rs if r.get("tri_80_20")]
    limites = sorted({l for r in rs for l in r.get("limites", [])})
    insights = {
        "fictif": any(re.search(r"fictiv", l, re.I) for l in limites),
        "entreprise": {"nom": a.entreprise, "secteur": "", "cout_horaire_eur": a.cout_horaire},
        "campagne": {"nom": "Campagne", "debut": debuts[0][:10], "fin": fins[-1][:10]},
        "personnes": {"invitees": max(a.invitees, len(personnes)), "participantes": len(personnes), "validees": len(personnes)},
        "heures_captees": round(sum(r.get("heures_captees", 0) for r in rs), 1),
        "nb_apps": len(app),
        "tri_80_20": {"captures_regardees": sum(x["captures_regardees"] for x in tri), "captures_gardees": sum(x["captures_gardees"] for x in tri)} if tri else None,
        "temps_par_categorie": [{"categorie": k, "heures_semaine": round(v / 60, 1)} for k, v in sorted(cat.items(), key=lambda x: -x[1])],
        "temps_par_app": [{"app": k, "heures_semaine": round(v / 60, 1)} for k, v in sorted(app.items(), key=lambda x: -x[1])],
        "taches": sorted(taches, key=lambda t: -t["frequence_par_semaine"] * t["duree_moyenne_min"]),
        "goulots": [{"type": k[0], "detail": k[1], "personnes": len(qui_goulot[k]), "heures_semaine": round(v, 1)} for k, v in sorted(goulots.items(), key=lambda x: -x[1])][:6],
        "usage_ia": [{"outil": k, "personnes": len(v["personnes"]), "heures_semaine": round(v["minutes"] / 60, 1), "usages": sorted(v["usages"])} for k, v in ia.items()],
        "questions_ouvertes": limites,
    }
    json.dump(insights, open(a.sortie, "w"), ensure_ascii=False, indent=1)
    print(f"{len(personnes)} personnes, {len(taches)} tâches ({sum(t['personnes'] >= 3 for t in taches)} visibles à 3 personnes ou plus) → {a.sortie}")

if __name__ == "__main__":
    main()
