#!/usr/bin/env python3
"""Le moteur du pack de workflows : pour chaque tâche répétée de l'audit, une skill est générée, testée, puis déployée.

Une « thèse de déploiement » fixe le niveau d'autonomie :
  1 suggère · 2 prépare et l'humain valide · 3 agit et notifie · 4 autonome.

Fonctions (importables) :
  generer(tache, these, sortie=None, ia=False)      -> chemin du dossier de skill (SKILL.md, tests.json, workflow.json)
  tester(dossier_skill, entrees=None)               -> rapport {"cas","passes","echecs","couverture_etapes","verdict",...}
  deployer(dossier_skill, cible, forcer=False, ...) -> reçu {"deploye": bool, ...}  (cibles : "local-demo", "equipe")
  pack(audit_taches, these, sortie=None, ia=False)  -> liste triée par gain, prête pour l'interface

CLI :
  python3 pack.py pack labs/phamphamh/demo/resumes --these '{"id":"t","nom":"T","autonomie":2,...}' [-o pack.json] [--ia]
  python3 pack.py generer <resume.json> --tache "<titre>" --these <fichier ou JSON> [--ia]
  python3 pack.py tester <dossier_skill> [--entrees <fichier.json>]
  python3 pack.py deployer <dossier_skill> --cible local-demo|equipe [--forcer]

Sans LLM par défaut (gabarit déterministe). --ia affine le SKILL.md avec `claude -p` si la commande existe ;
la version affinée n'est gardée que si elle passe encore ses propres tests, sinon on garde le gabarit.
Uniquement la bibliothèque standard de Python. N'écrit jamais dans ~/.claude.
"""
import argparse, glob, json, os, re, shutil, socket, subprocess, sys, tempfile, unicodedata
from datetime import datetime, timezone

ICI = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(ICI)
RACINE = os.path.dirname(os.path.dirname(LAB))
sys.path.insert(0, os.path.join(LAB, "fusion"))
try:
    import fusion  # regroupement officiel des tâches entre personnes (même mécanique que la 2e entrée)
except ImportError:  # pragma: no cover
    fusion = None

NIVEAUX = {1: "suggère, ne fait rien lui-même", 2: "prépare, un humain valide", 3: "agit puis notifie", 4: "autonome"}
PART_AUTOMATISABLE = {1: 0.25, 2: 0.5, 3: 0.75, 4: 0.9}  # part du temps rendue, selon l'autonomie
TYPES = {"input": "Entrée", "action": "Action", "output": "Sortie", "decision": "Décision", "check": "Vérification"}
MARQUE_HUMAIN = "VALIDATION HUMAINE"
SEUIL_COUVERTURE = 0.6  # part des mots-clés d'une étape retrouvés dans une instruction (et le même verbe d'action)
MOTS_VIDES = set("a au aux avec d de des du en et l la le les pour par sur un une dans son sa ses leur leurs ou plus sans "
                 "chaque est qui que ce cette ne pas si puis".split())
PAS_ASSEZ = "pas assez de données"
QUI = "l'humain responsable"  # la règle de la thèse (champ « humain ») est citée à chaque point de validation


# ---------- outils texte ----------

def normaliser(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9 ]+", " ", s)


def mots(s):
    return {m[:6] for m in normaliser(s).split() if m not in MOTS_VIDES and len(m) > 2}


def slug(s, n=64):
    s = re.sub(r"[^a-z0-9]+", "-", normaliser(s)).strip("-")[:n].strip("-")
    return s or "workflow"


def yaml_str(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'


def maintenant():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def lire_json(chemin, defaut=None):
    try:
        with open(chemin, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return defaut


def lire_txt(chemin):
    with open(chemin, encoding="utf-8") as f:
        return f.read()


def ecrire_txt(chemin, texte):
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(texte)


def ecrire_json(chemin, donnees):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=1)


def chemin_absolu(chemin):
    """Les chemins venant de l'interface sont relatifs à la racine du dépôt ; en ligne de commande, au dossier courant."""
    if os.path.isabs(chemin):
        return chemin
    depuis_racine = os.path.join(RACINE, chemin)
    return depuis_racine if os.path.exists(depuis_racine) or not os.path.exists(chemin) else os.path.abspath(chemin)


def relatif(chemin):
    try:
        return os.path.relpath(chemin, RACINE)
    except ValueError:
        return chemin


# ---------- thèse ----------

def verifier_these(these):
    if not isinstance(these, dict):
        raise ValueError("thèse invalide : un objet JSON est attendu")
    try:
        a = int(these.get("autonomie"))
    except (TypeError, ValueError):
        raise ValueError("thèse invalide : « autonomie » doit valoir 1, 2, 3 ou 4")
    if a not in NIVEAUX:
        raise ValueError("thèse invalide : « autonomie » doit valoir 1, 2, 3 ou 4")
    return {"id": str(these.get("id") or "these"), "nom": str(these.get("nom") or these.get("id") or "Thèse"),
            "autonomie": a, "humain": str(these.get("humain") or "un responsable désigné"),
            "tests_avant": [str(x) for x in these.get("tests_avant") or []],
            "suivi_apres": [str(x) for x in these.get("suivi_apres") or []]}


def exige_deuxieme_entree(these):
    t = normaliser(" ".join(these.get("tests_avant") or []))
    return any(k in t for k in ("2e entree", "deuxieme entree", "seconde entree", "autre personne"))


# ---------- génération ----------

def etapes_valides(tache):
    return [e for e in (tache or {}).get("etapes") or [] if isinstance(e, dict) and str(e.get("texte") or "").strip()]


def apps_de(tache):
    apps = list((tache or {}).get("apps") or [])
    for e in etapes_valides(tache):
        if e.get("app"):
            apps.append(e["app"])
    for p in (tache or {}).get("preuves") or []:
        if isinstance(p, dict) and p.get("app"):
            apps.append(p["app"])
    return list(dict.fromkeys(str(a).strip() for a in apps if str(a or "").strip()))


def instruction(e, these):
    """Une étape observée → une instruction, selon le niveau d'autonomie. Les décisions deviennent des points humains."""
    a, humain, regle = these["autonomie"], QUI, these["humain"]
    texte = str(e["texte"]).strip().rstrip(".")
    typ = e.get("type") if e.get("type") in TYPES else "action"
    entete = f"[{TYPES[typ]}{' · ' + e['app'] if e.get('app') else ''} · {'observé' if e.get('statut') != 'supposé' else 'supposé, à confirmer'}]"
    if typ == "input":
        corps = f"{texte}. Lis et relève les informations utiles, ne modifie rien à la source."
    elif typ == "check":
        corps = f"{texte}. Si la vérification échoue ou si un élément manque, arrête-toi et signale-le à {humain}."
    elif typ == "decision":
        if a <= 3:
            corps = (f"{MARQUE_HUMAIN} ({regle}) — décision : {texte}. Présente les éléments qui comptent pour décider, "
                     "ne tranche pas, attends la réponse avant de continuer.")
        else:
            corps = f"Décide selon la règle observée : {texte}. Note la décision et sa raison ; au moindre doute, demande à {humain}."
    elif typ == "output":
        if a == 1:
            corps = f"{texte}. Rédige seulement une proposition, que tu présentes à {humain} : tu ne l'envoies jamais toi-même."
        elif a == 2:
            corps = f"{MARQUE_HUMAIN} ({regle}) avant : {texte}. Montre exactement ce qui va partir, attends un accord explicite, puis exécute."
        elif a == 3:
            corps = f"{texte}. Exécute, puis notifie {humain} avec un résumé de ce qui a été fait."
        else:
            corps = f"{texte}. Exécute et garde une trace dans le journal du workflow."
    else:  # action
        if a == 1:
            corps = f"{texte}. Décris ce qu'il faudrait faire, sans l'exécuter."
        elif a == 2:
            corps = f"{texte}. Prépare-le en brouillon : rien n'est enregistré ni envoyé avant la validation humaine."
        else:
            corps = f"{texte}. Exécute-le."
    return f"{entete} {corps}"


def droits(these):
    a, h = these["autonomie"], QUI
    return {
        1: f"Tu **suggères** seulement. Tu lis, tu proposes ce qu'il faudrait faire, et c'est {h} qui agit. Aucune écriture dans les apps, aucun envoi.",
        2: f"Tu **prépares** tout (brouillons, saisies non enregistrées, réponses rédigées) et {h} valide avant toute écriture définitive ou tout envoi.",
        3: f"Tu **agis**, puis tu notifies {h}. Les décisions restent humaines : à chaque {MARQUE_HUMAIN}, tu t'arrêtes et tu attends.",
        4: f"Tu es **autonome** sur ce workflow. Tu gardes un journal de chaque exécution et de chaque décision ; {h} le relit après coup.",
    }[a]


def ne_jamais(these):
    a, h = these["autonomie"], QUI
    l = []
    if a <= 2:
        l.append(f"Envoyer quoi que ce soit à l'extérieur (mail, message, commande, paiement) sans l'accord explicite de {h}.")
    if a <= 3:
        l.append(f"Trancher une décision marquée {MARQUE_HUMAIN} à la place de {h}.")
    l += ["Inventer une donnée absente de la source (référence, prix, quantité, date, destinataire) : si elle manque, arrête-toi.",
          "Supprimer ou écraser une donnée existante dans une app.",
          "Utiliser une app ou un outil qui n'est pas dans la liste ci-dessus, ou y copier des données de l'entreprise.",
          "Continuer après une exception non prévue : tu t'arrêtes et tu demandes."]
    return l


def rendre_skill(tache, these):
    titre = str(tache.get("titre") or "").strip() or "Workflow sans titre"
    etapes = etapes_valides(tache)
    apps = apps_de(tache)
    a = these["autonomie"]
    freq = float(tache.get("frequence_par_semaine") or 0)
    duree = float(tache.get("duree_moyenne_min") or 0)
    entree = next((e for e in etapes if e.get("type") == "input"), etapes[0])
    declencheur = f"{str(entree['texte']).strip().rstrip('.')}{' (' + entree['app'] + ')' if entree.get('app') else ''}"
    nom = slug(titre)
    description = (f"{titre}{' (' + ', '.join(apps) + ')' if apps else ''}. À utiliser quand : {declencheur[0].lower() + declencheur[1:]}. "
                   f"Niveau d'autonomie {a} sur 4 : {NIVEAUX[a]} ({these['humain']}).")[:1024]
    exceptions = [str(x).strip() for x in tache.get("exceptions") or [] if str(x or "").strip()]
    goulots = [g.get("detail") if isinstance(g, dict) else str(g) for g in tache.get("goulots") or []]
    supposees = [(i + 1, e) for i, e in enumerate(etapes) if e.get("statut") == "supposé"]

    md = [f"---\nname: {nom}\ndescription: {yaml_str(description)}\n---\n",
          f"# {titre}\n",
          f"Workflow généré à partir de l'audit : observé environ {freq:g} fois par semaine, {duree:g} min à chaque fois "
          f"(≈ {freq * duree / 60:.1f} h par semaine). Thèse de déploiement : **{these['nom']}**, "
          f"niveau d'autonomie **{a} sur 4** ({NIVEAUX[a]}).\n",
          "## Déclencheur\n", f"Utilise cette skill quand : {declencheur}.\n",
          "## Outils et apps\n", "\n".join(f"- {x}" for x in apps) or "- Aucune app identifiée pendant l'audit : demande laquelle utiliser.", "",
          "## Ce que tu as le droit de faire\n", droits(these) + "\n",
          "## Étapes\n", "\n".join(f"{i + 1}. {instruction(e, these)}" for i, e in enumerate(etapes)), "",
          "## Exceptions\n",
          "\n".join(f"- Si : {x}. Arrête le workflow, ne devine pas, et transmets à {QUI} avec ce que tu as déjà préparé." for x in exceptions)
          + ("\n" if exceptions else "") + "- Tout cas qui n'est pas listé ici : arrête-toi et demande.\n",
          "## Ce qui ralentit aujourd'hui\n",
          "\n".join(f"- {g}" for g in goulots if g) or "- Rien de repéré pendant l'audit.", "",
          f"## Garde-fous de la thèse « {these['nom']} »\n",
          f"- Humain dans la boucle : {these['humain']}.",
          *[f"- Testé avant déploiement : {x}." for x in these["tests_avant"]],
          *[f"- Suivi après déploiement : {x}." for x in these["suivi_apres"]], "",
          "## Ne jamais faire\n", "\n".join(f"- {x}" for x in ne_jamais(these)), ""]
    if supposees:
        md += ["## À confirmer avant d'automatiser\n",
               "\n".join(f"- Étape {i} « {e['texte']} » : supposée, pas observée. Fais-la valider par l'équipe avant de l'exécuter seul." for i, e in supposees), ""]
    return nom, "\n".join(md).rstrip() + "\n"


def cas_de_test(tache, these, nom):
    etapes = etapes_valides(tache)
    cas = [{"nom": "référence : les étapes d'origine", "source": "reference", "etapes": etapes,
            "apps": apps_de({"apps": tache.get("apps"), "etapes": etapes}), "exceptions": list(tache.get("exceptions") or [])}]
    preuves = [p for p in tache.get("preuves") or [] if isinstance(p, dict)]
    if preuves:
        cas.append({"nom": f"preuves horodatées ({len(preuves)})", "source": "observee", "preuves": preuves})
    for x in tache.get("exceptions") or []:
        cas.append({"nom": f"exception : {x}", "source": "reference", "exceptions": [x]})
    for e in etapes:
        if e.get("type") == "decision":
            cas.append({"nom": f"décision : {e['texte']}", "source": "reference", "etapes": [e]})
    return {"skill": nom, "titre": tache.get("titre"), "autonomie": these["autonomie"], "cas": cas}


CONSIGNE_IA = """Tu améliores une skill Claude Code (fichier SKILL.md) générée automatiquement à partir d'un audit de poste de travail.
Rends-la plus claire et plus utile pour un agent qui l'exécute, en français, SANS changer ce qui suit :
- le frontmatter YAML : garde exactement la même ligne « name: » ; tu peux améliorer la description (une ligne, < 1024 caractères) ;
- les titres de sections (« ## Étapes », « ## Exceptions », « ## Outils et apps », etc.) ;
- dans « ## Étapes » : une ligne numérotée par étape, dans le même ordre, sans en retirer ni en fusionner ; garde le texte d'origine de chaque étape ;
- chaque mention « VALIDATION HUMAINE » reste là où elle est ;
- chaque exception reste listée dans « ## Exceptions » avec son texte d'origine ; chaque app reste nommée ;
- n'ajoute aucune donnée inventée (nom de client, montant, référence).
Réponds UNIQUEMENT avec le contenu complet du nouveau SKILL.md, sans bloc de code autour.

Le SKILL.md actuel :
"""


def affiner_ia(dossier, timeout=240):
    """Affine le SKILL.md avec `claude -p`. Ne garde la version affinée que si elle passe ses propres tests."""
    if not shutil.which("claude"):
        return {"demande": True, "utilise": False, "raison": "commande claude introuvable : gabarit déterministe gardé"}
    chemin = os.path.join(dossier, "SKILL.md")
    gabarit = lire_txt(chemin)
    try:
        r = subprocess.run(["claude", "-p", "--no-session-persistence"], input=CONSIGNE_IA + gabarit,
                           capture_output=True, text=True, timeout=timeout, cwd=tempfile.gettempdir())
    except (OSError, subprocess.TimeoutExpired) as ex:
        return {"demande": True, "utilise": False, "raison": f"claude n'a pas répondu ({type(ex).__name__}) : gabarit gardé"}
    sortie = re.sub(r"^```(?:markdown|md)?\s*\n|\n```\s*$", "", (r.stdout or "").strip())
    nom = re.search(r"^name:\s*(.+)$", gabarit, re.M).group(1).strip()
    if r.returncode or not sortie.startswith("---") or not re.search(rf"^name:\s*{re.escape(nom)}\s*$", sortie, re.M):
        return {"demande": True, "utilise": False, "raison": "réponse de claude sans frontmatter valide : gabarit gardé"}
    with tempfile.TemporaryDirectory() as tmp:  # on rejoue les tests de référence sur la version affinée avant de l'adopter
        for f in ("tests.json", "workflow.json"):
            shutil.copy(os.path.join(dossier, f), tmp)
        ecrire_txt(os.path.join(tmp, "SKILL.md"), sortie + "\n")
        rap = tester(tmp, [], ecrire=False, exiger_observe=False)
    if rap["echecs"]:
        return {"demande": True, "utilise": False,
                "raison": f"la version affinée casse {len(rap['echecs'])} test(s) (ex. {rap['echecs'][0]['raison']}) : gabarit gardé"}
    ecrire_txt(os.path.join(dossier, "SKILL.gabarit.md"), gabarit)
    ecrire_txt(chemin, sortie + "\n")
    return {"demande": True, "utilise": True, "raison": "affinée par claude -p, tests de référence repassés (le gabarit est dans SKILL.gabarit.md)"}


def generer(tache, these, sortie=None, ia=False):
    """Tâche de l'audit + thèse → dossier de skill Claude Code. Renvoie le chemin du dossier.
    sortie : dossier parent (défaut : donnees/workflows/<id de la thèse>/, ignoré par git)."""
    these = verifier_these(these)
    if not isinstance(tache, dict) or not etapes_valides(tache):
        raise ValueError(f"{PAS_ASSEZ} : la tâche n'a aucune étape observée, impossible d'en faire un workflow")
    nom, md = rendre_skill(tache, these)
    dossier = os.path.join(os.path.abspath(sortie) if sortie else os.path.join(RACINE, "donnees", "workflows", slug(these["id"])), nom)
    os.makedirs(dossier, exist_ok=True)
    for vieux in ("SKILL.gabarit.md", "rapport-tests.json"):  # une régénération invalide l'ancien rapport
        if os.path.exists(os.path.join(dossier, vieux)):
            os.remove(os.path.join(dossier, vieux))
    ecrire_txt(os.path.join(dossier, "SKILL.md"), md)
    ecrire_json(os.path.join(dossier, "tests.json"), cas_de_test(tache, these, nom))
    etapes = etapes_valides(tache)
    meta = {"nom": nom, "titre": tache.get("titre"), "these": these, "autonomie": these["autonomie"],
            "source": {"frequence_par_semaine": tache.get("frequence_par_semaine"), "duree_moyenne_min": tache.get("duree_moyenne_min"),
                       "apps": apps_de(tache), "nb_etapes": len(etapes), "personne": tache.get("_personne") or tache.get("personne")},
            "etapes_supposees": [e["texte"] for e in etapes if e.get("statut") == "supposé"],
            "points_humains": [e["texte"] for e in etapes if e.get("type") == "decision"] if these["autonomie"] <= 3 else [],
            "genere_le": maintenant(), "ia": {"demande": False, "utilise": False}}
    ecrire_json(os.path.join(dossier, "workflow.json"), meta)
    if ia:
        meta["ia"] = affiner_ia(dossier)
        ecrire_json(os.path.join(dossier, "workflow.json"), meta)
    return dossier


# ---------- test à sec ----------

def sections(md):
    """Découpe le SKILL.md en sections « ## » (clé normalisée) → lignes."""
    out, cle = {"": []}, ""
    for ligne in md.splitlines():
        if ligne.startswith("## "):
            cle = normaliser(ligne[3:]).strip(); out[cle] = []
        else:
            out[cle].append(ligne)
    return out


def section(secs, mot):
    for k, v in secs.items():
        if mot in k:
            return v
    return None


def lignes_etapes(md):
    """Les instructions numérotées de la section Étapes (avec leurs lignes de suite)."""
    secs = sections(md)
    lignes = section(secs, "etape")
    if lignes is None:
        lignes = md.splitlines()
    instr = []
    for l in lignes:
        if re.match(r"^\s*\d+[.)]\s", l):
            instr.append(l.strip())
        elif instr and l.strip() and not l.startswith("#"):
            instr[-1] += " " + l.strip()
    return instr


def verbe(texte):
    """Premier mot significatif (le verbe d'action, en général), sur 5 lettres : « saisir » ≈ « saisie »."""
    for m in normaliser(texte).split():
        if m not in MOTS_VIDES and len(m) > 2:
            return m[:5]
    return ""


def meilleure(texte, candidats, meme_verbe=True):
    """Instruction la plus proche d'un texte observé. Sans le même verbe, le score est nul :
    « Archiver le bon de commande » n'est pas couvert par « Ouvrir le bon de commande »."""
    m, v = mots(texte), verbe(texte)
    if not m:
        return None, 0.0
    best, score = None, 0.0
    for c in candidats:
        if meme_verbe and v and v not in {x[:5] for x in normaliser(c).split()}:
            continue
        s = len(m & mots(c)) / len(m)
        if s > score:
            best, score = c, s
    return best, score


def rejouer(cas, md, autonomie):
    """Rejoue UN cas sur le SKILL.md. Renvoie (échecs, avertissements, étapes observées vues, étapes observées couvertes)."""
    echecs, avert, vues, couvertes = [], [], 0, 0
    instr = lignes_etapes(md)
    doc = normaliser(md)
    etapes = [e for e in cas.get("etapes") or [] if isinstance(e, dict) and str(e.get("texte") or "").strip()]
    for e in etapes:
        ligne, score = meilleure(e["texte"], instr)
        couverte = ligne is not None and score >= SEUIL_COUVERTURE
        observee = e.get("statut") != "supposé"
        if observee:
            vues += 1
        if not couverte:
            if observee:
                echecs.append(f"étape observée non couverte par une instruction : « {e['texte']} »")
            else:
                avert.append(f"étape supposée non couverte : « {e['texte']} »")
            continue
        if observee:
            couvertes += 1
        if e.get("type") == "decision" and autonomie <= 3 and MARQUE_HUMAIN not in ligne:
            echecs.append(f"décision sans point de validation humaine (autonomie {autonomie}) : « {e['texte']} »")
    apps = list(cas.get("apps") or []) + [e.get("app") for e in etapes] + [p.get("app") for p in cas.get("preuves") or [] if isinstance(p, dict)]
    for app in dict.fromkeys(a for a in apps if a):
        cle = " ".join(normaliser(app).split())
        if not cle or not re.search(rf"(?<![a-z0-9]){re.escape(cle)}(?![a-z0-9])", " ".join(doc.split())):  # mot entier : « Sage » ≠ « message »
            echecs.append(f"app « {app} » utilisée mais absente de la skill")
    for p in cas.get("preuves") or []:
        try:
            if datetime.fromisoformat(p["fin"]) < datetime.fromisoformat(p["debut"]):
                echecs.append(f"preuve incohérente : fin avant début ({p.get('debut')})")
        except (KeyError, TypeError, ValueError):
            echecs.append("preuve sans horodatage lisible")
    exc = section(sections(md), "exception") or []
    for x in cas.get("exceptions") or []:
        ligne, score = meilleure(x, [l for l in exc if l.strip().startswith("-")], meme_verbe=False)
        if ligne is None or score < SEUIL_COUVERTURE:
            echecs.append(f"exception connue non traitée : « {x} »")
    return echecs, avert, vues, couvertes


def tester(dossier_skill, entrees=None, ecrire=True, exiger_observe=True):
    """Rejoue la skill « à sec » : ses cas de référence (tests.json) + les entrées observées
    (la même tâche chez une autre personne, ou des preuves horodatées).
    entrees : liste de cas ; chaque cas est une tâche au format du résumé ({"etapes","apps","exceptions","preuves"}),
              éventuellement avec "nom". None → seulement tests.json.
    Écrit rapport-tests.json dans le dossier (lu par deployer)."""
    dossier = chemin_absolu(dossier_skill)
    md = lire_txt(os.path.join(dossier, "SKILL.md"))
    meta = lire_json(os.path.join(dossier, "workflow.json"), {}) or {}
    tests = lire_json(os.path.join(dossier, "tests.json"), {}) or {}
    autonomie = int(meta.get("autonomie") or tests.get("autonomie") or 2)
    these = meta.get("these") or {}

    cas = list(tests.get("cas") or [])
    for i, x in enumerate(entrees or []):
        if not isinstance(x, dict) or not (x.get("etapes") or x.get("preuves") or x.get("exceptions") or x.get("apps")):
            continue  # entrée vide : rien à rejouer
        nom = x.get("nom") or (f"2e entrée : {x.get('titre')}" if x.get("titre") else f"entrée observée {i + 1}")
        cas.append({**x, "nom": nom, "source": "observee"})

    echecs, avert, vues, couvertes, passes = [], [], 0, 0, 0
    for c in cas:
        e, a, v, cv = rejouer(c, md, autonomie)
        vues += v; couvertes += cv
        echecs += [{"cas": c["nom"], "raison": r} for r in e]
        avert += [{"cas": c["nom"], "raison": r} for r in a]
        passes += 0 if e else 1

    observes = [c for c in cas if c.get("source") == "observee"]
    deuxieme = any(c.get("etapes") for c in observes)
    message = ""
    if exiger_observe and not observes:
        message = PAS_ASSEZ
        echecs.append({"cas": "-", "raison": f"{PAS_ASSEZ} : aucune entrée observée (2e entrée ou preuves horodatées) à rejouer"})
    elif exiger_observe and exige_deuxieme_entree(these) and not deuxieme:
        echecs.append({"cas": "-", "raison": "la thèse exige de rejouer sur une 2e entrée : aucune autre personne ne fait cette tâche dans l'audit"})
    rapport = {"skill": meta.get("nom") or tests.get("skill"), "autonomie": autonomie, "cas": len(cas), "passes": passes,
               "echecs": echecs, "avertissements": avert,
               "couverture_etapes": round(couvertes / vues, 3) if vues else 0.0,
               "deuxieme_entree": deuxieme,
               "verdict": "pret" if cas and not echecs else "a_revoir",
               "message": message or ("prêt à déployer" if cas and not echecs else f"{len(echecs)} point(s) à revoir"),
               "teste_le": maintenant()}
    if ecrire:
        ecrire_json(os.path.join(dossier, "rapport-tests.json"), rapport)
    return rapport


# ---------- déploiement ----------

def poste_courant():
    try:
        p = subprocess.run(["sh", os.path.join(RACINE, "scripts", "pseudo.sh")], capture_output=True, text=True, cwd=RACINE, timeout=10).stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        p = ""
    return slug(p or socket.gethostname().split(".")[0] or "poste", 40)


def deployer(dossier_skill, cible, forcer=False, poste=None, racine=None):
    """Copie la skill vers une cible et écrit un reçu deploiement.json.
    cible "local-demo" → donnees/deploiement/<poste>/skills/<nom>/ (ignoré par git, jamais ~/.claude)
    cible "equipe"     → labs/phamphamh/workflows/deployes/<nom>/ (partagé via le dépôt)
    Refuse si le dernier rapport de tests n'est pas « pret », sauf forcer=True."""
    racine = racine or RACINE
    dossier = chemin_absolu(dossier_skill)
    if not os.path.isfile(os.path.join(dossier, "SKILL.md")):
        return {"deploye": False, "raison": f"pas de SKILL.md dans {relatif(dossier)}"}
    meta = lire_json(os.path.join(dossier, "workflow.json"), {}) or {}
    rapport = lire_json(os.path.join(dossier, "rapport-tests.json"))
    nom = meta.get("nom") or os.path.basename(os.path.normpath(dossier))
    if cible == "local-demo":
        dest = os.path.join(racine, "donnees", "deploiement", slug(poste or poste_courant(), 40), "skills", nom)
    elif cible == "equipe":
        dest = os.path.join(racine, "labs", "phamphamh", "workflows", "deployes", nom)
    else:
        return {"deploye": False, "raison": f"cible inconnue « {cible} » (attendu : local-demo ou equipe)"}
    if os.path.realpath(dest).startswith(os.path.realpath(os.path.expanduser("~/.claude")) + os.sep):
        return {"deploye": False, "raison": "refus : on n'écrit jamais dans ~/.claude"}
    verdict = (rapport or {}).get("verdict")
    if verdict != "pret" and not forcer:
        raison = "skill jamais testée" if rapport is None else f"tests « {verdict} » : {'; '.join(e['raison'] for e in rapport.get('echecs', [])[:3])}"
        return {"deploye": False, "raison": f"déploiement refusé, {raison}. Corriger puis retester, ou forcer.", "cible": cible}
    if os.path.realpath(dest) != os.path.realpath(dossier):
        if os.path.isdir(dest):
            shutil.rmtree(dest)
        shutil.copytree(dossier, dest, ignore=shutil.ignore_patterns("deploiement.json", "__pycache__"))
    these = meta.get("these") or {}
    recu = {"deploye": True, "quand": maintenant(), "cible": cible, "chemin": relatif(dest), "skill": nom, "titre": meta.get("titre"),
            "these": {"id": these.get("id"), "nom": these.get("nom")}, "autonomie": meta.get("autonomie"),
            "humain": these.get("humain"), "suivi_apres": these.get("suivi_apres") or [],
            "tests": {k: (rapport or {}).get(k) for k in ("verdict", "cas", "passes", "couverture_etapes", "teste_le")},
            "force": bool(forcer and verdict != "pret")}
    if cible == "local-demo":
        recu["poste"] = os.path.basename(os.path.dirname(os.path.dirname(dest)))
    ecrire_json(os.path.join(dest, "deploiement.json"), recu)
    return recu


# ---------- le pack ----------

def aplatir(audit_taches):
    """Accepte une liste de tâches, un résumé ({"taches": …}) ou une liste de résumés. Seuls les résumés validés comptent."""
    if isinstance(audit_taches, dict):
        audit_taches = [audit_taches]
    taches = []
    for i, x in enumerate(audit_taches or []):
        if isinstance(x, dict) and "taches" in x:
            if x.get("valide_par_la_personne") is not True:
                continue  # règle du produit : un résumé non validé n'est jamais utilisé
            for t in x.get("taches") or []:
                if isinstance(t, dict) and t.get("titre"):
                    taches.append({**t, "_personne": x.get("personne") or f"personne-{i + 1}"})
        elif isinstance(x, dict) and x.get("titre"):
            taches.append({**x, "_personne": x.get("_personne") or x.get("personne") or "moi"})
    return taches


def grouper(taches):
    """Même tâche chez plusieurs personnes → un groupe (regroupement officiel de la fusion)."""
    if fusion is None or len({t["_personne"] for t in taches}) < 2:
        return [[t] for t in taches]
    g = fusion.regrouper_heuristique(taches, [], [])
    return [[taches[i] for i in grp["membres"]] for grp in g["taches"]]


def part_automatisable(tache, autonomie):
    etapes = etapes_valides(tache)
    part = PART_AUTOMATISABLE[autonomie]
    if autonomie <= 3 and etapes:  # les décisions restent humaines
        part *= 1 - 0.5 * sum(e.get("type") == "decision" for e in etapes) / len(etapes)
    return part


def pack(audit_taches, these, sortie=None, ia=False):
    """Génère + teste une skill par tâche répétée, triées par gain estimé. Renvoie la liste pour l'interface."""
    these = verifier_these(these)
    sortie = os.path.abspath(sortie) if sortie else os.path.join(RACINE, "donnees", "workflows", slug(these["id"]))
    lignes, vus = [], set()
    for membres in grouper(aplatir(audit_taches)):
        ref = max(membres, key=lambda m: (m.get("confiance") or 0, len(etapes_valides(m))))
        heures = sum(float(m.get("frequence_par_semaine") or 0) * float(m.get("duree_moyenne_min") or 0) for m in membres) / 60
        base = {"titre": ref.get("titre"), "heures_semaine": round(heures, 2), "autonomie": these["autonomie"],
                "personnes": len({m["_personne"] for m in membres}), "libelles": list(dict.fromkeys(m.get("titre") for m in membres))}
        if not etapes_valides(ref):
            lignes.append({**base, "id": slug(ref.get("titre") or "tache"), "gain_estime_h": 0.0, "verdict": "a_revoir",
                           "couverture": 0.0, "chemin_skill": None, "echecs": [{"cas": "-", "raison": f"{PAS_ASSEZ} : aucune étape"}]})
            continue
        sous = sortie
        nom = slug(ref["titre"])
        if nom in vus:  # deux tâches au même titre : dossiers distincts
            sous = os.path.join(sortie, f"{len(vus)}")
        vus.add(nom)
        dossier = generer(ref, these, sortie=sous, ia=ia)
        autres = [{"nom": f"2e entrée : {m['_personne']} — {m.get('titre')}", "etapes": m.get("etapes"), "apps": m.get("apps"),
                   "exceptions": m.get("exceptions"), "preuves": m.get("preuves")} for m in membres if m is not ref]
        rap = tester(dossier, autres)
        lignes.append({**base, "id": os.path.basename(dossier),
                       "gain_estime_h": round(heures * part_automatisable(ref, these["autonomie"]), 2),
                       "verdict": rap["verdict"], "couverture": rap["couverture_etapes"], "deuxieme_entree": rap["deuxieme_entree"],
                       "chemin_skill": relatif(dossier), "echecs": rap["echecs"],
                       "ia": (lire_json(os.path.join(dossier, "workflow.json"), {}) or {}).get("ia")})
    lignes.sort(key=lambda l: l["gain_estime_h"], reverse=True)
    return lignes


# ---------- CLI ----------

def charger_these(s):
    if os.path.exists(s):
        return lire_json(s)
    return json.loads(s)


def charger_resumes(chemins):
    out = []
    for c in chemins:
        for f in sorted(glob.glob(os.path.join(c, "*.json"))) if os.path.isdir(c) else [c]:
            d = lire_json(f)
            if d is not None:
                out.append(d)
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description="Pack de workflows : générer, tester, déployer des skills à partir de l'audit.")
    sp = p.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("pack"); a.add_argument("resumes", nargs="+"); a.add_argument("--these", required=True)
    a.add_argument("--sortie"); a.add_argument("-o", "--json"); a.add_argument("--ia", action="store_true")
    g = sp.add_parser("generer"); g.add_argument("resume"); g.add_argument("--tache", required=True)
    g.add_argument("--these", required=True); g.add_argument("--sortie"); g.add_argument("--ia", action="store_true")
    t = sp.add_parser("tester"); t.add_argument("dossier"); t.add_argument("--entrees")
    d = sp.add_parser("deployer"); d.add_argument("dossier"); d.add_argument("--cible", required=True, choices=["local-demo", "equipe"])
    d.add_argument("--forcer", action="store_true"); d.add_argument("--poste")
    args = p.parse_args(argv)

    if args.cmd == "pack":
        res = pack(charger_resumes(args.resumes), charger_these(args.these), sortie=args.sortie, ia=args.ia)
        if args.json:
            ecrire_json(os.path.abspath(args.json), res)
        for l in res:
            print(f"{l['gain_estime_h']:6.2f} h/sem gagnées · {l['verdict']:8} · couverture {l['couverture']:.0%} · "
                  f"{l['personnes']} pers. · {l['titre']}")
            for e in l["echecs"][:3]:
                print(f"         ↳ {e['cas']} : {e['raison']}")
    elif args.cmd == "generer":
        taches = aplatir(charger_resumes([args.resume])) or aplatir(lire_json(args.resume, {}).get("taches", []))
        cible = [x for x in taches if normaliser(x["titre"]).strip() == normaliser(args.tache).strip()]
        if not cible:
            sys.exit(f"tâche introuvable : {args.tache}")
        print(generer(cible[0], charger_these(args.these), sortie=args.sortie, ia=args.ia))
    elif args.cmd == "tester":
        ent = lire_json(args.entrees) if args.entrees else None
        print(json.dumps(tester(args.dossier, ent), ensure_ascii=False, indent=1))
    elif args.cmd == "deployer":
        r = deployer(args.dossier, args.cible, forcer=args.forcer, poste=args.poste)
        print(json.dumps(r, ensure_ascii=False, indent=1))
        if not r.get("deploye"):
            sys.exit(1)


if __name__ == "__main__":
    main()
