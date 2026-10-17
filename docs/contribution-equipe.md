# Qui a fait quoi (état au samedi 17/10, 18h15)

Vue pour le rendu : ce que chaque personne a livré, où c'est, et ce qui reste chez elle. Les commits automatiques de sauvegarde ne sont pas comptés.

## phamphamh — la boucle produit (la plus grosse pièce)
- **La boucle A→E** : collecteur dérush 80/20 (`labs/phamphamh/collecteur/`), résumé des tâches en un appel `claude -p` (`resume/`), **l'app locale** (`app/` : accueil, questions au dirigeant, relecture du salarié, Wrapped 10 slides avec preuve derrière chaque chiffre, PDF, bouton « Créer la skill »), fusion brique D (`fusion/fusion.py` : agrégats, moins-de-3, aucune identité), démo fictive Maison Corvo.
- **Le « cabinet IA automatisé »** : parcours 7 étapes (`parcours/`), 5 méthodes d'audit inspirées des grands cabinets, rapports (`rapport/`), pack de workflows testés (`workflows/`), recherche sourcée (`recherche/`). En ligne sur un VPS (accès protégé), déployé par `parcours/deployer-vps.sh`.
- **Le rapport de fin d'audit** (story 10 chapitres) sur nos vraies données : `labs/phamphamh/audit/construire.py`.
- **Les outils d'équipe** : skill `.claude/skills/equipe/`, `scripts/etat.sh` (qui fait quoi), `scripts/pousser.sh` (push sûr), `CLAUDE.md`/`AGENTS.md`.
- **L'exporteur screenpipe en un double-clic** pour chaque membre : `equipe/exporter-mon-screenpipe.command`.
- *Il a besoin de* : les exports screenpipe de chacun (double-clic → envoyer à phamphamh).

## adamaass — le second front + la recherche
- **Un front complet C+E en parallèle** : relecture + Wrapped 10 slides (`labs/adamaass/`), fusion D initiale (`labs/adamaass/fusion.py`), format d'insights documenté.
- **La recherche « cabinets IA »** : 8 étapes d'une mission, prix publiés (audit IA ≈ 1 100 € HT/jour, POC dès 6 000 €) — `analyse-cabinets-ia.md`, pour le pitch.
- **Son résumé validé et partagé** (1 des 2/3) + le signalement du bug « [object Object] » de la relecture.
- *Il a besoin de* : 3 résumés validés pour un vrai Wrapped d'équipe.

## Natsuwy — l'export, la preuve de la skill, et « tester en vrai »
- **L'export filtré de Mickael** (`equipe/mickael.json` + script d'export) : données screenpipe sans le bruit, utilisées dans le rapport d'audit.
- **Le test réel de la skill générée** : donnée à Claude avec une commande piégée (référence inconnue, stock insuffisant, écart de prix) → il s'arrête, applique l'exception prévue (« appel au commercial »), pose ses questions ; commande propre → vérification + brouillon, rien envoyé (journal 1755).
- **« Tester en vrai »** (17/10 soir) : un banc d'essai (`labs/natsuwy/tester-en-vrai/`) qui fait **faire la tâche à Claude dans un faux Gmail + faux Sage** et vérifie ses **actions** : autonomie « agit » → 4/4 (commande validée, client prévenu), arrêt net sur les deux exceptions ; autonomie « prépare » → rien n'est envoyé ni validé, mais la réponse reste dans le compte rendu au lieu d'un brouillon Gmail (il signale à `pack.py` la consigne à corriger). C'est la preuve du bonus « une tâche transformée en skill ».

## tmschrib — le portail client (arrivé ce soir)
- **Portail client « Étude & Pilotage »** : 6 écrans autonomes (HTML/CSS/JS, zéro dépendance) — vue d'ensemble, problèmes détectés, interactions & goulots, temps & outils, business case, pilotage continu ; démo « Maison Verlaine » (52 postes). `labs/tmschrib/dashboard-client/`, `bun server.js` → localhost:4300.
- *Propose* : le brancher sur les sorties du parcours de phamphamh (côté client final).

## 09125o
- **Le brief et le storyboard** de la vidéo (section 23) + les mesures du 16/10 soir (970 captures en 3 h, 59 % de copies exactes, 44 % d'écrans non regardés).
- **Le positionnement produit** : `produit/positionnement.md` (« le FDE en produit »).
- **La pièce « la 2e entrée »** : `labs/09125o/deuxieme-entree/` — même tâche chez plusieurs personnes (démo : 5 tâches communes ; vraie campagne : 0 commune, la fusion ne force rien), régénérable en une commande.
- **Les « dès que… »** : `labs/09125o/declencheurs/` — pour chaque tâche, l'événement qui la lance, la voie technique (connecteur apps → apps, appel API) et l'info à partager aux concernés ; chaque ligne garde sa preuve, chiffres pris de la fusion officielle (démo : 9 tâches → 22 déclencheurs ; campagne équipe : 6 → 13).
- **La voix off 2 min** : `.context/voix-off.md` (à figer avec JA ce soir).
- **La vitrine et le ménage** : README racine, kit de tournage, `docs/skill-exemple/` (le SKILL.md exact du bouton, provenance + test).
- **Les vérifications** : clone neuf des deux apps (200 partout), scan du dépôt avant ouverture, recette de capture corrigée.
- **Les correctifs** : doublon de l'accueil équipe (fusionné), « limites » toujours en texte (PR #3).

## JA (hors dépôt) — la vidéo
- Le tournage : le kit est prêt (`.context/kit-tournage.md`), le gel est prévu ce soir 23h.

## Reste à faire (les verrous du soir)
1. **3e validation** (phamphamh ou Natsuwy) → Wrapped d'équipe réel.
2. **Dépôt public** + accès au VPS s'il doit être montré au jury.
3. **PR #3** à fusionner (limites en texte) et décisions JA (FR/EN, lecteur, parcours dans la vidéo).
