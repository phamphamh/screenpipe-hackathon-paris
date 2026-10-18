"""La preuve « rien n'est écrit en dur » : l'IA lit, devant le jury, l'enregistrement brut d'un salarié d'Atelier Nova.

  python3 labs/phamphamh/pitch/en-direct/serveur.py   → http://localhost:8797

Même consigne et même entrée que la brique B (labs/phamphamh/resume/resume.py), un seul appel à `claude -p`,
dont le texte est relayé au navigateur au fil de l'eau. Chaque lecture réussie est gardée dans
donnees/en-direct/ (jamais commité) : si le réseau lâche sur scène, la page propose de la rejouer, avec son heure.
"""
import json, os, re, subprocess, sys, tempfile, time
from datetime import datetime
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

ICI = os.path.dirname(os.path.abspath(__file__))
DEPOT = os.path.abspath(os.path.join(ICI, "..", "..", "..", ".."))
NOVA = os.path.join(DEPOT, "donnees", "nova")
GARDE = os.path.join(DEPOT, "donnees", "en-direct")
sys.path.insert(0, os.path.join(DEPOT, "labs", "phamphamh", "resume"))
import resume as B  # noqa: E402  (CONSIGNE et ligne() de la brique B)

# les 6 salariés d'Atelier Nova, comme dans labs/adamaass/caibinet-nova/construire.py
EQUIPES = {"E-commerce": ["lea", "karim", "sophie"], "Opérations": ["nadia", "julien", "emma"]}
PRENOMS = {"lea": "Léa"}
PORT = int(os.environ.get("PORT", 8797))
MOTS_VIDES = set("un une des les le la de du d l et ou sur par pour dans depuis son sa ses en au aux à a".split())
# verbes et mots trop généraux : « filtrer la liste des produits » ne doit pas rejoindre « filtrer la liste des commandes »
MOTS_VIDES |= set("filtrer liste consulter consultation chercher rechercher retrouver suivre générer mettre jour modifier toutes tous".split())


def moments(p):
    d = json.load(open(os.path.join(NOVA, p, "moments.json")))
    return d["stats"], [m for m in d["moments"] if not m["hors_travail"] and m["minutes"] >= 0.2]


def taches_du_rapport():
    js = open(os.path.join(DEPOT, "labs", "adamaass", "caibinet-nova", "data.js")).read()
    data = json.loads(js[js.index("{"):js.rindex("}") + 1])
    return [t["titre"] for t in data["dash"]["taches"]]


def mots(t):
    return {w[:6] for w in re.findall(r"[a-zà-ÿ]+", t.lower()) if w not in MOTS_VIDES and len(w) > 2}


def dans_le_rapport(titre, rapport):
    """La tâche du rapport qui partage le plus de mots avec celle que l'IA vient de trouver (au moins 2)."""
    m = mots(titre)
    meilleur = max(rapport, key=lambda r: len(m & mots(r)), default=None)
    return meilleur if meilleur and len(m & mots(meilleur)) >= 2 else None


class Page(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def envoyer(self, code, corps, type_="application/json; charset=utf-8"):
        b = corps.encode() if isinstance(corps, str) else corps
        self.send_response(code); self.send_header("Content-Type", type_); self.send_header("Content-Length", str(len(b)))
        self.end_headers(); self.wfile.write(b)

    def evenement(self, nom, donnees):
        self.wfile.write(f"event: {nom}\ndata: {json.dumps(donnees, ensure_ascii=False)}\n\n".encode()); self.wfile.flush()

    def do_GET(self):
        u = urlparse(self.path); q = parse_qs(u.query); p = (q.get("p") or [""])[0]
        if u.path == "/":
            return self.envoyer(200, open(os.path.join(ICI, "index.html"), "rb").read(), "text/html; charset=utf-8")
        if u.path == "/api/salaries":
            out = []
            for eq, ps in EQUIPES.items():
                for x in ps:
                    st, ms = moments(x)
                    out.append({"id": x, "prenom": PRENOMS.get(x, x.capitalize()), "equipe": eq, "role": st.get("role", ""), "moments": len(ms),
                                "captures": st["captures_regardees"], "garde": os.path.exists(os.path.join(GARDE, x + ".json"))})
            return self.envoyer(200, json.dumps(out, ensure_ascii=False))
        if p not in {x for ps in EQUIPES.values() for x in ps}:
            return self.envoyer(404, "{}")
        if u.path == "/api/brut":
            st, ms = moments(p)
            return self.envoyer(200, json.dumps({"stats": st, "lignes": [
                {"h": m["debut"][5:16].replace("T", " "), "fenetre": m["fenetre"], "url": urlparse(m["url"]).path if m["url"] else "",
                 "texte": m["texte_nouveau"][:140]} for m in ms]}, ensure_ascii=False))
        if u.path == "/api/rejouer":
            f = os.path.join(GARDE, p + ".json")
            return self.envoyer(200, open(f).read()) if os.path.exists(f) else self.envoyer(404, "{}")
        if u.path == "/api/lire":
            return self.lire(p)
        self.envoyer(404, "{}")

    def lire(self, p):
        self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        _, ms = moments(p)
        entree = B.CONSIGNE + "\n\nLES MOMENTS :\n" + "\n".join(B.ligne(i, m) for i, m in enumerate(ms))
        t0 = time.time(); texte = ""
        try:
            proc = subprocess.Popen(["claude", "-p", "--model", "sonnet", "--no-session-persistence", "--output-format", "stream-json",
                                     "--verbose", "--include-partial-messages"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                    stderr=subprocess.DEVNULL, text=True, cwd=tempfile.gettempdir())  # hors du dépôt : pas de hooks d'équipe
            proc.stdin.write(entree); proc.stdin.close()
            for l in proc.stdout:
                try:
                    e = json.loads(l)
                except ValueError:
                    continue
                d = (e.get("event") or {}).get("delta") or {}
                if e.get("type") == "stream_event" and d.get("type") == "text_delta":
                    texte += d["text"]; self.evenement("texte", d["text"])
                elif e.get("type") == "result" and not texte:
                    texte = e.get("result") or ""
            proc.wait(timeout=30)
            bloc = re.search(r"\{.*\}", texte, re.S)
            if not bloc:
                raise ValueError("pas de JSON dans la réponse")
            ia = json.loads(bloc.group(0))
        except Exception as ex:  # réseau, crédit, JSON tronqué : on le dit, la page propose de rejouer la dernière lecture
            return self.evenement("erreur", str(ex)[:200])
        rapport = taches_du_rapport()
        fin = {"secondes": round(time.time() - t0), "heure": datetime.now().strftime("%H:%M"), "moments": len(ms), "taches": [
            {"titre": t["titre"], "preuves": len(t.get("preuves", [])), "etapes": [s["texte"] for s in t.get("etapes", [])][:4],
             "rapport": dans_le_rapport(t["titre"], rapport)} for t in ia.get("taches", [])]}
        os.makedirs(GARDE, exist_ok=True)
        json.dump(fin, open(os.path.join(GARDE, p + ".json"), "w"), ensure_ascii=False)
        self.evenement("fin", fin)


if __name__ == "__main__":
    print(f"En direct : http://localhost:{PORT}")
    ThreadingHTTPServer(("127.0.0.1", PORT), Page).serve_forever()
