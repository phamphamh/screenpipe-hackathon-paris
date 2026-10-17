# Wrapped : la boucle complète (labs/phamphamh)

**Lancer** : double-clic sur `labs/phamphamh/ouvrir-wrapped.command` (Finder), ou `python3 labs/phamphamh/app/serveur.py` → http://localhost:8787. Rien à installer (Python seul).

| Brique | Fichier | Ce qu'elle fait |
|---|---|---|
| A. Collecteur | `collecteur/collecte.py` | journée screenpipe → moments, écran regardé seulement, tri 80/20 → `donnees/<pseudo>/moments.json` |
| B. Résumé | `resume/resume.py` | moments → tâches répétées (un appel `claude -p`) → `donnees/<pseudo>/resume.json` |
| C. Relecture | `app/relecture.html` | le salarié corrige, retire, masque une app, conteste le score ; « Valider et partager » → `labs/<pseudo>/campagne/resume-valide.json` |
| D. Fusion | `fusion/fusion.py` | résumés validés + onboarding → insights (coûts, top tâches, goulots, IA, inconnues). Regroupement par mots-clés, ou par Claude (`--ia`) |
| E. Wrapped | `app/wrapped.html` | 10 slides, chaque chiffre cliquable vers ses preuves, export PDF, bouton « Créer la skill » (SKILL.md) |
| Onboarding | `app/onboarding.html` | les 5 questions du dirigeant (coût horaire → euros) |

**Deux campagnes** (bascule en haut de l'accueil) :
- **Démo · Maison Corvo** : entreprise fictive, 6 invités dont 1 qui n'a pas validé (`demo/generer.py`). Les relectures faites pendant la démo vont dans `donnees/demo/` (jamais commité) ; `POST /api/reinitialiser-demo` remet tout à zéro.
- **Notre équipe** : chacun lance A puis B sur son Mac, relit sa semaine dans l'app, valide. Le fichier validé est partagé par la sauvegarde automatique ; le Wrapped de l'équipe apparaît dès 3 validations.

**Confidentialité, appliquée dans le code** (`fusion.py`, `serveur.py:nettoyer`) : seuls les résumés validés comptent ; moins de 3 participants → pas de Wrapped ; une app, une catégorie ou un outil d'IA à moins de 3 personnes est fondu dans « Autres » ; aucune capture ni texte d'écran ne part (liste blanche de champs) ; serveur sur 127.0.0.1 seulement.

**Tests** : `cd labs/phamphamh/fusion && python3 -m unittest test_fusion` (10 cas de la section 6 du découpage).

**Le moment démo** : relire la salariée 3, dire « Non : ça demande du jugement » sur la saisie de commandes, valider → dans le Wrapped, la tâche n°1 à automatiser change.

**Avec le site d'adamaass** (`labs/adamaass/wrapped.html`) : `python3 fusion/fusion.py <résumés> --onboarding <fichier> --format adamaass -o insights.json`, puis « Charger un insights.json » dans sa page (testé : la démo Maison Corvo s'y affiche sans erreur). Le serveur le sert aussi : `/api/insights?campagne=demo&format=adamaass`.

**Le rapport de fin d'audit** (17/10) : ouvrir `labs/phamphamh/audit/rapport.html` dans un navigateur (double-clic). Story en 10 chapitres sur la soirée du 16/10 de 3 postes (phamphamh, mickael, 09125o) : apps et horaires seulement, aucun titre de fenêtre ni texte d'écran. Pour l'actualiser avec de nouveaux exports : `python3 labs/phamphamh/audit/construire.py`, puis recopier `donnees/audit/audit.html` ici.
