# Friday v1 System Design: Notion-First Project Intelligence

## Summary

Friday v1 is a Notion-first project intelligence pipeline. Ollama `granite3.3:2b` runs as the local heartbeat watcher roughly every 30 minutes, checks Notion session debriefs, and routes only new or blank-status debriefs to the correct GitHub/local project when it can do so safely.

DeepSeek is not part of the recurring watcher loop. DeepSeek runs only on valid review candidates found by Granite, then writes useful review output back to the Notion debrief as a comment and sends the same substantive review to Amit on Telegram with a short context header.

## Architecture

### Granite Heartbeat Watcher

The watcher runs roughly every 30 minutes through Friday heartbeat behavior.

Responsibilities:

- check Notion for session debriefs with `New` or blank review status
- use local lightweight state only for checkpoints and mappings
- use Ollama `granite3.3:2b` for routing
- extract project name, repo URL, local repo path, or repo hint
- resolve the matching GitHub/local repo when safe
- mark missing repo context as `Needs Repo Mapping`
- decide whether a debrief is safe to send to DeepSeek

The watcher must not produce project suggestions, review content, or product advice.

### On-Demand DeepSeek Review

DeepSeek runs only after Granite finds a valid new debrief with a safe project/repo match.

Inputs:

- full Notion session debrief
- matched GitHub repo URL or local repo path
- recent repo activity if available
- lightweight local project mapping context
- prior Notion review comments if available and useful

Outputs:

- what the session/debrief was about
- what changed
- what remains open
- recommended next-session prompt
- one or two high-signal suggestions
- risks or cleanup opportunities
- feature/product ideas if genuinely useful
- a clear no-useful-suggestions result when nothing is worth surfacing

DeepSeek does not edit code, tasks, docs, or project repositories. In v1, it may only produce planned review communication for Notion comments and Telegram.

### Storage Model

Notion is the source of truth for human-facing project intelligence.

Notion stores:

- session debriefs
- review status
- Friday review comments
- no-useful-suggestions notes
- missing repo mapping comments

Local state stays lightweight and technical only:

- last checked timestamp
- processed/dealt-with Notion page IDs if needed
- project-to-repo mapping cache
- unresolved mapping IDs if useful

Project repositories are read-only context. Do not store session debriefs or Friday reviews in repos by default.

### Notion Statuses

Friday should add or use a review status property on session debriefs:

- `New` or blank
- `Reviewed`
- `Needs Repo Mapping`
- `No Useful Suggestions`
- `Review Failed`

Future optional statuses:

- `Pending Amit Approval`
- `Suggestion Accepted`
- `Suggestion Rejected`

### Notion And Telegram Output

If useful suggestions exist:

- set Notion status to `Reviewed`
- write the full Friday review as a Notion comment on the session debrief
- send Amit a Telegram message with:
  - short context header
  - project name
  - short summary of what the session/debrief was about
  - why Friday is messaging
  - full Friday review

If no useful suggestions exist:

- set Notion status to `No Useful Suggestions`
- optionally add a short Notion comment saying the debrief was reviewed and no strong suggestions were found
- do not send Telegram

If repo mapping is missing:

- set Notion status to `Needs Repo Mapping`
- add a Notion comment explaining what could not be resolved
- send Telegram only if the missing mapping blocks repeated reviews or appears important

## Key Behaviors

### Project Matching

Friday should prefer explicit GitHub repo links or local repo paths in the Notion debrief.

If no explicit repo is present, Friday may use the local project mapping cache. If multiple repos could match, Friday must not guess silently. Instead, set or leave the debrief in `Needs Repo Mapping` and explain what is missing in a Notion comment.

Confirmed mappings can be added to the local mapping cache over time, but Notion remains the source of truth for debriefs and review output.

### Model Strategy

V1 installs and uses only `granite3.3:2b` for watcher/routing work.

Granite runs on the heartbeat. DeepSeek does not.

DeepSeek handles all deeper project reasoning and recommendations only after Granite finds a safe candidate.

Do not install Qwen for v1. If Granite is inaccurate or too weak, evaluate `gemma4:e2b` later.

### Review Quality Rules

Suggestions must be grounded in the debrief and repo context.

Friday should prefer one or two high-signal recommendations over long noisy lists.

If Friday lacks enough context, he should say so instead of inventing advice.

Friday should separate:

- next action
- improvement idea
- risk
- long-term product direction

### Initiative Level

V1 is suggest-only.

Friday does not automatically edit code, project docs, tasks, or project repos.

Writing planned review comments/statuses to Notion and sending Telegram notifications are communication actions, not autonomous project changes.

Later versions may allow approved project-memory updates, then limited automatic memory updates after trust is earned.

## Implementation Targets

Later implementation should likely add:

- heartbeat checklist entry
- read-only Notion debrief watcher
- Notion review status handling
- lightweight local state files
- project mapping cache
- Granite routing prompt/template
- on-demand DeepSeek review prompt/template
- Notion comment writer
- Telegram notifier with context header plus full review

## Test Plan

- Simulate Notion debriefs with blank/New, Reviewed, Needs Repo Mapping, and No Useful Suggestions statuses.
- Confirm Granite only routes blank/New debriefs.
- Confirm Granite does not generate advice.
- Confirm missing repo mapping produces `Needs Repo Mapping`.
- Confirm useful DeepSeek output would be mirrored to both Notion comment and Telegram, with Telegram context header.
- Confirm no-useful-suggestions output updates Notion but does not Telegram.
- Confirm no full debrief/review archive is stored locally.

## Assumptions

- Notion can support a review status property and comments on debrief pages.
- Telegram integration will be used for notifications after the Notion watcher path is proven.
- Local state remains technical only and does not become the primary review archive.
- `granite3.3:2b` is used only for watcher/routing work.
- DeepSeek is already connected to Friday and handles deeper reasoning on demand.
- Friday remains suggest-only until Amit explicitly promotes him to approved writes or automatic updates.
