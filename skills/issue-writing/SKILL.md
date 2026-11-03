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

## Writing rules

Read [references/writing-rules.md](references/writing-rules.md) before you write, and apply every rule in it: the STE
rules, the fluff to delete and the precision rules. Sentence limits in an issue: 20 words or fewer in Change, Decisions
and Acceptance, and 25 words or fewer in Problem and Impact.

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
- [ ] No banned word, empty adverb, empty phrase, contrast phrase, ALL CAPS emphasis, em dash or emoji remains.
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
