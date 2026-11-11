#!/usr/bin/env sh
# Fails when the copies of a shared reference file differ.
set -eu
for skill in issue-writing issue-review; do
  cmp "skills/$skill/references/writing-rules.md" skills/pr-writing/references/writing-rules.md
done
