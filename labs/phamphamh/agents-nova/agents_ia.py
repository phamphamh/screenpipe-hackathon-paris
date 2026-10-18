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


def passage(agent_id):
    """Un passage de l'agent : prochaine demande (rotation), vrai agent Claude, bilan dans runs.jsonl."""
    global en_cours
    liste = demandes(agent_id)
    deja = [r for r in lire_jsonl("runs.jsonl") if r.get("agent") == agent_id]
    i = len(deja) % len(liste)
    d = liste[i]
    run = datetime.now().strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:4]
    t0 = time.time()
    en_cours = {"run": run, "agent": agent_id, "demande_fr": d["fr"], "depuis": maintenant()}
    env = {**os.environ, "AGENT_ID": agent_id, "AGENT_RUN": run}
    ecrire_jsonl("journal.jsonl", {"ts": maintenant(), "agent": agent_id, "run": run, "n": 0, "type": "demande",
                                   "etape": "Reçoit une demande", "detail": d["fr"], "demande": d["intention"],
                                   "demande_id": d["id"], "capture": None})
    if agent_id == "prix-produit" and i == 0 and os.path.exists(os.path.join(SORTIE, "prix-origine.json")):
        # nouveau tour de rotation : on remet les prix d'origine, pour que les baisses ne s'empilent pas
        subprocess.run([sys.executable, OUTIL, "restaurer-prix"], env=env, capture_output=True, timeout=60)
    dossier = os.path.join(TRAVAIL, run)
    os.makedirs(dossier, exist_ok=True)
    cmd = ["claude", "-p", d["intention"], "--model", MODELE, "--append-system-prompt", consigne(agent_id),
           "--allowedTools", f"Bash(python3 {OUTIL}:*)", "--permission-mode", "default", "--output-format", "json",
           "--strict-mcp-config", "--no-session-persistence"]
    statut, reponse, cout = "echec", "", None
    try:
        p = subprocess.run(cmd, cwd=dossier, env=env, capture_output=True, text=True, timeout=DELAI_S)
        try:
            sortie = json.loads(p.stdout)
            reponse = (sortie.get("result") or "").strip()
            cout = sortie.get("total_cost_usd")
            statut = "echec" if sortie.get("is_error") or not reponse else "ok"
        except json.JSONDecodeError:
            reponse = (p.stderr or p.stdout or "sortie illisible").strip()[:300]
    except subprocess.TimeoutExpired:
        reponse = f"Délai dépassé ({DELAI_S} s) : l'agent n'a pas fini."
    except Exception as e:
        reponse = f"Lancement impossible : {e}"[:300]
    duree = round(time.time() - t0, 1)
    actions = sum(1 for l in lire_jsonl("journal.jsonl") if l.get("run") == run and l.get("type") == "outil")
    ecrire_jsonl("journal.jsonl", {"ts": maintenant(), "agent": agent_id, "run": run, "n": actions + 1,
                                   "type": "resultat", "etape": "Répond" if statut == "ok" else "Échec",
                                   "detail": reponse, "statut": statut, "capture": None})
    bilan = {"run": run, "agent": agent_id, "demande_id": d["id"], "demande": d["intention"], "fr": d["fr"],
             "statut": statut, "reponse": reponse, "duree_s": duree, "actions": actions, "cout_usd": cout,
             "fini": maintenant()}
    ecrire_jsonl("runs.jsonl", bilan)
    en_cours = None
    return bilan


if __name__ == "__main__":
    print(json.dumps(passage(sys.argv[1] if len(sys.argv) > 1 else "rapport-ventes"), ensure_ascii=False, indent=1))
