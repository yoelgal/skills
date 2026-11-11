---
name: pr-writing
description: >-
  Write or edit a pull request title and description in the author's voice: short, plain, and readable by someone new
  to the repo. Use when you open a pull request, or rewrite or update a description. Trigger phrases: write the PR
  description, PR body, describe this PR, rewrite the PR description, pr writing.
---

# PR writing

A reviewer reads the description once, then reads the diff. The description tells them what was wrong, what the change
does and why they can trust it. The diff and CI carry everything else.

Read [references/writing-rules.md](references/writing-rules.md) before you write. It sets the voice, the plain-words
rules and the title rules. Its length rules matter most here.

## Budget

- Summary: 80 words or fewer.
- All prose: 200 words or fewer. Media, tables, code blocks and `<details>` blocks do not count.
- A design, a migration or a contract change with callers may use up to 350 words. Say in the summary why it is large.

Size the description to the diff. A small change gets a few sentences and no sections. If you are over budget, cut.

## Structure

```markdown
<Ticket line, when the repo links tickets this way: "Closes ENG-123".>

<Summary, no heading. What was broken, as a user or an operator sees it. Why. What the change does now. Say "Small one."
when it is.>

## Testing

<How the change is proved: the tests it adds and whether they fail without it, a check CI does not run, and before and
after output when the Verification rule below applies.>

## Notes

<One line each: a decision a reviewer could question, with its reason. Something a reviewer would expect this to change
and it does not. A follow-up, with its ticket.>
```

Omit a section with no content. Optionally end with `<details><summary>Details</summary>` holding depth a careful
reviewer might want: each test and what it guards, full output, real-speed videos. Another skill may append its own
section after Notes.

**Title.** Follow the repo's title format first: check recent merged PRs for the prefix, scope and ticket format. After
the prefix, follow the title rules in the writing rules, in 72 characters or fewer.

- Write: `fix(peeler): stop a banana from being peeled twice by two orders`
- Do not write: `fix(peeler): record the banana id before the first await in peel`, `fix: race condition`, `Fix ENG-123`

## Rules

- Open with the problem, never with a list of files.
- Describe the change as it is now. After review, rewrite the description to match. No "Round 2" or "now also".
- Tests: say how many the change adds and whether they fail without it. If a test passes without the change, say what
  it guards. Name a test only when its name tells the reviewer something the summary does not.
- Do not list a check that CI runs, such as the test suite, lint or a typecheck, and never write "tests pass". List a
  check only when CI does not run it, such as a mutation test score.
- Verification: when the change alters a contract a caller depends on (an API, an error, an event), or depends on a real
  system the tests mock, run the built code against that system or a local stand-in. Show the result before and after,
  in Testing. If you could not run it, write "Not checked:" and the reason. For any other change, skip it.
- If the change alters a contract, name each caller in Notes and say what the change does to it.
- Do not claim more than the change does.
- Check the title and the description for secrets and private details before you submit.

## Review history

A review skill such as `council` or `sol-loop` may append its results. Keep them to one visible line ("Council: 3
rounds, final scores 8.5, 8 and 9.5, all findings fixed.") and put any table or per-round findings in `<details>`.

## Workflow

1. Collect the facts: the diff against the base branch, the ticket, and any checks CI does not run. Read the diff.
2. Write the summary as if it were the whole description. Could the reviewer start on the diff now?
3. Add Testing and Notes only for what the reviewer would get wrong without them.
4. Cut to budget, then give the title and description to whoever opens the PR, or update the open PR.

When the user gives you a draft to edit, keep their facts and decisions. Change the words and the length. If a fact is
unclear, ask. Do not invent it.

## Example

Before (accurate, but a form, and twice as long as it needs to be):

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

After:

> **fix(peeler): stop a banana from being peeled twice by two orders**
>
> Two orders for the same banana at the same moment both got peeled, because `InMemoryPeeler.peel` recorded the banana
> only after its first await. It now records it up front, so the second order gets the same peel, or `conflict` if it
> asked for a different style. If the peel fails, the banana is freed so a retry can peel it.
>
> ## Testing
>
> 2 new tests for concurrent orders (same style, different style). Both fail without the change.
>
> ## Notes
>
> - `LocalPeeler.removeSkin` (`local-peeler.ts:36`) loses an update when orders for two bananas touch one bunch. Left
>   for a follow-up.

## Credits

The words to delete adapt [no-ai-slop](https://github.com/petergyang/no-ai-slop) by Peter Yang, MIT License.
