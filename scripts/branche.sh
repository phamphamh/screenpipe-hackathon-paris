#!/bin/sh
# La branche distante où sauvegarder : celle suivie par la branche locale, sinon la branche du même nom.
up=$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null | sed 's|^origin/||')
[ -n "$up" ] && echo "$up" || git rev-parse --abbrev-ref HEAD
