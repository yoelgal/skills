---
name: issue-writing
description: >-
  Write or edit an issue or ticket in plain prose that follows the rules of ASD-STE100 Simplified Technical English.
  Use when you file a bug, write a ticket from a finding, or rewrite an issue that is hard to act on. Trigger phrases:
  write an issue, file a ticket, draft an issue, clean up this ticket, rewrite this issue, issue writing.
---

# Issue writing

An issue is an instruction to an engineer who does not have your context. The engineer reads it once, then uses it as
the specification. Each sentence must give that engineer a fact, a consequence, a requirement or a decision. Delete all
other sentences.

This skill controls the words and the structure. The `issue-review` skill controls the content: coverage, impact,
docs and scope. Write with this skill, review with `issue-review`, then file.

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

- Write: `Crate shipper reports a failed unload as a failed shipment`
- Do not write: `Fix banana issue`, `[BUG] Improve error handling in shipper`, `Investigate unload failures 🍌`

## Writing rules

Read [references/writing-rules.md](references/writing-rules.md) before you write, and apply every rule in it. Sentence limits in an issue: 20 words or
fewer in Change, Decisions and Acceptance, and 25 words or fewer in Problem and Impact.

## Workflow

1. Collect the facts: the code locations, the current behaviour, and the consequence. Read the code. Do not write from
   memory.
2. Run `issue-review` on the draft, if the user has it. Fold its findings into the draft.
3. File the issue, or give the draft to the user.

When the user gives you a draft to edit, keep their facts and their decisions. Change the words and the structure only.
Return the edited draft and a short list of the changes. If a fact is unclear, ask. Do not invent it.

## Example

> **Crate shipper reports a failed unload as a failed shipment**
>
> ## Problem
>
> `CrateShipper.shipOnce` (`crate-shipper.ts:72-84`) calls `ship` and `warehouse.unload` in one `try`. When `ship`
> succeeds and `unload` fails, the `catch` logs `crate shipment failed` and increments `crates.ship.failures`. Both are
> false. The bananas are at the market.
>
> ## Impact
>
> - A warehouse fault shows as a market fault, so triage goes to the wrong dependency.
> - When unloads continue to fail, the shipper sends the same oldest 25 crates each second. Newer crates do not ship.
>
> ## Change
>
> - Catch `ship` failures and `unload` failures separately.
> - On an unload failure, log `crate unload failed after shipment` with `crateId`.
> - Count unload failures on `crates.unload.failures`.
> - Add `CrateUnloadFailedAlarm`, with the same threshold and periods as `CrateShipFailedAlarm`.
>
> ## Acceptance
>
> - A unit test: the unload fails, the shipper counts an unload failure, the crate stays.
> - The infra snapshot contains `CrateUnloadFailedAlarm`.
