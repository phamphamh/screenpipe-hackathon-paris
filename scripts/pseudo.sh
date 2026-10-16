#!/bin/sh
# Affiche le pseudo de la personne : $PSEUDO, sinon le login GitHub, sinon git user.name. Toujours en minuscules.
p=${PSEUDO:-$(gh api user --jq .login 2>/dev/null)}
[ -n "$p" ] || p=$(git config user.name)
printf '%s\n' "$p" | tr '[:upper:]' '[:lower:]' | tr -cd 'a-z0-9_.\n-'
