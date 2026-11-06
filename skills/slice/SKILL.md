---
name: slice
description: Walk the next slice from pick to merge, resuming wherever it left off.
disable-model-invocation: true
---

A **slice** is one backlog item, built on its own branch `slice/<slug>` off the base branch and specced in one spec.
Running `/slice` detects the phase and runs it. Shape is the one phase that needs the user throughout; Build runs on its
own and comes back to the user only where a step below says to.

Read the repo's **profile**, `docs/agents/workflow.md`, first. It names the base branch, the actors, the packs, the
backlog, where specs live, the gates, the smoke runs and the docs to keep in step; every command, path and noun below
that it defines comes from it. With no profile, tell the user to run `/agent-kit:setup`, which drafts one, and stop.

- **Green** means every one of the profile's gates passes, run exactly as written there.
- The **kit** is this plugin, at `${CLAUDE_PLUGIN_ROOT}`. A **pack** is a folder of rules shared by a family of repos,
  outside the kit; the profile's Packs line gives each one's path. A pack may hold numbered rules, a `criteria.md` and
  a `break-it.md`.
- The **criteria** are `${CLAUDE_PLUGIN_ROOT}/reference/criteria.md`, each pack's `criteria.md` and the repo's
  `docs/agents/criteria.md`, where they exist. **Real**, **guarded**, **unverified risk** and **overbuilt** are as its
  **Worth guarding** defines them.
- The **probes** are `${CLAUDE_PLUGIN_ROOT}/reference/probes.md`, each pack's `break-it.md` and the repo's
  `docs/agents/break-it.md`.
- The **review contract** is `${CLAUDE_PLUGIN_ROOT}/reference/review-contract.md`.
- The **decisions** are `docs/agents/decisions.md`: settled findings, one line each with its reason, under the heading
  of the audit area it touches or `## General`. Create the file with a `# Decisions` heading the first time.
- The **rules** are the sentences marked **R*n*.** in the repo's `CLAUDE.md` and `AGENTS.md` files, plus the numbered
  rules of each pack the profile lists.
- The **ledger** is the spec's `## Progress` section: one line per finished step below, and one per review finding as
  the review contract writes it. Update it as each step finishes. It is how a run after `/clear` knows where it is.

## Detect the phase

1. On the base branch: **Pick**.
2. On `audit/<date>`: tell the user to run `/agent-kit:audit`. Stop.
3. On `slice/<slug>`: find its spec as the profile's Tracker says.
   - No spec: **Shape**.
   - Spec found: **Build**, resuming at the first step its ledger doesn't record as done.
4. On any other branch: tell the user `/agent-kit:slice` runs from the base branch or a `slice/` branch. Stop.

State the phase, the branch, the spec (if any) and the last ledger line in one line, then run the phase.

## Pick

1. Read the backlog, `git log --oneline <base>`, `git branch --no-merged <base>` and the open specs.
2. Count the slices merged since the last audit commit, as the profile's Tracker says. At three or more, tell the user
   to run `/agent-kit:audit` first. Stop.
3. Propose the next slice by the profile's Backlog rule. Offer up to two alternatives, one line each.
4. Once the user agrees: `git pull` on the base branch, then `git checkout -b slice/<slug>`.
5. Continue straight into **Shape**.

## Shape

Name the slice's kind in one line: **feature**, **bug**, or **no-code** (docs, config, tooling only).

1. **Diagnose**, for a bug whose cause isn't known: call the Skill tool with `mattpocock-skills:diagnosing-bugs`. Done
   when a reproduction confirms the root cause; that reproduction is the test plan's first row.
2. **Grill**: call the Skill tool with `mattpocock-skills:grilling` and `mattpocock-skills:domain-modeling`, starting
   from the backlog item and any notes it links. What the profile's Read list, the ADRs and the decisions already say is
   settled; ask only what they leave open. Where a question has more than one reasonable answer, present the options
   scored by the criteria, with a recommendation. Ask each question through a concrete story an actor would recognise
   (a named member, what happened, what they see on which page, what they click next), not through status values,
   function names or row labels. Ask only about real scenarios: check one you're unsure of yourself first, and ask with
   the evidence or with what you tried. This overrides domain-modeling's "invent scenarios" and grilling's "ask the
   whole frontier". Done when the user confirms shared understanding.
3. **Test plan**, except for no-code: write the spec template's Test plan table yourself, from the user stories and
   every probe the slice touches; a probe with nothing real behind it is dropped in one line. For each row, find the
   existing test file and the closest existing test it goes beside, and how a test makes it happen. Show the user only:
   - rows marked **can't produce**, each with the design change that would let a test reach it (pull the decision into
     a module a test reaches; inject the clock, randomness or dependency), or the option to drop it;
   - rows whose source is weak, to keep or cut;
   - the probes you dropped, one line each.

   Done when every row has a test that can produce it, and the user agrees the changes and cuts.
4. **Size**: when the agreed work spans more than two audit areas, or splits into parts that each deliver value alone,
   propose a split. This slice keeps the first part; the rest go to the backlog the way `/idea` writes items. Done when
   the user agrees the scope.
5. **Spec**: write it from the conversation with [spec-template.md](spec-template.md) and what the profile's Spec
   contents add to it, without re-interviewing. Its first line is `Branch: slice/<slug>`, and its ledger records Shape
   as done. Write an ADR for each hard-to-reverse decision, as the criteria define it. A rule that will hold beyond this
   slice goes in the doc that owns it, not only in the spec. Publish the spec as the profile's Tracker says.
6. Tell the user: `/clear`, then `/agent-kit:slice` to build. Stop.

## Build

1. **Read** the spec, every doc in the profile's Read list, the ADRs the spec touches, and the rules.
2. **TDD**: call the Skill tool with `mattpocock-skills:tdd`, one test per test plan row, in the file the row names.
   Write no test, guard or handler without a row. A real scenario found while building gets a row first, with its
   source, and is guarded only when the criteria say so. Done when every row's test passes and the tree is green.
3. **Smoke**: run each of the profile's Smoke runs whose condition the slice meets, first adding or extending a scenario
   that covers the change where the profile says to. Done when every one passes.
4. **Docs**: check every decision and every change an actor would notice against each doc in the profile's Docs list,
   and against every open backlog item and spec that mentions what changed. Done when each one already matches or is
   updated in this slice. It comes before Review so the reviewers read finished docs.
5. **Review**: commit the working tree as `wip: review round <n>` (squashed at Merge), so each round can diff against
   the last. Run the review contract with the target `git diff <base>` plus untracked files and the spec as the intent.
   Before each later round, commit the fixes as the next `wip:` commit. After every fix, stay green, keep step 3's smoke
   runs passing, and keep the docs matching what the fix changed. Append each rejection with a reason that would apply
   again, each unverified risk (`unverified risk: <scenario>`) and each user-settled outcome to the decisions. Done when
   the contract's stop rule says agreed, or the user settles what it leaves stuck.
6. **Merge**: show:
   - every gate and smoke run with its result, and any not run with the reason;
   - the review contract's report;
   - every line added to the rules, the criteria or the decisions;
   - the proposed commit message, in the profile's Commits style.

   Then ship. If a `full-send` skill is available and the user asked for full send, hand it the branch: it files, waits
   on and merges the PR. Otherwise ask permission, and on yes: squash the `wip:` commits into one (`git reset --soft
   <base>`, then commit), `git checkout <base>`, `git merge --ff-only slice/<slug>`, then close the spec as the
   profile's Tracker says. A change to the kit itself (its skills, criteria or probes) is never edited in the plugin's install folder: list it in the report as a proposal for the kit's repo.

When the user overrules a recommendation for a reason that would apply again, propose that reason as a rule: in a
pack's standards when it holds for every repo using the pack, otherwise as the next **R*n*.** in the `CLAUDE.md` or
`AGENTS.md` it belongs to; or as a line in the criteria. A rule a linter or type check could enforce goes there
instead, as a gate.
