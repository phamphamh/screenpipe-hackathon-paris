#!/bin/sh
# Pousse sans jamais écraser les autres : vérifie, commit, rebase sur le travail des autres, puis push (jamais en forçant).
# Usage : sh scripts/pousser.sh "message du commit"
cd "$(git rev-parse --show-toplevel)" || exit 1
MSG=$1; ME=$(sh scripts/pseudo.sh); BR=$(git rev-parse --abbrev-ref HEAD)
[ -n "$ME" ] || { echo "Pseudo introuvable : lance avec PSEUDO=ton-login sh scripts/pousser.sh \"...\""; exit 1; }
git add -A
# 1. Fichiers interdits : données screenpipe, médias bruts, secrets
bad=$(git diff --cached --name-only | grep -iE '\.(sqlite|db|mp4|wav|m4a|mov|env)$|(^|/)\.env|secrets' )
if [ -n "$bad" ]; then echo "STOP : fichiers à ne pas commiter :"; echo "$bad"; git reset -q; exit 1; fi
if git diff --cached | grep -qE 'sp-[0-9a-f]{8}|Bearer [A-Za-z0-9_-]{8,}|sk-[A-Za-z0-9]{20,}|gh[op]_[A-Za-z0-9]{20,}'; then
  echo "STOP : une clé API semble présente dans tes changements. Retire-la, puis relance."; git reset -q; exit 1; fi
# 2. Ce qui part : les changements en attente + les commits pas encore poussés
base=$(git merge-base HEAD origin/main 2>/dev/null || echo HEAD)
files=$( (git diff --cached --name-only; git diff --name-only "$base" HEAD) | sort -u)
others=$(printf '%s\n' "$files" | grep -E '^(labs/[^/]+/|chantiers/[^/]+\.md$)' | grep -vE "^labs/$ME/|^chantiers/$ME\.md$|^(labs|chantiers)/README\.md$")
if [ -n "$others" ]; then
  echo "STOP : tu as modifié le lab ou le chantier de quelqu'un d'autre :"; echo "$others"
  echo "Copie plutôt dans labs/$ME/, ou propose-lui une PR."; git reset -q; exit 1; fi
edited=$(git diff --cached --name-only --diff-filter=M | grep -E '^journal/.+/[0-9]{4}-' | grep -v -- "-$ME\.md$")
[ -n "$edited" ] && { echo "STOP : on ne modifie pas l'entrée de journal d'un autre :"; echo "$edited"; git reset -q; exit 1; }
# 3. Commit
if ! git diff --cached --quiet; then
  [ -n "$MSG" ] || { echo "Donne un message : sh scripts/pousser.sh \"ce que j'ai fait\""; git reset -q; exit 1; }
  git commit -q -m "$MSG" || exit 1
fi
[ "$(git rev-list --count "origin/$BR..HEAD" 2>/dev/null || echo 1)" -gt 0 ] || { echo "Rien à pousser."; exit 0; }
# 4. Rebase sur le travail des autres, puis push sans forcer (3 essais)
for i in 1 2 3; do
  if git ls-remote --exit-code --heads origin "$BR" >/dev/null 2>&1; then
    if ! git pull -q --rebase origin "$BR"; then
      git rebase --abort 2>/dev/null
      echo "CONFLIT avec le travail de quelqu'un : rien n'a été poussé, ton commit est intact."
      echo "Règle : garder les deux versions. Lance « git pull --rebase origin $BR », résous en gardant les lignes des autres, puis relance ce script."
      exit 1
    fi
  fi
  if git push -q origin "HEAD:$BR"; then echo "Poussé sur $BR ($(git log -1 --format=%h))."; exit 0; fi
  sleep 2
done
echo "Le push a échoué 3 fois : réessaie dans une minute."; exit 1
