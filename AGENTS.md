# Dépôt de l'équipe — hackathon screenpipe × 42 Paris

Avant toute chose dans ce dépôt, applique le skill `.claude/skills/equipe/SKILL.md`. Les personnes de l'équipe **ne sont pas techniques** : ne leur demande jamais de taper une commande.
- Récupération et sauvegarde automatiques : avec Claude Code, des hooks s'en chargent (`.claude/settings.json`). Avec Codex, il n'y a pas de hooks : lance toi-même `sh scripts/debut.sh` au début de la session, puis `sh scripts/sauver.sh < /dev/null` après chaque modification.
- Tu écris dans `labs/<pseudo>/`, `chantiers/<pseudo>.md` et `journal/`. Dans les fichiers partagés, uniquement des modifications ciblées. Jamais de push forcé.

Le projet : `produit/decoupage.md`. Tout le contexte : `.context/hackathon-brief.md`.
