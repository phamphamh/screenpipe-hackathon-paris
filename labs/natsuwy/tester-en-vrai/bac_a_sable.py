#!/usr/bin/env python3
"""Faux Gmail + faux Sage pour tester une skill « en vrai » : Claude agit dedans, chaque appel est tracé.

L'état vit dans etat.json (à côté de ce fichier), la trace dans actions.jsonl.
  python3 bac_a_sable.py aide
  python3 bac_a_sable.py gmail recus | lire <id> | brouillon <a> <objet> <corps> | envoyer <a> <objet> <corps>
  python3 bac_a_sable.py sage article <ref> | creer-commande <client> '<lignes JSON>' | valider-commande <numero>
Garde-fou (optionnel) : si etat.json contient {"politique": {"approbation_requise": ["gmail envoyer", "sage valider-commande"]}},
ces actions ne s'exécutent pas : elles deviennent une demande « en attente » que seul un humain tranche, avec approbations.py
(un outil à part, jamais donné à l'agent). Chaque appel est écrit dans audit.jsonl.
Uniquement la bibliothèque standard de Python. Aucune donnée ne sort de la machine.
"""
import json, os, sys
from datetime import datetime

ICI = os.path.dirname(os.path.abspath(__file__))
ETAT = os.path.join(ICI, "etat.json")
TRACE = os.path.join(ICI, "actions.jsonl")
AUDIT = os.path.join(ICI, "audit.jsonl")
# Les appels qui changent quelque chose (le reste ne fait que lire).
EFFETS = {"gmail brouillon", "gmail envoyer", "sage creer-commande", "sage valider-commande"}

AIDE = """Apps disponibles (Maison Corvo) :
  gmail recus                              liste les mails reçus
  gmail lire <id>                          affiche un mail
  gmail brouillon <a> <objet> <corps>      enregistre un brouillon (rien n'est envoyé)
  gmail envoyer <a> <objet> <corps>        ENVOIE un mail au destinataire
  sage article <ref>                       désignation, stock, prix négocié du client
  sage creer-commande <client> '<lignes>'  crée une commande en brouillon ; lignes = [{"ref":"REF-1","qte":2,"prix":3.1}]
  sage valider-commande <numero>           enregistre définitivement la commande (part en préparation)"""


def utiliser_dossier(dossier):
    """Pointe l'état, la trace et l'audit vers un autre dossier (utilisé par approbations.py)."""
    global ETAT, TRACE, AUDIT
    ETAT, TRACE, AUDIT = (os.path.join(dossier, n) for n in ("etat.json", "actions.jsonl", "audit.jsonl"))


def maintenant():
    return datetime.now().isoformat(timespec="seconds")


def charger():
    with open(ETAT, encoding="utf-8") as f:
        return json.load(f)


def sauver(etat):
    with open(ETAT, "w", encoding="utf-8") as f:
        json.dump(etat, f, ensure_ascii=False, indent=1)


def tracer(args, ok, sortie):
    with open(TRACE, "a", encoding="utf-8") as f:
        f.write(json.dumps({"quand": datetime.now().isoformat(timespec="seconds"), "appel": args, "ok": ok, "sortie": sortie[:300]}, ensure_ascii=False) + "\n")


def auditer(acteur, statut, appel, sortie, demande=None, par=None, motif=None):
    """Journal d'audit : qui a fait quoi, quand, avec quel résultat. On n'y réécrit jamais, on ajoute."""
    evt = {"quand": maintenant(), "acteur": acteur, "statut": statut, "action": " ".join(appel[:2]), "appel": appel,
           "demande": demande, "par": par, "motif": motif, "sortie": sortie[:300]}
    with open(AUDIT, "a", encoding="utf-8") as f:
        f.write(json.dumps({k: v for k, v in evt.items() if v is not None}, ensure_ascii=False) + "\n")


def gmail(etat, args):
    g = etat["gmail"]
    if args[:1] == ["recus"]:
        return "\n".join(f"[{m['id']}] de {m['de']} : {m['objet']}" for m in g["recus"]) or "Boîte vide."
    if args[:1] == ["lire"] and len(args) == 2:
        m = next((m for m in g["recus"] if m["id"] == args[1]), None)
        if not m:
            raise ValueError(f"mail {args[1]} introuvable")
        return f"De : {m['de']}\nObjet : {m['objet']}\n\n{m['corps']}"
    if args[:1] in (["brouillon"], ["envoyer"]) and len(args) == 4:
        boite = "brouillons" if args[0] == "brouillon" else "envoyes"
        g[boite].append({"a": args[1], "objet": args[2], "corps": args[3]})
        return "Brouillon enregistré, rien n'a été envoyé." if boite == "brouillons" else f"Mail envoyé à {args[1]}."
    raise ValueError("commande gmail inconnue (voir : aide)")


def sage(etat, args):
    s = etat["sage"]
    if args[:1] == ["article"] and len(args) == 2:
        a = s["articles"].get(args[1])
        if not a:
            raise ValueError(f"article {args[1]} introuvable dans Sage")
        return f"{args[1]} · {a['designation']} · stock {a['stock']} · prix négocié {a['prix']:.2f} €"
    if args[:1] == ["creer-commande"] and len(args) == 3:
        lignes = json.loads(args[2])
        alertes = []
        for l in lignes:
            a = s["articles"].get(l.get("ref"))
            if not a:
                raise ValueError(f"article {l.get('ref')} introuvable dans Sage, commande refusée")
            if int(l["qte"]) > a["stock"]:
                alertes.append(f"stock insuffisant pour {l['ref']} ({a['stock']} en stock)")
        num = f"CV-{1001 + len(s['commandes'])}"
        s["commandes"].append({"numero": num, "client": args[1], "statut": "brouillon",
                               "lignes": [{"ref": l["ref"], "qte": int(l["qte"]), "prix": round(float(l["prix"]), 2)} for l in lignes]})
        return f"Commande {num} créée en brouillon." + (" Attention : " + "; ".join(alertes) if alertes else "")
    if args[:1] == ["valider-commande"] and len(args) == 2:
        c = next((c for c in s["commandes"] if c["numero"] == args[1]), None)
        if not c:
            raise ValueError(f"commande {args[1]} introuvable")
        c["statut"] = "validee"
        return f"Commande {args[1]} validée : elle part en préparation."
    raise ValueError("commande sage inconnue (voir : aide)")


def appliquer(etat, argv):
    app = {"gmail": gmail, "sage": sage}.get(argv[0])
    if not app:
        raise ValueError(f"app inconnue « {argv[0]} » (gmail ou sage)")
    return app(etat, argv[1:])


def main(argv):
    if not argv or argv[0] in ("aide", "-h", "--help"):
        print(AIDE)
        return 0
    etat = charger()
    try:
        exigees = etat.get("politique", {}).get("approbation_requise", [])
        if " ".join(argv[:2]) in exigees:
            demandes = etat.setdefault("approbations", [])
            num = f"A-{len(demandes) + 1}"
            demandes.append({"id": num, "appel": argv, "demandee": maintenant(), "statut": "en_attente"})
            sortie = (f"En attente d'approbation (demande {num}) : « {' '.join(argv[:2])} » n'a PAS été exécuté. "
                      f"Un humain doit l'approuver ; tu ne peux pas le faire toi-même.")
            statut = "en_attente"
        else:
            sortie, statut = appliquer(etat, argv), "executee"
        sauver(etat)
        tracer(argv, True, sortie)
        auditer("agent", statut, argv, sortie, demande=num if statut == "en_attente" else None)
        print(sortie)
        return 0
    except (ValueError, KeyError, json.JSONDecodeError) as e:
        tracer(argv, False, str(e))
        auditer("agent", "erreur", argv, str(e))
        print(f"Erreur : {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
