"""Construit un rapport d'audit par méthode : donnees/audit/audit.json + méthodes → donnees/rapport/<id>.html.

Méthodes : labs/phamphamh/recherche/methodes.json si le fichier existe et se lit (la vraie version, écrite par la
recherche), sinon labs/phamphamh/rapport/methodes-defaut.json. Même schéma :
  [{"id","nom","inspire_de","promesse","ton","chapitres":[{"id","titre","question","viz","metriques":[],"lecture"}],
    "visuels_signature":[],"sources":[]}]
Dans titre, question et lecture, {id_de_metrique} est remplacé par la valeur calculée (catalogue dans rapport.html).

Sortie : donnees/rapport/<id>.html (un par méthode ; chaque fichier embarque toutes les méthodes, ?methode=<id> en change)
et donnees/rapport/index.json. Le dossier donnees/ est ignoré par git.
Usage : python3 labs/phamphamh/rapport/construire.py [--audit chemin/audit.json] [--methodes chemin/methodes.json]
"""
import argparse, json, os, re, sys
from datetime import datetime

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(os.path.join(ICI, "..", "..", ".."))
VIZ_CONNUES = {"chiffre-cle", "barres-empilees", "frise", "reseau", "anneau", "liste-classee", "matrice-2x2", "cascade",
               "arbre", "vsm", "carte-chaleur", "course", "bureau-3d", "plan"}
METRIQUES = {"temps_total", "postes", "postes_frise", "periode", "part_ia", "part_agent", "ecart_ia", "cat_1", "cat_1_part",
             "ecran_median_s", "bascules_heure", "plongee_max", "minutes_ensemble", "meme_sujet_min", "outils",
             "outils_partages", "outils_ia", "taches", "heures_taches", "heures_automatisables", "heures_restantes",
             "heures_an", "jours_an", "gains_rapides", "taches_deja_ia", "taches_sensibles", "tache_1", "tache_1_heures",
             "cible", "cible_gain", "pce", "actions"}


def js(x):
    """JSON sûr dans une balise <script>."""
    return json.dumps(x, ensure_ascii=False).replace("</", "<\\/")


def charger_methodes(chemin_force=None):
    candidats = [chemin_force] if chemin_force else [os.path.join(RACINE, "labs", "phamphamh", "recherche", "methodes.json"),
                                                      os.path.join(ICI, "methodes-defaut.json")]
    for chemin in candidats:
        if not chemin or not os.path.exists(chemin):
            continue
        try:
            m = json.load(open(chemin, encoding="utf-8"))
            if isinstance(m, dict):
                m = m.get("methodes", [])
            m = [x for x in m if isinstance(x, dict) and x.get("id") and x.get("chapitres")]
            if m:
                return m, chemin
            print(f"⚠ {chemin} : aucune méthode exploitable, on passe au suivant", file=sys.stderr)
        except (ValueError, OSError) as e:
            print(f"⚠ {chemin} illisible ({e}), on passe au suivant", file=sys.stderr)
    sys.exit("Aucun fichier de méthodes exploitable.")


def verifier(m):
    """Avertit sur ce que le moteur ne sait pas dessiner ou calculer ; le rapport se construit quand même."""
    for ch in m["chapitres"]:
        if ch.get("viz") not in VIZ_CONNUES:
            print(f"  ⚠ {m['id']}/{ch.get('id')} : viz « {ch.get('viz')} » inconnue, l'écran dira qu'elle n'est pas disponible")
        for champ in ("titre", "question", "lecture"):
            for cle in re.findall(r"\{([a-z0-9_]+)\}", ch.get(champ) or ""):
                if cle not in METRIQUES:
                    print(f"  ⚠ {m['id']}/{ch.get('id')} : métrique {{{cle}}} inconnue dans {champ}, affichée « n.d. »")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--audit", default=os.path.join(RACINE, "donnees", "audit", "audit.json"))
    p.add_argument("--methodes", default=None)
    p.add_argument("--sortie", default=os.path.join(RACINE, "donnees", "rapport"))
    a = p.parse_args()

    if not os.path.exists(a.audit):
        sys.exit(f"Pas de données d'audit : {a.audit}. Lancer d'abord labs/phamphamh/audit/construire.py")
    audit = json.load(open(a.audit, encoding="utf-8"))
    methodes, source = charger_methodes(a.methodes)
    gabarit = open(os.path.join(ICI, "rapport.html"), encoding="utf-8").read()
    os.makedirs(a.sortie, exist_ok=True)

    print(f"méthodes : {os.path.relpath(source, RACINE)} ({len(methodes)})")
    index = []
    for m in methodes:
        verifier(m)
        page = (gabarit.replace("__DATA__", js(audit))
                       .replace("__METHODES__", js(methodes))
                       .replace("__METHODE__", js(m)))
        fichier = os.path.join(a.sortie, f"{m['id']}.html")
        open(fichier, "w", encoding="utf-8").write(page)
        index.append({"id": m["id"], "nom": m.get("nom"), "inspire_de": m.get("inspire_de"), "promesse": m.get("promesse"),
                      "fichier": f"{m['id']}.html", "chapitres": [{"id": c.get("id"), "viz": c.get("viz")} for c in m["chapitres"]]})
        print(f"  {m['id']:<10} {len(m['chapitres'])} chapitres → {os.path.relpath(fichier, RACINE)}")
    json.dump({"genere_le": datetime.now().astimezone().isoformat(timespec="seconds"), "audit": os.path.relpath(a.audit, RACINE),
               "methodes_source": os.path.relpath(source, RACINE), "rapports": index},
              open(os.path.join(a.sortie, "index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"index → {os.path.relpath(os.path.join(a.sortie, 'index.json'), RACINE)}")


if __name__ == "__main__":
    main()
