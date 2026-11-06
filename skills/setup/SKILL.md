---
name: setup
description: Check and set up agent-kit for this machine and this repo, including the optional council.
disable-model-invocation: true
---

Sets up what agent-kit needs, checking before changing anything. Run it from inside a repo. Each step says what it
found in one line; ask before writing any file, and never ask the user to paste a secret into the chat.

1. **Account**: the Claude folder is `$CLAUDE_CONFIG_DIR`, or `~/.claude` when it's unset. Say which, and which
   account `claude auth status` reports. Done when both are stated.
2. **Dependencies**: `/agent-kit:slice` calls the `mattpocock-skills` plugin's `grilling`, `domain-modeling`, `tdd`
   and `diagnosing-bugs` skills. When they aren't in this session's skill list, tell the user to run
   `/plugin install mattpocock-skills@claude-plugins-official`, then `/reload-plugins`. Done when they're listed or the
   user has the command.
3. **Profile**: the repo's `docs/agents/workflow.md`, written from `${CLAUDE_PLUGIN_ROOT}/templates/workflow.md`.
   - **Missing**: offer to draft it. Read the build files (`package.json`, `pom.xml`, `Makefile` or the like), the CI
     config, the README and docs, `AGENTS.md`/`CLAUDE.md` and `git log`, and fill every section the template has from
     what they show: gates exactly as CI runs them, the base branch, the backlog and tracker, the docs to keep in
     step, the commit style. Ask only for what they don't show, one question at a time. Show the draft; write it on
     approval.
   - **Present**: list each template heading it lacks (a newer template may add one, such as Review), and offer to add
     each with its defaults.

   Done when the profile exists with every template heading, or the user declines.
4. **Council** (optional): ask whether the user wants council reviews, which run each review past several models of
   their choosing. Without it, reviews use the kit's three `agent-kit:reviewer` agents, which need no setup. If they
   don't want it, skip to step 5.
   - The config is `council.md` in the Claude folder from step 1, in the format of
     `${CLAUDE_PLUGIN_ROOT}/templates/council.md`. Present: show its seats and ask what to change. Missing: copy the
     template there.
   - Fill in the seats with the user, one at a time: the model, and where it runs.
     - `via: t3` needs T3 Code. When the `t3-code` MCP tools are listed, call `orchestrator_capabilities` and offer the
       instances and models it reports. When they aren't, say a T3 seat with a Claude model will run as a local
       subagent here, and one with any other model won't run.
     - `via: api` needs an OpenRouter key and credit. Have the user store the key themselves, outside the chat: on
       macOS `security add-generic-password -s openrouter -a "$USER" -w` (it prompts for the key), elsewhere an
       `OPENROUTER_API_KEY` environment variable. Then run `python3 -I ${CLAUDE_PLUGIN_ROOT}/skills/council/oneshot.py
       check` and report the credit it shows. Offer model ids from `https://openrouter.ai/api/v1/models`, with their
       price per million tokens.
   - Ask for the fallback seats (used when a member can't run), each with a lens, and the optional personal
     `budget_usd`.
   - When any seat is `via: api` and the repo's profile has no **Paid seats** cap, say that paid seats won't run here
     until the profile sets one, and offer to add it.

   Done when `council.md` has every seat the user wants and the check in step 4 passes for each api seat, or the user
   stops.
5. **Summary**: one line each: the account, the profile (present or missing), and what reviews in this repo will use
   now (council with its seats, or the three fallback reviewers), with the reason.
