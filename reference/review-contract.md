# Review contract

The one definition of how a review runs and when it stops, for `/slice`'s review and `/audit` alike. Whoever reviews
(a council of other providers, or the fallback reviewers), the brief, the finding format, the verification and the stop
rule below are the same, so every run judges findings the same way.

## Settings

The repo sets these in its profile's `## Review` section; one it leaves out takes the default.

| Setting | Default | Used by |
|---|---|---|
| **Max rounds** | 3 | Stop |
| **Pass score** | none | Stop: every reviewer's score must reach it |
| **Also required** | none | Stop: each condition listed (e.g. "smoke passes") must hold |
| **Paid seats** | none | Council: the most a review may spend on paid seats, e.g. `up to $3`; none means no paid seats |

## Who reviews

Check once, at the first round, and state the mode in one line:

- **Council**: invoke the kit's `agent-kit:council` skill with the brief below as its request, filled in, and the
  **Paid seats** cap. It returns
  each seat's verdict, score and findings in the format below, or `council unavailable` when the user has no council
  configured or none of its seats can run.
- **Fallback**: when council replies `council unavailable`, spawn exactly three agents of type
  `agent-kit:reviewer` in parallel, one per lens: **intent** (does the change do what the intent says, for every
  caller), **rules** (the rules, docs and decisions), **simplicity** (code, tests or guards the intent doesn't need).
  Each gets the brief below plus its lens. Use no other agent type, whatever else is installed: an older `break-it`,
  `rules-reviewer` or a general-purpose agent doesn't follow this brief's reply format.

The mode holds for every round of this review, unless council becomes unavailable partway; then later rounds use
the fallback and the report says from which round. The report names the mode that ran. A fallback run is
never reported as a council.

## Brief

Fill in the `<…>` and send it word for word. Round 2 onward adds the ledger section.

```
Review only. Do not edit, commit, push, comment on PRs, or start subagents.
Repo: <abs path>  Base: <sha>  Round: <n>
Target: <the one diff command used every round> (and read untracked files)
Intent: <the spec path, or 1-2 sentences>  Out of scope: <…>
Gates: <each gate with its result>
Read first: <the profile's Read list, the rules files covering the target, docs/agents/decisions.md>

Report a finding only with evidence:
- Behaviour: where the scenario comes from (a test or command you ran, with its output; a line in this repo that
  produces the input; the dependency's own types or docs, quoted; a log or error report), and the test that would go
  red on it (file it belongs in, and what it does). No source, or no test that could reproduce it: do not report it.
- Rule: the rule's file, number and text, quoted, and the offending file and line.
- Doc: the doc and the code, both quoted, with file and line.
- Untestable: an intended behaviour no test can reach; quote the spec line and say what blocks a test.
Anything settled in decisions.md stays settled. Style is not a finding unless a rule asks for it.

Severity:
- blocker: an intended case (a spec story or test plan row) is wrong.
- should: a bug a real caller or actor hits on a path that exists today; a broken rule; a doc that says otherwise;
  an untestable intended behaviour.
- nit: everything else.

Reply:
VERDICT: APPROVE or CHANGES
SCORE: <n>/10
F1 [blocker|should|nit] <file>:<line> <claim>. Evidence: <…>. Fix: <smallest fix>.
(ids stay stable across rounds)
```

From round 2 the brief also carries:

```
Ledger: <every id with its status and evidence>
Changed since round <n-1>: git diff <last round's commit>
Check only open ids and the changed lines. Mark each id: resolved, or still open: <reason>. A new finding counts only
on a changed line, or as an omission a changed line causes.
```

## Verify

Every finding, before acting on it:

1. **Re-rate it yourself.** Another path, a rare case or a small cost is a nit, whatever label it came with. A finding
   without the evidence the brief asks for is rejected.
2. **Behaviour**: write the test it names and run it. Red: confirmed. Green: rejected, with the output. **Rule, doc**:
   check the quotes. They match: confirmed. **Untestable**: confirmed when the spec line is real and no seam reaches
   it; the fix is the design change that makes it testable, or dropping the line with the user.
3. **Confirmed blocker or should**: the smallest fix. Prefer deleting or narrowing over a new lock, cache, helper or
   option. If the fix changes what an actor sees and the spec didn't settle it, ask the user first.
4. **Nit**: never fixed during the review, however cheap: a nit fix grows the diff the next round must re-review.
   Decline it in one line and list it as a follow-up in the report; the user picks which to do afterwards. A nit never
   starts another round.
5. **Disagree**: say why with evidence (file:line, test, output). Never agree just to end the loop.

Rerun the gates, then `git diff --shortstat <base>`. If the review grew the diff beyond what its fixes need, cut first.

## Ledger

One line per finding, kept in the spec's `## Progress` (or the audit's notes): `F<n> <severity> <file>:<line>
<claim> — fixed <sha> | rejected: <evidence> | declined (nit) | disputed: <both sides>`. Rejections with a reason that
would apply again go to the decisions.

## Stop

- **Agreed**: no blocker or should is open after verification (or every reviewer's verdict is APPROVE on the current
  diff), every reviewer's score reaches the **Pass score**, and every **Also required** condition holds. Stop.
- **Next round** only when a blocker or should was fixed in behaviour code, or a reviewer scored under the **Pass
  score**. A comment, doc or format-only fix needs no new round.
- **Low score with nothing open**: the next round's brief asks that reviewer what keeps its score under the pass score,
  with evidence. A reason that verifies as a blocker or should is fixed. Otherwise the score stands: the review is
  stuck on it, and the user decides.
- **Budget**: **Max rounds**. Up to 2 more only for security, auth, data loss or concurrency, while a blocker with
  evidence stays open.
- **Stuck**: an id still disputed after two replies, or the budget ends with one open: show both sides in 2-3 lines
  each and the user decides. Budget end is not approval.

## Report

The mode, the rounds, and a table with a row per reviewer and a column per round holding its verdict and score: every
reviewer that ran, in every round, with `no score` when one gave none and `no reply` when one failed. A missing row
means the review didn't run as this contract says; say so. Then the findings fixed and rejected, one line each; the
nits declined, as follow-ups; and the diff size before and after review. When the mode was fallback because the user
has no council configured, end with: `No council configured; run /agent-kit:setup to add one.`

```markdown
## Review

Mode: council (Claude Opus, GPT Sol, Gemini Pro) · Rounds: 2 · Diff: +412/-38 → +398/-41

| Reviewer | Round 1 | Round 2 |
| --- | --- | --- |
| Claude Opus | CHANGES 7/10 | APPROVE 9/10 |
| GPT Sol | CHANGES 8/10 | APPROVE 9/10 |
| Gemini Pro | APPROVE 9/10 | no reply |
```
