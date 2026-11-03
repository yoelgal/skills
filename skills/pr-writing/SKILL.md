---
name: pr-writing
description:
  Write or edit a pull request title and description in plain, fluff-free prose that follows the writing rules of
  ASD-STE100 Simplified Technical English (STE). The description says what was wrong, what the change does, how it was
  proved, and what it leaves out, so a reviewer can judge the diff without your context. Use when opening a PR, filling
  in a PR description for another skill such as file-pr, rewriting a PR description that is hard to review, or updating
  one after review changes. Triggers on "write the PR description", "PR body", "describe this PR", "rewrite the PR
  description", "pr writing".
---

# PR writing

A PR description is the reviewer's guide to the diff. The reviewer reads it once, then reads the diff with it beside
them. Each sentence must give that reviewer a fact, a consequence, a decision or a piece of evidence. Delete all other
sentences.

The description is also where the reasons for the code go. A reason that does not earn a code comment (why an
alternative was rejected, where a value came from, what another team does) goes here. Provenance goes in the ticket.

## Structure

Use these sections, in this order. Omit a section that has no content. Do not add other sections. Another skill may
append its own sections (a review table, a model line) after Follow-ups.

```markdown
<Ticket link, one line, when the repo links tickets this way.>

## Problem

<What the code did before this change, with file:line. What was wrong with that.>

## Change

<What the change does, one item per bullet, in the present tense. Each decision a reviewer could question, with its
reason.>

## Tests

<Each test the change adds or changes, one per bullet: what it checks, and whether it fails without the change.>

## Verification

<The exact commands that were run, and their results.>

## Not changed

<Each thing a reviewer could expect this change to touch and it does not: a doc, a changeset, a migration. Give the
reason for each.>

## Follow-ups

<Each problem found and left out of scope, with a location and the ticket that holds it, if one exists.>
```

**Title.** Follow the repo's title format first: look at recent merged PRs for the prefix, the scope and the ticket
format. In the words after the prefix, state the result in the present tense, with the names from the code. Keep the
title to 72 characters or fewer when the format allows it.

- Write: `fix(ledger): apply concurrent in-memory posts of one key once`
- Do not write: `fix: race condition`, `Fix ENG-123`, `Improve idempotency handling 🚀`

## Writing rules

Read [references/writing-rules.md](references/writing-rules.md) before you write, and apply every rule in it: the STE
rules, the fluff to delete and the precision rules. Sentence limits in a PR description: 25 words or fewer in Problem,
and 20 words or fewer in every other section.

## PR rules

- Open with the problem. Do not open with a list of the files you changed. The diff shows the files.
- Describe the current state of the change. After review changes, rewrite the description to match the code. Do not
  write "Round 2", "previously" or "now also". The commits and the review threads hold the history.
- For each test, say whether it fails without the change. If a test passes without the change, say so and say what it
  guards.
- Give the exact command for each check that was run, and its result with numbers: "`pnpm vitest run`: 1055 passed".
  Do not write "tests pass".
- Write "Not checked:" and the item for a check that was not run, for example an environment that was not deployed.
- Do not claim more than the change does. If the change fixes one case, name the cases it does not fix under
  Follow-ups.
- Put a code location on each claim about the code: `path/file.ts:72` or a function name.
- Before you submit, check the title and the description for secrets and private details.

## Workflow

1. Collect the facts: the diff against the base branch, the ticket, the test results and the checks that ran. Read the
   diff. Do not write from memory.
2. Write the title.
3. Write each section in the structure above.
4. Apply the writing rules and delete the fluff, sentence by sentence.
5. Run the check below. Fix each failure, then run the check again.
6. Give the title and the description to the skill or the person that opens the PR, or update the open PR.

When the user gives you a draft to edit, keep their facts and their decisions. Change the words and the structure only.
Return the edited draft and a short list of the changes. If a fact is unclear, ask. Do not invent it.

## Check

Do each test on the final draft:

- [ ] The title follows the repo's format, states the result in the present tense, and uses the names from the code.
- [ ] The description opens with the problem.
- [ ] Each claim about the code has a location.
- [ ] No sentence in Problem is longer than 25 words. No sentence in another section is longer than 20 words.
- [ ] Each test says whether it fails without the change.
- [ ] Each check in Verification has its exact command and its result.
- [ ] Nothing in the description describes an earlier version of the change.
- [ ] Each thing has one name everywhere in the description.
- [ ] No banned word, empty adverb, empty phrase, contrast phrase, ALL CAPS emphasis, em dash or emoji remains.
- [ ] If you delete any sentence, the reviewer loses information. (Test each sentence. Delete it if not.)

## Example

Before:

> **Fix race condition in ledger**
>
> This PR fixes a nasty race condition that could cause double-posting! 🎉 I refactored the post method to be more
> robust — essentially we now track in-flight commits rather than only finished ones. Also cleaned up some stuff and
> added tests. All tests pass. Round 2: addressed review feedback.

After:

> **fix(ledger): apply concurrent in-memory posts of one key once**
>
> ## Problem
>
> `InMemoryLedger.post` (`in-memory-ledger.ts:84`) records an idempotency key after it awaits `applyLegs`. Two
> concurrent posts of one key both pass the key check, so the legs apply twice.
>
> ## Change
>
> - `post` records the key and the pending commit before the first await.
> - A concurrent post of the same key and body returns the same commit.
> - A concurrent post of the same key with a different body fails with `conflict`.
> - If the commit fails, `post` deletes the key, so a retry can post.
>
> ## Tests
>
> - Two concurrent posts of one key: one posting, one id. Fails without the change.
> - Two concurrent posts of one key with different bodies: the second gets `conflict`. Fails without the change.
>
> ## Verification
>
> - `pnpm vitest run`: 1055 passed, 12 skipped.
> - `pnpm tsc --noEmit`: no errors.
>
> ## Follow-ups
>
> - `LocalLedger.applyLegs` (`local-ledger.ts:36`) loses an update when posts of different keys touch one account.

## Credits

The writing rules adapt the fluff patterns, the banned words and the empty phrases of
[no-ai-slop](https://github.com/petergyang/no-ai-slop) by Peter Yang, MIT License. The sentence and word rules follow
the writing rules of ASD-STE100 Simplified Technical English.
