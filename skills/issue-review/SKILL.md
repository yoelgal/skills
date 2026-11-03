---
name: issue-review
description:
  Review an issue or ticket for what its draft missed, before it is filed or before work starts. It checks factual
  claims against the code, alerting and detection coverage, how the failure behaves when it persists, the docs and
  runbooks that must change, operational premises, decisions left open, and scope. Use when writing or filing an issue,
  reviewing someone else's ticket, or picking up a ticket to implement, in any tracker (Linear, GitHub, Jira) and any
  codebase. Triggers on "review this issue", "review the ticket", "what did this ticket miss", "tighten this ticket",
  "issue review", or before creating an issue from a finding.
---

# Issue review

A first-draft ticket describes the bug its writer saw. It usually misses what the fix touches beyond the bug: the alarm
that was quietly covering it, the runbook an on-call engineer will open, the doc that counts the thing being changed,
the decision nobody wrote down. This review finds those before an implementer does, or before a reviewer finds them in
the PR.

The output is a short numbered list of gaps headed **Where it needs tightening**. Each gap carries evidence, why it
matters, and the exact edit to the ticket. Today's behaviour, if the ticket doesn't change it, is not a reason to block
the ticket. Say so, and keep the gap.

This skill checks what an issue says. The `issue-writing` skill controls how the issue says it. When you edit the issue
after the review, apply `issue-writing` to the text you change.

## Inputs

- The issue: fetch it from the tracker, read a draft the user pasted, or write the draft first when the user is filing a
  finding.
- The code: the checkout the issue is about. Every check below reads the code. A review done from the ticket text alone
  repeats the ticket's mistakes.
- The repo's own rules: `CONTRIBUTING.md`, `AGENTS.md`/`CLAUDE.md`, and the nearest nested ones. They often say which
  docs must change with which code, and that list is part of the review.

## Checks

Run every check. Most issues fail two or three of them. Record a finding only with evidence: a `file:line`, a command
and its output, or a quoted line of the ticket.

### 1. Claims match the code

Verify every factual statement in the ticket: file paths and line numbers, function and metric names, current behaviour,
environments and stages, counts, defaults. Read the code that sets each one, such as the config that turns a feature on
per environment. Don't trust a doc that describes it, since docs drift. A wrong claim in a ticket gets copied into the
fix, the docs and the next ticket. If you wrote the ticket yourself, check it with the same rigour.

### 2. Detection coverage survives the change

When the change moves, splits, renames, re-labels or removes a signal (a metric, log line, error code, event or status),
find everything that consumed the old signal: alerts, dashboards, SLOs, log-based metrics, scripts, agent skills. Then
answer:

- What alerted on this failure before the change, and how fast?
- After the change, what alerts on it, how fast, and does the alert point at the right runbook section?
- Does the ticket make the new alert **required**? Wording such as "add an alarm if one exists" or "consider alerting"
  is a gap whenever an alert does exist or is needed. Rewrite it as a requirement in the acceptance criteria.

A fix that makes a signal more accurate can also make it silent.

### 3. The failure mode when it persists

Tickets describe one occurrence ("one harmless duplicate", "a single retry"). Work out what happens when the fault lasts
for an hour:

- Retry and polling loops: what repeats, how often, and against what?
- Ordering: does a stuck item block everything behind it, as in an oldest-first read or a FIFO queue?
- Amplification: does each cycle send load downstream, such as duplicates, idempotent calls or writes?
- Who notices, and when?

If the real impact is worse than the ticket says, rewrite the Impact section. Severity and paging follow from it.

### 4. Severity and alerting mapped to config

"Pages at P1", "critical" and "notify on-call" mean nothing until they are mapped to the codebase's alert config. Find
how the existing comparable alerts set severity or paging: an explicit field, a router default per environment, or a
topic or channel. State the concrete setting in the ticket, including which environments page.

### 5. Docs blast radius

Grep the repo for every identifier the change touches: metric names, alert names, log messages, config keys, file and
component names. Also find every place that **lists or counts** them. List each hit the change must update:

- runbooks: alert tables, log-message tables, triage steps, verify steps, intros that say "the three alarms"
- observability docs: metric tables, alert tables, totals ("that is N alarms")
- runbook and alert indexes
- dashboards defined in code
- agent skills and automation that name alerts, metrics or counts
- READMEs and architecture docs

A count or a list that the change makes wrong is a finding, even several files away. If the repo's rules say docs ship
in the same change, the ticket lists them.

### 6. The operator's premise holds

Runbook remedies in tickets are often guesses: "check the role has permission X", "check the queue URL". Verify each one
against the infra code. Is the permission already granted? Can the setting actually drift? Point the remedy at the
likely causes, such as throttling, quotas, system errors or the dependency's own health, and name where the operator
sees them (which dashboard widget, which metric).

### 7. Decisions left open

List every choice the implementer would otherwise make silently:

- return values and counters in edge cases
- metric attributes and labels, matching the sibling metrics
- log message wording and the fields that identify the item
- names: the alarm, the metric, the config key
- defaults and backwards compatibility

Write each as "pick one:" with the options and a recommendation. Note which ones only tests observe; those are cheap
either way, but they still get decided.

### 8. Scope

- Pre-existing problems found during the review (stale docs, wrong counts, drift) go in a **separate ticket**, linked,
  unless the change can't be correct without fixing them. Say in each ticket what the other one owns.
- A change that mixes a refactor with a behaviour change is two tickets.
- Note the follow-ups the review raises and doesn't resolve, such as backoff on a persistent failure. Write them as
  questions for the owner, not as scope creep.

### 9. Acceptance is checkable

Each acceptance criterion maps to a test, a snapshot, or a doc diff a reviewer can see. Rewrite "works correctly" or "is
monitored" as observable outcomes. Bug fixes need a regression test that fails without the fix.

## Output

```markdown
**Where it needs tightening:**

1. **<Short title, stated as the fix.>** <Evidence: file:line or quoted ticket text.> <Why it matters, in one or two
   sentences.> <The ticket edit: what to add or change in the description or acceptance.>
2. ...

**Decisions to make:** <each open choice, with options and a recommendation>

**Out of scope / separate ticket:** <pre-existing drift, follow-ups>
```

Order the items by consequence, with lost detection and understated impact first. Skip a check that found nothing. Don't
pad the list.

## Applying it

- **Filing a new issue:** run the review on your own draft and fold the fixes into it before filing. Don't file the
  draft and comment on it.
- **Reviewing someone's issue:** post the review as a comment on the issue. Edit the description only if the user asks.
- **Starting implementation:** settle every item under "Decisions to make" with the owner before writing code, then
  record the decisions on the issue.
- **After implementation:** run it again against the branch. Anything the ticket missed and the branch fixed is worth a
  comment, so the ticket explains the PR.

## Example (anonymised)

> **Ticket:** "The outbox drainer wraps `publish` and `delete` in one `try`, so a failed delete is logged and counted as
> a failed publish. Split them and add a `delete.failures` metric; add it to alarms if one exists."
>
> **Where it needs tightening:**
>
> 1. **The alarm is required, not optional.** `PublishFailedAlarm` (`alarms.ts:48`, threshold 0 for 3 minutes) is what
>    fires today when deletes fail. Moving delete failures to an unalarmed metric leaves only the backlog alarm, which
>    is slower and points at the wrong runbook section. Acceptance: add `DeleteFailedAlarm`, or alarm on both metrics.
> 2. **A persistent delete failure is worse than one duplicate.** The drainer reads oldest first, so it re-sends the
>    same oldest batch every cycle and newer rows never drain. That's today's behaviour too, so it doesn't block the
>    ticket, but the new alarm pages at the same severity as the other outbox alarms.
> 3. **The runbook is missing.** The outbox runbook needs the new alarm in its alarm table, the new log line in its log
>    table, and a "delete fails" triage case that points at the table, not the queue.
> 4. **The metrics doc needs a row** for the new metric (`observability.md:69`), and the alarm total further down
>    changes too.
>
> **Decisions to make:** what `drainOnce` returns on a delete failure. Pick one: count it in `failed` (the row stays;
> recommended), or add a separate count. Only tests read it.
