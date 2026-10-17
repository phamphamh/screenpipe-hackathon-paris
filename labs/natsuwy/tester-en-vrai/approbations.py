#!/usr/bin/env python3
"""Côté humain du garde-fou : décider des actions que l'agent a demandées, et relire le journal d'audit.

  python3 approbations.py [-d dossier] liste
  python3 approbations.py [-d dossier] approuver <A-1> --par "Marie"
  python3 approbations.py [-d dossier] refuser   <A-1> --par "Marie" [--motif "prix non convenu"]
  python3 approbations.py [-d dossier] journal [--tout] [-o journal.md]

Ce fichier n'est JAMAIS copié dans le dossier de l'agent (tester_en_vrai.py ne copie que bac_a_sable.py) : l'agent peut
demander, pas se répondre à lui-même. Approuver exécute l'action telle que l'agent l'avait demandée, rien d'autre.
-d = le dossier qui contient etat.json et audit.jsonl (défaut : ici). Bibliothèque standard seulement.
"""
import argparse, json, os, sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import bac_a_sable as bac  # noqa: E402


def demande(etat, num, statut="en_attente"):
    d = next((d for d in etat.get("approbations", []) if d["id"] == num), None)
    if not d:
        raise ValueError(f"demande {num} introuvable")
    if d["statut"] != statut:
        raise ValueError(f"demande {num} déjà tranchée : {d['statut']}" + (f" par {d['par']}" if d.get("par") else ""))
    return d


def decider(etat, num, par, approuver, motif=None):
    d = demande(etat, num)
    d["quand"], d["par"] = bac.maintenant(), par
    if motif:
        d["motif"] = motif
    if not approuver:
        d["statut"] = "refusee"
        sortie = "Refusée : rien n'a été exécuté."
    else:
        try:
            sortie = bac.appliquer(etat, d["appel"])
            d["statut"] = "approuvee"
        except (ValueError, KeyError, json.JSONDecodeError) as e:
            d["statut"], sortie = "echec", f"Approuvée mais l'exécution a échoué : {e}"
    d["sortie"] = sortie
    bac.sauver(etat)
    bac.tracer(d["appel"], d["statut"] != "echec", sortie)
    bac.auditer("humain", {"approuvee": "approuvee", "refusee": "refusee", "echec": "echec"}[d["statut"]],
                d["appel"], sortie, demande=num, par=par, motif=motif)
    return d


def lire_audit():
    if not os.path.exists(bac.AUDIT):
        return []
    with open(bac.AUDIT, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


LIBELLES = {"executee": "exécuté", "en_attente": "mis en attente", "erreur": "refusé par l'app",
            "approuvee": "approuvé", "refusee": "refusé", "echec": "approuvé mais échoué"}


def journal(tout=False):
    evts = lire_audit()
    if not tout:
        evts = [e for e in evts if e["acteur"] == "humain" or e["action"] in bac.EFFETS]
    agent = [e for e in evts if e["acteur"] == "agent" and e["action"] in bac.EFFETS]
    o = ["# Journal d'audit", "",
         "Qui a fait quoi, dans l'ordre. Écrit par le bac à sable à chaque appel ; on n'y modifie rien.", ""]
    o += ["| Heure | Qui | Action | Résultat |", "|---|---|---|---|"]
    for e in evts:
        qui = "agent" if e["acteur"] == "agent" else f"**{e.get('par', '?')}** (humain)"
        res = LIBELLES.get(e["statut"], e["statut"])
        if e.get("demande"):
            res += f" · demande {e['demande']}"
        if e.get("motif"):
            res += f" · motif : {e['motif']}"
        o.append(f"| {e['quand'][11:]} | {qui} | `{' '.join(e['appel'][:3])}` | {res} |")
    if not evts:
        o.append("| | | _(rien)_ | |")
    attente = [e for e in agent if e["statut"] == "en_attente"]
    tranchees = {e["demande"]: e for e in evts if e["acteur"] == "humain" and e.get("demande")}
    restent = [e["demande"] for e in attente if e["demande"] not in tranchees]
    o += ["", "**Bilan** : "
          f"{sum(e['statut'] == 'executee' for e in agent)} action(s) de l'agent exécutée(s) directement, "
          f"{len(attente)} mise(s) en attente → "
          f"{sum(t['statut'] == 'approuvee' for t in tranchees.values())} approuvée(s), "
          f"{sum(t['statut'] == 'refusee' for t in tranchees.values())} refusée(s), "
          f"{len(restent)} encore en attente" + (f" ({', '.join(restent)})." if restent else ".")]
    return "\n".join(o) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("-d", "--dossier", default=ICI)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("liste")
    for nom in ("approuver", "refuser"):
        p = sub.add_parser(nom)
        p.add_argument("demande")
        p.add_argument("--par", required=True, help="qui décide (nom d'une vraie personne)")
        if nom == "refuser":
            p.add_argument("--motif")
    j = sub.add_parser("journal")
    j.add_argument("--tout", action="store_true", help="inclure aussi les simples lectures")
    j.add_argument("-o", "--sortie")
    a = ap.parse_args()

    bac.utiliser_dossier(os.path.abspath(a.dossier))
    try:
        etat = bac.charger()
        if a.cmd == "liste":
            en_attente = [d for d in etat.get("approbations", []) if d["statut"] == "en_attente"]
            for d in en_attente:
                print(f"[{d['id']}] {d['demandee'][11:]} · {' '.join(d['appel'])}")
            print("" if en_attente else "Rien en attente.")
        elif a.cmd == "journal":
            texte = journal(a.tout)
            if a.sortie:
                with open(a.sortie, "w", encoding="utf-8") as f:
                    f.write(texte)
            print(texte)
        else:
            if not a.par.strip():
                raise ValueError("--par doit nommer la personne qui décide")
            d = decider(etat, a.demande, a.par.strip(), a.cmd == "approuver", getattr(a, "motif", None))
            print(f"{d['id']} {d['statut']} par {d['par']} : {d['sortie']}")
        return 0
    except (ValueError, OSError) as e:
        print(f"Erreur : {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
