---
name: issue-writing
description: >-
  Write or edit an issue or ticket in the author's voice: short, plain, and readable by someone new to the repo. Use
  when you file a bug, write a ticket from a finding, or rewrite an issue that is too long or hard to act on. Trigger
  phrases: write an issue, file a ticket, draft an issue, clean up this ticket, rewrite this issue, issue writing.
---

# Issue writing

An issue tells an engineer without your context what is wrong and what to change. They read it once, then work from it.

This skill controls the words and the length. The `issue-review` skill controls the content. Write with this skill,
review with `issue-review`, then file.

Read [references/writing-rules.md](references/writing-rules.md) before you write. It sets the voice, the plain-words
rules and the title rules.

## Budget

- Summary: 80 words or fewer.
- All prose: 200 words or fewer. Code blocks, logs and `<details>` blocks do not count.
- Put agent-only detail (file lists, implementation plans, reproduction logs) in a collapsed "Agent notes" section at
  the end. Keep it to what an implementer needs.

## Structure

```markdown
<Summary, no heading. What is wrong, as a user or an operator sees it, with the code location. Why. What it costs, and
what happens if it keeps happening.>

## Change

<What to do, one requirement per bullet, in the imperative.>

## Acceptance

<What a reviewer can see when it is done: a test, a snapshot, an alert, a doc change.>

## Decisions

<Optional. Each open choice: "Pick one:" with the options and a recommendation.>

## Out of scope

<Optional. What this issue does not do, and the issue that does.>
```

Omit an optional section when it is empty. Do not add other sections.

**Title.** State the defect or the result in the present tense, in 70 characters or fewer, following the title rules in
the writing rules.

- Write: `Failed crate unloads are reported as failed shipments`
- Do not write: `Fix banana issue`, `[BUG] Improve error handling in shipper`, `Investigate unload failures 🍌`

## Workflow

1. Collect the facts: the code locations, the current behaviour and the consequence. Read the code.
2. Write the summary as if it were the whole issue. Could an engineer start from it?
3. Add Change and Acceptance, then the optional sections if they have content. Cut to budget.
4. Run `issue-review` on the draft, if the user has it. Fold in its findings and stay within budget.
5. File the issue, or give the draft to the user.

When the user gives you a draft to edit, keep their facts and decisions. Change the words and the length. If a fact is
unclear, ask. Do not invent it.

## Example

> **Failed crate unloads are reported as failed shipments**
>
> `CrateShipper.shipOnce` (`crate-shipper.ts:72`) wraps `ship` and `warehouse.unload` in one `try`, so a failed unload
> logs `crate shipment failed` and counts on `crates.ship.failures`. Triage then goes to the market, not the warehouse.
> If unloads keep failing, the shipper re-sends the same oldest 25 crates every second and newer crates never ship.
>
> ## Change
>
> - Catch ship and unload failures separately.
> - On an unload failure, log `crate unload failed after shipment` with the `crateId`, and count it on
>   `crates.unload.failures`.
> - Add `CrateUnloadFailedAlarm`, with the same threshold as `CrateShipFailedAlarm`.
>
> ## Acceptance
>
> - A unit test where the unload fails: the unload failure is counted and the crate stays.
> - The infra snapshot contains `CrateUnloadFailedAlarm`.

## Credits

The words to delete adapt [no-ai-slop](https://github.com/petergyang/no-ai-slop) by Peter Yang, MIT License.
