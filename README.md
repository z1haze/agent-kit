# agent-kit

A Claude Code plugin for building software in small, reviewed slices. It owns the process; each repo describes
itself in a few files under `docs/agents/`.

## Commands

| Command | What it does |
|---|---|
| `/agent-kit:setup` | Checks this machine and repo, drafts the repo's profile if it has none, and optionally sets up council |
| `/agent-kit:idea` | Adds an idea to the backlog as one slice-ready item |
| `/agent-kit:slice` | Walks the next slice: pick, grill, test plan, spec, build, review, merge. Each run resumes where the last stopped |
| `/agent-kit:audit [full]` | After every third slice: reviews what the slices changed together, for what a per-slice review can't see |

## Install

```
/plugin marketplace add z1haze/agent-kit
/plugin install agent-kit@agent-kit
```

A repo can also list the plugin in its `.claude/settings.json`, so Claude Code offers to install it when the folder
is trusted. It installs the `mattpocock-skills` plugin it depends on. For a private copy of this repo, your git needs
to reach it without a prompt (`gh auth login`, then `gh auth setup-git`).

Then run `/agent-kit:setup` inside the repo.

## What lives where

| | Where | Shared with |
|---|---|---|
| The process: skills, review contract, criteria, probes, templates | this plugin | everyone who installs it |
| The repo's facts: gates, backlog, docs to keep in step, review rules (rounds, pass score, paid-seat cap) | the repo's `docs/agents/workflow.md` (the **profile**), plus optional `criteria.md`, `break-it.md`, `audit-areas.md`, `decisions.md` | everyone working in the repo |
| Who reviews for you: council seats (models, where they run, effort) and your own spend cap | `council.md` in your Claude folder (`$CLAUDE_CONFIG_DIR`, or `~/.claude`) | only you |

Only the profile is required. Without `council.md`, every review uses the kit's three reviewers, which need no setup.

## Reviews

Every review, in `/agent-kit:slice` and `/agent-kit:audit`, runs under `reference/review-contract.md`: one brief,
findings only with evidence (a source and a test that would fail), blocker/should/nit severities, a ledger across
rounds, and a stop rule the repo's profile tunes. Council, when you've configured it, runs that brief past the seats
in your `council.md`, which can be T3 Code agent threads or one-shot OpenRouter requests.
