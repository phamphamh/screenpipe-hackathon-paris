#!/usr/bin/env python3
"""La démo DeloAI · Atelier Nova : les données, l'audit, et les agents déployés qui tournent pour de vrai.

- sert la page (labs/phamphamh/agents-nova/index.html) et le dashboard (labs/phamphamh/dashboard-nova/) ;
- fait tourner l'agent « Rapport de ventes » toutes les INTERVALLE minutes dans la boutique de test (c'est ça, « déployé ») ;
- GET /api/etat : agents, passages, journal ; POST /api/lancer : un passage tout de suite.

Usage : python3 labs/phamphamh/agents-nova/serveur.py   →  http://localhost:8798
Variables : INTERVALLE (minutes, défaut 15), PORT (défaut 8798).
"""
import json, os, threading, time
from datetime import datetime, timezone, timedelta
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

import agent_rapport

ICI = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(ICI)
SORTIE = agent_rapport.SORTIE
PORT = int(os.environ.get("PORT", 8798))
INTERVALLE = float(os.environ.get("INTERVALLE", 15))
HUMAIN_S = 23  # médiane mesurée sur 20 démos WONDERBREAD « rapport de ventes »
PAR_SEMAINE = 790  # fréquence du rapport chez Atelier Nova (×10), dashboard d'adamaass
# les 5 skills recommandées par l'audit (dashboard, écran Recommandation) ; une seule est déployée
AGENTS = [
    {"id": "rapport-ventes", "nom": "Rapport de ventes", "equipe": "E-commerce", "statut": "en service"},
    {"id": "prix-produit", "nom": "Prix produit", "equipe": "Opérations", "statut": "en préparation"},
    {"id": "commandes-annulees", "nom": "Commandes annulées", "equipe": "Opérations", "statut": "en préparation"},
    {"id": "avis-produit", "nom": "Avis produit", "equipe": "E-commerce", "statut": "en préparation"},
    {"id": "variantes-produit", "nom": "Variantes produit", "equipe": "Opérations", "statut": "en préparation"},
]
verrou = threading.Lock()
etat = {"en_cours": False, "prochain": None}


def lire_jsonl(nom, n=None):
    chemin = os.path.join(SORTIE, nom)
    if not os.path.exists(chemin):
        return []
    lignes = [json.loads(l) for l in open(chemin) if l.strip()]
    return lignes[-n:] if n else lignes


def deploiement():
    """Date du déploiement : écrite au premier démarrage, gardée ensuite."""
    chemin = os.path.join(SORTIE, "deploiement.json")
    if not os.path.exists(chemin):
        os.makedirs(SORTIE, exist_ok=True)
        json.dump({"agent": "rapport-ventes", "depuis": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                   "intervalle_min": INTERVALLE}, open(chemin, "w"))
    return json.load(open(chemin))


def passage():
    if not verrou.acquire(blocking=False):
        return False
    etat["en_cours"] = True
    try:
        agent_rapport.lancer("02/01/2023", "02/28/2023")
    finally:
        etat["en_cours"] = False
        verrou.release()
    return True


def planificateur():
    while True:
        etat["prochain"] = (datetime.now(timezone.utc) + timedelta(minutes=INTERVALLE)).isoformat(timespec="seconds")
        time.sleep(INTERVALLE * 60)
        passage()


def resume():
    runs = lire_jsonl("runs.jsonl")
    ok = [r for r in runs if r.get("statut") == "ok"]
    duree = round(sum(r["duree_s"] for r in ok) / len(ok), 1) if ok else None
    return {
        "deploiement": deploiement(), "intervalle_min": INTERVALLE, "en_cours": etat["en_cours"], "prochain": etat["prochain"],
        "agents": AGENTS, "passages": len(runs), "reussis": len(ok), "actions": sum(r.get("actions", 0) for r in runs),
        "duree_agent_s": duree, "duree_humain_s": HUMAIN_S, "par_semaine": PAR_SEMAINE,
        "heures_rendues_semaine": round(PAR_SEMAINE * HUMAIN_S / 3600, 1),
        "dernier": runs[-1] if runs else None, "runs": runs[-12:][::-1], "journal": lire_jsonl("journal.jsonl", 40),
    }


class Gestion(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=LAB, **k)

    def log_message(self, *a):
        pass

    def envoyer_json(self, obj, code=200):
        corps = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store"); self.send_header("Content-Length", str(len(corps)))
        self.end_headers(); self.wfile.write(corps)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.send_response(302); self.send_header("Location", "/agents-nova/"); self.end_headers(); return
        if self.path.startswith("/api/etat"):
            return self.envoyer_json(resume())
        if self.path.startswith("/captures/"):
            chemin = os.path.normpath(os.path.join(SORTIE, self.path[1:].split("?")[0]))
            if not chemin.startswith(os.path.join(SORTIE, "captures")) or not os.path.isfile(chemin):
                return self.send_error(404)
            corps = open(chemin, "rb").read()
            self.send_response(200); self.send_header("Content-Type", "image/jpeg")
            self.send_header("Content-Length", str(len(corps))); self.end_headers(); self.wfile.write(corps); return
        return super().do_GET()

    def do_POST(self):
        if self.path.startswith("/api/lancer"):
            if etat["en_cours"]:
                return self.envoyer_json({"lance": False, "raison": "un passage est déjà en cours"})
            threading.Thread(target=passage, daemon=True).start()
            return self.envoyer_json({"lance": True})
        self.send_error(404)


if __name__ == "__main__":
    deploiement()
    threading.Thread(target=planificateur, daemon=True).start()
    print(f"Démo DeloAI : http://localhost:{PORT}  (agent toutes les {INTERVALLE:g} min)")
    ThreadingHTTPServer(("127.0.0.1", PORT), Gestion).serve_forever()
