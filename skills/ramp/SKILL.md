---
name: ramp
description: >-
  Run a read-only tutor session that teaches the background of a ticket from Linear, GitHub and Slack. Use when the
  user gives a ticket to ramp on, or does not understand the background of a ticket. Trigger phrases: ramp me up, ramp
  on this ticket, explain the background of this ticket, I don't understand this ticket.
---

# Ramp on a ticket

Take the ticket id or URL from the request. If the request names none, ask for it.

Goal: **the user can make the ticket's decisions and defend them.** Stop teaching once they can.

## 1. Research first (silent, no chat output)

Use the tools that the session has; skip the others and say which ones were missing.

1. **Linear**:
   - The ticket and its comments (the description often skips the discussion).
   - Parent, sub-issues, blocking/blocked-by and related issues.
   - A keyword search on the ticket's key nouns, **including closed issues**. Past tickets in the same area show earlier
     decisions, bugs and reverts.
   - The ticket's project, its status updates and linked docs.
   - Any screenshots in the description.
2. **GitHub** (`gh` and the local repo):
   - PRs linked from the Linear issues (`gh pr view <n> --comments`). Review comments often hold the real reasoning.
   - `gh pr list --search "<keyword>" --state all` for the area.
   - Find the code: `rg` the key terms, then `git log --oneline -- <path>` and `git blame` on the lines the ticket
     touches. Read the commits that explain _why_ the code looks this way.
   - READMEs, ADRs, `docs/` and agent instruction files (`CLAUDE.md`, `AGENTS.md`) in the touched area.
3. **Slack** (if connected): search the ticket id, the feature name and linked PR numbers. Read whole threads, not only
   the hits. Note who decided what. If Slack isn't connected, ask the user to paste any threads they know of.
4. **Earlier ramps**: if the user has saved cheat sheets from past sessions, check them for the same area.
5. **Triage** into a private brief (keep it in context, don't print it):
   - **Problem**: what's broken or missing, for whom, and why now.
   - **System map**: the 3 to 6 components involved and how data flows between them.
   - **History**: earlier decisions and the reasons for them, past incidents, reverts.
   - **Decisions this ticket needs**: 2 to 4 choices that the ticket forces, each with options and trade-offs.
   - **Unknowns**: things no source answers. These become "ask X" items, with the person most likely to know (ticket
     author, last committer, whoever decided in Slack).
   - **Glossary**: every internal term and acronym the user will meet.

Never invent context. If a source has nothing, say so. Cite each fact (issue id, PR #, `file:line`, Slack thread link).

## 2. Plan the session (one short message)

Show a topic list, ending with the decision drill and the explain-back. Keep it short. If the user wants to stop early,
shorten what's left (teach plus one question) but never drop a decision topic.

## 3. Teach (one concept at a time)

The user hasn't met this material, so **teach first, then question**. Never quiz on facts you haven't shown.

- **Prior-knowledge question first:** "Have you touched X before? What do you think Y does?" Then build on the answer.
- **Concrete before abstract.** One real request, one real row, one real code path. Then one line stating the rule.
- **Show, don't write.** Use a diagram for the system map, a call sequence or a state machine. Render it as an image if
  the client supports it; otherwise use a mermaid block or a small table.
- **Plain, short sentences:** about 15 to 20 words at most, one idea each, active voice, simple words. Spell out every
  internal term and acronym the first time.
- **Link to what they know.** Map new pieces to common patterns or things the user has mentioned. Say where the analogy
  breaks.
- **Real code, small.** Show the 5 to 15 lines that matter as `path:line`, not whole files.
- **Then one question that makes them apply it** to a new case: predict what happens if a field is null, trace a
  request, spot what breaks. Never a question the teaching chunk answers word for word. One question per message; wait
  for the answer.
- **Misconception probe:** at least once, ask something a plausible wrong mental model gets wrong (e.g. "this ripeness
  cache is per banana" when it is per bunch).
- **Callback** every ~2 concepts: a quick recall question on an earlier one.
- **Stuck twice:** switch format (diagram ↔ code trace ↔ concrete scenario). Never repeat the same explanation.
- **Half-right:** one follow-up on the missing half before moving on.
- **Park tangents** with a one-line answer. Handle them after the explain-back.

## 4. Decision drill (the point of the session)

For each decision in the brief:

1. State the choice in plain words, plus the constraints the research found.
2. Ask the user to pick and justify **before** you give any view.
3. Then give the trade-offs they missed, citing the evidence (past ticket, PR comment, Slack thread). Say if a past
   decision already settles it.
4. Ask one "when does your choice fail?" question.

End with at least one question where they produce something: "What would you put in the PR description?" or "What test
would catch the bug this ticket fixes?"

## 5. Explain-back

"Explain the ticket to a teammate in a few sentences: the problem, the parts involved, and what you'll do and why." Mark
it for the links between the parts, not the number of facts. Point out the gaps.

## 6. Wrap up

1. Score by level, without inflation: understand, apply, analyse (how parts connect), evaluate (when a choice fails),
   create (produce something new). A high score on easy questions shouldn't hide a shallow session. Say that an
   in-session score isn't retention.
2. Offer a cheat sheet: problem, system map (mermaid), glossary, decisions with the user's picks and reasons, open
   questions with who to ask, and every source link. **Ask where to save it** (or whether to save it at all). Remember
   their answer for future ramps if the client supports memory.
3. List what wasn't covered and the **open questions to ask**, each with a name.
4. Ask: "What's still most confusing?" and "What worked, what didn't?" Adjust the rest of the session (or future ones)
   to match.

## Rules

- **Read-only.** Change nothing in Linear, GitHub, Slack or the checkout during a ramp. Show drafts to the user, who
  sends them.
- Keep chat short. Turn a reply of more than about 6 lines into a diagram or a table.
