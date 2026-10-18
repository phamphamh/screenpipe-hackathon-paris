#!/usr/bin/env python3
"""Les agents IA déployés d'Atelier Nova : un vrai agent Claude traite une vraie demande dans la boutique de test.

Un passage = la prochaine demande de l'agent (rotation dans demandes.json, tirées de WONDERBREAD), confiée à
`claude -p` avec la skill de l'agent (les étapes observées chez les salariés, labs/adamaass/exemples/nova-backoffice.json)
et un seul outil autorisé : boutique.py. Journal : donnees/agents-nova/journal.jsonl ; bilan : runs.jsonl.

Usage : python3 agents_ia.py <prix-produit|rapport-ventes|commandes-annulees>
"""
import json, os, subprocess, sys, time, uuid
from datetime import datetime, timezone

import boutique

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = boutique.RACINE
SORTIE = boutique.SORTIE
OUTIL = os.path.join(ICI, "boutique.py")
DELAI_S = int(os.environ.get("DELAI_AGENT", 150))
MODELE = os.environ.get("MODELE_AGENT", "sonnet")
# hors du dépôt : sinon les hooks du dépôt (sauvegarde git automatique) se déclencheraient dans l'agent
TRAVAIL = os.path.expanduser("~/.cache/deloai-agents")

# skill de l'audit → tâche observée chez les salariés (labs/adamaass/exemples/nova-backoffice.json)
SKILLS = {
    "prix-produit": {"tache": "t1", "nom": "Prix produit", "consigne": (
        "Les variantes sont des produits simples nommés « Nom-TAILLE-Couleur » (ex. « Gwyn Endurance Tee-XS-Yellow »). "
        "Ordre des tailles : XS < S < M < L < XL (pantalons : tailles numériques). Ne change que les variantes simples "
        "qui correspondent exactement à la demande, une par une, avec `prix <sku> <nouveau_prix>` (arrondi au centime).")},
    "rapport-ventes": {"tache": "t2", "nom": "Rapport de ventes", "consigne": (
        "Dates au format MM/JJ/AAAA. Rapport des commandes = `rapport orders`, meilleures ventes = `rapport bestsellers`, "
        "remboursements = `rapport refunded`, taxes = `rapport tax`. « Le mois dernier » = le mois civil précédent entier.")},
    "commandes-annulees": {"tache": "t5", "nom": "Commandes annulées", "consigne": (
        "Statuts Magento : canceled (annulée), complete (terminée), pending, processing. Les commandes sortent triées "
        "de la plus récente à la plus ancienne. Pour compter sur tout l'historique, prends --limite 200.")},
}

en_cours = None  # {run, agent, demande_fr, depuis} pendant un passage (lu par serveur.py)


def maintenant():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def lire_jsonl(nom):
    chemin = os.path.join(SORTIE, nom)
    return [json.loads(l) for l in open(chemin) if l.strip()] if os.path.exists(chemin) else []


def ecrire_jsonl(nom, obj):
    os.makedirs(SORTIE, exist_ok=True)
    with open(os.path.join(SORTIE, nom), "a") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def demandes(agent_id):
    return json.load(open(os.path.join(ICI, "demandes.json")))["agents"][agent_id]


def etapes(tache_id):
    d = json.load(open(os.path.join(RACINE, "labs", "adamaass", "exemples", "nova-backoffice.json")))
    t = next(t for t in d["taches"] if t["id"] == tache_id)
    return t["titre"], [e["texte"] for e in t["etapes"]], t.get("personnes"), t.get("frequence_par_semaine")


def consigne(agent_id):
    s = SKILLS[agent_id]
    titre, liste, personnes, freq = etapes(s["tache"])
    lignes = "\n".join(f"{i}. {e}" for i, e in enumerate(liste, 1))
    return f"""Tu es l'agent « {s['nom']} » d'Atelier Nova, déployé dans le back-office Magento de la boutique.
Ta skill vient de l'observation de {personnes} salariés qui font cette tâche ({freq} fois par semaine) : « {titre} ».
Étapes observées chez eux :
{lignes}

Ton seul outil : la commande Bash `python3 {OUTIL} …` (rien d'autre, pas de cd, pas de pipe). Sous-commandes :
- `python3 {OUTIL} chercher "<mots du nom>"` : produits dont le nom contient tous les mots (sku, nom, prix, id)
- `python3 {OUTIL} prix <sku> <nouveau_prix>` : change le prix d'un produit (affiche ancien → nouveau)
- `python3 {OUTIL} commandes [--statut canceled] [--client "<nom>"] [--limite N]` : commandes, plus récentes d'abord
- `python3 {OUTIL} rapport <orders|refunded|tax|bestsellers> --du MM/JJ/AAAA --au MM/JJ/AAAA` : rapport de l'admin, avec totaux
{s['consigne']}

Règles : tu es autonome, ne pose aucune question. Fais le minimum d'appels nécessaires.
Réponds en français, en 2 phrases courtes maximum, avec le résultat chiffré (ce que tu as fait ou trouvé).
Texte simple sans markdown, montants en dollars ($) comme dans la boutique, aucun commentaire sur ta méthode."""


PORT_CDP = int(os.environ.get("PORT_CDP", 9333))


def ouvrir_fenetre():
    """Mode visible : UNE fenêtre Chromium (1280×800, à gauche de l'écran) pour tout le passage.
    boutique.py s'y reconnecte à chaque appel grâce à BOUTIQUE_CDP."""
    import urllib.request
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        exe = p.chromium.executable_path
    proc = subprocess.Popen([exe, f"--remote-debugging-port={PORT_CDP}", f"--user-data-dir={TRAVAIL}/chromium-profil",
                             "--window-position=0,0", "--window-size=1280,800", "--no-first-run",
                             "--no-default-browser-check", "--disable-features=Translate", "about:blank"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(150):  # premier lancement d’un profil neuf : jusqu’à 30 s
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{PORT_CDP}/json/version", timeout=1)
            return proc
        except Exception:
            time.sleep(0.2)
    proc.terminate()
    raise RuntimeError("la fenêtre Chromium ne répond pas")


def personne_workflow(personne, agent_id=None):
    """(personne, workflow) depuis personnes.json (construire_personnes.py)."""
    gens = json.load(open(os.path.join(ICI, "personnes.json")))
    p = next(x for x in gens if x["id"] == personne)
    w = next(w for w in p["workflows"] if agent_id in (None, w["agent"]))
    return p, w


def passage(agent_id, visible=None, personne=None):
    """Un passage de l'agent : prochaine demande (rotation), vrai agent Claude, bilan dans runs.jsonl.
    visible=True (ou BOUTIQUE_VISIBLE=1) : l'agent agit dans une fenêtre Chromium qu'on voit (démo en direct)."""
    global en_cours
    if visible is None:
        visible = os.environ.get("BOUTIQUE_VISIBLE") == "1"
    liste = demandes(agent_id)
    deja = [r for r in lire_jsonl("runs.jsonl") if r.get("agent") == agent_id]
    i = len(deja) % len(liste)
    d = liste[i]
    qui = None
    if personne:  # la demande du workflow de cette personne (bureau 3D → « Créer le workflow »)
        qui, w = personne_workflow(personne, agent_id)
        d = {"id": f"{personne}-{agent_id}", "intention": w["demande"]["en"], "fr": w["demande"]["fr"]}
    run = datetime.now().strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:4]
    t0 = time.time()
    en_cours = {"run": run, "agent": agent_id, "demande_fr": d["fr"], "depuis": maintenant(),
                "personne": personne}
    env = {**os.environ, "AGENT_ID": agent_id, "AGENT_RUN": run, "BOUTIQUE_VISIBLE": "1" if visible else "0",
           "AGENT_BANDEAU": (f"DeloAI · {SKILLS[agent_id]['nom']} · pour {qui['prenom']}" if qui else
                             f"DeloAI · {SKILLS[agent_id]['nom']} · demande Stanford : {d['intention']}")}
    env.pop("BOUTIQUE_CDP", None)
    ecrire_jsonl("journal.jsonl", {"ts": maintenant(), "agent": agent_id, "run": run, "n": 0, "type": "demande",
                                   "etape": f"{qui['prenom']} · {SKILLS[agent_id]['nom']}" if qui else "Reçoit une demande",
                                   "detail": d["fr"], "demande": d["intention"], "demande_id": d["id"],
                                   "personne": personne, "capture": None})
    if agent_id == "prix-produit" and i == 0 and os.path.exists(os.path.join(SORTIE, "prix-origine.json")):
        # nouveau tour de rotation : on remet les prix d'origine, pour que les baisses ne s'empilent pas
        subprocess.run([sys.executable, OUTIL, "restaurer-prix"], env=env, capture_output=True, timeout=60)
    fenetre = None
    if visible:
        try:
            fenetre = ouvrir_fenetre()
            env["BOUTIQUE_CDP"] = f"http://127.0.0.1:{PORT_CDP}"
            subprocess.run([sys.executable, OUTIL, "accueil"], env=env, capture_output=True, timeout=90)
        except Exception as e:  # sans fenêtre partagée, chaque appel ouvre sa propre fenêtre visible
            print(f"fenêtre partagée impossible : {e}", file=sys.stderr)
    dossier = os.path.join(TRAVAIL, run)
    os.makedirs(dossier, exist_ok=True)
    cmd = ["claude", "-p", d["intention"], "--model", MODELE, "--append-system-prompt", consigne(agent_id),
           "--allowedTools", f"Bash(python3 {OUTIL}:*)", "--permission-mode", "default", "--output-format", "json",
           "--strict-mcp-config", "--no-session-persistence"]
    statut, reponse, cout = "echec", "", None
    try:
        delai = DELAI_S * 2 if visible else DELAI_S  # au ralenti, l'interface d'admin prend plus de temps
        p = subprocess.run(cmd, cwd=dossier, env=env, capture_output=True, text=True, timeout=delai)
        try:
            sortie = json.loads(p.stdout)
            reponse = (sortie.get("result") or "").strip()
            cout = sortie.get("total_cost_usd")
            statut = "echec" if sortie.get("is_error") or not reponse else "ok"
        except json.JSONDecodeError:
            reponse = (p.stderr or p.stdout or "sortie illisible").strip()[:300]
    except subprocess.TimeoutExpired:
        reponse = f"Délai dépassé : l'agent n'a pas fini."
    except Exception as e:
        reponse = f"Lancement impossible : {e}"[:300]
    finally:
        if fenetre:
            time.sleep(4)  # on laisse le résultat à l'écran un instant
            fenetre.terminate()
    duree = round(time.time() - t0, 1)
    actions = sum(1 for l in lire_jsonl("journal.jsonl") if l.get("run") == run and l.get("type") == "outil")
    ecrire_jsonl("journal.jsonl", {"ts": maintenant(), "agent": agent_id, "run": run, "n": actions + 1,
                                   "type": "resultat", "etape": "Répond" if statut == "ok" else "Échec",
                                   "detail": reponse, "statut": statut, "capture": None})
    bilan = {"run": run, "agent": agent_id, "demande_id": d["id"], "demande": d["intention"], "fr": d["fr"],
             "statut": statut, "reponse": reponse, "duree_s": duree, "actions": actions, "cout_usd": cout,
             "visible": bool(visible), "personne": personne,
             "fini": maintenant()}
    ecrire_jsonl("runs.jsonl", bilan)
    en_cours = None
    return bilan


if __name__ == "__main__":
    # python3 agents_ia.py <agent> [--visible]
    print(json.dumps(passage(sys.argv[1] if len(sys.argv) > 1 else "rapport-ventes", True if "--visible" in sys.argv else None),
                     ensure_ascii=False, indent=1))
