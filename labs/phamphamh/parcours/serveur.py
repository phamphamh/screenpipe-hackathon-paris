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
import glob, gzip, importlib.util, json, os, re, subprocess, sys, threading, traceback, unicodedata, urllib.request, webbrowser
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


# ---------- étape 1 : l'onboarding ----------

ONB_DEFAUT = {"entreprise": "Équipe hackathon screenpipe", "taille": 5, "activite": "Studio produit : on construit des outils IA pour les PME",
              "cout_horaire": 40, "priorites": ["Gagner du temps sur la saisie", "Mieux utiliser l'IA", "Protéger la concentration"],
              "irritants": "On jongle entre trop d'outils et on refait les mêmes manipulations chaque jour."}
CHAMPS_ONB = ("entreprise", "taille", "activite", "cout_horaire", "priorites", "irritants")


def onboarding():
    o = lire(os.path.join(ETAT, "onboarding.json"))
    if o:
        return {**ONB_DEFAUT, **o}
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
            return json.loads(r.read() or b"{}").get("status") in ("healthy", "degraded", "ok") or r.status == 200
    except Exception:
        return False


def postes():
    """Même ordre que labs/phamphamh/audit/construire.py, pour que P01, P02… désignent les mêmes personnes."""
    out = []
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
    for chemin in sorted(glob.glob(os.path.join(RACINE, "labs", "*", "campagne", "resume-valide.json"))):
        qui = chemin.split(os.sep)[-3]
        r = lire(chemin) or {}
        if any(p["qui"] == qui for p in out):
            continue
        per = r.get("periode") or {}
        out.append({"qui": qui, "source": "Résumé validé", "lance": True, "export": True, "valide": r.get("valide_par_la_personne") is True,
                    "heures": round(nombre(r.get("heures_captees")), 1), "debut": per.get("debut"), "fin": per.get("fin"), "taches": len(r.get("taches") or [])})
    for i, p in enumerate(out):
        p["id"] = f"P{i + 1:02d}"
    return out


def etat():
    ps = postes()
    total = round(sum(p["heures"] for p in ps), 1)
    audit = lire(os.path.join(RACINE, "donnees", "audit", "audit.json"))
    return {
        "onboarding": onboarding(), "postes": ps, "total_heures": total, "seuil": SEUIL,
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


def taches_audit():
    """Les tâches des résumés validés (lus en direct), au format de donnees/audit/audit.json."""
    taches = []
    for chemin in sorted(glob.glob(os.path.join(RACINE, "labs", "*", "campagne", "resume-valide.json"))):
        r = lire(chemin) or {}
        qui = chemin.split(os.sep)[-3]
        for t in r.get("taches") or []:
            if not t.get("titre"):
                continue
            taches.append({"poste": qui, "titre": t["titre"], "frequence_par_semaine": t.get("frequence_par_semaine"),
                           "duree_moyenne_min": t.get("duree_moyenne_min"), "apps": t.get("apps") or [],
                           "etapes": [{"type": e.get("type"), "texte": e.get("texte"), "app": e.get("app"), "statut": e.get("statut")} for e in t.get("etapes") or []],
                           "goulots": [g.get("type") if isinstance(g, dict) else g for g in t.get("goulots") or []],
                           "confiance": t.get("confiance"), "automatisable": t.get("automatisable") or {}})
    if not taches:
        taches = (lire(os.path.join(RACINE, "donnees", "audit", "audit.json")) or {}).get("taches") or []
    return taches


FACTEUR_AUTONOMIE = {1: .5, 2: .75, 3: .9, 4: 1.0}


def evaluer(t, these):
    """Le chiffrage de secours : heures par semaine, gain possible, niveau d'autonomie."""
    heures = nombre(t.get("frequence_par_semaine")) * nombre(t.get("duree_moyenne_min")) / 60
    apps = " ".join(t.get("apps") or []).lower()
    types = [e.get("type") for e in t.get("etapes") or []]
    goulots = t.get("goulots") or []
    score = nombre((t.get("automatisable") or {}).get("score"), -1)
    if score >= 0:
        base = score / 100 * .85
    elif "unclear" in goulots:
        base = .15
    elif "decision" not in types and any(g in ("switching", "waiting") for g in goulots):
        base = .7
    else:
        base = .4
    if re.search(r"orca|claude|chatgpt|codex", apps):
        etat_ia = "Déjà avec l'IA"
    elif base >= .5:
        etat_ia = "L'IA peut le faire"
    elif base >= .25:
        etat_ia = "L'IA aide"
    else:
        etat_ia = "À observer"
    niveau = 4 if base >= .6 and "decision" not in types else 3 if "decision" not in types else 2
    aut = int(max(1, min(niveau, int(nombre(these.get("autonomie"), 2)))))
    gain = round(base * FACTEUR_AUTONOMIE.get(aut, .75), 2)
    return {"heures_semaine": round(heures, 1), "gain": gain, "autonomie": aut, "etat_ia": etat_ia}


def tache_id(t):
    return slug(f"{t.get('poste', '')}-{t.get('titre', '')}")


def pack_secours(taches, these):
    out = []
    for t in taches:
        out.append({"id": tache_id(t), "titre": t.get("titre"), "poste": t.get("poste"), **evaluer(t, these), "tache": t})
    out = [x for x in out if x["heures_semaine"] > 0]
    out.sort(key=lambda x: -x["heures_semaine"] * max(x["gain"], .05))
    return out[:8]


def premier(d, *cles, defaut=None):
    for k in cles:
        if isinstance(d, dict) and d.get(k) not in (None, ""):
            return d[k]
    return defaut


def pack(these_id):
    these = these_par_id(these_id)
    taches = taches_audit()
    secours = pack_secours(taches, these)
    mod, note = moteur(), None
    if mod and callable(getattr(mod, "pack", None)):
        try:
            res = mod.pack(taches, these)
            if isinstance(res, dict):
                res = premier(res, "workflows", "taches", "pack", "cartes", defaut=[])
            cartes = []
            for x in res or []:
                if not isinstance(x, dict):
                    continue
                src = x.get("tache") if isinstance(x.get("tache"), dict) else x
                titre = premier(x, "titre", "nom", "title", defaut=src.get("titre"))
                base = next((s for s in secours if s["titre"] == titre), None) or {"id": tache_id(src), **evaluer(src, these)}
                gain = nombre(premier(x, "gain", "gain_estime", "gain_pct"), base["gain"])
                cartes.append({"id": premier(x, "id", defaut=base["id"]), "titre": titre, "poste": premier(x, "poste", defaut=src.get("poste")),
                               "heures_semaine": round(nombre(premier(x, "heures_semaine", "heures", "heures_par_semaine"), base["heures_semaine"]), 1),
                               "gain": gain / 100 if gain > 1 else gain,
                               "autonomie": int(nombre(premier(x, "autonomie", "niveau_autonomie"), base["autonomie"])),
                               "etat_ia": premier(x, "etat_ia", "statut", defaut=base.get("etat_ia")), "tache": json_sur(x)})
            if cartes:
                return {"these": these, "simulation": False, "workflows": cartes, "note": None}
            note = "Le moteur n'a renvoyé aucune tâche : chiffrage de secours."
        except Exception as e:
            note = f"Le moteur a échoué ({type(e).__name__}) : chiffrage de secours."
            traceback.print_exc()
    return {"these": these, "simulation": True, "workflows": secours, "note": note}


# ---------- Générer, Tester, Déployer ----------

def remesure(jours=7):
    return (datetime.now() + timedelta(days=jours)).strftime("%Y-%m-%d")


def sim_generer(t, these):
    etapes = t.get("etapes") or []
    l = [f"Lecture de la tâche « {t.get('titre')} » ({len(etapes)} étapes observées)"]
    for k, e in enumerate(etapes, 1):
        l.append(f"Étape {k} · {e.get('type') or 'action'} · {e.get('texte')}" + (f" [{e.get('app')}]" if e.get("app") else ""))
    l.append(f"Règle de la thèse « {these.get('nom')} » : {these.get('humain') or 'validation humaine'}")
    for g in (these.get("garde_fous") or [])[:2]:
        l.append(f"Garde-fou ajouté : {g}")
    dossier = f"skills/{slug(t.get('titre'))}"
    l.append(f"Skill écrite : {dossier}/SKILL.md ({18 + 4 * len(etapes)} lignes)")
    return {"lignes": l, "dossier": dossier, "verdict": "pret"}


def sim_tester(t, these, dossier):
    etapes = t.get("etapes") or []
    l, couvertes = [f"Chargement de {dossier}", f"Rejeu sur {max(3, len(etapes))} cas observés"], []
    for k, e in enumerate(etapes, 1):
        ok = e.get("statut") != "supposé"
        couvertes.append(ok)
        l.append(f"{'✓' if ok else '!'} Étape {k} : {e.get('texte')}" + ("" if ok else " (supposée, à confirmer avec la personne)"))
    for x in (these.get("tests_avant") or [])[:2]:
        l.append(f"✓ Contrôle de la thèse : {x}")
    couv = sum(couvertes) / len(couvertes) if couvertes else 0
    conf = nombre(t.get("confiance"), .6)
    verdict = "pret" if couv >= .6 and conf >= .6 else "a_revoir"
    l.append(f"Couverture des étapes : {round(couv * 100)} % · confiance du résumé : {round(conf * 100)} %")
    return {"lignes": l, "couverture": [1 if c else 0 for c in couvertes], "verdict": verdict}


def sim_deployer(t, these, dossier, cible, ps):
    postes_cible = [p["id"] for p in ps if p["qui"] == t.get("poste")] if cible == "local-demo" else [p["id"] for p in ps]
    l = [f"Paquet {dossier} vérifié",
         f"Cible : {'ce Mac, en démonstration' if cible == 'local-demo' else 'toute l’équipe'} ({', '.join(postes_cible) or 'ce poste'})",
         "Branchement dans Claude Code et Orca : consignes copiées",
         f"Point de contrôle humain : {these.get('humain') or 'validation avant envoi'}",
         f"Remesure programmée le {remesure()}"]
    return {"lignes": l, "verdict": "pret", "postes": postes_cible}


def normaliser(res, defaut):
    """Accepte ce que renvoie le moteur (chemin, dict, liste…) et en tire des lignes lisibles et un verdict."""
    out = dict(defaut)
    if isinstance(res, (str, os.PathLike)):
        out["dossier"] = str(res)
        out["lignes"] = [f"Résultat : {res}"]
        return out
    if isinstance(res, (list, tuple)):
        out["lignes"] = [str(x) for x in res][:60]
        return out
    if not isinstance(res, dict):
        out["lignes"] = [str(res)]
        return out
    lignes = premier(res, "lignes", "journal", "log", "logs", "etapes_log")
    if isinstance(lignes, str):
        lignes = lignes.splitlines()
    if not lignes:
        lignes = [f"{k} : {v if not isinstance(v, (dict, list)) else json.dumps(v, ensure_ascii=False)[:160]}" for k, v in res.items()][:20]
    out["lignes"] = [str(x) for x in lignes][:80]
    d = premier(res, "dossier", "dossier_skill", "chemin", "path", "skill")
    if d:
        out["dossier"] = str(d)
    v = premier(res, "verdict", "statut")
    if v is not None:
        out["verdict"] = "pret" if str(v).lower().replace("ê", "e") in ("pret", "ok", "ready", "succes", "true", "vert") else "a_revoir"
    elif "ok" in res or "pret" in res:
        out["verdict"] = "pret" if (res.get("ok") or res.get("pret")) else "a_revoir"
    c = premier(res, "couverture", "coverage")
    if isinstance(c, list):
        out["couverture"] = [1 if x else 0 for x in c]
    elif c is not None:
        n = len(out.get("couverture") or []) or 5
        f = nombre(c)
        f = f / 100 if f > 1 else f
        out["couverture"] = [1 if k < round(f * n) else 0 for k in range(n)]
    if res.get("postes"):
        out["postes"] = res["postes"]
    out["brut"] = json_sur(res)
    return out


def workflow(action, corps):
    t = corps.get("tache") or {}
    these = these_par_id(corps.get("these"))
    dossier = corps.get("dossier") or f"skills/{slug(t.get('titre'))}"
    cible = "equipe" if corps.get("cible") == "equipe" else "local-demo"
    ps = postes()
    if action == "generer":
        sim = sim_generer(t, these)
    elif action == "tester":
        sim = sim_tester(t, these, dossier)
    else:
        sim = sim_deployer(t, these, dossier, cible, ps)
    mod, res = moteur(), None
    fn = getattr(mod, action, None) if mod else None
    if callable(fn):
        try:
            if action == "generer":
                r = fn(t, these)
            elif action == "tester":
                r = fn(dossier, t.get("entrees") or t.get("exemples") or [{"etape": e.get("texte"), "type": e.get("type")} for e in t.get("etapes") or []])
            else:
                r = fn(dossier, cible)
            res = normaliser(r, {**sim, "lignes": []})
            res["simulation"] = False
            if not res["lignes"]:
                res["lignes"] = sim["lignes"]
        except Exception as e:
            traceback.print_exc()
            res = {**sim, "simulation": True, "note": f"Le moteur a échoué ({type(e).__name__} : {str(e)[:140]}). Résultat simulé."}
    if res is None:
        res = {**sim, "simulation": True, "note": None if mod is None else f"Le moteur n'a pas encore de fonction « {action} ». Résultat simulé."}
    if action == "deployer":
        f = os.path.join(ETAT, "deploiements.json")
        deps = [d for d in (lire(f) or []) if d.get("id") != corps.get("id")]
        ev = evaluer(t, these)
        deps.append({"id": corps.get("id") or slug(t.get("titre")), "titre": t.get("titre"), "poste": t.get("poste"), "these": these.get("nom"),
                     "cible": cible, "postes": res.get("postes") or sim.get("postes"), "dossier": res.get("dossier", dossier),
                     "heures_avant": nombre(corps.get("heures_semaine"), ev["heures_semaine"]), "gain": nombre(corps.get("gain"), ev["gain"]),
                     "autonomie": corps.get("autonomie") or ev["autonomie"],
                     "deploye_le": datetime.now().isoformat(timespec="minutes"), "remesure_le": remesure(), "simulation": res["simulation"]})
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
            if p == "/api/etat":
                return self.envoyer(200, etat())
            if p == "/api/methodes":
                return self.envoyer(200, methodes())
            if p == "/api/theses":
                return self.envoyer(200, theses())
            if p == "/api/pack":
                return self.envoyer(200, pack(q.get("these", "")))
            if p == "/api/suivi":
                return self.envoyer(200, {"deploiements": lire(os.path.join(ETAT, "deploiements.json")) or [], "postes": postes()})
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
                ecrire(os.path.join(ETAT, "onboarding.json"), {k: v for k, v in c.items() if k in CHAMPS_ONB})
                return self.envoyer(200, {"ok": True})
            if p == "/api/choix":
                f = os.path.join(ETAT, "choix.json")
                ecrire(f, {**(lire(f) or {}), **{k: v for k, v in self.corps().items() if k in ("methode", "these", "etape")}})
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
