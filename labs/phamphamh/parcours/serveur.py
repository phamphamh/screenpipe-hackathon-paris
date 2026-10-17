"""Le parcours « cabinet de conseil IA automatisé » : une seule app, sept étapes en clic.

Lancer : python3 labs/phamphamh/parcours/serveur.py   → http://127.0.0.1:8790
Uniquement la bibliothèque standard. Écoute sur 127.0.0.1 seulement.

Branchements (tous facultatifs, le parcours marche sans eux et s'y branche dès qu'ils apparaissent) :
- méthodes d'audit : labs/phamphamh/recherche/methodes.json, sinon labs/phamphamh/rapport/methodes-defaut.json
- thèses de déploiement : labs/phamphamh/recherche/theses.json
- rapports : donnees/rapport/<id>.html
- moteur de workflows : labs/phamphamh/workflows/pack.py (pack, generer, tester, deployer)
Sans eux : données de secours intégrées, et les workflows sont simulés (marqués « simulation »).
"""
import glob, gzip, importlib.util, json, os, re, subprocess, sys, threading, traceback, unicodedata, urllib.request, webbrowser  # noqa: E401
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse

ICI = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(ICI)
RACINE = os.path.dirname(os.path.dirname(LAB))
ETAT = os.path.join(ICI, "etat")  # ignoré par git (voir .gitignore du dossier)
PORT = int(os.environ.get("PORT", 8790))
SEUIL = {"postes": 3, "heures": 10}
STATIQUES = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".svg": "image/svg+xml"}

sys.path.insert(0, ICI)
from secours import METHODES, THESES  # noqa: E402


# ---------- petits outils ----------

def lire(chemin):
    try:
        with open(chemin, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def ecrire(chemin, donnees):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    tmp = chemin + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=1)
    os.replace(tmp, chemin)


def slug(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:48] or "workflow"


def nombre(x, defaut=0.0):
    try:
        return float(x)
    except (TypeError, ValueError):
        return defaut


def rel(chemin):
    return os.path.relpath(chemin, RACINE)


def json_sur(x):
    """Rend n'importe quel retour du moteur sérialisable."""
    try:
        return json.loads(json.dumps(x, ensure_ascii=False, default=str))
    except (TypeError, ValueError):
        return str(x)


# ---------- les deux campagnes ----------
# « equipe » : notre équipe pour de vrai (exports + résumés validés de labs/*/campagne/).
# « demo »   : l'entreprise fictive Maison Corvo (labs/phamphamh/demo), comme dans app/serveur.py.

DEMO = os.path.join(LAB, "demo")


def campagne(x):
    return "demo" if x == "demo" else "equipe"


def resumes(camp):
    """[(qui, résumé)] ; le champ personne est remplacé par un nom lisible (le moteur s'en sert pour nommer les postes)."""
    out = []
    if camp == "demo":
        for f in sorted(glob.glob(os.path.join(DEMO, "resumes", "*.json"))):
            pid = os.path.basename(f)[:-5]
            r = lire(os.path.join(RACINE, "donnees", "demo", f"{pid}.json")) or lire(f)
            if isinstance(r, dict):
                out.append((pid, {**r, "personne": pid}))
    else:
        for f in sorted(glob.glob(os.path.join(RACINE, "labs", "*", "campagne", "resume-valide.json"))):
            r = lire(f)
            if isinstance(r, dict):
                qui = f.split(os.sep)[-3]
                out.append((qui, {**r, "personne": qui}))
    return out


# ---------- étape 1 : l'onboarding ----------

ONB_DEFAUT = {"entreprise": "Équipe hackathon screenpipe", "taille": 5, "activite": "Studio produit : on construit des outils IA pour les PME",
              "cout_horaire": 40, "priorites": ["Gagner du temps sur la saisie", "Mieux utiliser l'IA", "Protéger la concentration"],
              "irritants": "On jongle entre trop d'outils et on refait les mêmes manipulations chaque jour."}
CHAMPS_ONB = ("entreprise", "taille", "activite", "cout_horaire", "priorites", "irritants")


def onboarding(camp):
    o = lire(os.path.join(ETAT, f"onboarding-{camp}.json"))
    if o:
        return o
    if camp == "demo":
        o = lire(os.path.join(DEMO, "onboarding.json")) or {}
        m = re.search(r"(\d+)\s*salari", o.get("activite") or "")
        return {"taille": int(m.group(1)) if m else 48, **{k: v for k, v in o.items() if k in CHAMPS_ONB}}
    for f in [os.path.join(LAB, "campagne", "onboarding.json")] + sorted(glob.glob(os.path.join(RACINE, "labs", "*", "campagne", "onboarding.json"))):
        o = lire(f)
        if o:
            return {**ONB_DEFAUT, **{k: v for k, v in o.items() if k in CHAMPS_ONB}}
    return dict(ONB_DEFAUT)


# ---------- étape 2 : l'observation ----------

_cache_gz = {}


def heures_export_complet(chemin):
    """Heures captées = minutes distinctes avec une capture, divisées par 60. Mis en cache selon la date du fichier."""
    cle = (chemin, os.path.getmtime(chemin))
    if cle in _cache_gz:
        return _cache_gz[cle]
    minutes, debut, fin = set(), None, None
    try:
        with gzip.open(chemin, "rt", encoding="utf-8") as f:
            for ligne in f:
                try:
                    t = (json.loads(ligne).get("content") or {}).get("timestamp")
                except ValueError:
                    continue
                if t:
                    minutes.add(t[:16])
                    debut = t if debut is None or t < debut else debut
                    fin = t if fin is None or t > fin else fin
    except (OSError, EOFError):
        pass
    r = (round(len(minutes) / 60, 1), debut, fin)
    _cache_gz[cle] = r
    return r


def screenpipe_local():
    try:
        with urllib.request.urlopen("http://127.0.0.1:3030/health", timeout=0.6) as r:
            return r.status == 200
    except Exception:
        return False


def postes(camp="equipe"):
    """Équipe : même ordre que labs/phamphamh/audit/construire.py, pour que P01, P02… désignent les mêmes personnes."""
    out = []
    if camp == "demo":
        for qui, r in resumes("demo"):
            per = r.get("periode") or {}
            out.append({"qui": qui, "source": "Démo · résumé de la semaine", "lance": True, "export": True, "valide": r.get("valide_par_la_personne") is True,
                        "heures": round(nombre(r.get("heures_captees")), 1), "debut": per.get("debut"), "fin": per.get("fin"), "taches": len(r.get("taches") or [])})
    else:
        for chemin in sorted(glob.glob(os.path.join(RACINE, "donnees", "equipe", "screenpipe-*.jsonl.gz"))):
            qui = os.path.basename(chemin).split("-")[1]
            if any(p["qui"] == qui for p in out):
                continue
            h, d, f = heures_export_complet(chemin)
            out.append({"qui": qui, "source": "Export complet", "lance": True, "export": True, "valide": False, "heures": h, "debut": d, "fin": f})
        for chemin in sorted(glob.glob(os.path.join(RACINE, "equipe", "*.json"))):
            qui = os.path.splitext(os.path.basename(chemin))[0]
            d = lire(chemin) or {}
            if any(p["qui"] == qui for p in out) or not isinstance(d, dict) or "blocs" not in d:
                continue
            h = round(sum(nombre(v) for v in (d.get("temps_par_app_s") or {}).values()) / 3600, 1)
            per = d.get("periode") or {}
            out.append({"qui": qui, "source": "Export par blocs", "lance": True, "export": True, "valide": False, "heures": h, "debut": per.get("debut"), "fin": per.get("fin")})
        for qui, r in resumes("equipe"):
            if any(p["qui"] == qui for p in out):
                continue
            per = r.get("periode") or {}
            out.append({"qui": qui, "source": "Résumé validé", "lance": True, "export": True, "valide": r.get("valide_par_la_personne") is True,
                        "heures": round(nombre(r.get("heures_captees")), 1), "debut": per.get("debut"), "fin": per.get("fin"), "taches": len(r.get("taches") or [])})
    for i, p in enumerate(out):
        p["id"] = f"P{i + 1:02d}"
    return out


def etat(camp):
    ps = postes(camp)
    total = round(sum(p["heures"] for p in ps), 1)
    audit = lire(os.path.join(RACINE, "donnees", "audit", "audit.json"))
    return {
        "campagne": camp, "onboarding": onboarding(camp), "postes": ps, "total_heures": total, "seuil": SEUIL,
        "assez": len(ps) >= SEUIL["postes"] and total >= SEUIL["heures"],
        "screenpipe_local": screenpipe_local(),
        "audit": {"existe": bool(audit), "genere_le": (audit or {}).get("genere_le"), "taches": len((audit or {}).get("taches") or [])},
        "export": {"script": "equipe/exporter-mon-screenpipe.command", "existe": os.path.exists(os.path.join(RACINE, "equipe", "exporter-mon-screenpipe.command"))},
        "choix": lire(os.path.join(ETAT, "choix.json")) or {},
        "moteur": moteur_info(),
    }


# ---------- étapes 3 et 5 : méthodes et thèses ----------

def liste_specs(chemins, secours, cle):
    for chemin in chemins:
        d = lire(chemin)
        if isinstance(d, dict):
            d = d.get(cle) or d.get("items") or next((v for v in d.values() if isinstance(v, list)), None)
        if isinstance(d, list):
            d = [x for x in d if isinstance(x, dict) and x.get("id") and x.get("nom")]
            if d:
                return {"source": rel(chemin), "secours": False, cle: d}
    return {"source": "données de secours intégrées", "secours": True, cle: secours}


def methodes():
    return liste_specs([os.path.join(LAB, "recherche", "methodes.json"), os.path.join(LAB, "rapport", "methodes-defaut.json")], METHODES, "methodes")


def theses():
    return liste_specs([os.path.join(LAB, "recherche", "theses.json")], THESES, "theses")


def these_par_id(i):
    ts = theses()["theses"]
    return next((t for t in ts if t["id"] == i), ts[0] if ts else {"id": "defaut", "nom": "Par défaut", "autonomie": 2})


# ---------- étape 4 : le rapport ----------

def rapport(id_):
    propre = os.path.join(RACINE, "donnees", "rapport", f"{slug(id_)}.html")
    if os.path.exists(propre):
        return propre, "methode"
    for chemin in (os.path.join(LAB, "audit", "rapport.html"), os.path.join(RACINE, "donnees", "audit", "audit.html")):
        if os.path.exists(chemin):
            return chemin, "repli"
    return None, "absent"


# ---------- étape 6 : le moteur de workflows ----------

_moteur = {"mtime": None, "mod": None, "erreur": None}
_verrou = threading.Lock()


def moteur():
    """Importe workflows/pack.py s'il existe ; le recharge s'il change. Ne lève jamais."""
    chemin = os.path.join(LAB, "workflows", "pack.py")
    with _verrou:
        if not os.path.exists(chemin):
            _moteur.update(mtime=None, mod=None, erreur="pas encore écrit")
            return None
        m = os.path.getmtime(chemin)
        if _moteur["mtime"] == m:
            return _moteur["mod"]
        try:
            dossier = os.path.dirname(chemin)
            if dossier not in sys.path:
                sys.path.insert(0, dossier)
            spec = importlib.util.spec_from_file_location("parcours_pack", chemin)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            _moteur.update(mtime=m, mod=mod, erreur=None)
        except Exception as e:  # le fichier peut être en cours d'écriture
            _moteur.update(mtime=m, mod=None, erreur=f"{type(e).__name__}: {e}")
        return _moteur["mod"]


def moteur_info():
    mod = moteur()
    fonctions = [f for f in ("pack", "generer", "tester", "deployer") if mod and callable(getattr(mod, f, None))]
    return {"branche": bool(mod), "fonctions": fonctions, "raison": _moteur["erreur"], "fichier": "labs/phamphamh/workflows/pack.py"}


def taches_de(camp):
    """Les tâches des résumés validés, à plat, avec la personne (même règle que le moteur : un résumé non validé ne compte pas)."""
    out = []
    for qui, r in resumes(camp):
        if r.get("valide_par_la_personne") is not True:
            continue
        for t in r.get("taches") or []:
            if isinstance(t, dict) and t.get("titre"):
                out.append({**t, "_personne": qui, "poste": qui})
    return out


FACTEUR_AUTONOMIE = {1: .5, 2: .75, 3: .9, 4: 1.0}


def evaluer(t, these):
    """Chiffrage de secours (sans moteur) : heures par semaine, gain possible, niveau d'autonomie."""
    heures = nombre(t.get("frequence_par_semaine")) * nombre(t.get("duree_moyenne_min")) / 60
    types = [e.get("type") for e in t.get("etapes") or []]
    goulots = [g.get("type") if isinstance(g, dict) else g for g in t.get("goulots") or []]
    score = nombre((t.get("automatisable") or {}).get("score"), -1)
    if score >= 0:
        base = score / 100 * .85
    elif "unclear" in goulots:
        base = .15
    elif "decision" not in types and any(g in ("switching", "waiting") for g in goulots):
        base = .7
    else:
        base = .4
    aut = int(max(1, min(4, int(nombre(these.get("autonomie"), 2)))))
    return {"heures_semaine": round(heures, 1), "gain": round(base * FACTEUR_AUTONOMIE.get(aut, .75), 2), "autonomie": aut}


def personne_de(t):
    return t.get("_personne") or t.get("personne") or t.get("poste")


def groupes(camp, mod=None):
    """[(référence, autres)] : la même tâche chez plusieurs personnes forme un groupe (regroupement du moteur s'il est là)."""
    taches = taches_de(camp)
    if mod and callable(getattr(mod, "grouper", None)):
        try:
            gs = mod.grouper(taches)
        except Exception:
            gs = [[t] for t in taches]
    else:
        gs = [[t] for t in taches]
    out = []
    for membres in gs:
        ref = max(membres, key=lambda m: (m.get("confiance") or 0, len([e for e in m.get("etapes") or [] if isinstance(e, dict) and e.get("texte")])))
        out.append((ref, [m for m in membres if m is not ref]))
    return out


def vue_tache(t):
    """Ce que l'interface affiche d'une tâche (et renvoie au serveur pour Générer)."""
    return {"titre": t.get("titre"), "poste": personne_de(t), "etapes": [{"type": e.get("type"), "texte": e.get("texte"), "app": e.get("app"), "statut": e.get("statut")}
                                                                      for e in t.get("etapes") or [] if isinstance(e, dict)]}


def pack(these_id, camp):
    these = these_par_id(these_id)
    mod = moteur()
    gs = groupes(camp, mod)
    par_titre = {ref.get("titre"): (ref, autres) for ref, autres in gs}
    if mod and callable(getattr(mod, "pack", None)):
        try:
            lignes = mod.pack([r for _, r in resumes(camp)], these)
            cartes = []
            for x in lignes:
                ref, autres = par_titre.get(x.get("titre"), ({"titre": x.get("titre")}, []))
                h = nombre(x.get("heures_semaine"))
                cartes.append({"id": x.get("id") or slug(x.get("titre")), "titre": x.get("titre"), "poste": personne_de(ref),
                               "heures_semaine": round(h, 1), "gain": round(nombre(x.get("gain_estime_h")) / h, 2) if h else 0,
                               "gain_h": nombre(x.get("gain_estime_h")), "autonomie": int(nombre(x.get("autonomie"), 2)),
                               "personnes": x.get("personnes") or 1 + len(autres), "libelles": x.get("libelles") or [],
                               "tache": vue_tache(ref)})
            return {"these": these, "simulation": False, "workflows": cartes, "note": None}
        except Exception as e:
            traceback.print_exc()
            note = f"Le moteur a échoué ({type(e).__name__} : {str(e)[:120]}). Chiffrage de secours."
    else:
        note = None
    cartes = []
    for ref, autres in gs:
        ev = evaluer(ref, these)
        if ev["heures_semaine"] > 0:
            cartes.append({"id": slug(f"{personne_de(ref)}-{ref.get('titre')}"), "titre": ref.get("titre"), "poste": personne_de(ref), **ev,
                           "gain_h": round(ev["heures_semaine"] * ev["gain"], 2), "personnes": 1 + len(autres), "tache": vue_tache(ref)})
    cartes.sort(key=lambda c: -c["gain_h"])
    return {"these": these, "simulation": True, "workflows": cartes[:10], "note": note}


# ---------- Générer, Tester, Déployer ----------

def remesure(jours=7):
    return (datetime.now() + timedelta(days=jours)).strftime("%Y-%m-%d")


def dossier_sur(d):
    """N'accepte qu'un dossier de skill sous donnees/workflows/ (chemin relatif à la racine ou absolu)."""
    if not d:
        raise ValueError("aucun dossier de skill : lance d'abord Générer")
    absolu = os.path.realpath(d if os.path.isabs(d) else os.path.join(RACINE, d))
    base = os.path.realpath(os.path.join(RACINE, "donnees", "workflows")) + os.sep
    if not absolu.startswith(base):
        raise ValueError("dossier de skill refusé (hors de donnees/workflows)")
    return absolu


def reel_generer(mod, ref, autres, these):
    dossier = mod.generer(ref, these)
    l = [f"Tâche « {ref.get('titre')} » · {len(ref.get('etapes') or [])} étapes observées chez {personne_de(ref)}"
         + (f", et {len(autres)} autre{'s' if len(autres) > 1 else ''} personne{'s' if len(autres) > 1 else ''} qui la font aussi" if autres else ""),
         f"Approche « {these.get('nom')} » · autonomie {these.get('autonomie')} sur 4"]
    md = ""
    try:
        with open(os.path.join(dossier, "SKILL.md"), encoding="utf-8") as f:
            md = f.read()
    except OSError:
        pass
    dans, n = False, 0
    for ligne in md.splitlines():
        if ligne.startswith("## "):
            dans = ligne.strip() == "## Étapes"
            continue
        if dans and re.match(r"^\d+\. ", ligne) and n < 12:
            l.append("Instruction " + ligne.strip()[:220])
            n += 1
    meta = lire(os.path.join(dossier, "workflow.json")) or {}
    tests = lire(os.path.join(dossier, "tests.json")) or {}
    for p in meta.get("points_humains") or []:
        l.append(f"Point de validation humaine : {p}")
    l += [f"✓ SKILL.md écrit ({len(md.splitlines())} lignes)", f"✓ tests.json : {len(tests.get('cas') or [])} cas de référence",
          f"✓ Dossier : {rel(dossier)}"]
    return {"lignes": l, "dossier": rel(dossier), "verdict": "pret", "fichiers": sorted(os.listdir(dossier))}


def reel_tester(mod, dossier, autres):
    entrees = [{"nom": f"2e entrée : {personne_de(m)} — {m.get('titre')}", "etapes": m.get("etapes"), "apps": m.get("apps"),
                "exceptions": m.get("exceptions"), "preuves": m.get("preuves")} for m in autres]
    r = mod.tester(dossier, entrees)
    l = [f"Rejeu à sec de {r.get('cas', 0)} cas" + (f", dont {len(entrees)} chez une autre personne" if entrees else ", sans 2e personne")]
    l.append(f"{'✓' if r.get('passes') == r.get('cas') else '!'} Cas réussis : {r.get('passes', 0)} sur {r.get('cas', 0)}")
    for e in r.get("echecs") or []:
        l.append(f"! {e.get('raison')}" + (f" · {e.get('cas')}" if e.get("cas") not in (None, "-") else ""))
    for a in (r.get("avertissements") or [])[:4]:
        l.append(f"Remarque : {a.get('raison')}")
    cov = nombre(r.get("couverture_etapes"))
    l.append(f"Couverture des étapes observées : {round(cov * 100)} %")
    l.append(f"{'✓ Prêt à déployer' if r.get('verdict') == 'pret' else '! À revoir : ' + str(r.get('message') or '')}")
    return {"lignes": l, "verdict": "pret" if r.get("verdict") == "pret" else "a_revoir", "taux": cov,
            "raisons": [e.get("raison") for e in r.get("echecs") or []], "dossier": rel(dossier), "rapport": json_sur(r)}


def reel_deployer(mod, dossier, cible, forcer, ref):
    r = mod.deployer(dossier, cible, forcer=forcer, poste=personne_de(ref) if cible == "local-demo" else None)
    if not r.get("deploye"):
        return {"lignes": [f"! Déploiement refusé : {r.get('raison')}"], "verdict": "a_revoir", "refuse": True, "raisons": [r.get("raison")], "dossier": rel(dossier)}
    t = r.get("tests") or {}
    l = [f"✓ Copié vers {r.get('chemin')}",
         f"Cible : {'un poste, en démonstration (' + str(r.get('poste')) + ')' if cible == 'local-demo' else 'toute l’équipe, partagé par le dépôt'}",
         f"Autonomie {r.get('autonomie')} sur 4 · humain : {r.get('humain') or '—'}",
         f"Tests au moment du déploiement : {t.get('verdict')}, {t.get('passes')} sur {t.get('cas')} cas"]
    if r.get("force"):
        l.append("! Déployé en forçant malgré des tests à revoir")
    for s in (r.get("suivi_apres") or [])[:2]:
        l.append(f"Suivi : {s}")
    l.append(f"✓ Reçu écrit · remesure programmée le {remesure()}")
    return {"lignes": l, "verdict": "pret", "dossier": rel(dossier), "recu": json_sur(r), "poste_deploye": r.get("poste")}


def sim_generer(t, these):
    etapes = t.get("etapes") or []
    l = [f"Tâche « {t.get('titre')} » · {len(etapes)} étapes observées"]
    for k, e in enumerate(etapes, 1):
        l.append(f"Instruction {k}. {e.get('texte')}" + (f" ({e.get('app')})" if e.get("app") else ""))
    l.append(f"Humain : {these.get('humain') or 'validation humaine'}")
    l.append(f"✓ SKILL.md écrit (simulation, rien n'est créé sur le disque)")
    return {"lignes": l, "dossier": f"skills/{slug(t.get('titre'))}", "verdict": "pret"}


def sim_tester(t, these):
    etapes = t.get("etapes") or []
    l, couvertes = [f"Rejeu de {len(etapes)} étapes (simulation)"], []
    for k, e in enumerate(etapes, 1):
        ok = e.get("statut") != "supposé"
        couvertes.append(ok)
        l.append(f"{'✓' if ok else '!'} Étape {k} : {e.get('texte')}" + ("" if ok else " (supposée, à confirmer)"))
    couv = sum(couvertes) / len(couvertes) if couvertes else 0
    l.append(f"Couverture des étapes : {round(couv * 100)} %")
    return {"lignes": l, "taux": couv, "verdict": "pret" if couv >= .6 else "a_revoir",
            "raisons": [f"étape supposée, à confirmer : « {e.get('texte')} »" for e in etapes if e.get("statut") == "supposé"]}


def sim_deployer(t, cible):
    return {"lignes": [f"Cible : {'un poste, en démonstration' if cible == 'local-demo' else 'toute l’équipe'} (simulation)",
                       f"✓ Remesure programmée le {remesure()}"], "verdict": "pret"}


def workflow(action, corps):
    camp = campagne(corps.get("campagne"))
    t = corps.get("tache") or {}
    these = these_par_id(corps.get("these"))
    cible = "equipe" if corps.get("cible") == "equipe" else "local-demo"
    mod = moteur()
    fn = getattr(mod, action, None) if mod else None
    if callable(fn):
        ref, autres = next(((r, a) for r, a in groupes(camp, mod) if r.get("titre") == t.get("titre")), (None, []))
        if ref is None:
            return {"lignes": [f"! Tâche introuvable dans les résumés de cette campagne : « {t.get('titre')} »"], "verdict": "a_revoir", "simulation": False}
        try:
            if action == "generer":
                res = reel_generer(mod, ref, autres, these)
            elif action == "tester":
                res = reel_tester(mod, dossier_sur(corps.get("dossier")), autres)
            else:
                res = reel_deployer(mod, dossier_sur(corps.get("dossier")), cible, bool(corps.get("forcer")), ref)
            res["simulation"] = False
        except ValueError as e:
            return {"lignes": [f"! {e}"], "verdict": "a_revoir", "simulation": False, "raisons": [str(e)]}
        except Exception as e:
            traceback.print_exc()
            return {"lignes": [f"! Le moteur a échoué : {type(e).__name__} : {str(e)[:200]}"], "verdict": "a_revoir", "simulation": False}
    else:
        res = sim_generer(t, these) if action == "generer" else sim_tester(t, these) if action == "tester" else sim_deployer(t, cible)
        res["simulation"] = True
        res["note"] = "Moteur de workflows absent : résultat simulé, rien n'est installé." if mod is None else f"Le moteur n'a pas de fonction « {action} » : résultat simulé."
    if action == "deployer" and not res.get("refuse"):
        f = os.path.join(ETAT, "deploiements.json")
        deps = [d for d in (lire(f) or []) if not (d.get("id") == corps.get("id") and d.get("campagne") == camp)]
        ps = {p["qui"]: p["id"] for p in postes(camp)}
        cibles = [ps.get(res.get("poste_deploye") or t.get("poste"), res.get("poste_deploye") or t.get("poste"))] if cible == "local-demo" else list(ps.values())
        deps.append({"id": corps.get("id") or slug(t.get("titre")), "campagne": camp, "titre": t.get("titre"), "poste": t.get("poste"), "these": these.get("nom"),
                     "cible": cible, "postes": cibles, "dossier": res.get("dossier"),
                     "heures_avant": nombre(corps.get("heures_semaine")), "gain": nombre(corps.get("gain")), "autonomie": corps.get("autonomie"),
                     "deploye_le": datetime.now().isoformat(timespec="minutes"), "remesure_le": remesure(), "simulation": res["simulation"],
                     "force": bool(corps.get("forcer"))})
        ecrire(f, deps)
    return res


# ---------- le serveur ----------

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def envoyer(self, code, corps, type_="application/json; charset=utf-8"):
        b = corps if isinstance(corps, bytes) else json.dumps(corps, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", type_)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def fichier(self, chemin):
        with open(chemin, "rb") as f:
            return self.envoyer(200, f.read(), STATIQUES.get(os.path.splitext(chemin)[1], "application/octet-stream"))

    def corps(self):
        n = int(self.headers.get("Content-Length") or 0)
        try:
            return json.loads(self.rfile.read(n) or b"{}") if 0 < n < 2_000_000 else {}
        except ValueError:
            return {}

    def do_GET(self):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        p = u.path
        try:
            if p in ("/", "/index.html"):
                return self.fichier(os.path.join(ICI, "index.html"))
            camp = campagne(q.get("campagne"))
            if p == "/api/etat":
                return self.envoyer(200, etat(camp))
            if p == "/api/methodes":
                return self.envoyer(200, methodes())
            if p == "/api/theses":
                return self.envoyer(200, theses())
            if p == "/api/pack":
                return self.envoyer(200, pack(q.get("these", ""), camp))
            if p == "/api/suivi":
                return self.envoyer(200, {"deploiements": [d for d in lire(os.path.join(ETAT, "deploiements.json")) or [] if d.get("campagne", "equipe") == camp], "postes": postes(camp)})
            if p.startswith("/api/rapport/"):
                chemin, source = rapport(unquote(p[len("/api/rapport/"):]))
                return self.envoyer(200, {"source": source, "fichier": rel(chemin) if chemin else None})
            if p.startswith("/rapport/"):
                chemin, _ = rapport(unquote(p[len("/rapport/"):]))
                if chemin:
                    return self.fichier(chemin)
                return self.envoyer(404, b"<p style='font-family:sans-serif'>Aucun rapport pour l'instant.</p>", "text/html; charset=utf-8")
            nom = os.path.basename(p)
            if os.path.splitext(nom)[1] in STATIQUES and os.path.exists(os.path.join(ICI, nom)):
                return self.fichier(os.path.join(ICI, nom))
            self.envoyer(404, {"erreur": "introuvable"})
        except Exception as e:
            traceback.print_exc()
            self.envoyer(500, {"erreur": str(e)})

    def do_POST(self):
        p = urlparse(self.path).path
        try:
            if p == "/api/onboarding":
                c = self.corps()
                ecrire(os.path.join(ETAT, f"onboarding-{campagne(c.get('campagne'))}.json"), {k: v for k, v in c.items() if k in CHAMPS_ONB})
                return self.envoyer(200, {"ok": True})
            if p == "/api/choix":
                f = os.path.join(ETAT, "choix.json")
                ecrire(f, {**(lire(f) or {}), **{k: v for k, v in self.corps().items() if k in ("methode", "these", "etape", "campagne")}})
                return self.envoyer(200, {"ok": True})
            m = re.fullmatch(r"/api/workflow/(generer|tester|deployer)", p)
            if m:
                return self.envoyer(200, workflow(m.group(1), self.corps()))
            if p == "/api/exporter":
                script = os.path.join(RACINE, "equipe", "exporter-mon-screenpipe.command")
                if sys.platform == "darwin" and os.path.exists(script):
                    subprocess.Popen(["open", "-a", "Terminal", script])
                    return self.envoyer(200, {"ok": True})
                return self.envoyer(200, {"ok": False, "raison": "Ouvre equipe/exporter-mon-screenpipe.command à la main."})
            if p == "/api/reinitialiser":
                for f in ("deploiements.json", "choix.json"):
                    try:
                        os.remove(os.path.join(ETAT, f))
                    except OSError:
                        pass
                return self.envoyer(200, {"ok": True})
            self.envoyer(404, {"erreur": "introuvable"})
        except Exception as e:
            traceback.print_exc()
            self.envoyer(500, {"erreur": str(e)})


def main():
    s = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)  # local uniquement
    url = f"http://127.0.0.1:{PORT}"
    print(f"Parcours prêt : {url}  (Ctrl+C ou fermer la fenêtre pour arrêter)")
    if "--sans-navigateur" not in sys.argv:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        s.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
