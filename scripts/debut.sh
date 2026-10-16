#!/bin/sh
# Lancé automatiquement au début de chaque session Claude Code (hook SessionStart).
# Récupère le travail des autres, puis donne à Claude l'état de l'équipe et ses consignes.
cd "$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
echo "=== Équipe hackathon : début de session (automatique)"
if [ -z "$(git config user.name)" ] || [ -z "$(git config user.email)" ]; then
  echo "ACTION POUR CLAUDE : git ne connaît pas encore la personne. Demande-lui son prénom et son email GitHub, puis lance git config user.name \"...\" et git config user.email \"...\" dans ce dépôt."
fi
if ! git ls-remote -q origin HEAD >/dev/null 2>&1; then
  echo "ACTION POUR CLAUDE : impossible de joindre GitHub (pas connecté ou pas de réseau). Guide la personne pas à pas pour se connecter (gh auth login, ou GitHub Desktop), sans jargon."
elif ! git pull -q --rebase --autostash origin "$(sh scripts/branche.sh)" 2>/dev/null; then
  git rebase --abort 2>/dev/null
  echo "ACTION POUR CLAUDE : la récupération du travail des autres a échoué (conflit). Résous-le en gardant les deux versions, sans rien supprimer des autres."
fi
ME=$(sh scripts/pseudo.sh)
sh scripts/etat.sh 2>/dev/null
echo
echo "=== Consignes pour Claude (la personne n'est pas technique)"
echo "- Ton interlocuteur s'appelle « $ME » dans le dépôt. Ne lui demande JAMAIS de taper une commande git ou un script : tout est sauvegardé et partagé automatiquement à la fin de chacune de tes réponses."
echo "- Commence par lui résumer en 3 lignes simples ce que font les autres (d'après l'état ci-dessus)."
[ -f "chantiers/$ME.md" ] || echo "- La personne n'a pas encore de fiche : demande-lui sur quoi elle veut travailler, puis crée chantiers/$ME.md (format dans .claude/skills/equipe/SKILL.md)."
echo "- Travaille dans labs/$ME/ ; dans les fichiers partagés, fais seulement des modifications ciblées. Ne modifie jamais labs/<autre>/ ni chantiers/<autre>.md."
echo "- Quand son sujet change, mets à jour chantiers/$ME.md. Quand quelque chose marche, ajoute une entrée dans journal/<date>/<HHMM>-$ME.md."
echo "- Si son idée recoupe le chantier de quelqu'un d'autre, dis-le-lui avant de coder."
exit 0
