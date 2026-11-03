---
name: issue-writing
description:
  Write or edit an issue or ticket in plain, fluff-free prose that follows the writing rules of ASD-STE100 Simplified
  Technical English (STE). Every sentence states a fact, a consequence, a requirement or a decision. Use when filing a
  bug, writing a ticket from a finding, editing a draft issue, or rewriting an issue that is hard to act on, in any
  tracker (Linear, GitHub, Jira). Triggers on "write an issue", "file a ticket", "draft an issue", "clean up this
  ticket", "rewrite this issue", "issue writing". Run the issue-review skill on the result before filing, when it is
  installed.
---

# Issue writing

An issue is an instruction to an engineer who does not have your context. The engineer reads it once, then uses it as
the specification. Each sentence must give that engineer a fact, a consequence, a requirement or a decision. Delete all
other sentences.

This skill controls the words and the structure. The `issue-review` skill controls the content: coverage, impact, docs
and scope. Write with this skill, review with `issue-review`, then file.

## Structure

Use these sections, in this order. Omit a section that has no content. Do not add other sections.

```markdown
## Problem

<What the code does now, with file:line. What is wrong with that.>

## Impact

<What goes wrong, for whom, how often. Include the case where the fault continues.>

## Change

<Requirements, one per bullet, in the imperative.>

## Decisions

<Each open choice: "Pick one:" with the options and a recommendation.>

## Acceptance

<Checkable outcomes: a test, a snapshot, an alert, a doc change.>

## Out of scope

<What this issue does not do, and the issue that does it.>
```

**Title.** State the defect or the result in present tense, in 70 characters or fewer. Use the names from the code.

- Write: `Outbox drainer reports a failed delete as a failed publish`
- Do not write: `Fix outbox issue`, `[BUG] Improve error handling in drainer`, `Investigate delete failures 🐛`

## STE writing rules

These are the writing rules of ASD-STE100. The standard also has a dictionary of approved words. This skill does not
include the dictionary. Apply its principle: one word, one meaning, and the simplest common word.

### Words

- Use one term for one thing. Use the name from the code (the metric name, the class name, the alarm name). Repeat it.
  Do not use synonyms for variety.
- Give a word only one meaning. If "check" is a verb, do not also use it as a noun for a CI job.
- Use the simplest common word: "use", not "utilize"; "start", not "initiate"; "show", not "demonstrate"; "help", not
  "facilitate"; "about", not "approximately".
- Write the full verb, not a noun made from a verb: "decide", not "make a decision"; "the drainer deletes the row", not
  "the deletion of the row is performed".
- Keep noun clusters to three words or fewer. "outbox delete failure count" is the limit. Break longer clusters with
  "of", "for" or a relative clause.
- Do not use contractions: "do not", not "don't".
- Use technical names (code identifiers, product names, error codes) as they are, in backticks.

### Sentences

- Write one idea per sentence.
- Keep a sentence to 20 words or fewer in the Change, Decisions and Acceptance sections. Keep it to 25 words or fewer in
  the Problem and Impact sections.
- Use the active voice. Name the actor: "The drainer deletes the row", not "The row is deleted".
- Use the simple tenses: simple present, simple past, future with "will". Do not use progressive forms such as "is
  failing" or "has been failing".
- Do not use "-ing" words as verbs or nouns, except in technical names. Write "when the delete fails", not "on failing
  to delete".
- Write requirements in the imperative: "Add an alarm", not "An alarm should be added" or "We might want to add an
  alarm".
- Keep the articles ("the", "a"). Do not write in telegraphic style.
- Put a condition before the instruction: "If the delete fails, log the row's key."

### Paragraphs and lists

- Give each paragraph one topic. Use six sentences or fewer.
- Use a list for three or more parallel items, or for steps. Use prose for one or two items.
- Write list items in the same grammatical form. Start each requirement with a verb.

## Fluff to delete

Delete these on sight. Each one delays the reader or tells the reader what to think in place of a fact.

**Openers and meta-text.** "This ticket aims to", "The purpose of this issue is", "As discussed", "Just a heads-up",
"Context:", "TL;DR", "Background" over a section that only repeats the Problem. Start with the fact.

**Hedges without a reason.** "Maybe", "possibly", "might", "it seems", "we may want to", "consider". Keep a hedge only
when there is a real unknown, and write the unknown as a fact: "The cause is not known. The logs from 02:00 to 03:00 are
missing."

**Puffery and labels.** "critical", "crucial", "important to note", "significant", "major issue", "a testament to",
"plays a key role". Show the consequence and let the reader judge it: write "Newer rows do not drain while the fault
continues", not "This is a critical issue".

**Interpretive metadiscourse.** "The key point is", "Note that", "It is worth noting", "As you can see", "This
distinction matters". Delete the aside and keep the fact.

**Weasel attribution.** "People say", "it is widely known", "best practice says". Name the source (a doc, a person, a
file:line), or delete the claim.

**Binary contrast and colon reveals.** "This is not X, it is Y." "The real problem: the delete." State Y directly: "The
delete fails."

**Trailing -ing analysis.** "...highlighting the need for better monitoring." Replace it with the consequence: "...so no
alarm fires."

**Recap endings and kickers.** "In summary", "Overall", "Ultimately", or a last line that restates the issue. End on the
last requirement or acceptance criterion.

**Narrative and provenance.** How the bug was found, who noticed it, how long the search took. Put provenance in a
comment if it helps. The description holds only what the implementer needs.

**Formatting noise.** Emoji, bold inside sentences for emphasis, headings over one-sentence sections, horizontal rules,
nested bullets deeper than two levels. Use bold only for a list item's label.

**Banned words.** delve, foster, leverage, utilize, facilitate, empower, streamline, robust, seamless, cutting-edge,
holistic, synergy, paradigm, game changer, tapestry, realm, landscape (outside geography), multifaceted, meticulous,
intricate, paramount, transformative, elevate, embark, supercharge, harness, ever-evolving, unlock, navigate (outside UI
navigation), journey.

**Empty adverbs.** just, simply, actually, really, basically, literally, truly, fundamentally, importantly, crucially,
inherently, clearly, obviously. Delete each one unless it changes the meaning.

**Empty phrases.** in order to (write "to"), at this point in time (write "now"), due to the fact that (write
"because"), in terms of, with regard to, when it comes to, going forward, at the end of the day, the reality is.

**Em dashes.** Do not use them. Use a period, a comma, a colon before a list, or parentheses.

## Precision rules

- Give a location for every claim about the code: `path/file.ts:72`, a function name, or a config key.
- Give numbers with units: "3 one-minute periods", "about 25 messages each second". Do not write "quickly" or "a lot".
- Name the environment when behaviour differs between environments: "in prd", "in dev and stg".
- Quote log messages, metric names and error text exactly, in backticks.
- Do not state as fact what you did not check. Write "Not checked:" and the item.

## Workflow

1. Collect the facts: the code locations, the current behaviour, and the consequence. Read the code. Do not write from
   memory.
2. Write the title.
3. Write each section in the structure above.
4. Apply the STE rules and delete the fluff, sentence by sentence.
5. Run the check below. Fix each failure, then run the check again.
6. Run `issue-review` on the draft, if it is installed. Fold its findings into the draft.
7. File the issue, or give the draft to the user.

When the user gives you a draft to edit, keep their facts and their decisions. Change the words and the structure only.
Return the edited draft and a short list of the changes. If a fact is unclear, ask. Do not invent it.

## Check

Do each test on the final draft:

- [ ] The title is 70 characters or fewer, in present tense, with the names from the code.
- [ ] Each claim about the code has a location.
- [ ] No sentence in Change, Decisions or Acceptance is longer than 20 words. No sentence in Problem or Impact is longer
      than 25 words.
- [ ] Each requirement starts with a verb in the imperative.
- [ ] No passive sentence hides the actor.
- [ ] Each thing has one name everywhere in the issue.
- [ ] No banned word, empty adverb, empty phrase, em dash or emoji remains.
- [ ] No sentence tells the reader what to think in place of a fact.
- [ ] Each acceptance criterion is a thing that a reviewer can see: a test, a snapshot, an alert or a doc diff.
- [ ] If you delete any sentence, the implementer loses information. (Test each sentence. Delete it if not.)

## Example

Before:

> **Fix outbox delete handling**
>
> Hey team! While looking into some flaky metrics, I noticed something interesting. It seems like the outbox drainer
> might be robustly handling errors in a way that's a bit misleading — essentially, when a delete fails, it's being
> reported as a publish failure. This is a pretty critical issue for observability going forward. We should probably
> consider splitting these out and maybe adding some monitoring around it.

After:

> **Outbox drainer reports a failed delete as a failed publish**
>
> ## Problem
>
> `OutboxDrainer.drainOnce` (`outbox-drainer.ts:72-84`) calls `publish` and `store.delete` in one `try`.
> When `publish` succeeds and `delete` fails, the `catch` logs `outbox publish failed` and increments
> `outbox.publish.failures`. Both are false. The message is on the queue.
>
> ## Impact
>
> - A table fault shows as a queue fault, so triage goes to the wrong dependency.
> - When deletes continue to fail, the drainer sends the same oldest 25 rows each second. Newer rows do not drain.
>
> ## Change
>
> - Catch `publish` failures and `delete` failures separately.
> - On a delete failure, log `outbox delete failed after publish` with `idempotencyKey`.
> - Count delete failures on `outbox.delete.failures`.
> - Add `OutboxDeleteFailedAlarm`, with the same threshold and periods as `OutboxPublishFailedAlarm`.
>
> ## Acceptance
>
> - A unit test: the delete fails, the delete failure is counted, the row stays.
> - The infra snapshot contains `OutboxDeleteFailedAlarm`.

## Credits

The fluff patterns, the banned words and the empty phrases adapt [no-ai-slop](https://github.com/petergyang/no-ai-slop)
by Peter Yang, MIT License. The sentence and word rules follow the writing rules of ASD-STE100 Simplified Technical
English.
