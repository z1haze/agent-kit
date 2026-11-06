# Workflow

The profile `/slice`, `/idea` and `/audit` read (the agent-kit plugin). Each section heading below is one they refer to by
name; keep the headings.

- **Base branch**: `main`
- **Actors**: who uses what this repo ships, as reviewers name them in "noticed by" (e.g. customers, admins).
- **Packs**: the path of each rule pack this repo follows (a folder of rules shared by a family of repos, outside
  the kit), or none.

## Read

Docs every builder and reviewer reads first, in order: e.g. `CLAUDE.md`, `GLOSSARY.md`, `docs/DESIGN.md`.

## Gates

The commands that must all pass, exactly as run (e.g. `npm test`).

## Smoke

Each run with its command and the condition that triggers it in `/slice`, and where a new scenario goes. `/audit` runs
them all. "None" if the repo has none.

## Backlog

- **Where**: the file or tracker query holding the items.
- **Pick**: the rule `/slice` uses to propose the next item.
- **Item format**: how `/idea` writes one, and where detail that doesn't fit goes.
- **Never on the backlog**: what `/idea` refuses or splits off, if anything.

## Tracker

- **Spec**: where a spec lives, how to publish it, and how to find a branch's spec (first line `Branch: slice/<slug>`).
- **Close**: what closes a spec after the merge.
- **Slices since the last audit**: how to count them.

## Spec contents

What a spec here must also cover, beyond the template: actors to separate in User Stories, Implementation Decisions
items, what Assumptions and Out of Scope always name. "None" if the template is enough.

## Review

How every review in this repo stops, whoever reviews (agent-kit's `reference/review-contract.md`). Leave a line out
for its default.

- **Max rounds**: 3
- **Pass score**: none, or a score out of 10 every reviewer must reach before review stops.
- **Also required**: none, or conditions that must hold before review stops (e.g. "smoke passes").
- **Paid seats**: none, or the most one review may spend on paid council seats (e.g. `up to $3`).

## Docs

Every doc `/slice`'s Docs step checks against the diff, with when each applies.

## Commits

- **Style**: subject and body conventions, any trailer.
- **Audit commit**: how an audit commit's subject starts.
