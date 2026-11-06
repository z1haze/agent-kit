Branch: slice/<slug>

## Problem Statement

The problem an actor faces, from their perspective. The actors are the profile's.

## Solution

The solution, from the same perspective.

## User Stories

A numbered list covering every actor and every path through the change, each in the form:

1. As a <actor>, I want <feature>, so that <benefit>

## Implementation Decisions

The decisions made, such as:

- The modules built or changed, and their interfaces
- Stored data, config, permissions, commands, endpoints and wire shapes
- Architectural decisions, with the ADR for each hard-to-reverse one

No file paths or code snippets: they go stale. The exception is a snippet from a prototype that encodes a decision more
precisely than prose (a schema, a type shape, a state machine), trimmed to the decision-rich part and marked as from a
prototype.

## Assumptions

Each unverified outside behaviour the slice relies on (an upstream API, a server, a file format), the answer it assumes,
and what changes if that answer is wrong. Omit the section when there are none.

## Test plan

Every test Build writes comes from a row here; a test with no row is overbuilt. One row per user story path, and one
per failure mode that is real and guarded (criteria, **Worth guarding**). Walk the probes here: each probe the slice
touches gets a row, or is dropped because nothing real produces it.

| # | Scenario (what the actor does and sees) | Source | Test lives in | How the test produces it |
|---|---|---|---|---|
| T1 | A shopper signs in from two tabs; both land signed in | observed: Datadog "Sign-in failed", 2026-10-27 | `login.test.ts`, beside "signs in" | two pending `state` cookies, then each callback |

- **Source**: for a user story, its story number; for a failure mode, where we know it happens (observed, documented,
  produced by our code, malformed operator input).
- **Test lives in**: an existing test file and the closest existing test, at the highest seam that reaches it.
- **How the test produces it**: the fake, fixture or call that makes it happen. When nothing can, write **can't
  produce** and the design change (in Implementation Decisions) that would let a test reach it, or drop the row with
  the user.

Only external behaviour is tested, never implementation details.

## Out of Scope

What this slice leaves out.

## Further Notes

Anything else.

## Progress

- Shape: done
