---
name: setup
description: Check and set up agent-kit for this machine and this repo, including the optional council.
disable-model-invocation: true
---

Sets up what agent-kit needs, checking before changing anything. Run it from inside a repo. The user may be new to
the kit: write every question in plain words, never in the kit's terms alone.

Rules for every step:

- **Look only where a step says.** Never search the home folder, other repos or other Claude folders for configs or
  kit files; what isn't at the named path doesn't exist for this user.
- **Checks never fail.** Test for a file with `test -f <path> && echo found || echo missing`, so a missing file reads
  as a normal answer, not an error.
- **One question at a time**, each with: what the setting does, in one or two plain sentences; what happens with each
  answer; and a recommended answer, first.
- **Never ask the user to paste a secret into the chat.**
- **Show before writing**: the exact text a file will get, then ask to write it.

## Steps

1. **Account**: the Claude folder is `$CLAUDE_CONFIG_DIR`, or `~/.claude` when it's unset. Say which, and which
   account `claude auth status` reports. Done when both are stated.
2. **Dependencies**: `/agent-kit:slice` uses the `mattpocock-skills` plugin's `grilling`, `domain-modeling`, `tdd`,
   `diagnosing-bugs` and `codebase-design` skills. When they aren't in this session's skill list, give the user
   `/plugin install mattpocock-skills@claude-plugins-official`, then `/reload-plugins`. Done when they're listed or the
   user has the commands.
3. **Profile**: the repo's `docs/agents/workflow.md`, in the format of `${CLAUDE_PLUGIN_ROOT}/templates/workflow.md`.
   - **Missing**: offer to draft it. Read the build files (`package.json`, `pom.xml`, `Makefile` or the like), the CI
     config, the README and docs, `AGENTS.md`/`CLAUDE.md` and `git log`, and fill every section from what they show:
     gates exactly as CI runs them, the base branch, the backlog and tracker, the docs to keep in step, the commit
     style. Ask only for what they don't show.
   - **Present**: name each template section it lacks, and offer to add each.
   - **The Review section**, when it's added: ask each setting as its own question, in this order and these words
     (adjusted to the repo), and leave any the user doesn't care about at its default:
     - *Max rounds*: "After reviewers report, the fixes get reviewed again, up to this many rounds; anything still
       open after the last round comes to you. Recommended: 3."
     - *Pass score*: "Each reviewer scores the change out of 10. Should review keep going until every reviewer scores
       at least a set number? Recommended: no, review stops when no real problem is left open."
     - *Also required*: "Anything else that must be true before review stops?" Offer only conditions this profile
       supports, such as its smoke runs when it has some. Recommended: nothing extra.
     - *Paid seats*: don't ask here; write `none`. Step 4 offers to change it if the user sets up paid seats.

   Done when the profile exists with every template section, or the user declines.
4. **Council** (optional). Ask first, before checking anything about it: "Reviews normally use three Claude
   reviewers, which need no setup. A council instead runs each review past models you choose: other Claude models,
   or GPT and Gemini through OpenRouter (paid). Set one up? Recommended: no, unless you want outside models." On no,
   go to step 5.
   - The config is `council.md` in the Claude folder from step 1, and only there; its format is
     `${CLAUDE_PLUGIN_ROOT}/templates/council.md`, an example, never the user's own seats. Found: show its seats and
     ask what to change. Missing: start from the template's shape with no seats filled in.
   - Fill in the seats one at a time: the model, and where it runs.
     - **T3 Code** (`via: t3`): only when the `t3-code` MCP tools are listed. Call `orchestrator_capabilities` and
       offer the instances and models it reports. When they aren't listed, say a Claude seat will run here as a
       local reviewer and any other model needs T3 Code.
     - **OpenRouter** (`via: api`): needs a key and credit. Have the user store the key themselves, outside the chat:
       on macOS `security add-generic-password -s openrouter -a "$USER" -w` (it prompts for the key), elsewhere an
       `OPENROUTER_API_KEY` environment variable. Then run `python3 -I ${CLAUDE_PLUGIN_ROOT}/skills/council/oneshot.py
       check` and report the credit. Offer model ids from `https://openrouter.ai/api/v1/models`, with their price per
       million tokens.
   - Ask for the fallback seats (used when a member can't run), each with a lens: intent, rules or simplicity.
   - Ask for an optional personal spend limit per review (`budget_usd`).
   - When any seat uses OpenRouter and the profile's Review section has no Paid seats limit, say those seats won't
     run in this repo until it has one, and offer to set it as step 3 does.

   Done when `council.md` has the seats the user wants and the check passes for each OpenRouter seat, or the user
   stops.
5. **Summary**: one line each: the account, the profile (present or missing), and what reviews in this repo will use
   now (council with its seats, or the three Claude reviewers), with the reason.
