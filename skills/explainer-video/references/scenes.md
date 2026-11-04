# Scenes

One Manim scene per chapter, in `scenes/chNN.py`, as a subclass of `Voiced` from `scenes/common.py`.

## Sync

- `with self.beat(key):` adds the beat's audio at the current time. At the end of the block, the scene waits for the
  rest of the beat plus `PAD` (0.25 s). Pass `pad=` to change it for one beat.
- `self.cue(word)` waits until 0.12 s before the word is spoken. Show the thing as its name is said.
- `self.left()` gives the seconds left in the beat. Use it to fit a closing animation into the time left.
- If the animations in a beat take longer than its audio, the build log prints `[overrun] <beat>`. Fix it: shorten the
  animations, or move some of them to the next beat. Do not slow the voice.
- `self.chapter_title(cls)` shows the chapter card from the title in `narration.py`, then moves it to a header at top
  left. `self.clear()` fades everything except the header.

## Visual rules

- Show the mechanism. Each diagram shows what moves where, and what each part does to it. Do not add decoration.
- Build each diagram one part at a time, each part on its cue. The full diagram appears only at the rule beat.
- Animate the thing that moves: a `token` that travels along an arrow (`self.travel(points)`), a `Bucket` level that
  rises or falls, a row that fades when it is deleted.
- Show failure on the same diagram: a red cross on the step that fails, then what happens next.
- Keep each hue to the meaning in the chapter plan.
- Put identifiers on screen in the mono face (`M(...)`), exactly as they are in the source.
- Keep text at 20 pt or more at 1080p. Use `fit(mob, max_width)` on every label that comes from data.
- Keep all content inside x from -6.8 to 6.8 and y from -3.7 to 3.4. The header uses the top-left corner.
- Show at most about 12 words of caption at one time. The voice carries the words; the screen carries the structure.
- Do not use third-party characters, logos, music or intros. Make the visual identity your own.

## Common faults

| Fault                                 | Fix                                                                                             |
| ------------------------------------- | ----------------------------------------------------------------------------------------------- |
| A label overlaps a shape              | Place with `next_to(..., buff=)`, not with absolute positions on both                           |
| Text clips at the frame edge          | `fit()` it, or move the group with `.move_to()` after you arrange it                            |
| A diagram does not fit after it grows | Plan the final layout first, then reveal its parts. Do not rearrange mid-beat.                  |
| A cue fails after an edit             | The word moved or changed. Change the cue, or keep the word.                                    |
| A chapter has silence at its end      | The last beat's animations are short. That is correct: the beat waits for its audio.            |
| Audio drifts late in the joined video | Keep the `aresample=async=1` filter in `build.sh`, and re-render the chapters at one frame rate |
