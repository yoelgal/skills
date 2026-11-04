"""Speak every beat in narration.py with Kokoro-82M, locally.

Writes audio/<beat>.wav and audio/timings.json: {beat: {"hash", "duration": s, "words": [[word, start_s], ...]}}.
A beat is spoken again only when its text, voice or speed changes.
"""

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro import KPipeline

from narration import CHAPTERS, SPEED, VOICE

RATE = 24000
ROOT = Path(__file__).parent
OUT = ROOT / "audio"
OUT.mkdir(exist_ok=True)
TIMINGS = OUT / "timings.json"


def main() -> None:
    timings = json.loads(TIMINGS.read_text()) if TIMINGS.exists() else {}
    pipeline = None
    for _, _, beats in CHAPTERS:
        for key, text in beats:
            digest = hashlib.sha1(f"{VOICE}|{SPEED}|{text}".encode()).hexdigest()
            wav = OUT / f"{key}.wav"
            if timings.get(key, {}).get("hash") == digest and wav.exists():
                continue
            if pipeline is None:
                pipeline = KPipeline(lang_code=VOICE[0], repo_id="hexgrad/Kokoro-82M")
            chunks, words, offset = [], [], 0.0
            for result in pipeline(text, voice=VOICE, speed=SPEED):
                audio = result.audio.numpy() if hasattr(result.audio, "numpy") else np.asarray(result.audio)
                for tok in result.tokens or []:
                    if tok.start_ts is not None and any(c.isalnum() for c in tok.text):
                        words.append([tok.text, round(offset + tok.start_ts, 3)])
                chunks.append(audio)
                offset += len(audio) / RATE
            audio = np.concatenate(chunks)
            sf.write(wav, audio, RATE)
            timings[key] = {"hash": digest, "duration": round(len(audio) / RATE, 3), "words": words}
            print(f"{key}: {timings[key]['duration']:.1f}s", file=sys.stderr)
    keys = {k for _, _, beats in CHAPTERS for k, _ in beats}
    timings = {k: v for k, v in timings.items() if k in keys}
    TIMINGS.write_text(json.dumps(timings, indent=1))
    total = sum(v["duration"] for v in timings.values())
    print(f"total narration: {total / 60:.1f} min", file=sys.stderr)


if __name__ == "__main__":
    main()
