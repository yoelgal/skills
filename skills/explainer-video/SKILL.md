---
name: explainer-video
description:
  Make a narrated, animated explainer video, in the style of a math-animation channel, about a system, codebase, concept or
  document set. Researches the sources, writes a script for the ear, speaks it with a local text-to-speech model
  (Kokoro-82M), animates each chapter with Manim Community Edition in sync with the spoken words, and checks the render.
  Use when the user asks for an explainer video, an animated walkthrough, a narrated overview of a codebase or a doc, or
  "a 3b1b-style video" about something.
---

# Explainer video

The output is an mp4 with narration, a `script.md` and a project that renders again with one command. The viewer is a
person who must understand the subject after one watch. Each step below serves that viewer.

The pipeline:

```text
sources -> fact list -> chapter plan -> narration.py -> tts.py (wav + word timings) -> scenes/chNN.py -> build.sh -> mp4
```

`narration.py` is the single source of truth. The voice, the scenes and `script.md` all read it. Change words there,
never in a scene.

## 1. Brief

Settle these before research. Ask only for what the request and the sources do not say.

- **Viewer.** Who watches, and what they know now.
- **Goal.** One sentence: after the video, the viewer can do or explain what.
- **Sources.** The docs, code, notes or transcripts the video may use. Nothing else is a source.
- **Length.** A target in minutes. Default: 1 to 2 minutes for each chapter, 10 to 15 minutes in total.
- **Confidentiality.** If the material is internal, keep all of it on the machine: local TTS, no upload to any service.
- **Output folder.** Outside the user's repos, unless the user names one.

Long renders block a session. When the harness supports background work, run the job in the background and tell the
user where the files will be.

## 2. Research and the fact list

Read every source in full before you write a word of script. Write `facts.md` in the project folder: one line per fact,
each with its source (`path:line`, a doc section, "call with X on <date>"). The script may say only what this list holds.

Mark each fact that comes from a person, not a document, as such. The video must label a rough or spoken figure on
screen, for example "about 20%, from the kickoff call".

## 3. Chapter plan

- Give each chapter one idea and one diagram that grows across the chapter.
- Order: why it exists, then the model, then the mechanics, then what goes wrong, then a recap.
- Budget the words. Kokoro `af_heart` at speed 1.0 speaks about 150 words a minute. The finished video runs about 10%
  longer than the narration, for chapter cards and pauses. A 12-minute video is about 1,650 words.
- Cut a topic before you rush one. Name each cut in the final report, with the reason.
- Fix the colour meanings for the whole video in the plan, for example "blue is a service, teal is a store, gold is a
  message, red is a failure". Keep them.

## 4. Script

Write `narration.py` from the template. Read [references/script-writing.md](references/script-writing.md) first. It
holds the rules for spoken text, beats and cue words.

Then do a fact pass: compare each sentence with `facts.md`. Rewrite each sentence that claims more than its source, for
example an absolute ("never", "only") where the source has an exception. Where two sources disagree, follow the more
specific one and note it.

## 5. Set up the project

Copy [template/](template/) to the output folder. It holds a working two-chapter example; replace its content.

```sh
brew install ffmpeg cairo pango pkg-config espeak-ng   # macOS; use the apt equivalents on Linux
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python manim kokoro soundfile numpy
chmod +x build.sh sheet.sh
```

The first run of `tts.py` downloads the Kokoro weights (about 330 MB) from Hugging Face. After that, everything runs
offline.

| File               | Function                                                                                                                                              |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `narration.py`     | Title, output name, voice, and the chapters as keyed beats                                                                                            |
| `tts.py`           | Speaks each beat to `audio/<beat>.wav` with word start times in `audio/timings.json`. Speaks a beat again only when its text, voice or speed changes. |
| `scenes/common.py` | Palette, shapes (`node`, `cylinder`, `queue_shape`, `pill`, `arrow`, `token`, `Bucket`) and the `Voiced` scene base                                   |
| `scenes/chNN.py`   | One Manim scene for chapter NN. The class name is the first item of the chapter in `narration.py`.                                                    |
| `make_script.py`   | Writes `script.md` from `narration.py`, with the spoken length of each chapter                                                                        |
| `build.sh`         | TTS, then all chapters in parallel, then one loudness-normalised mp4. `./build.sh l` makes a 480p preview.                                            |
| `sheet.sh`         | A contact sheet of frames from a render                                                                                                               |

## 6. Voice

Run `.venv/bin/python tts.py` as soon as the script exists. It prints the length of each beat and the total. Fix the
length now, in the words: an over-long script costs nothing to cut before the scenes exist.

Kokoro-82M is the default: it is small, fast (about 5 times real time on an Apple M3 Pro) and gives a start time for
each word, which the scenes sync to. Change `VOICE` in `narration.py` for a different voice; the first letter selects
the language (`a` American English, `b` British English). Use a different local model only if it also gives word
timings, and say why in the report.

## 7. Scenes

Read [references/scenes.md](references/scenes.md) before the first scene. The core pattern:

```python
class Ch02Buckets(Voiced):
    def construct(self):
        self.chapter_title("Ch02Buckets")
        with self.beat("c2a"):            # plays c2a.wav; waits out the rest of the beat at the end
            self.cue("function")          # waits until the word "function" is spoken
            self.play(FadeIn(fn))
        self.clear()
```

Render one chapter while you work on it:

```sh
.venv/bin/manim -ql --disable_caching scenes/ch02.py Ch02Buckets
```

## 8. Render and check

1. Run `./build.sh l`. Fix each `[overrun]` line: the scene's animations ran past its narration.
2. Make a contact sheet for each chapter (`./sheet.sh <video> sheet.png 4`) and look at it. Fix clipped text,
   overlaps, text off the frame edge, and labels that are too small to read at 1080p.
3. Run `./build.sh` for the 1080p render.
4. Check the final file:
   - Every chapter is present, in order (`ffprobe`, or a contact sheet of the whole video).
   - The audio stays in sync to the end. Compare the start of the last chapter's narration in the joined file with its
     start in that chapter's own render. The difference must be under 0.1 s.
   - The duration is near the target. If it is far over, cut words and render again. Do not speed up the voice.
5. Do a last fact pass on `script.md` against `facts.md`. Fix, then re-render only the chapters that changed and run
   the join step of `build.sh` again.

## 9. Report

Give the user:

- The path and duration of the mp4, and the path of `script.md`.
- The chapter list.
- The renderer and the voice, and where the audio was made (local).
- What the video says that is not in the documents, and where it came from.
- What you cut, and why.
- What you checked and how (frames, sync, facts), and anything you did not check.
