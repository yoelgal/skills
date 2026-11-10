---
name: pr-writing
description:
  Write or edit a pull request title and description in plain prose that follows the rules of ASD-STE100 Simplified
  Technical English. Use when you open a pull request, or rewrite or update a description. Trigger phrases: write the
  PR description, PR body, describe this PR, rewrite the PR description, pr writing.
---

# PR writing

A PR description is the reviewer's guide to the diff. The reviewer reads it once, then reads the diff with it beside
them. Each sentence must give that reviewer a fact, a consequence, a decision or a piece of evidence. Delete all other
sentences.

The description is also where the reasons for the code go. A reason that does not earn a code comment (why the author
chose against an alternative, where a value came from, what another team does) goes here.

## Structure

Use these sections, in this order. Problem and Change are the default. Add another section only when it holds a fact the
reviewer cannot get from the diff. Do not add other sections. Another skill may append its own sections (a review table,
a model line) after Follow-ups.

```markdown
<Ticket link, one line, when the repo links tickets this way.>

## Problem

<What the code did before this change, with file:line. What was wrong with that.>

## Change

<What the change does, one item per bullet, in the present tense. Each decision a reviewer could question, with its
reason.>

## Tests

<The tests that prove the change, one per bullet: what each one checks, and whether it fails without the change.>

## Verification

<Only when the rule on runs outside CI applies: the command and its trimmed output, before and after the change.>

## Not changed

<Each thing a reviewer could expect this change to touch and it does not: a doc, a changeset, a migration. Give the
reason for each.>

## Follow-ups

<Each problem found and left out of scope, with a location and the ticket that holds it, if one exists.>
```

**Title.** Follow the repo's title format first: look at recent merged PRs for the prefix, the scope and the ticket
format. In the words after the prefix, state the result in the present tense, with the names from the code. Keep the
title to 72 characters or fewer when the format allows it.

- Write: `fix(peeler): peel a banana once when two orders for it arrive together`
- Do not write: `fix: race condition`, `Fix ENG-123`, `Improve banana handling 🍌`

## Length

Size the description to the diff. A small change gets a few sentences. Do not walk through the diff file by file, and do
not repeat what the code shows. Say what changed and why. If a sentence still makes sense with the diff closed, it
belongs. If it only narrates the diff, delete it.

## Writing rules

Read [references/writing-rules.md](references/writing-rules.md) before you write, and apply every rule in it. Sentence limits in a PR description: 25
words or fewer in Problem, and 20 words or fewer in every other section.

## PR rules

- Describe the current state of the change. After review changes, rewrite the description to match the code. Do not
  write "Round 2", "previously" or "now also". The commits and the review threads hold the history.
- If a test passes without the change, say what it guards.
- Do not list a check that CI runs, such as the test suite, lint or a typecheck, and never write "tests pass". List a
  check only when CI does not run it, such as a mutation test score.
- Add Verification when the change alters a contract that a caller depends on, such as an API, an error or an event. Add
  it too when the change depends on a real system that the tests mock. Run the built code against that system or a local
  stand-in, and show the result before and after the change. If a test already runs the real path end to end, name it in
  Tests in its place. If you could not run it, write "Not checked:" and the reason. For any other change, omit
  Verification.
- If the change alters a contract, name each caller of it and say what the change does to that caller.
- Do not claim more than the change does. If the change fixes one case, name the cases it does not fix under Follow-ups.
- Before you submit, check the title and the description for secrets and private details.

## Workflow

1. Collect the facts: the diff against the base branch, the ticket and the checks that CI does not run. Read the diff.
   Do not write from memory.
2. Give the title and the description to the skill or the person that opens the PR, or update the open PR.

When the user gives you a draft to edit, keep their facts and their decisions. Change the words and the structure only.
Return the edited draft and a short list of the changes. If a fact is unclear, ask. Do not invent it.

## Example

> **fix(peeler): peel a banana once when two orders for it arrive together**
>
> ## Problem
>
> `InMemoryPeeler.peel` (`in-memory-peeler.ts:84`) records the banana id after it awaits `removeSkin`. Two concurrent
> orders for one banana both pass the id check, so the peeler peels it twice.
>
> ## Change
>
> - `peel` records the id and the pending peel before the first await.
> - A concurrent order for the same banana and style returns the same peel.
> - A concurrent order for the same banana with a different style fails with `conflict`.
> - If the peel fails, `peel` deletes the id, so a retry can peel.
>
> ## Tests
>
> - Two concurrent orders for one banana: one peel, one id. Fails without the change.
> - Two concurrent orders for one banana with different styles: the second gets `conflict`. Fails without the change.
>
> ## Follow-ups
>
> - `LocalPeeler.removeSkin` (`local-peeler.ts:36`) loses an update when orders for two bananas touch one bunch.
