#!/bin/bash
# Narration -> chapter scenes (in parallel) -> one mp4.
# Usage: ./build.sh [quality]   quality: h (1080p30, default) or l (480p15 preview)
set -euo pipefail
cd "$(dirname "$0")"
Q="${1:-h}"
PY=.venv/bin/python
MANIM=.venv/bin/manim

$PY tts.py
$PY make_script.py

if [ "$Q" = "h" ]; then FLAGS=(-r 1920,1080 --fps 30); DIR=1080p30; else FLAGS=(-ql); DIR=480p15; fi
mkdir -p logs
# One "chNN:ClassName" per chapter, in narration order.
SCENES=($($PY -c 'from narration import CHAPTERS; print(" ".join(f"ch{i:02d}:{c[0]}" for i, c in enumerate(CHAPTERS, 1)))'))
OUT=$($PY -c 'from narration import OUTPUT; print(OUTPUT)')
[ "$Q" = "h" ] || OUT="${OUT%.mp4}-preview.mp4"

pids=()
for s in "${SCENES[@]}"; do
  f=${s%%:*}; k=${s##*:}
  $MANIM "${FLAGS[@]}" --disable_caching "scenes/$f.py" "$k" > "logs/$f.log" 2>&1 &
  pids+=($!)
done
fail=0
for p in "${pids[@]}"; do wait "$p" || fail=1; done
grep -h "overrun" logs/*.log || true
[ $fail = 0 ] || { echo "a scene failed, see logs/"; exit 1; }

: > logs/concat.txt
for s in "${SCENES[@]}"; do
  f=${s%%:*}; k=${s##*:}
  echo "file '$PWD/media/videos/$f/$DIR/$k.mp4'" >> logs/concat.txt
done
# Join the chapters, then normalise loudness over the whole programme.
ffmpeg -loglevel error -y -f concat -safe 0 -i logs/concat.txt -c:v copy \
  -af "aresample=async=1:first_pts=0,loudnorm=I=-16:TP=-1.5:LRA=11,apad" -shortest \
  -c:a aac -b:a 160k -ar 48000 -movflags +faststart "$OUT"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT" | awk '{printf "'"$OUT"': %d:%02d\n", $1/60, $1%60}'
