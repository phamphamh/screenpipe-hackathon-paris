#!/bin/sh
# Affiche le pseudo de la personne, en minuscules : $PSEUDO, sinon le login GitHub (gardé en cache), sinon git user.name.
c="$(git rev-parse --git-dir 2>/dev/null)/equipe-pseudo"
if [ -n "$PSEUDO" ]; then p=$PSEUDO
elif [ -s "$c" ]; then p=$(cat "$c")
else p=$(gh api user --jq .login 2>/dev/null); [ -n "$p" ] || p=$(git config user.name); [ -n "$p" ] && printf '%s' "$p" > "$c"
fi
printf '%s\n' "$p" | tr '[:upper:]' '[:lower:]' | tr -cd 'a-z0-9_.\n-'
