# skills

Agent skills for Claude Code, Codex, Cursor and other agents that read `SKILL.md`.

| Skill                                            | What it does                                                                                                                                                              |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`issue-review`](skills/issue-review/SKILL.md)   | Reviews an issue or ticket for what the draft missed: alerting coverage, failure when it persists, docs blast radius, open decisions, scope                               |
| [`issue-writing`](skills/issue-writing/SKILL.md) | Writes issues in fluff-free prose that follows the ASD-STE100 Simplified Technical English rules, in a fixed Problem / Impact / Change / Decisions / Acceptance structure |

## Install

With the [`skills`](https://github.com/vercel-labs/skills) CLI (Node.js 22.20 or later):

```sh
# every skill in this repo, into the current project
npx skills add yoelgal/skills

# one skill, for every project (-g), for Claude Code
npx skills add yoelgal/skills --skill issue-review -g -a claude-code
```

## Layout

Each skill is `skills/<name>/SKILL.md`, with `name` and `description` frontmatter. Scaffold a new one with
`npx skills init <name>` inside `skills/`.

## Credits

`issue-writing` adapts parts of [no-ai-slop](https://github.com/petergyang/no-ai-slop) (MIT). See
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Licence

MIT. See [LICENSE](LICENSE).
