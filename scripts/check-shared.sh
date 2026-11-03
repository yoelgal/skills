#!/usr/bin/env sh
# Fails when the copies of a shared reference file differ.
set -eu
cmp skills/issue-writing/references/writing-rules.md skills/pr-writing/references/writing-rules.md
