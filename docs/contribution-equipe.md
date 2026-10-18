# Qui a fait quoi (état au dimanche 18 octobre, 14h55)

Vue pour le rendu : la répartition du travail, ce que chaque personne a livré, où c'est, et ce qui reste ouvert. Le détail par personne suit la répartition.

## La répartition du travail sur le rendu final

Principe : on répartit **au poids dans le rendu final** (ce que le jury voit et lit), pas au nombre de commits ni de lignes de code. Le test : si on retire la personne, qu'est-ce qui disparaît du rendu ? Les fronts non retenus comptent pour leur influence, pas en double. La vidéo compte à part (hors dépôt). Les pourcentages sont des ordres de grandeur.

| Personne | Part du dépôt/produit | Part du rendu complet (avec vidéo) | Ce qui porte sa part |
|---|---|---|---|
| **phamphamh** | ~58 % | ~49 % | La boucle produit complète (collecteur → app → fusion → Wrapped → bouton skill), le parcours cabinet (7 étapes), **la démo live** (2 écrans, agents Claude dans le Magento, personnes ×10), le script + le deck du pitch, l'outillage d'équipe. Tout ce que le jury voit tourner. |
| **JA** | — | ~15 % | La vidéo : tournage, montage, habillage, voix (hors dépôt). |
| **adamaass** | ~14 % | ~12 % | L'audit Atelier Nova (les 5 chiffres qui ouvrent la démo et le récit, le dashboard, les données ×10) + la recherche cabinets (prix sourcés du pitch) ; le second front Wrapped et la fusion initiale, absorbés. |
| **09125O** | ~13 % | ~11 % | Le récit officiel (« le contexte pas la donnée », le FDE en produit, la description du rendu), les pièces produit **déclencheurs** (« dès que… », fusionnées) et **2e entrée** ; la vitrine (README, captures, docs) ; la charte campagne + « un seul front » ; les vérifications avant rendu ; le logo. |
| **Natsuwy** | ~9 % | ~8 % | L'export des données réelles sans bruit (il alimente l'audit) + « tester en vrai » (Gmail/Sage en sandbox) — la preuve d'honnêteté citée dans le README. |
| **tmschrib** | ~6 % | ~5 % | Le portail client, 6 écrans (hors vidéo, pour la suite côté client). |

Contrôle par le volume brut (lignes ajoutées au dépôt) : phamphamh ~35 000 (~65 %, dont les sauvegardes automatiques qui portent son contenu), adamaass ~11 400 (~21 %, dont ~6 500 de fichiers de données/exemples), 09125O ~3 800, Natsuwy ~2 200, tmschrib ~1 600. La répartition ci-dessus s'en écarte volontairement : elle remonte le récit, les preuves et la vérification (qui ne pèsent pas en lignes mais portent le rendu) et redescend les fichiers de données générés.

**Version courte (prête à coller dans le rendu)** :
- **phamphamh** — le produit et la démo live : la boucle audit → agents Claude dans le vrai back-office.
- **adamaass** — l'audit : les 5 chiffres du récit, le dashboard, les données ×10 ; la recherche cabinets pour le pitch.
- **09125O** — le récit (le contexte, le FDE en produit) et deux pièces du produit (déclencheurs, 2e entrée) ; le README et la description du rendu.
- **Natsuwy** — les données réelles nettoyées et les tests en sandbox (Gmail/Sage).
- **tmschrib** — le portail client.
- **JA** — la vidéo.

Non comptés : Youssef (validation du script du pitch) et les données externes (WONDERBREAD / WebArena), créditées dans le README.

## phamphamh — la boucle produit (la plus grosse pièce)
- **La boucle A→E** : collecteur dérush 80/20 (`labs/phamphamh/collecteur/`), résumé des tâches en un appel `claude -p` (`resume/`), **l'app locale** (`app/` : accueil, questions au dirigeant, relecture du salarié, Wrapped 10 slides avec preuve derrière chaque chiffre, PDF, bouton « Créer la skill »), fusion brique D (`fusion/fusion.py` : agrégats, moins-de-3, aucune identité), démo fictive Maison Corvo.
- **La démo de la vidéo (18/10)** : `labs/phamphamh/agents-nova/` — 2 écrans (Audit / Office), **3 agents Claude en service** dans le vrai back-office Magento (WebArena) : rapport de ventes, changement de prix, commandes annulées ; script anglais ([`script.md`](../labs/phamphamh/agents-nova/script.md)) et deck ([`slides.html`](../labs/phamphamh/agents-nova/slides.html)) ; 6 personnes réelles ×10 (WONDERBREAD).
- **Le « cabinet IA automatisé »** : parcours 7 étapes (`parcours/`), 5 méthodes d'audit inspirées des grands cabinets, rapports (`rapport/`), pack de workflows testés (`workflows/`), recherche sourcée (`recherche/`). En ligne sur un VPS (accès protégé), déployé par `parcours/deployer-vps.sh`.
- **Le rapport de fin d'audit** (story 10 chapitres) sur nos vraies données : `labs/phamphamh/audit/construire.py`.
- **Les outils d'équipe** : skill `.claude/skills/equipe/`, `scripts/etat.sh` (qui fait quoi), `scripts/pousser.sh` (push sûr), `CLAUDE.md`/`AGENTS.md`, exporteur screenpipe en un double-clic (`equipe/exporter-mon-screenpipe.command`).
- **Le 18/10** : fusion des PR #3 et #4 ; tête anglaise du README et captures de la démo.
- *Il a besoin de* : le dépôt en public (propriétaire du dépôt).

## adamaass — l'audit et la recherche
- **L'audit Atelier Nova** : le dashboard `labs/adamaass/nova-dashboard/` (renommé DeloAI) est celui de la démo de la vidéo — 5 chiffres (71,7 k€/an, 41 h/sem, 40 % sur le catalogue, le rapport 790×/sem, 30,1 k€/an récupérables), données ×10 (`caibinet-nova/`).
- **Un front complet C+E en parallèle** : relecture + Wrapped 10 slides (`labs/adamaass/`), fusion D initiale (`labs/adamaass/fusion.py`), format d'insights documenté — absorbé par le front retenu.
- **La recherche « cabinets IA »** : 8 étapes d'une mission, prix publiés (audit IA ≈ 1 100 € HT/jour, POC dès 6 000 €) — `analyse-cabinets-ia.md`, pour le pitch.
- **Son résumé validé et partagé** (2 des 3 validations) + le signalement du bug « [object Object] » de la relecture.
- *Il a besoin de* : la 3e validation pour un vrai Wrapped d'équipe.

## Natsuwy — l'export, la preuve de la skill, et « tester en vrai »
- **L'export filtré de Mickael** (`equipe/mickael.json` + script d'export) : données screenpipe sans le bruit, utilisées dans le rapport d'audit.
- **Le test réel de la skill générée** : donnée à Claude avec une commande piégée (référence inconnue, stock insuffisant, écart de prix) → il s'arrête, applique l'exception prévue (« appel au commercial »), pose ses questions ; commande propre → vérification + brouillon, rien envoyé (journal 1755).
- **« Tester en vrai »** : un banc d'essai (`labs/natsuwy/tester-en-vrai/`) qui fait **faire la tâche à Claude dans un faux Gmail + faux Sage** et vérifie ses **actions** : autonomie « agit » → 4/4, arrêt net sur les deux exceptions ; autonomie « prépare » → rien n'est envoyé ni validé. C'est la preuve du bonus « une tâche transformée en skill » — citée dans les limites honnêtes du README.

## tmschrib — le portail client (arrivé le 17/10 au soir)
- **Portail client « Étude & Pilotage »** : 6 écrans autonomes (HTML/CSS/JS, zéro dépendance) — vue d'ensemble, problèmes détectés, interactions & goulots, temps & outils, business case, pilotage continu ; démo « Maison Verlaine » (52 postes). `labs/tmschrib/dashboard-client/`, `bun server.js` → localhost:4300.
- *Propose* : le brancher sur les sorties du parcours de phamphamh (côté client final).

## 09125O
- **Le récit officiel** : `produit/positionnement.md`, recalé le 18/10 sur le nom **DeloAI** — le FDE en produit, la description du rendu prête à coller (3 longueurs) ; la phrase « le problème n'est pas la donnée, c'est le contexte » est reprise dans le script de la vidéo.
- **Les « dès que… »** : `labs/09125o/declencheurs/` — pour chaque tâche, l'événement qui la lance, la voie technique et l'info à partager ; chaque ligne garde sa preuve. **PR #4 fusionnée le 18/10** : c'est maintenant dans le produit — bloc « Ce qu'il faut brancher (dès que…) » du Wrapped, `fusion.py`, section « Déclencheurs » du SKILL.md généré.
- **La « 2e entrée »** : `labs/09125o/deuxieme-entree/` — reprise comme exigence produit (« skill testée sur une seconde personne » dans le README, « rejouer sur la 2e entrée » dans `parcours/secours.py`).
- **Le brief et le storyboard** de la vidéo (section 23) + les mesures du 16/10 soir (970 captures en 3 h, 59 % de copies exactes, 44 % d'écrans non regardés) — trace de départ, remplacée dans le rendu par l'audit ×10.
- **La vitrine et le ménage** : README (version française réécrite ; tête anglaise ajoutée par phamphamh le 18/10), captures `docs/captures/`, kit de tournage, `docs/skill-exemple/` (le SKILL.md exact du bouton, provenance + test), ce fichier.
- **Les documents de confiance** : `produit/charte-campagne.md` (consentement, anonymisation, droits), `produit/fusion-fronts.md` (décision « un seul front »).
- **Les correctifs** : doublon de l'accueil équipe (PR #2), « limites » toujours en texte (PR #3, **fusionnée**).
- **Les vérifications** : clone neuf des deux apps (200 partout), scan du dépôt avant ouverture, recette de capture corrigée.
- **Le logo** : `labs/09125o/logo-deloai/` — round 2 (Le Run / Le curseur tracé / La tuile) en attente du choix de l'équipe ; round 1 écarté.

## JA (hors dépôt) — la vidéo
- Tournage et montage de la vidéo 2 min. Le lien sera collé dans le README dès qu'il est en ligne. Kit de tournage : `.context/kit-tournage.md`.

## Reste à faire avant le rendu
1. **Dépôt public** — encore privé au 18/10 ; seul le propriétaire peut le basculer. Sans ça, le jury ne peut pas ouvrir le lien GitHub.
2. **Le lien de la vidéo** à coller dans le README (section « La vidéo (2 min) »).
3. **La 3e validation** (phamphamh ou Natsuwy) pour le Wrapped d'équipe réel — 2 des 3 sont faites.
4. Le VPS (`cabinet.159-69-41-115.sslip.io`) est protégé — à ouvrir seulement s'il doit être montré au jury.
