# Choosing between options

When more than one option survives **Not options** (below), show two or three of them, score each against the criteria below
in this order, and recommend the first option that wins on the highest criterion where they differ. The user decides.
Each pack's `criteria.md` and the repo's `docs/agents/criteria.md` sharpen these for their domain:
what **Correct** must never allow, the **Testable** seam order, and their own **Not options**.

1. **Correct**: matches the spec, the design doc and the glossary in every scenario worth guarding (below). No data
   lost, duplicated or leaked to the wrong actor; a "no" the spec lists is a refusal and any other a fault.
2. **Easy to follow**: the behaviour lives in the module the design doc names for it, and each name it uses (type,
   method, config key, flag) is already in the glossary or design doc or is added there. Between options, fewer new
   names wins; tied, fewer changed lines wins. When widening a rule the code already has would cover a scenario,
   widen it; don't add a guard beside it.
3. **Consistent**: reuses the module, helper or pattern the repo already uses for the same kind of work, named by
   file; an option that adds a second way to do something the repo already does loses.
4. **Testable**: the behaviour is reachable from a seam that already has tests, highest seam first.
5. **Small**: fewer new modules, config keys, permissions, commands, endpoints and dependencies.

An option that adds something no backlog item needs loses on **Small** even if it scores well elsewhere.

**Simplest wins.** Among options that are all **Correct**, the one with the fewest moving parts (new state, UI, names,
places to check, lines) wins, even over a more thorough one. Making a race harmless after the fact beats preventing it
with a lock. This holds for code already written: an audit flags it as OVERBUILT.

## Worth guarding

A test, guard or review finding exists only for a **real** scenario. A scenario is real when it has a source:

- *observed*: a live response, a log, an error report, a test or command someone ran;
- *documented*: the dependency's own types or docs, quoted, or an open assumption the repo records;
- *produced by our code*: a line in this repo that passes the input;
- *operator input*: config or a command argument that is malformed (wrong type, unknown name, out of the range its
  docs state, an unparsable file). Well-formed input is never guarded, whatever its size or meaning.

Anything else is imagined: no test, no guard, no finding and no question to the user, whoever thought of it. When
unsure, find out before raising it: run the code, write a throwaway test, or call the real dependency where the repo
allows. A scenario that can't be checked is dropped, unless it would be Severe; then it goes to the user as a question,
saying what was tried.

A real scenario is **guarded** (one test, at the highest seam that reaches it, plus the fix) when either:

- it's **Severe**: data lost, duplicated or leaked to the wrong actor, a secret exposed, money wrong, or a crash (each
  pack's and the repo's criteria add to this list); or
- it's **routine**: it needs no specific other plugin or service, no two events landing at the same moment, no setup
  built on purpose to trigger it and no non-default setting, and an actor would notice it with no retry or setting
  that gets past it.

Any other real scenario is an **unverified risk**: one line in `docs/agents/decisions.md`, no test, no fix.

**Testable up front.** Every guarded scenario must be producible by a test. When no test can produce one, that's a
design problem, settled in Shape: pull the decision into a module a test reaches, inject the clock, randomness or
dependency, or drop the scenario with the user. A behaviour nothing can test is never shipped as if it were covered.

**Overbuilt**, and cutting it is a fix: a test or guard for a scenario that isn't real or isn't guarded; a test of
behaviour another test covers at a higher seam; a test asserting anything besides its own scenario's outcome; code a
simpler version would keep correct in every guarded scenario.

## Not options

- One that breaks a hard rule of a pack the profile lists. It goes to the user as a conflict, never as an option.
- One that contradicts an ADR. Show it only beside the ADR it would supersede and why that ADR is worth reopening; it
  becomes an option once the user reopens it.
- One that relies on an outside behaviour the repo records as an open, blocking question. Name it and stop there. One
  that relies on an unverified but non-blocking assumption names it and says what breaks if it's wrong.

## Recording

- A decision on a stored data format, a wire or config shape, permission names or a public API gets an ADR in
  `docs/adr/`.
- Any other decision goes in the spec, or in `docs/agents/decisions.md` when it settles a finding.
- When the user overrules a recommendation for a reason that names no detail of this one change, propose that reason as a new line here
  (every repo), in the repo's `docs/agents/criteria.md`, or as a rule.
