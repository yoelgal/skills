"""Write script.md, the narration by chapter with each chapter's spoken length, from narration.py."""

import json
from pathlib import Path

from narration import CHAPTERS, OUTPUT, TITLE, VOICE

root = Path(__file__).parent
timings = json.loads((root / "audio" / "timings.json").read_text())
out = [f"# {TITLE}: narration script", "", f"Narration for `{OUTPUT}`, by chapter. Voice: Kokoro-82M `{VOICE}`.", ""]
total = 0.0
for _, title, beats in CHAPTERS:
    secs = sum(timings[k]["duration"] for k, _ in beats)
    total += secs
    out += [f"## {title}", "", f"*Narration: {secs / 60:.1f} min*", ""]
    out += [text + "\n" for _, text in beats]
out += ["---", "", f"Total narration: {total / 60:.1f} min. The video adds chapter cards and pauses."]
(root / "script.md").write_text("\n".join(out) + "\n")
print(f"script.md written, {total / 60:.1f} min of narration")
