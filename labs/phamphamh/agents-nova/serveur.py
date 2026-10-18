#!/usr/bin/env python3
"""La démo DeloAI · Atelier Nova : les données, l'audit, et les agents IA déployés qui tournent pour de vrai.

- sert la page (labs/phamphamh/agents-nova/index.html) et le dashboard (labs/phamphamh/dashboard-nova/) ;
- fait tourner les 3 agents en service à tour de rôle, un passage toutes les INTERVALLE minutes : chaque passage est
  un vrai agent Claude qui traite une vraie demande (WONDERBREAD) dans la boutique de test (agents_ia.py) ;
- GET /api/etat : agents, passages, journal ; POST /api/lancer?agent=<id>[&visible=1] : un passage tout de suite
  (visible=1 : l'agent agit dans une fenêtre Chromium qu'on voit, pour la démo en direct).

Usage : python3 labs/phamphamh/agents-nova/serveur.py   →  http://localhost:8798
Variables : INTERVALLE (minutes, défaut 5), PORT (défaut 8798).
"""
import json, os, threading, time
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import agents_ia

ICI = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(ICI)
SORTIE = agents_ia.SORTIE
PORT = int(os.environ.get("PORT", 8798))
INTERVALLE = float(os.environ.get("INTERVALLE", 5))
# temps humain médian par tâche (secondes), mesuré sur les démos WONDERBREAD
# (donnees/wonderbread/traces/demos_sop_and_trace_only/<dossier>/*.json, dernier secs_from_start)
HUMAIN_S = {
    "rapport-ventes": 23,       # médiane mesurée sur 20 démos « rapport de ventes »
    "prix-produit": 58.4,       # médiane de 34 démos, tâches 777 à 782 (prix des variantes)
    "commandes-annulees": 35.7, # médiane de 40 démos, tâches 196, 198, 202, 288 à 292 (commandes annulées)
}
# les 5 skills recommandées par l'audit (dashboard, écran Recommandation) ; 3 sont déployées
AGENTS = [
    {"id": "prix-produit", "nom": "Prix produit", "equipe": "Opérations", "statut": "en service"},
    {"id": "rapport-ventes", "nom": "Rapport de ventes", "equipe": "E-commerce", "statut": "en service"},
    {"id": "commandes-annulees", "nom": "Commandes annulées", "equipe": "Opérations", "statut": "en service"},
    {"id": "avis-produit", "nom": "Avis produit", "equipe": "E-commerce", "statut": "en préparation"},
    {"id": "variantes-produit", "nom": "Variantes produit", "equipe": "Opérations", "statut": "en préparation"},
]
EN_SERVICE = [a["id"] for a in AGENTS if a["statut"] == "en service"]
verrou = threading.Lock()


def lire_jsonl(nom, n=None):
    chemin = os.path.join(SORTIE, nom)
    if not os.path.exists(chemin):
        return []
    lignes = []
    for l in open(chemin):
        try:
            lignes.append(json.loads(l))
        except json.JSONDecodeError:  # ligne en cours d'écriture
            pass
    return lignes[-n:] if n else lignes


def deploiement():
    """Date du déploiement : écrite au premier démarrage, gardée ensuite."""
    chemin = os.path.join(SORTIE, "deploiement.json")
    if not os.path.exists(chemin):
        os.makedirs(SORTIE, exist_ok=True)
        json.dump({"depuis": datetime.now(timezone.utc).isoformat(timespec="seconds")}, open(chemin, "w"))
    return {"depuis": json.load(open(chemin))["depuis"]}


def passage(agent_id, visible=False, personne=None):
    """Un passage ; False si un autre passage est déjà en cours. Le planificateur reste invisible."""
    if not verrou.acquire(blocking=False):
        return False
    try:
        agents_ia.passage(agent_id, visible, personne)
    except Exception as e:  # le planificateur ne doit jamais mourir
        print(f"passage {agent_id} : {e}", flush=True)
        agents_ia.en_cours = None
    finally:
        verrou.release()
    return True


def prochain_agent():
    """L'agent en service qui est passé le moins récemment (rotation)."""
    derniers = {r.get("agent"): r.get("fini", "") for r in lire_jsonl("runs.jsonl")}
    return min(EN_SERVICE, key=lambda a: (derniers.get(a, ""), EN_SERVICE.index(a)))


def planificateur():
    while True:
        time.sleep(INTERVALLE * 60)
        passage(prochain_agent())


def resume():
    runs = lire_jsonl("runs.jsonl")
    ok = [r for r in runs if r.get("statut") == "ok"]
    agents = []
    for a in AGENTS:
        siens = [r for r in runs if r.get("agent") == a["id"]]
        agents.append({**a, "passages": len(siens), "reussis": sum(r.get("statut") == "ok" for r in siens),
                       "derniere_reponse": siens[-1].get("reponse") if siens else None})
    return {
        "deploiement": deploiement(), "intervalle_min": INTERVALLE, "en_cours": agents_ia.en_cours, "agents": agents,
        "passages": len(runs), "reussis": len(ok), "actions": sum(r.get("actions", 0) for r in runs),
        "humain_s_economise": round(sum(HUMAIN_S.get(r.get("agent"), 0) for r in ok), 1),
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
        if self.path.startswith("/api/personnes"):
            return self.envoyer_json(json.load(open(os.path.join(ICI, "personnes.json"))))
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
        url = urlparse(self.path)
        if url.path == "/api/lancer":
            q = parse_qs(url.query)
            personne = (q.get("personne") or [None])[0]
            agent = (q.get("agent") or [None])[0]
            if personne:
                try:
                    agent = agents_ia.personne_workflow(personne, agent)[1]["agent"]
                except StopIteration:
                    return self.envoyer_json({"lance": False, "raison": f"pas de workflow {agent or ''} pour {personne}"}, 400)
            agent = agent or prochain_agent()
            visible = (q.get("visible") or ["0"])[0] in ("1", "true", "oui")
            if agent not in EN_SERVICE:
                return self.envoyer_json({"lance": False, "raison": f"agent inconnu ou pas en service : {agent}"}, 400)
            if verrou.locked() or agents_ia.en_cours:
                return self.envoyer_json({"lance": False, "raison": "un passage est déjà en cours",
                                          "en_cours": agents_ia.en_cours}, 409)
            threading.Thread(target=passage, args=(agent, visible, personne), daemon=True).start()
            return self.envoyer_json({"lance": True, "agent": agent, "visible": visible, "personne": personne})
        self.send_error(404)


if __name__ == "__main__":
    deploiement()
    threading.Thread(target=planificateur, daemon=True).start()
    print(f"Démo DeloAI : http://localhost:{PORT}  (un agent toutes les {INTERVALLE:g} min, à tour de rôle)", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), Gestion).serve_forever()
