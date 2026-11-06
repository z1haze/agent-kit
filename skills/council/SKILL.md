---
name: council
description: Run a review brief past several models at once, as configured in the user's council.md. Invoked by the review contract's Council mode, or when the user says "council".
---

# Council

A council runs one review brief past several reviewers (**seats**) and returns each reply. It belongs to the kit, but
its seats are personal: which models, where they run, and what they may cost come from the user's **config**, not
from here. Every step below says what to do when something it needs is missing; none of them is a reason to stop
except where it says to reply `council unavailable`.

## Config

The config is the first of these that exists: `$CLAUDE_CONFIG_DIR/council.md`, `~/.claude/council.md`. Its format is
`${CLAUDE_PLUGIN_ROOT}/templates/council.md`.

- **No config**: reply `council unavailable: no council.md` and stop. The review contract then runs its fallback.
- Read `members`, `fallback` and the optional `budget_usd` from it. The **spend limit** for this review is the lower
  of the caller's **Paid seats** cap (from the repo's profile) and `budget_usd`; with no cap from the caller, it is 0
  and no `via: api` seat can run.
- Never put a different model, instance or effort in a seat than the one the config names.

## Seat check

Before anything is sent, check each `members` seat by its `via`, and state in one line which seats run and why.

- **`via: api`** (one OpenRouter request): run `python3 -I ${CLAUDE_SKILL_DIR}/oneshot.py check`.
  - Exit 2 (no key) or 4 (refused): the seat can't run.
  - The spend limit is 0, or `ok` but the credit or the key's remaining limit is under the spend limit: the seat
    can't run.
- **`via: t3`** (a T3 Code agent thread): the `t3-code` MCP tools must be listed, and `orchestrator_capabilities`
  must resolve the seat's model on its `instance`.
  - No T3 tools, and the model is a Claude model: the seat runs as a local `agent-kit:reviewer` subagent instead, with
    the seat's model, on this session's account. Say so: the `instance` pin doesn't hold outside T3.
  - No T3 tools, and the model isn't Claude: the seat can't run.
  - T3 is there but the model doesn't resolve on that instance: the seat can't run.

Then:

- Every `members` seat can run: run **members**.
- Otherwise check the `fallback` seats the same way. Every one can run: run **fallback**, saying which member failed
  and why.
- Neither: reply `council unavailable: <each seat that failed, and why>` and stop.

The list chosen at round 1 holds for every round. If a seat fails in a later round, retry it once; if it still fails,
switch to fallback from that round and say so.

## Run the seats

All seats of a round run in parallel. Don't edit the reviewed files while a review runs. A fallback seat gets the
brief plus `Lens: <its lens>`; a member seat gets the brief word for word.

- **`via: t3`**: `delegate_task` on the seat's instance and model, at its effort (`role: "review"`, `mode: "async"`,
  a new `clientRequestId` each round). Save each `taskId`; wait for the notices, don't poll.
- **Local subagent** (a `t3` seat outside T3): spawn an `agent-kit:reviewer` with the seat's model and the brief.
- **`via: api`**: write the brief to a temp file and run, as a background shell command,
  `python3 -I ${CLAUDE_SKILL_DIR}/oneshot.py review --model <model> --effort <effort> --repo <repo> --base <base>
  --brief <file> --max-usd <spend limit left>`. Add `--paths <the target's paths>` when the brief limits the target to
  paths, `--include <each Read-first file>`, and from round 2 `--base <last round's commit>`. Wait for it to exit.
  - Exit 3: the estimate is over the spend limit left. Ask the user before going over; otherwise the seat gets
    `no reply`.
  - It stops with "over the cap": the target is too big for one request. Retry once with `--paths` narrowed to the
    files the brief's target changed most; still too big: `no reply`.
  - Exit 4: OpenRouter refused or failed; retry once, then `no reply`.
  - Add each reply's `cost_usd` to the run's spend.

A seat that times out, errors or returns nothing is not approval: retry it once, then mark it `no reply`.

## Return

Each seat's reply unchanged, labelled with its name, its lens (fallback seats), its model, where it ran, and the effort
it ran with (`effort not exposed` when the route doesn't say). The caller verifies the findings and decides the next
round under its own rules. Seats keep no history: each round starts each seat fresh with the
caller's new brief.

When the user said "council" directly, with no brief: run `${CLAUDE_PLUGIN_ROOT}/reference/review-contract.md` with
this council as its reviewers.

## Report

A table with a row per seat and a column per round: verdict and score, `no score` when a seat gave none (never invent
one), `no reply` when it failed. Then which list ran and why, where each seat ran, each api seat's cost, and the
run's total spend against the spend limit.
