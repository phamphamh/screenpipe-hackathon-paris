# Outils d'équipe : chacun construit, personne n'écrase
- **Fait** : skill `.claude/skills/equipe/`, `CLAUDE.md` + `AGENTS.md`, `scripts/etat.sh` (qui fait quoi), `scripts/pousser.sh` (push sûr)
- **Preuve** : 8 cas testés sur un dépôt de test : lab d'un autre refusé, clé API refusée, vidéo refusée, 2 push simultanés OK, même ligne modifiée = conflit sans perte, rien à pousser, journal d'un autre refusé, état affiché
- **Pas vérifié** : sous Windows (Git Bash devrait marcher, pas testé) ; avec Codex
- **Pour les autres** : au début de chaque session, `sh scripts/etat.sh` ; pour pousser, `sh scripts/pousser.sh "message"`
