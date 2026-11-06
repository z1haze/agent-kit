# Probes

The checklist `/slice`'s Shape walks while writing the test plan. A probe is a question to ask of the change, not a
finding: each one the slice touches becomes a test plan row when something real produces its scenario (criteria,
**Worth guarding**), or is dropped in one line when nothing does. Each pack's `break-it.md` and the repo's
`docs/agents/break-it.md` add their own.

- **Concurrency**: two calls interleaving (two clicks, two users, two devices or tabs, a save racing a load); work on a
  thread or in a callback that touches state it shouldn't from there.
- **Lifecycle**: before config and data have loaded, when a load fails, across a reload, during shutdown, and when the
  actor leaves, disconnects or times out mid-action.
- **Partial writes**: a write that fails halfway; a crash between two stores that must agree; a retry that applies a
  write twice.
- **Old data and old clients**: data written by an older version; an older client, caller or config file against this
  change.
- **Config and permissions**: a missing key, a value out of range, a value set but of the wrong type, a file that
  doesn't parse on reload; a caller without the permission, and each permission default.
- **Isolation**: one actor seeing or changing another's data, through an id, a shared cache, or state that outlives the
  request or session that filled it.
- **Dependencies**: each outside dependency absent, failing, slow, or answering something unexpected.
- **Limits**: numbers at 0, 1, negative and the type's maximum; empty lists; strings at their caps and in non-ASCII;
  a repeated input.
- **Secrets**: a secret or personal data reaching a log, an error report, a message, a URL or a response it doesn't
  belong in.
- **Assumptions**: unverified outside behaviour the change relies on: name it and what breaks if it's wrong.
- **Promises**: a promise a doc or ADR makes for the area that the change breaks, or behaviour that differs from a
  similar module in a way an actor would notice.
