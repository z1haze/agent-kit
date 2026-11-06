---
name: idea
description: Add a feature idea to the backlog as one slice-ready item.
disable-model-invocation: true
---

An **idea** becomes one backlog item that `/slice` can later pick. This skill records it; `/slice` grills it when its
slice starts, so ask only what the item itself needs.

Read the repo's **profile**, `docs/agents/workflow.md`, first: its Backlog section says where items live, their format,
and where detail that doesn't fit an item goes. The **criteria** are `${CLAUDE_PLUGIN_ROOT}/reference/criteria.md`, each pack's
`criteria.md` and the repo's `docs/agents/criteria.md`, where they exist.

1. **Read** the backlog, the open specs and every doc in the profile's Read list. Done when you can name the backlog
   items, modules, ADRs and glossary terms the idea touches.
2. **Clarify**: ask only for what the item can't be written without: what it does for an actor, what it depends on, and
   anything already decided. Name each clash you found and settle it with the user, offering options scored by the
   criteria where there is more than one:
   - a term used differently from the glossary, or a new term;
   - overlap with a backlog item;
   - a dependency on unmerged work;
   - a contradiction with an ADR or a doc;
   - anything the criteria's **Not options** or the profile's Backlog section rules out.

   If the idea is several slices, propose the split. Done when every clash is settled and each item fits in one slice.
3. **Place**: propose where each item goes in the backlog, given that earlier items unblock later ones. Done when the
   user agrees.
4. **Write** each item in the backlog's existing format, in glossary terms. Detail that doesn't fit (examples, edge
   cases, open options) goes where the profile's Backlog section says. Show the items and any detail; on approval,
   write them.
5. Tell the user the item is ready for `/slice` from the base branch. Leave committing to the user.
