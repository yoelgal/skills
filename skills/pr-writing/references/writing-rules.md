# Writing rules

Shared by the `issue-writing` and `pr-writing` skills. The two copies of this file must stay identical. Run
`scripts/check-shared.sh` from the repo root after an edit.

## STE writing rules

### Words

- Use one term for one thing. Use the name from the code (the metric name, the class name, the alarm name). Repeat it.
  Do not use synonyms for variety.
- Describe what a thing is, not what it is not: "the crate stays in the warehouse", not "the crate is not lost".
- Give a word only one meaning. If "check" is a verb, do not also use it as a noun for a CI job.
- Use the simplest common word: "use", not "utilize"; "start", not "initiate"; "show", not "demonstrate"; "help", not
  "facilitate"; "about", not "approximately".
- Write the full verb, not a noun made from a verb: "decide", not "make a decision"; "the shipper unloads the crate",
  not "the unloading of the crate is performed".
- Keep noun clusters to three words or fewer. "crate unload failure count" is the limit. Break longer clusters with
  "of", "for" or a relative clause.
- Do not use contractions: "do not", not "don't".
- Use technical names (code identifiers, product names, error codes) as they are, in backticks.

### Sentences

- Write one idea per sentence.
- Use the active voice. Name the actor: "The shipper unloads the crate", not "The crate is unloaded".
- Use the simple tenses: simple present, simple past, future with "will". Do not use progressive forms such as "is
  failing" or "has been failing".
- Do not use "-ing" words as verbs or nouns, except in technical names. Write "when the unload fails", not "on failing
  to unload".
- Write requirements in the imperative: "Add an alarm", not "An alarm should be added" or "We might want to add an
  alarm".
- Keep the articles ("the", "a"). Do not write in telegraphic style.
- Put a condition before the instruction: "If the unload fails, log the crate's id."

### Paragraphs and lists

- Give each paragraph one topic. Use six sentences or fewer.
- Use a list for three or more parallel items, or for steps. Use prose for one or two items.
- Write list items in the same grammatical form. Start each requirement with a verb.

## Fluff to delete

Delete these on sight. Each one delays the reader or tells the reader what to think in place of a fact.

**Openers and meta-text.** "This ticket aims to", "This PR", "The purpose of this issue is", "As discussed", "Just a
heads-up", "Context:", "TL;DR", "Background" over a section that only repeats the Problem. Start with the fact.

**Hedges without a reason.** "Maybe", "possibly", "might", "it seems", "we may want to", "consider". Keep a hedge only
when there is a real unknown, and write the unknown as a fact: "The cause is not known. The logs from 02:00 to 03:00 are
missing."

**Puffery and labels.** "critical", "crucial", "important to note", "significant", "major issue", "a testament to",
"plays a key role". Show the consequence and let the reader judge it: write "Newer crates do not ship while the fault
continues", not "This is a critical issue".

**Interpretive metadiscourse.** "The key point is", "Note that", "It is worth noting", "As you can see", "This
distinction matters". Delete the aside and keep the fact.

**Weasel attribution.** "People say", "it is widely known", "best practice says". Name the source (a doc, a person, a
file:line), or delete the claim.

**Binary contrast and colon reveals.** "This is not X, it is Y." "The real problem: the unload." State Y directly: "The
unload fails."

**Contrast language.** "rather than X", "instead of Y", "as opposed to Z". State what the thing is or does. Write "The
shipper keeps the crate", not "The shipper keeps the crate rather than dropping it".

**Trailing -ing analysis.** "...highlighting the need for better monitoring." Replace it with the consequence: "...so no
alarm fires."

**Recap endings and kickers.** "In summary", "Overall", "Ultimately", or a last line that restates the text above it.
End on the last requirement or acceptance criterion.

**Narrative and provenance.** How the bug was found, who noticed it, how long the search took. Put it in a comment on
the issue or PR if it helps. The description holds only what the reader needs to act.

**Formatting noise.** Emoji, ALL CAPS for emphasis, bold inside sentences for emphasis, headings over one-sentence
sections, horizontal rules, nested bullets deeper than two levels. Use bold only for a list item's label.

**Banned words.** delve, foster, leverage, utilize, facilitate, empower, streamline, robust, seamless, cutting-edge,
holistic, synergy, paradigm, game changer, tapestry, realm, landscape (outside geography), multifaceted, meticulous,
intricate, paramount, transformative, elevate, embark, supercharge, harness, ever-evolving, unlock, navigate (outside UI
navigation), journey.

**Empty adverbs.** just, simply, actually, really, basically, literally, truly, fundamentally, importantly, crucially,
inherently, clearly, obviously. Delete each one unless it changes the meaning.

**Empty phrases.** in order to (write "to"), at this point in time (write "now"), due to the fact that (write
"because"), in terms of, with regard to, when it comes to, going forward, at the end of the day, the reality is.

**Em dashes.** Do not use them. Use a period, a comma, a colon before a list, or parentheses.

## Precision rules

- Give a location for every claim about the code: `path/file.ts:72`, a function name, or a config key.
- Give numbers with units: "3 one-minute periods", "about 25 messages each second". Do not write "quickly" or "a lot".
- Name the environment when behaviour differs between environments: "in prd", "in dev and stg".
- Quote log messages, metric names and error text exactly, in backticks.
- Do not state as fact what you did not check. Write "Not checked:" and the item.
