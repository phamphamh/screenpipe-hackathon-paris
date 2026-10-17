"""Portail CAIbinet (style de labs/tmschrib/dashboard-client) rempli avec les vraies données d'« Atelier Nova ».

Sources (dans donnees/, jamais commitées) :
- donnees/nova/insights-officiel.json : la fusion officielle (labs/phamphamh/fusion/fusion.py) des 6 salariés back-office
- donnees/nova/<pseudo>/moments.json et resume-valide.json : les moments (heures, écrans) et les résumés validés
Sortie : labs/adamaass/caibinet-nova/data.js (chiffres agrégés par équipe de 3, aucun texte d'écran).
Ce que Nova ne mesure pas (attentes entre équipes, copier-coller, autres applis) est affiché « non mesuré », jamais inventé.
Usage : python3 labs/adamaass/caibinet-nova/construire.py
"""
import json, os, re
from collections import Counter, defaultdict
from datetime import datetime

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(os.path.join(ICI, "..", "..", ".."))
NOVA = os.path.join(RACINE, "donnees", "nova")
EQUIPES = {"E-commerce": ["lea", "karim", "sophie"], "Opérations": ["nadia", "julien", "emma"]}
EQUIPE_DE = {p: e for e, ps in EQUIPES.items() for p in ps}
SEMAINES_AN = 46
NOMS_J = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
NOMS_JL = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
SECTIONS = [("Rapports", ("reports/",)), ("Catalogue", ("catalog/", "catalog_rule/")), ("Commandes", ("sales/order", "sales/invoice", "admin/order_shipment")),
            ("Avis", ("review/",)), ("Clients", ("customer/",)), ("Marketing", ("sales_rule/", "cms/", "search/"))]

def section(url):
    r = url.split("/admin/", 1)[-1]
    for nom, prefixes in SECTIONS:
        if r.startswith(prefixes):
            return nom
    return "Accueil"

def hm(h):
    m = round(h * 60)
    return f"{m // 60} h {m % 60:02d}" if m >= 60 else f"{m} min"

def euros(x):
    return f"{round(x):,} €".replace(",", " ")

ins = json.load(open(os.path.join(NOVA, "insights-officiel.json")))
cout_h = ins["cout_horaire"]
resumes = {p: json.load(open(os.path.join(NOVA, p, "resume-valide.json"))) for p in EQUIPE_DE}
moments = {p: json.load(open(os.path.join(NOVA, p, "moments.json")))["moments"] for p in EQUIPE_DE}

# ---------- temps : par jour, par heure, par écran, enchaînements ----------
DATES = sorted({datetime.fromisoformat(m["debut"]).date() for ms in moments.values() for m in ms})  # les vrais jours travaillés
JOURS = [f"{NOMS_J[d.weekday()]} {d.day}" for d in DATES]
par_jour, chaleur, par_equipe_section = Counter(), defaultdict(float), defaultdict(Counter)
seq3, paires, bascules = Counter(), Counter(), 0
for p, ms in moments.items():
    prec = []
    for m in ms:
        t = datetime.fromisoformat(m["debut"])
        j = DATES.index(t.date())
        par_jour[j] += m["minutes"]
        if 8 <= t.hour <= 18:
            chaleur[(j, t.hour)] += m["minutes"]
        s = section(m["url"])
        par_equipe_section[EQUIPE_DE[p]][s] += m["minutes"]
        if not prec or prec[-1] != s:
            if prec:
                paires[f"{prec[-1]} → {s}"] += 1
                bascules += 1
            prec.append(s)
            if len(prec) >= 3:
                seq3[" → ".join(prec[-3:])] += 1

noms_sections = [n for n, _ in SECTIONS] + ["Accueil"]
tot_eq = {e: sum(c.values()) for e, c in par_equipe_section.items()}

# ---------- tâches et problèmes (fusion officielle) ----------
def qui_fait(tache):
    lib = set(tache.get("libelles") or [tache["titre"]])
    return sorted({p for p, r in resumes.items() for t in r["taches"] if t["titre"] in lib})

def categorie(t):
    titre = t["titre"].lower()
    gl = {g if isinstance(g, str) else g.get("type") for g in t.get("goulots", [])}
    if re.match(r"(recherch|retrouv|consult|filtr)", titre):
        return "Recherche"
    if "rework" in gl:
        return "Ressaisie"
    return "Répétition"

visibles = [t for t in ins["taches"] if (t.get("nb_personnes") or 0) >= 3]
visibles.sort(key=lambda t: -t["heures_par_semaine"])
problemes = []
for i, t in enumerate(visibles, 1):
    ps = qui_fait(t)
    equipes = sorted({EQUIPE_DE[p] for p in ps})
    score = t["automatisable"]["score"]
    auto = "oui" if score >= 75 else "partiel" if score >= 45 else "non"
    h = t["heures_par_semaine"]
    etapes = [e["texte"] for e in t.get("etapes", [])]
    problemes.append({
        "id": i, "cat": categorie(t), "path": ", ".join(equipes) or "—", "title": t["titre"],
        "metaBits": [f"{t['frequence_par_semaine']} fois / sem.", f"{hm(h)} / sem.", f"Automatisable : {auto}"],
        "annualCost": round(h * SEMAINES_AN * cout_h), "status": "À valider",
        "detail": {
            "description": (t["automatisable"].get("pourquoi") or [""])[0],
            "lostPerWeek": hm(h), "confidence": "Élevée" if (t.get("confiance") or 0) >= 0.7 else "Moyenne",
            "observed": [f"{t['frequence_par_semaine']} occurrences sur la semaine observée",
                         f"{t['nb_personnes']} personnes concernées ({', '.join(equipes)})",
                         f"{len(t.get('exceptions', []))} exception(s) relevée(s) : {(t.get('exceptions') or ['aucune'])[0][:90]}",
                         f"{len(t.get('libelles') or [])} façons de la nommer chez les salariés"],
            "sequence": [re.sub(r"\s*\(.*?\)", "", e)[:28] for e in etapes[:3]] or ["Magento"],
            "solution": f"Skill « {t['titre']} » : les étapes observées deviennent une automatisation, les décisions restent humaines (score {score}/100).",
        },
    })
masquees = [t for t in ins["taches"] if (t.get("nb_personnes") or 0) < 3]

# ---------- business case ----------
h_total = sum(t["heures_par_semaine"] for t in ins["taches"])
gain_an = sum(t["gain_par_mois"] for t in ins["taches"]) * 12
h_gagnees_sem = sum(t["heures_gagnees_par_mois"] for t in ins["taches"]) * 12 / SEMAINES_AN
modules = []
for k, titre in enumerate(ins["a_automatiser"][:5], 1):
    t = next(x for x in ins["taches"] if x["titre"] == titre)
    pid = next((p["id"] for p in problemes if p["title"] == titre), None)
    sc = t["automatisable"]["score"]
    modules.append({"order": k, "name": f"Skill · {titre}", "tag": "Gain rapide" if sc >= 80 else None,
                    "problems": f"n° {pid:02d}" if pid else "moins de 3 pers.",
                    "recovered": f"{hm(t['heures_gagnees_par_mois'] * 12 / SEMAINES_AN)} / sem.",
                    "gain": round(t["gain_par_mois"] * 12), "delay": "1 sem." if sc >= 80 else "2 sem."})

# ---------- signaux, interactions ----------
communes = [t for t in visibles if len({EQUIPE_DE[p] for p in qui_fait(t)}) == 2]
top_section = max(((s, sum(par_equipe_section[e][s] for e in EQUIPES)) for s in noms_sections), key=lambda x: x[1])[0]
nodes = [{"id": "ecom", "label": "E-commerce", "sub": f"3 pers. · {hm(tot_eq['E-commerce'] / 60)}", "x": 14, "y": 30},
         {"id": "ops", "label": "Opérations", "sub": f"3 pers. · {hm(tot_eq['Opérations'] / 60)}", "x": 14, "y": 72}]
pos = {s: (80, 8 + 17 * k) for k, s in enumerate(["Catalogue", "Commandes", "Rapports", "Avis", "Clients", "Marketing"])}  # une colonne d'écrans
edges = []
for s, (x, y) in pos.items():
    total_s = sum(par_equipe_section[e][s] for e in EQUIPES)
    if total_s < 1:
        continue
    nodes.append({"id": s.lower(), "label": s, "sub": f"{round(total_s)} min observées", "x": x, "y": y,
                  **({"highlight": "goulot"} if s == top_section else {})})
    for e, eid in (("E-commerce", "ecom"), ("Opérations", "ops")):
        part = par_equipe_section[e][s] / max(tot_eq[e], 1)
        if part >= 0.10:
            edges.append({"from": eid, "to": s.lower(), "label": f"{round(part * 100)} %",
                          "detail": f"{e} · {s} : {round(part * 100)} % de son temps", "level": "goulot" if part >= 0.3 else "attente" if part >= 0.15 else "fluide"})

goulots_txt = {"rework": "Travail refait", "switching": "Allers-retours", "waiting": "Attente", "handoff": "Passage de relais", "unclear": "Flou"}
bottlenecks = []
for g in ins["goulots"][:3]:
    ex = (g.get("exemples") or [""])[0]
    pid = next((p["id"] for p in problemes if p["title"] in g.get("taches", [])), None)
    bottlenecks.append({"tag": goulots_txt.get(g["type"], g["type"]), "title": f"{hm(g['heures_par_semaine'])} par semaine, dans {g['nb_taches']} tâches",
                        "text": ex if isinstance(ex, str) else json.dumps(ex, ensure_ascii=False), "link": f"Voir le problème n° {pid:02d}" if pid else None, "problemId": pid})

# ---------- outils ----------
by_team = []
for e in EQUIPES:
    vals = [round(100 * par_equipe_section[e][s] / max(tot_eq[e], 1)) for s in noms_sections]
    by_team.append({"team": e, "values": vals})
maxc = max(chaleur.values() or [1])
heat = [[min(5, round(5 * chaleur[(j, h)] / maxc)) for h in range(8, 19)] for j in range(len(DATES))]
pic = max(chaleur, key=chaleur.get)

top3 = visibles[:3]
part_top3 = sum(t["heures_par_semaine"] for t in top3) / max(sum(t["heures_par_semaine"] for t in visibles), 0.01)
VERDICTS = {
    "overview": f"Observation terminée. <b>{visibles[0]['titre']}</b> revient {visibles[0]['frequence_par_semaine']} fois par semaine chez les 6 postes : c'est la première tâche à regarder.",
    "problems": f"<b>{len(problemes)} problèmes</b> à valider avec vous. Les 3 premiers pèsent {round(part_top3 * 100)} % du temps perdu.",
    "interactions": f"Les 2 équipes font <b>les mêmes {len(communes)} tâches</b>. C'est l'écran <b>{top_section}</b> qui concentre le plus de temps.",
    "tools": f"Tout le travail observé se passe dans Magento, avec <b>{round(bascules / (len(DATES) * 6))} changements d'écran</b> par jour et par poste.",
    "business": f"<b>{len(modules)} skills</b> récupèrent {euros(gain_an)} par an. La première se construit en {modules[0]['delay']}",
    "piloting": "Rien n'est encore en production. Cet écran prendra le relais une fois la première skill déployée.",
}

DATA = {
    "verdicts": VERDICTS,
    "maxKpi": 3,
    "firm": "CAIbinet",
    "client": {"name": "Atelier Nova", "postes": 6, "equipes": 2, "abonnement": "Pas encore d'abonnement (projection)"},
    "consultant": "Équipe hackathon",
    "studyLabel": "Étude d'efficacité opérationnelle",
    "demoTag": "Données WONDERBREAD · salariés fictifs",
    "steps": [
        {"n": 1, "label": "Installation", "date": "lun. 12 oct.", "status": "done", "sub": "Terminé"},
        {"n": 2, "label": "Observation", "date": f"{DATES[0].day} → {DATES[-1].day} oct.", "status": "done", "sub": f"{len(DATES)} jours"},
        {"n": 3, "label": "Analyse par l'IA", "date": "fin d'observation", "status": "done", "sub": "Terminé"},
        {"n": 4, "label": "Restitution & rapport", "date": "aujourd'hui", "status": "active", "sub": "En cours"},
        {"n": 5, "label": "Logiciel sur mesure", "date": "à planifier", "status": "upcoming", "sub": "À venir"},
    ],
    "advancementPct": 70,
    "overview": {
        "dayLabel": "Observation terminée · restitution en cours",
        "stats": [
            {"label": "Gain annuel récupérable", "value": euros(gain_an), "sub": f"en automatisant {len(ins['a_automatiser'])} tâches", "accent": "good"},
            {"label": "Postes observés", "value": "6 / 6", "sub": "2 équipes de 3 · back-office Magento"},
            {"label": "Heures de travail observées", "value": f"{ins['chiffres']['heures_captees']:.1f} h".replace(".", ","), "sub": f"temps actif dans l'outil, sur {len(DATES)} jours"},
            {"label": "Workflows identifiés", "value": str(ins["chiffres"]["taches_repetees"]), "sub": f"dont {len(visibles)} communs à 3 personnes ou plus"},
            {"label": "Problèmes détectés", "value": str(len(problemes)), "sub": f"{len(masquees)} autres non détaillés (moins de 3 pers.)"},
        ],
        "dailyHours": [{"day": JOURS[j], "value": round(par_jour[j] / 60, 2), "known": True} for j in range(len(DATES))],
        "teamCoverage": [{"team": e, "have": 3, "total": 3} for e in EQUIPES],
        "signals": [{"tag": p["cat"], "path": p["path"], "text": p["title"], "meta": " · ".join(p["metaBits"][:2]),
                     "confidence": "Confiance élevée" if p["detail"]["confidence"] == "Élevée" else "Confiance moyenne · à confirmer"} for p in problemes[:3]],
        "signalsUpdated": "à la fin de l'observation",
        "toRelaunch": [],
        "toRelaunchEmpty": "Aucun : les 6 postes ont validé leur résumé (validation de démo, sans relecture humaine).",
        "compliance": [
            "Données publiques WONDERBREAD (Stanford, CC-BY-4.0)",
            "Salariés fictifs : prénoms inventés, un annotateur réel différent par poste",
            "Aucune capture ni texte d'écran dans ce portail",
            "Analyse par équipe de 3 personnes minimum",
            "Tâche partagée par moins de 3 personnes : non détaillée",
            "Résumés validés pour la démo, sans relecture humaine",
        ],
        "nextSteps": [
            {"date": "Aujourd'hui", "text": "Restitution : Wrapped, rapport du cabinet et liste des déclencheurs"},
            {"date": "Ensuite", "text": "Relecture des résumés par chaque salarié, pour de vrai"},
            {"date": "Puis", "text": f"Skill n° 1 : « {ins['a_automatiser'][0]} »"},
        ],
    },
    "problemsMeta": {"total": len(problemes), "hoursPerWeek": hm(sum(p_["heures_par_semaine"] for p_ in visibles)),
                     "annualCost": sum(p["annualCost"] for p in problemes), "validated": 0,
                     "categories": ["Tous"] + sorted({p["cat"] for p in problemes})},
    "problems": problemes,
    "extraProblemsCount": len(masquees),
    "extraProblemsHoursSupplement": f"{hm(sum(t['heures_par_semaine'] for t in masquees))} / sem.",
    "interactions": {
        "stats": [
            {"label": "Tâches communes aux 2 équipes", "value": str(len(communes)), "sub": f"sur {len(visibles)} visibles"},
            {"label": "Écrans Magento utilisés", "value": str(sum(1 for s in noms_sections if sum(par_equipe_section[e][s] for e in EQUIPES) >= 1)), "sub": "sections du back-office"},
            {"label": "Écran le plus utilisé", "value": top_section, "sub": ""},
            {"label": "Temps passé à attendre une info", "value": "Non mesuré", "sub": "un seul outil observé"},
        ],
        "weekLabel": f"Du {DATES[0].day} au {DATES[-1].day} octobre ({len(DATES)} jours travaillés)",
        "nodes": nodes, "edges": edges,
        "legend": [{"label": "moins de 15 % du temps", "level": "fluide"}, {"label": "15 à 30 %", "level": "attente"}, {"label": "plus de 30 %", "level": "goulot"}],
        "legendNote": "Équipe → écran du back-office : part de son temps",
        "bottlenecks": bottlenecks,
        "waitTeams": [], "waitMatrix": [],
        "waitNote": "Non mesuré : Atelier Nova n'a été observé que dans Magento. Les attentes entre équipes demandent la messagerie (mail, chat) dans la capture.",
    },
    "tools": {
        "stats": [
            {"label": "Temps dans votre outil métier", "value": "100 %", "sub": "Magento (seul outil observé)"},
            {"label": "Changements d'écran", "value": str(round(bascules / (len(DATES) * 6))), "sub": "par jour et par poste"},
            {"label": "Allers-retours entre écrans", "value": str(bascules), "sub": "sur la semaine"},
            {"label": "Temps en messagerie et tableurs", "value": "Non mesuré", "sub": "absent de ces données"},
        ],
        "appCategories": noms_sections, "byTeam": by_team,
        "byTeamTitle": "Répartition du temps par écran du back-office",
        "callout": f"Le catalogue et les commandes concentrent l'essentiel du temps. {problemes[0]['title']} revient {visibles[0]['frequence_par_semaine']} fois par semaine chez les 2 équipes.",
        "heatmapHours": [f"{h}h" for h in range(8, 19)], "heatmapDays": JOURS, "heatmapMatrix": heat,
        "heatmapPeakNote": f"Pic : {NOMS_JL[DATES[pic[0]].weekday()]} {DATES[pic[0]].day} oct., {pic[1]} h–{pic[1] + 1} h",
        "sequences": [{"path": k, "count": v} for k, v in seq3.most_common(4)],
        "copyPasteTitle": "Allers-retours les plus fréquents",
        "copyPaste": [{"path": k, "count": v} for k, v in paires.most_common(4)],
    },
    "businessCase": {
        "stats": [
            {"label": "Coût annuel des tâches répétées observées", "value": euros(h_total * SEMAINES_AN * cout_h), "sub": f"{hm(h_total)} par semaine, sur {len(ins['taches'])} tâches"},
            {"label": "Gain annuel récupérable", "value": euros(gain_an), "sub": f"{round(100 * h_gagnees_sem / max(h_total, 0.01))} % du temps de ces tâches", "accent": "good"},
            {"label": "Capacité libérée", "value": f"{h_gagnees_sem / 35:.2f} ETP".replace(".", ","), "sub": "base 35 h / semaine"},
        ],
        "modules": modules,
        "modulesNote": "Tâches WONDERBREAD courtes (moins d'1 min 30) : les montants sont faibles, mais chaque chiffre vient d'une tâche observée et cliquable.",
        "beforeAfter": {"before": hm(h_total), "after": hm(h_total - h_gagnees_sem), "beforeH": round(h_total, 3), "afterH": round(h_total - h_gagnees_sem, 3), "note": f"{hm(h_gagnees_sem)} rendues chaque semaine aux 6 postes observés."},
        "investment": [{"label": "Étude (une fois)", "value": "[À COMPLÉTER]"}, {"label": "Abonnement logiciel", "value": "[À COMPLÉTER]"},
                       {"label": "Gain net la première année", "value": "[À COMPLÉTER]"}, {"label": "Retour sur investissement", "value": "[À COMPLÉTER]"}],
        "assumptions": [f"Coût horaire chargé : {cout_h:.0f} €/h", f"Semaines travaillées : {SEMAINES_AN} / an", f"Base : {len(DATES)} jours d'observation, 6 postes",
                        "Fréquences = occurrences observées sur la semaine", "Gain = coût × score d'automatisation (fusion officielle)", "Résumés non relus par des humains : à confirmer"],
    },
    "piloting": {
        "inProductionSince": "Projection · aucun module n'est encore en production",
        "stats": [
            {"label": "Heures récupérables par mois", "value": hm(h_gagnees_sem * SEMAINES_AN / 12), "sub": "si les 5 skills sont déployées", "progress": 0},
            {"label": "Valeur annuelle visée", "value": euros(gain_an), "sub": "pas encore générée"},
            {"label": "Tâches automatisables", "value": str(len(ins["a_automatiser"])), "sub": "classées par gain"},
            {"label": "Adoption", "value": "—", "sub": "mesurée après déploiement"},
        ],
        "chart": {"xLabels": ["Étude", "Aujourd'hui"], "measured": [round(h_total, 2), round(h_total, 2)], "objective": round(h_total - h_gagnees_sem, 2),
                  "objectiveLabel": hm(h_total - h_gagnees_sem), "annotations": []},
        "modules": [{"name": m["name"], "status": "Planifié"} for m in modules],
        "toHandle": [
            {"icon": "warning", "title": "Cas d'arrêt à définir", "text": "La page « Dès que… » relève les exceptions de chaque tâche : il faut dire qui prévenir.", "link": "Ouvrir les déclencheurs"},
            {"icon": "info", "title": f"{ins['chiffres']['heures_captees']:.1f} h observées sur 10 h demandées".replace(".", ","), "text": "Les tâches WONDERBREAD sont courtes : le seuil du cabinet n'est pas atteint.", "link": "Voir les limites"},
            {"icon": "plus", "title": "Relecture par les salariés", "text": "Les résumés ont été validés pour la démo : une vraie campagne passe par la relecture.", "link": "Lancer la relecture"},
        ],
        "nextImpact": {"dateRange": "Après le module n° 1", "text": "3 jours d'observation pour mesurer le gain réel de la première skill.", "note": "Hors de ces campagnes, aucune capture d'écran : seuls les journaux des skills."},
        "requests": [],
    },
}
open(os.path.join(ICI, "data.js"), "w").write(
    "// Généré par construire.py à partir des données Atelier Nova (WONDERBREAD, salariés fictifs) : ne pas éditer à la main.\n"
    "const DATA = " + json.dumps(DATA, ensure_ascii=False, indent=1) + ";\n")
print(f"{len(problemes)} problèmes · {len(masquees)} masqués · {bascules} allers-retours · pic {pic} · {len(edges)} liens · coût {euros(h_total * SEMAINES_AN * cout_h)} · gain {euros(gain_an)}")
