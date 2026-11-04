#!/bin/bash
# sheet.sh <video> <out.png> [every_seconds]: a 4x6 contact sheet of frames, to spot-check a render.
v="$1"; out="$2"; every="${3:-4}"
ffmpeg -loglevel error -y -i "$v" -vf "fps=1/${every},scale=480:-1,tile=4x6:padding=4" -frames:v 1 "$out"
