---
name: audit
description: Review what several slices changed together, for what a per-slice review can't see, and fix what's confirmed.
disable-model-invocation: true
argument-hint: "[full]"
---

An **audit** runs after every three slices. Each slice was already reviewed on its own, so an audit doesn't review the
code again; it looks for what only shows across slices:

- **consistency**: two slices solving the same kind of thing two ways, or naming one concept two ways;
- **duplication**: logic, helpers or tests repeated across the changes;
- **drift**: docs, ADRs, the glossary or the decisions saying something the code no longer does;
- **dead code**: code, config, tests or decisions lines nothing reaches any more;
- **rules**: a rule broken in code no slice review saw (a shared file several slices edited).

Read the repo's **profile**, `docs/agents/workflow.md`, first. Its gates, smoke runs, actors, tracker and commit style
apply below. With no profile, tell the user to run `/agent-kit:setup`, which drafts one, and stop.
**Green**, the **rules**, the **criteria**, the **decisions** and the **review contract** are as `/slice` defines them
(`${CLAUDE_PLUGIN_ROOT}/skills/slice/SKILL.md`).

The **scope** is `git diff <last audit commit>` (the profile's Commits section), or the whole codebase when there is
none or the argument is `full`. Run `full` only when the user asks: a whole-codebase review keeps finding one more
thing, which is why the default is the scope.

## Steps

1. **Branch**: on the base branch with a clean tree, `git checkout -b audit/<yyyy-mm-dd>`. On an existing `audit/`
   branch, resume from its notes in `.audit-notes.md` (untracked, deleted at Merge).
2. **Setup**: state the scope and its commit range in one line.
3. **Areas**: use the areas in `docs/agents/audit-areas.md`, limited to those holding scoped files. When it's missing,
   split the codebase into three to six areas, each small enough for one agent to read whole, and write them there; a
   new path outside every area joins the closest one in that file.
4. **Review**: run the review contract once per area, in parallel, with the target the scope's diff limited to the
   area's paths, and as the intent the five things this skill looks for (listed above), so it reviews only those.
   Keep its ledger in the notes. Done when every area's contract stops at agreed or stuck.
5. **Settle** with the user every confirmed finding an actor would notice, every drift where it's unclear whether the
   code or the doc is right, every one too big for this branch (it needs its own grill, or reshapes a module), and
   whatever the contract left stuck: as a table with one row each, an example (state and actions → what the actor
   sees) and the proposed outcome, chosen by the criteria. An outcome is a fix, no change, or **deferred**: a backlog
   item written the way `/idea` writes one, its decisions line reading `deferred to <item>`. Record each outcome in the
   decisions. Proceed on the rest without asking. Done when every such finding has an agreed outcome.
6. **Prune**: remove each decisions line whose code is gone. Done when every line still names live code.
7. **Smoke**: run every one of the profile's Smoke runs. A failure is a finding; fix it under the contract. Done when
   every run passes.
8. **Merge**: show, and ask permission:
   - every gate and smoke run with its result;
   - each area's review contract report; every deferred item and every unverified risk;
   - every line added to the rules and decisions;
   - the proposed commit message, an audit commit in the profile's Commits style.

   On yes: commit, `git checkout <base>`, `git merge --ff-only audit/<yyyy-mm-dd>`. A change to the kit itself (its skills, criteria or probes) is never edited in the plugin's install folder: list it in the report as a proposal for the kit's repo.

A rule broken in more than one audit is a gap: propose making it a lint or type check in the gates, or, when no tool
can check it, a clearer rule. When the user overrules a proposal for a reason that would apply again, propose it as a
rule: in a pack's standards when it holds for every repo using the pack, otherwise as the next **R*n*.** in the
`CLAUDE.md` or `AGENTS.md` it belongs to.
