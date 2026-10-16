#!/bin/sh
# Lance la version d'origine et la version corrigée en même temps, sur le même écran, pendant $1 secondes.
S=$(cd "$(dirname "$0")/.." && pwd); D=${1:-600}; T=$(date +%H%M%S)
rm -rf "$S/bench/orig-$T" "$S/bench/fix-$T"; mkdir -p "$S/bench/orig-$T" "$S/bench/fix-$T"
timeout $D "$S/screenpipe-orig" record --port 3041 --data-dir "$S/bench/orig-$T" --disable-audio --disable-telemetry > "$S/bench/orig-$T.log" 2>&1 &
timeout $D "$S/screenpipe-fix"  record --port 3042 --data-dir "$S/bench/fix-$T"  --disable-audio --disable-telemetry > "$S/bench/fix-$T.log" 2>&1 &
echo "$T" > "$S/bench/latest"; wait; echo "DONE $T"
