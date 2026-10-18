"""Le produit Wrapped en local : onboarding du dirigeant, relecture par le salarié (brique C) et le Wrapped (brique E).

Lancer : python3 labs/phamphamh/app/serveur.py   → ouvre http://localhost:8787
Deux campagnes :
- « demo »   : l'entreprise fictive Maison Corvo (labs/phamphamh/demo). Les relectures faites pendant la démo vont dans donnees/demo/ (jamais commité).
- « equipe » : notre équipe pour de vrai. Chacun relit SON résumé (donnees/<pseudo>/resume.json, produit par les briques A et B) ;
               « Valider et partager » écrit labs/<pseudo>/campagne/resume-valide.json, que la sauvegarde automatique partage avec l'équipe.
Uniquement la bibliothèque standard de Python.
"""
import glob, hashlib, json, os, subprocess, sys, threading, webbrowser
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

ICI = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(ICI)
RACINE = os.path.dirname(os.path.dirname(LAB))
sys.path.insert(0, os.path.join(LAB, "fusion"))
from fusion import fusionner, texte_limite, vers_front_adamaass  # noqa: E402

PORT = int(os.environ.get("PORT", 8787))
DEMO = os.path.join(LAB, "demo")
DEMO_RELUS = os.path.join(RACINE, "donnees", "demo")
PAGES = {"/": "accueil.html", "/relecture": "relecture.html", "/wrapped": "wrapped.html", "/onboarding": "onboarding.html", "/commun.css": "commun.css"}


def pseudo():
    try:
        return subprocess.run(["sh", os.path.join(RACINE, "scripts", "pseudo.sh")], capture_output=True, text=True, cwd=RACINE).stdout.strip() or "moi"
    except OSError:
        return "moi"


def lire(chemin):
    try:
        return json.load(open(chemin))
    except (OSError, ValueError):
        return None


def ecrire(chemin, donnees):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    tmp = chemin + ".tmp"
    json.dump(donnees, open(tmp, "w"), ensure_ascii=False, indent=1)
    os.replace(tmp, chemin)


# ---------- les campagnes ----------

def participants(campagne):
    """[(identifiant, résumé, source)] : pour la démo, la version relue pendant la démo remplace l'originale."""
    out = []
    if campagne == "demo":
        for f in sorted(glob.glob(os.path.join(DEMO, "resumes", "*.json"))):
            pid = os.path.basename(f)[:-5]
            relu = os.path.join(DEMO_RELUS, f"{pid}.json")
            out.append((pid, lire(relu) or lire(f), "relu pendant la démo" if os.path.exists(relu) else "démo"))
    else:
        for f in sorted(glob.glob(os.path.join(RACINE, "labs", "*", "campagne", "resume-valide.json"))):
            out.append((f.split(os.sep)[-3], lire(f), "partagé"))
    return [(p, r, s) for p, r, s in out if r]


def onboarding_chemin(campagne):
    return os.path.join(DEMO, "onboarding.json") if campagne == "demo" else os.path.join(LAB, "campagne", "onboarding.json")


def onboarding(campagne):
    if campagne == "demo":
        return lire(onboarding_chemin("demo")) or {}
    for f in [onboarding_chemin("equipe")] + sorted(glob.glob(os.path.join(RACINE, "labs", "*", "campagne", "onboarding.json"))):
        if lire(f):
            return lire(f)
    return {"entreprise": "Notre équipe", "cout_horaire": 40}


def resume_a_relire(campagne, personne):
    if campagne == "demo":
        r = lire(os.path.join(DEMO_RELUS, f"{personne}.json")) or lire(os.path.join(DEMO, "resumes", f"{personne}.json"))
    else:
        moi = pseudo()
        r = lire(os.path.join(RACINE, "labs", moi, "campagne", "resume-valide.json")) or lire(os.path.join(RACINE, "donnees", moi, "resume.json"))
    if r:
        r["limites"] = [t for t in (texte_limite(l) for l in r.get("limites") or []) if t]
    return r


def chemin_valide(campagne, personne):
    if campagne == "demo":
        return os.path.join(DEMO_RELUS, f"{personne}.json")
    return os.path.join(RACINE, "labs", pseudo(), "campagne", "resume-valide.json")


# ---------- ce qui a le droit de sortir de la machine ----------

def txt(x, n=200):
    return str(x or "")[:n]


def nombre(x, defaut=0):
    try:
        return round(float(x), 2)
    except (TypeError, ValueError):
        return defaut


def nettoyer(r, personne):
    """Liste blanche : seuls ces champs partent. Aucun texte capturé, aucune capture, aucun texte long."""
    taches = []
    for t in r.get("taches") or []:
        if t.get("retiree") or not t.get("titre"):
            continue
        auto = t.get("automatisable") or {}
        taches.append({
            "titre": txt(t["titre"], 120), "frequence_par_semaine": nombre(t.get("frequence_par_semaine")),
            "duree_moyenne_min": nombre(t.get("duree_moyenne_min")), "apps": [txt(a, 60) for a in t.get("apps") or []][:8],
            "etapes": [{"type": txt(e.get("type"), 12), "texte": txt(e.get("texte"), 160), "app": txt(e.get("app"), 60),
                        "statut": "supposé" if e.get("statut") == "supposé" else "observé"} for e in t.get("etapes") or [] if e.get("texte")][:12],
            "exceptions": [txt(x, 160) for x in t.get("exceptions") or []][:6],
            "goulots": [{"type": txt(g.get("type"), 12), "detail": txt(g.get("detail"), 160)} for g in t.get("goulots") or []][:6],
            "automatisable": {"score": max(0, min(100, nombre(auto.get("score"), 50))), "pourquoi": txt(auto.get("pourquoi"), 240),
                              **({"corrige_par_la_personne": txt(auto["corrige_par_la_personne"], 60)} if auto.get("corrige_par_la_personne") else {})},
            "confiance": max(0, min(1, nombre(t.get("confiance"), 0.5))),
            "preuves": [{"debut": txt(p.get("debut"), 40), "fin": txt(p.get("fin"), 40), "app": txt(p.get("app"), 60)}
                        for p in t.get("preuves") or [] if isinstance(p, dict)][:40],
        })
    return {
        "campagne": txt(r.get("campagne"), 60), "personne": personne,
        "periode": {"debut": txt((r.get("periode") or {}).get("debut"), 40), "fin": txt((r.get("periode") or {}).get("fin"), 40)},
        "heures_captees": nombre(r.get("heures_captees")),
        "temps_par_app": [{"app": txt(a.get("app"), 60), "minutes": nombre(a.get("minutes"))} for a in r.get("temps_par_app") or [] if not a.get("masquee")],
        "temps_par_categorie": [{"categorie": txt(c.get("categorie"), 80), "minutes": nombre(c.get("minutes"))} for c in r.get("temps_par_categorie") or [] if not c.get("retiree")],
        "usage_ia": [{"outil": txt(u.get("outil"), 60), "minutes": nombre(u.get("minutes")), "usages": [txt(x, 120) for x in u.get("usages") or []][:6]}
                     for u in r.get("usage_ia") or [] if not u.get("retiree")],
        "taches": taches, "limites": [txt(x, 300) for x in r.get("limites") or []][:8],
        "tri_80_20": {k: nombre((r.get("tri_80_20") or {}).get(k)) for k in ("captures_regardees", "captures_gardees", "part")},
        "valide_par_la_personne": True, "valide_le": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


# ---------- le serveur ----------

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def envoyer(self, code, corps, type_="application/json; charset=utf-8"):
        b = corps if isinstance(corps, bytes) else json.dumps(corps, ensure_ascii=False).encode()
        self.send_response(code); self.send_header("Content-Type", type_); self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)

    def corps(self):
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n) or b"{}") if n < 2_000_000 else {}

    def do_GET(self):
        u = urlparse(self.path); q = {k: v[0] for k, v in parse_qs(u.query).items()}
        camp = "demo" if q.get("campagne", "demo") == "demo" else "equipe"
        if u.path in PAGES:
            f = PAGES[u.path]
            return self.envoyer(200, open(os.path.join(ICI, f), "rb").read(), "text/css; charset=utf-8" if f.endswith(".css") else "text/html; charset=utf-8")
        if u.path == "/api/campagne":
            moi = pseudo()
            return self.envoyer(200, {
                "campagne": camp, "moi": moi, "onboarding": onboarding(camp),
                "participants": [{"id": p, "valide": r.get("valide_par_la_personne") is True, "source": s,
                                  "taches": len(r.get("taches") or []), "heures": r.get("heures_captees")} for p, r, s in participants(camp)],
                "mon_resume_brut": os.path.exists(os.path.join(RACINE, "donnees", moi, "resume.json")),
                "mon_resume_partage": os.path.exists(os.path.join(RACINE, "labs", moi, "campagne", "resume-valide.json"))})
        if u.path == "/api/insights":
            resumes = [r for _, r, _ in participants(camp)]
            ins = fusionner(resumes, onboarding(camp), "ia" if q.get("ia") == "1" else "heuristique")
            return self.envoyer(200, vers_front_adamaass(ins, camp == "demo") if q.get("format") == "adamaass" else ins)
        if u.path == "/api/resume":
            r = resume_a_relire(camp, q.get("personne", ""))
            return self.envoyer(200, r) if r else self.envoyer(404, {"erreur": "Aucun résumé à relire. Lance d'abord les briques A et B sur ta machine."})
        self.envoyer(404, {"erreur": "introuvable"})

    def do_POST(self):
        u = urlparse(self.path); q = {k: v[0] for k, v in parse_qs(u.query).items()}
        camp = "demo" if q.get("campagne", "demo") == "demo" else "equipe"
        if u.path == "/api/valider":
            personne = q.get("personne") if camp == "demo" else "equipe-" + hashlib.sha1(pseudo().encode()).hexdigest()[:6]
            propre = nettoyer(self.corps(), personne)
            ecrire(chemin_valide(camp, q.get("personne", "")), propre)
            return self.envoyer(200, {"ok": True, "partage": propre})
        if u.path == "/api/retirer":
            f = chemin_valide(camp, q.get("personne", ""))
            if camp == "demo":
                r = lire(os.path.join(DEMO, "resumes", f"{q.get('personne', '')}.json"))
                if r:
                    ecrire(f, {**r, "valide_par_la_personne": False})
            elif os.path.exists(f):
                os.remove(f)
            return self.envoyer(200, {"ok": True})
        if u.path == "/api/reinitialiser-demo":
            for f in glob.glob(os.path.join(DEMO_RELUS, "*.json")):
                os.remove(f)
            return self.envoyer(200, {"ok": True})
        if u.path == "/api/onboarding" and camp == "equipe":
            ecrire(onboarding_chemin("equipe"), {k: v for k, v in self.corps().items() if k in ("entreprise", "activite", "priorites", "cout_horaire", "outils", "irritants")})
            return self.envoyer(200, {"ok": True})
        self.envoyer(404, {"erreur": "introuvable"})


def main():
    s = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)  # local uniquement : rien n'est exposé sur le réseau
    url = f"http://localhost:{PORT}"
    print(f"Wrapped prêt : {url}  (Ctrl+C pour arrêter)")
    if "--sans-navigateur" not in sys.argv:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    s.serve_forever()


if __name__ == "__main__":
    main()
