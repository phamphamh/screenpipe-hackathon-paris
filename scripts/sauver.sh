#!/bin/sh
# Lancé automatiquement à la fin de chaque réponse de Claude (hook Stop) : sauvegarde et partage le travail.
# Si quelque chose bloque, on rend la main à Claude (code 2) avec l'explication pour qu'il corrige.
cd "$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
input=$(cat 2>/dev/null)
case "$input" in *'"stop_hook_active":true'*|*'"stop_hook_active": true'*) loop=1;; *) loop=0;; esac
BR=$(sh scripts/branche.sh)
if [ -z "$(git status --porcelain)" ] && [ "$(git rev-list --count "origin/$BR..HEAD" 2>/dev/null || echo 0)" = 0 ]; then exit 0; fi
ME=$(sh scripts/pseudo.sh)
files=$(git status --porcelain | awk '{print $NF}' | sed 's|/$||')
n=$(printf '%s\n' "$files" | grep -c .)
list=$(printf '%s\n' "$files" | head -3 | tr '\n' ',' | sed 's/,$//; s/,/, /g')
[ "$n" -gt 3 ] && list="$list (+$((n-3)))"
out=$(sh scripts/pousser.sh "Sauvegarde auto de $ME : $list" 2>&1); code=$?
[ $code = 0 ] && exit 0
[ $loop = 1 ] && { echo "Sauvegarde automatique toujours bloquée : $out" >&2; exit 0; }
{ echo "La sauvegarde automatique a été bloquée. Corrige ça toi-même sans demander de commande à la personne, puis termine :"; echo "$out"; } >&2
exit 2
