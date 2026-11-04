# Script writing

The script is heard once, at the speed of the voice, with a picture in front of it. Write for that listener, not for a
reader.

## Beats

A chapter is a list of beats: `("c3b", "spoken text")`. A beat is one to three sentences, 10 to 40 words, that go with
one change on screen.

- Key each beat `c<chapter><letter>`: `c3a`, `c3b`. Do not reuse a key: the audio cache uses it.
- Start a new beat where the picture changes. A beat with no new picture is a beat to cut.
- Keep a beat under about 15 seconds. A long beat gives the scene a long stretch with one cue.

## Words for the ear

- Write each identifier the way it should be said. `recordEvent` is "record event". `ADR-0006` is "A D R six".
  `svc-prd-eu1` is "the production service". Put the exact identifier on screen, not in the voice.
- Write numbers as they are said when the voice could misread them: "forty-two columns", "about twenty percent",
  "ninety days".
- Do not use symbols, slashes, parentheses or abbreviations in spoken text. Say "and", "or", "for example".
- Keep sentences short. One idea per sentence. Put the subject and the verb early.
- Define a term the first time it is spoken, then use exactly that term every time after. Do not use synonyms for
  variety: the viewer will think there are two things.
- Use a concrete example before the rule: "a customer pays ten dollars for one order", then the general case.
- Speak to the viewer: "you", "your". If the video is for one person, use their name once, in the first beat.
- Read each beat aloud, or listen to its wav. Rewrite each sentence that sounds unnatural.

## Cue words

A cue word is a word in the beat that a scene waits for before it shows something: `self.cue("outbox")`.

- Plan the cue words when you write the beat. Put the noun that names the new thing in the sentence that shows it.
- A cue matches the start of a spoken word, case and punctuation ignored, and searches forward from the last cue in the
  beat. Cues in one beat must be in spoken order.
- Use a distinctive word. "the" and "a" match too early.
- If you edit a beat, check its cues still occur in order. A missing cue fails the render and names the beat.

## Structure of a chapter

1. One beat that says what the chapter answers.
2. The example, built up one step for each beat.
3. The general rule, in one sentence, with the full diagram on screen.
4. If the chapter has a failure mode, show it last: what breaks, then what stops it.

The last chapter is a recap: one beat for each earlier chapter, in the same words that chapter used.

## Accuracy

- Every claim comes from the fact list. If a sentence needs a fact that is not there, find the source or cut the
  sentence.
- Keep the source's qualifiers: "about", "in production", "for most events". A dropped qualifier is a false claim.
- Do not state what the system returns, sends or guarantees unless the source says it for that exact case.
- Mark a figure from a person, not a document, as approximate in the voice and on screen.
