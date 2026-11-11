# Writing rules

Shared by the `issue-writing`, `issue-review` and `pr-writing` skills. The copies of this file must stay identical. Run
`scripts/check-shared.sh` from the repo root after an edit.

Write like the author: an engineer who tells a busy teammate exactly what they need to know, then stops. The reader
should understand the situation in one read and know what to do next. Detail they might need lives in the diff, the code
or a collapsed section, never in the prose.

## Do all the work, show the conclusion

Short text keeps the full rigour. Read the code, run the checks, prove each claim, and confirm each test fails without
the fix. Then report the conclusion in one line: "3 new tests, each fails without the fix", not three bullets that each
say so. The visible part is for a human who reads it once. Depth that a reviewer or an agent might want (each test, full
logs, the reasoning behind a choice) goes in a collapsed `<details>` block at the end, kept to what is useful.

If a sentence states a fact the reader needs, keep it however short the budget is. Cut wording, never facts.

## Plain words

Write for an engineer a few weeks into the repo. They know the language and the stack, but not every service name, flag
or past decision. Do not explain what a pull request or a process is. Do explain, in a few words, a term only this repo
or this change uses.

- Say what happens in everyday words first, then give the code name if the reader needs it: "the dev script leaves the
  API server running after you quit it (`start-full-stack.sh`)", not "`cleanup_processes` signals the job PID only".
- One piece of jargon per sentence at most. If a sentence stacks two ("non-allowlisted public procedures"), rewrite it
  around what the user or the system does.
- Read it aloud. If you would not say it that way to a teammate at standup, rewrite it.

## Titles

A title is the one line most people read. It must make complete sense on its own to that new starter.

- Say what changes, for whom, in plain words. Use a code name only when it is the clearest name for the thing.
- No stacked qualifiers, no internal shorthand, no AI phrasing ("ensure", "handle", "robust", "properly").
- Write: `Stop the dev servers when the start script exits`. Not: `Signal the process group in cleanup_processes`.
- Write: `Block third-party app tokens on endpoints that don't allow them`. Not: `Refuse OAuth app tokens on public
  procedures that are not allowlisted`.
- Write: `Show the HTTP status when the payment service returns a non-JSON error`. Not: `Report a non-JSON upstream
  error by its HTTP status`.

## Voice

- **Lead with what happened, in plain words.** Describe the symptom the way a user or an operator sees it, then the
  cause, then the fix. "After the verification link, home flashed 'check your email' for a split second, because the
  redirect ran before the session knew the email was verified."
- **Link cause and effect with "because" and "so".** "The page now refreshes the session before it redirects, so home
  always reads a verified session." One sentence like that replaces a paragraph of bullets.
- **Name things by what they are first, by identifier second.** "the verify page" in the summary, `VerifyEmailPage` in
  the detail that needs it.
- **Say the size and the state.** "Small one." "Tested on the iOS simulator, before and after videos below."
  "Nothing reads the new secrets yet, the API side follows."
- **Tell the reader what to do.** "Start at #101, each PR stacks on the one before." "The platform team owns the secret,
  so they set the value." End with the question you need answered, if there is one: "OK with this direction?"
- **Own mistakes in one line.** "My mistake, the docs say write-only. Fixed in #212."
- **Sound like a person.** Contractions are fine. Write in the first person when you did something. Use full sentences,
  but short ones, joined with commas when the ideas belong together.

## Length

Length is the most common failure. Every skill that loads this file gives a word budget. Stay under it.

- Write the summary first, as if it were the whole document. Add more only when a reader would act wrongly without it.
- One idea per sentence, about 20 words or fewer.
- One line per bullet. A bullet that needs two lines is two facts, or one fact with padding.
- Use a list only for three or more parallel items. One or two items go in a sentence.
- Do not repeat a fact in two sections. Do not restate the title in the body.
- Do not list what the diff, the test names or the CI log already show. Point at them.
- Put long evidence (logs, full test lists, real-speed videos) in a `<details>` block.

## Delete on sight

- **Openers and meta-text:** "This PR", "This ticket aims to", "Context:", "TL;DR", "Background", "As discussed".
- **Hedges without a reason:** "maybe", "possibly", "it seems", "we may want to", "consider". If something is unknown,
  say what is unknown: "Cause unknown, the logs for 02:00 to 03:00 are missing."
- **Labels in place of consequences:** "critical", "significant", "major", "important to note". Say what breaks.
- **Contrast framing:** "rather than X", "instead of Y", "not X, it's Y", "The real problem: ...". Say what it is.
- **Trailing analysis:** "..., highlighting the need for better monitoring." Say the consequence: "..., so no alarm
  fires."
- **Recaps and kickers:** "In summary", "Overall", a last line that repeats what is above it.
- **Narrative:** how the bug was found, who noticed it, how long it took.
- **Formatting noise:** emoji, ALL CAPS, bold for emphasis, em dashes, headings over one sentence, horizontal rules.
- **Words:** delve, foster, leverage, utilize, facilitate, empower, streamline, robust, seamless, holistic, paradigm,
  landscape, multifaceted, meticulous, intricate, paramount, transformative, elevate, embark, supercharge, harness,
  unlock, journey.
- **Empty words:** just, simply, actually, really, basically, essentially, literally, truly, clearly, obviously, in
  order to, due to the fact that, in terms of, with regard to, going forward.

## Precision

- Use one name for one thing, the name from the code. Do not vary it.
- Put a location on a claim about the code when the reader needs to find it: `path/file.ts:72` or a function name.
- Give numbers with units: "flashed in 4 of 4 runs", "times out after 5 s". Not "quickly" or "often".
- Quote log lines, metric names and error text exactly, in backticks.
- Say what you did not check: "Not checked: prod."

## GitHub and trackers

The voice comes from the author's Slack messages. In a PR or an issue, keep the voice and drop the chat habits: use
sentence case, no "pls", no emoji, no greetings.
