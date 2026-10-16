#!/bin/sh
# Qui fait quoi : chantiers en cours, dernières entrées du journal, branches et commits récents.
cd "$(git rev-parse --show-toplevel)" || exit 1
git fetch -q origin 2>/dev/null || echo "(pas de réseau : état local seulement)"
echo "== Chantiers en cours"
found=0
for f in chantiers/*.md; do
  [ "$(basename "$f")" = README.md ] && continue; [ -f "$f" ] || continue; found=1
  who=$(basename "$f" .md)
  now=$(grep -m1 'En ce moment' "$f" | sed 's/.*En ce moment\*\* *: *//')
  touch=$(grep -m1 'Je touche' "$f" | sed 's/.*Je touche\*\* *: *//')
  when=$(grep -m1 'Mis à jour' "$f" | sed 's/.*Mis à jour *: *//')
  echo "- $who : $now  [touche : $touch] ($when)"
done
[ $found = 1 ] || echo "- personne n'a encore déclaré de chantier"
echo; echo "== Journal (8 dernières entrées)"
ls journal/*/*.md 2>/dev/null | sort | tail -8 | while read -r f; do
  echo "- $(basename "$(dirname "$f")") $(basename "$f" .md | sed 's/^\([0-9][0-9]\)\([0-9][0-9]\)-/\1h\2 /') : $(head -1 "$f" | sed 's/^# *//')"
done
echo; echo "== Branches en cours (hors main)"
git for-each-ref --sort=-committerdate --format='- %(refname:lstrip=3) : %(authorname), %(committerdate:relative) — %(contents:subject)' refs/remotes/origin | grep -vE '^- (main|HEAD) :' | head -8
echo; echo "== Derniers commits sur main"
git log origin/main --format='- %h %an (%ar) : %s' -6 2>/dev/null || git log --format='- %h %an (%ar) : %s' -6
echo; echo "== Chez toi (non poussé)"
git status --short | head -15
ahead=$(git rev-list --count origin/main..HEAD 2>/dev/null); [ "${ahead:-0}" -gt 0 ] && echo "$ahead commit(s) pas encore poussé(s)"
true
