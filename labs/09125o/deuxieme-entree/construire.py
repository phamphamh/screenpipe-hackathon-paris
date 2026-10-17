#!/usr/bin/env python3
"""La 2e entrée — la même tâche chez plusieurs personnes (pièce de 09125o).

Prend les résumés VALIDÉS d'une campagne (la démo Maison Corvo par défaut), retrouve
les tâches que la fusion regroupe entre personnes, et montre côte à côte les façons
de faire. Puis : la skill générée par l'app reprend la façon d'UNE personne de
référence — ce que cette façon couvre déjà chez les autres, et ce qu'il faut ajouter.

Réutilise la mécanique de regroupement officielle (labs/phamphamh/fusion/fusion.py),
sans la modifier : ce que la page montre est exactement ce que le produit fusionne.

Usage :
    python3 construire.py [--resumes labs/phamphamh/demo/resumes] [--sortie resultat.html]
Sorties : resultat.html (la page) + RESULTAT.md (le résumé chiffré).
"""
import argparse, html, json, os, sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(os.path.join(ICI, "..", "..", ".."))
sys.path.insert(0, os.path.join(RACINE, "labs", "phamphamh", "fusion"))
import fusion  # noqa: E402

TYPES = {"action": "Action", "input": "Entrée", "output": "Sortie", "decision": "Décision", "check": "Vérification"}


def e(s):
    return html.escape(str(s if s is not None else ""))


def nom_personne(pid):
    if pid.startswith("anonyme-"):
        return "Salarié " + pid.split("-", 1)[1]
    return pid


def similar(t1, t2):
    n1, n2 = fusion.normaliser(t1).strip(), fusion.normaliser(t2).strip()
    if n1 == n2:
        return 1.0
    if n1 and n2 and (n1 in n2 or n2 in n1):
        return 0.85
    return len(fusion.mots(t1) & fusion.mots(t2)) / (len(fusion.mots(t1) | fusion.mots(t2)) or 1)


def construire(dossier):
    resumes = [r for r in fusion.charger([dossier]) if r.get("valide_par_la_personne") is True]
    taches = []
    for rang, r in enumerate(resumes):
        for t in r.get("taches") or []:
            if t.get("titre"):
                taches.append({**t, "_personne": r["personne"], "_rang": rang})
    cats = sorted({c["categorie"] for r in resumes for c in r.get("temps_par_categorie") or []})
    outils = sorted({u["outil"] for r in resumes for u in r.get("usage_ia") or []})
    g = fusion.regrouper_heuristique(taches, cats, outils)

    groupes = []
    for grp in g["taches"]:
        membres = sorted([taches[i] for i in grp["membres"]], key=lambda m: m["_personne"])
        if len({m["_personne"] for m in membres}) < 2:
            continue
        ref = max(membres, key=lambda m: (m.get("confiance") or 0, len(m.get("etapes") or [])))
        pers = [m["_personne"] for m in membres]

        # lignes du tableau : on part des étapes de la référence, puis on aligne celles des autres
        lignes = []
        for et in ref.get("etapes") or []:
            lignes.append({"etape": et, "present": {ref["_personne"]: True}, "apps": {ref["_personne"]: et.get("app")}})
        for m in membres:
            if m is ref:
                continue
            utilisees = set()
            for ligne in lignes:
                best, score = None, 0.0
                for idx, et in enumerate(m.get("etapes") or []):
                    if idx in utilisees:
                        continue
                    s = similar(ligne["etape"]["texte"], et.get("texte", ""))
                    if s > score:
                        best, score = idx, s
                if best is not None and score >= 0.6:
                    utilisees.add(best)
                    ligne["present"][m["_personne"]] = True
                    ligne["apps"][m["_personne"]] = (m["etapes"][best] or {}).get("app")
                else:
                    ligne["present"][m["_personne"]] = False
            for idx, et in enumerate(m.get("etapes") or []):
                if idx not in utilisees:  # étape propre à cette personne : pas dans la façon de référence
                    lignes.append({"etape": et,
                                   "present": {p: (p == m["_personne"]) for p in pers},
                                   "apps": {m["_personne"]: et.get("app")}})

        outils_qui_varient = []
        for ligne in lignes:
            apps = {a for a in ligne["apps"].values() if a}
            if len(apps) >= 2:
                outils_qui_varient.append({"texte": ligne["etape"].get("texte", ""), "apps": sorted(apps)})

        couvertes = {}
        for p in pers:
            total = len([1 for m in membres if m["_personne"] == p for _ in m.get("etapes") or []])
            dedans = sum(1 for ligne in lignes if ligne["present"].get(p) and ref["_personne"] in ligne["present"] and ligne["present"][ref["_personne"]])
            couvertes[p] = {"total": total, "couvertes": min(dedans, total)}
        groupes.append({"titre": ref["titre"], "membres": membres, "ref": ref["_personne"], "pers": pers,
                        "lignes": lignes, "outils_qui_varient": outils_qui_varient, "couverture": couvertes,
                        "libelles": list(dict.fromkeys(m["titre"] for m in membres))})

    groupes.sort(key=lambda x: (len(x["pers"]), len(x["outils_qui_varient"])), reverse=True)
    return {"dossier": os.path.relpath(os.path.abspath(dossier), RACINE),
            "nb_valides": len(resumes), "groupes": groupes,
            "campagne_demo": all(r.get("campagne") == "demo-maison-corvo" for r in resumes) if resumes else True}


def bloc_etape(ligne, pers_actives, ref):
    et = ligne["etape"]
    badges = f'<span class="type">{e(TYPES.get(et.get("type"), et.get("type")))}</span>'
    if et.get("statut") == "supposé":
        badges += '<span class="suppose">supposé</span>'
    marques = []
    for p in pers_actives:
        if ligne["present"].get(p):
            app = ligne["apps"].get(p)
            marques.append(f'<span class="marque-p" title="app">{e(app or "app inconnue")}</span>')
        else:
            marques.append('<span class="absent">—</span>')
    return badges, marques


def page_html(d):
    c = []
    c.append(f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>La 2e entrée — la même tâche chez plusieurs personnes</title>
<style>
:root {{ --encre:#17141f; --encre-2:#4a4556; --encre-3:#8a8496; --papier:#f6f3ec; --carte:#fff;
  --trait:#e6e1d6; --violet:#5b3df5; --violet-pale:#ece8ff; --ambre:#b7791f; --ambre-pale:#fbf0dc;
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
.etiquette.violet {{ background:var(--violet-pale); color:var(--violet); }}
main {{ max-width:1060px; margin:0 auto; padding:28px 24px 60px; }}
h1 {{ font-size:34px; letter-spacing:-.02em; margin:14px 0 4px; }}
h1 em {{ font-family:var(--serif); font-style:italic; font-weight:400; color:var(--violet); }}
.sous {{ color:var(--encre-2); max-width:760px; }}
.bandeau-chiffres {{ display:flex; gap:10px; flex-wrap:wrap; margin:18px 0 8px; }}
.chiffre {{ background:var(--carte); border:1px solid var(--trait); border-radius:12px; padding:10px 14px; }}
.chiffre b {{ display:block; font-size:20px; }}
.chiffre span {{ color:var(--encre-3); font-size:12.5px; }}
.carte {{ background:var(--carte); border:1px solid var(--trait); border-radius:14px; padding:20px 22px;
  margin:16px 0; box-shadow:0 1px 2px rgba(23,20,31,.05); }}
.carte h2 {{ margin:0 0 2px; font-size:20px; letter-spacing:-.01em; }}
.carte .meta {{ color:var(--encre-3); font-size:13px; margin-bottom:14px; }}
table {{ border-collapse:collapse; width:100%; }}
th, td {{ text-align:left; vertical-align:top; padding:8px 10px; border-top:1px solid var(--trait); }}
th {{ font-size:12.5px; color:var(--encre-3); font-weight:600; border-top:0; }}
td.etape p {{ margin:0 0 3px; }}
.type {{ font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:.04em; color:var(--encre-2);
  background:#efebe2; border-radius:6px; padding:2px 7px; margin-right:6px; }}
.suppose {{ font-size:11px; font-weight:600; color:var(--ambre); background:var(--ambre-pale); border-radius:6px; padding:2px 7px; }}
.marque-p {{ display:inline-block; font-size:12px; background:var(--violet-pale); color:var(--violet);
  border-radius:8px; padding:3px 8px; margin:2px 4px 2px 0; }}
.absent {{ color:var(--encre-3); }}
.outil-diff {{ font-size:12px; color:var(--ambre); font-weight:600; }}
.skill {{ background:#faf8f3; border:1px dashed var(--trait); border-radius:12px; padding:14px 16px; margin-top:14px; }}
.skill h3 {{ margin:0 0 6px; font-size:14px; }}
.skill ul {{ margin:6px 0 0; padding-left:18px; }}
.skill li {{ margin:3px 0; }}
.ok {{ color:#1f9d6b; font-weight:600; }}
.note {{ color:var(--encre-3); font-size:12.5px; }}
footer {{ max-width:1060px; margin:0 auto; padding:0 24px 40px; color:var(--encre-3); font-size:12.5px; }}
</style></head><body>
<header class="bandeau"><span class="marque"><i></i>Wrapped</span>
<span><span class="etiquette">pièce de 09125o</span>
&nbsp;<span class="etiquette {'violet' if d['campagne_demo'] else ''}">{'Démo · Maison Corvo (fictive)' if d['campagne_demo'] else 'Campagne réelle — à relire avant tout partage'}</span></span></header>
<main>
<h1>La 2e entrée, <em>prise au sérieux.</em></h1>
<p class="sous">La fusion de l'app regroupe les tâches faites par plusieurs personnes. Mais la skill est écrite à partir
de <b>la façon d'une personne de référence</b> (celle qui a le plus de confiance et d'étapes). Cette page montre, tâche par tâche :
la même activité chez chacun, ce que la façon de référence couvre déjà, et <b>ce qu'il reste à absorber</b> — souvent le même travail,
mais pas le même outil. Données : les résumés validés de la démo (fictive, étiquetée).</p>""")

    nb = len(d["groupes"])
    nb_pers = len({p for gr in d["groupes"] for p in gr["pers"]})
    nb_outils = sum(1 for gr in d["groupes"] if gr["outils_qui_varient"])
    orphelines = sum(gr["couverture"][p]["total"] - gr["couverture"][p]["couvertes"] for gr in d["groupes"] for p in gr["pers"] if p != gr["ref"])
    c.append(f"""<div class="bandeau-chiffres">
<div class="chiffre"><b>{nb}</b><span>tâches à ≥ 2 personnes</span></div>
<div class="chiffre"><b>{nb_pers}</b><span>salariés concernés</span></div>
<div class="chiffre"><b>{nb_outils}</b><span>tâches à outil variable</span></div>
<div class="chiffre"><b>{orphelines}</b><span>étapes hors référence</span></div>
</div>""")
    if d["campagne_demo"]:
        c.append('<p class="note">Démo Maison Corvo : 6 salariés invités, 5 résumés validés, 1 sans validation (jamais compté).</p>')

    for gr in d["groupes"]:
        ref_nom = nom_personne(gr["ref"])
        c.append('<section class="carte">')
        c.append(f'<h2>{e(gr["titre"])}</h2>')
        libs = " · ".join(f'« {e(l)} »' for l in gr["libelles"][:4])
        c.append(f'<div class="meta">{len(gr["pers"])} personnes · {libs} · façon de référence : <b>{e(ref_nom)}</b></div>')
        c.append("<table><tr><th>Étapes</th>" + "".join(f"<th>{e(nom_personne(p))}</th>" for p in gr["pers"]) + "</tr>")
        for ligne in gr["lignes"]:
            badges, marques = bloc_etape(ligne, gr["pers"], gr["ref"])
            apps_presents = {a for a in ligne["apps"].values() if a}
            diff = ' <span class="outil-diff">outil différent</span>' if len(apps_presents) >= 2 else ""
            c.append(f'<tr><td class="etape">{badges}{diff}<p>{e(ligne["etape"].get("texte"))}</p></td>'
                     + "".join(f"<td>{m}</td>" for m in marques) + "</tr>")
        c.append("</table>")

        # couverture / à absorber
        lignes_skill = []
        for p in gr["pers"]:
            if p == gr["ref"]:
                continue
            cv = gr["couverture"][p]
            manque = cv["total"] - cv["couvertes"]
            if manque == 0:
                lignes_skill.append(f'<li>{e(nom_personne(p))} : les {cv["total"]} étapes sont déjà dans la façon de référence. <span class="ok">couvert</span></li>')
            else:
                propres = [l for l in gr["lignes"] if l["present"].get(p) and not l["present"].get(gr["ref"])]
                detail = " ; ".join(e(l["etape"].get("texte")) for l in propres[:4])
                lignes_skill.append(f'<li>{e(nom_personne(p))} : {manque} étape(s) propre(s) à ajouter — {detail}</li>')
        outils = [f'étape « {e(o["texte"])[:70]} » : ' + " / ".join(e(a) for a in o["apps"]) for o in gr["outils_qui_varient"]]
        c.append('<div class="skill"><h3>Ce que ça change pour la skill</h3><ul>')
        nb_etapes_ref = sum(1 for l in gr["lignes"] if l["present"].get(gr["ref"]))
        c.append(f'<li>La skill actuelle reprend la façon de <b>{e(ref_nom)}</b> ({nb_etapes_ref} étapes).</li>')
        c.extend(lignes_skill)
        for app_line in outils:
            c.append(f'<li>Même étape, outil différent selon la personne → {app_line}</li>')
        c.append("</ul></div></section>")

    c.append("""</main>
<footer>Généré par <code>labs/09125o/deuxieme-entree/construire.py</code> — le regroupement vient de la fusion officielle
(<code>labs/phamphamh/fusion/fusion.py</code>), rien n'est recalculé à la main. En relecture, chacun a validé son propre résumé ;
le Wrapped, lui, n'affiche que des agrégats (« moins de 3 personnes → masqué »).</footer>
</body></html>""")
    return "\n".join(c)


def resultat_md(d):
    l = [f"# La 2e entrée — résultat", "",
         f"Source : `{d['dossier']}` · {d['nb_valides']} résumés validés · généré par `construire.py`.", ""]
    for gr in d["groupes"]:
        ref = nom_personne(gr["ref"])
        l.append(f"## {gr['titre']} — {len(gr['pers'])} personnes")
        for m in gr["membres"]:
            l.append(f"- {nom_personne(m['_personne'])} : « {m['titre']} » · {m.get('frequence_par_semaine')}×/sem × {m.get('duree_moyenne_min')} min · apps {', '.join(m.get('apps') or [])}")
        l.append(f"- Façon de référence (reprise par la skill) : **{ref}**")
        for p in gr["pers"]:
            if p == gr["ref"]:
                continue
            cv = gr["couverture"][p]
            l.append(f"- {nom_personne(p)} : {cv['couvertes']}/{cv['total']} étapes déjà couvertes par la référence")
        for o in gr["outils_qui_varient"]:
            l.append(f"- Outil qui varie : {' / '.join(o['apps'])} (étape « {o['texte']} »)")
        l.append("")
    l.append("Limites : démo Maison Corvo (fictive) ; sur une campagne réelle, page à relire avant tout partage.")
    return "\n".join(l)


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--resumes", default=os.path.join(RACINE, "labs", "phamphamh", "demo", "resumes"))
    a.add_argument("--sortie", default=os.path.join(ICI, "resultat.html"))
    args = a.parse_args()
    d = construire(args.resumes)
    open(args.sortie, "w").write(page_html(d))
    md = os.path.join(os.path.dirname(args.sortie), "RESULTAT.md")
    open(md, "w").write(resultat_md(d))
    print(f"{len(d['groupes'])} tâches communes à ≥2 personnes → {os.path.relpath(args.sortie, RACINE)}")
    for gr in d["groupes"]:
        print(f"- {gr['titre']} : {len(gr['pers'])} personnes, ref {nom_personne(gr['ref'])}, "
              f"{len(gr['outils_qui_varient'])} étape(s) à outil variable")
    print(f"→ {os.path.relpath(md, RACINE)}")


if __name__ == "__main__":
    main()
