---
# Council config, read by agent-kit's council skill. Copy it to $CLAUDE_CONFIG_DIR/council.md (or ~/.claude/council.md)
# and edit it there, or run /agent-kit:setup. It's personal: it names the seats (who reviews, where, at what effort),
# never committed to a repo. A repo's review rules (rounds, pass score, paid-seat cap) are in its profile's Review
# section. Without this file, reviews use the kit's three reviewers.

budget_usd: 3.00       # optional: your own cap per review on paid (api) seats; the repo's Paid seats cap still applies, and the lower wins

# A seat: name, where it runs (via), model, effort.
#   via: t3   a T3 Code agent thread on `instance`; reads the code and runs commands itself. Outside T3, a Claude
#             model runs as a local subagent on the current account, and any other model can't run.
#   via: api  one OpenRouter request: the brief, the diff and the changed files in one prompt, no tools. Needs an
#             OpenRouter key in OPENROUTER_API_KEY, or the macOS keychain (service "openrouter").
members:
  - name: Claude Opus
    via: t3
    instance: Claude
    model: claude-opus-5-5
    effort: xhigh
  - name: GPT
    via: api
    model: openai/<model id from openrouter.ai/models>
    effort: xhigh
  - name: Gemini
    via: api
    model: google/<model id from openrouter.ai/models>
    effort: xhigh

# Runs instead of members when a member can't. Same shape, plus the review contract's lens (intent, rules,
# simplicity), since the seats are likely all one model maker.
fallback:
  - name: Claude Opus
    via: t3
    instance: Claude
    model: claude-opus-5-5
    effort: xhigh
    lens: intent
  - name: Claude Opus
    via: t3
    instance: Claude
    model: claude-opus-5-5
    effort: xhigh
    lens: rules
  - name: Claude Opus
    via: t3
    instance: Claude
    model: claude-opus-5-5
    effort: xhigh
    lens: simplicity
---

Notes for the council skill, if any.
