# Friday v1 System Design: Notion-First Project Intelligence

## Summary

Friday v1 is a Notion-first project intelligence pipeline. OpenClaw runs the recurring cron wrapper with `qwen3:1.7b` roughly every 30 minutes, and the Python watcher uses Ollama `falcon3:3b` as the internal local router to check Notion session debriefs and route only new or blank-status debriefs to the correct GitHub/local project when it can do so safely.

DeepSeek is not part of the recurring watcher loop. DeepSeek runs only on valid review candidates found by the local router, then writes useful review output back to the Notion debrief as a comment and sends the same substantive review to Amit on Telegram with a short context header.

## Architecture

### Cron Wrapper And Local Router

The watcher runs roughly every 30 minutes through an OpenClaw cron job.

Responsibilities:

- check Notion for session debriefs with `New` or blank review status
- use local lightweight state only for checkpoints and mappings
- use `qwen3:1.7b` only to launch the strict `exec` command through OpenClaw
- use Ollama `falcon3:3b` for the actual debrief routing inside the Python script
- extract project name, repo URL, local repo path, or repo hint
- resolve the matching GitHub/local repo when safe
- mark missing repo context as `Needs Repo Mapping`
- decide whether a debrief is safe to send to DeepSeek

The wrapper and router must not produce project suggestions, review content, or product advice.

### On-Demand DeepSeek Review

DeepSeek runs only after the local router finds a valid new debrief with a safe project/repo match.

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
- processed Voicepal brainstorm digests

Local state stays lightweight and technical only:

- last checked timestamp
- processed/dealt-with Notion page IDs if needed
- project-to-repo mapping cache
- unresolved mapping IDs if useful

Project repositories are read-only context. Do not store session debriefs or Friday reviews in repos by default.

### Voicepal Brainstorm Digests

Friday accepts Voicepal brainstorm text through the Telegram intake path, then stores a processed digest in a `Brainstorm Digests` Notion data source.

Friday does not copy the full raw transcript into Notion or local files. Voicepal remains the raw archive. Local state stores only technical fingerprints and created Notion page IDs for duplicate prevention.

Digest properties:

- `Name`: existing Voicepal/shared title plus date
- `Date`
- `Source`: `Voicepal Telegram`
- `Owner`: `Friday`, `Jarvis`, `Mixed`, or `Unknown`
- `Project`
- `Domain`: `Project`, `Personal`, `School`, `Business`, `Finance Module`, or `Mixed`
- `Status`: `New`, `Processed`, `Needs Clarification`, `Linked to Debrief`, `Ignored`, or `Archived`
- `Confidence`
- `Linked Debrief` when configured in Notion
- `Source Ref`
- `Proposed Actions Count`

Routing separates who builds or acts from what the content is about. Building or improving Jarvis is Friday-owned project work with project `Jarvis`. Pure personal-life context is Jarvis-owned handoff context until a Jarvis-Friday bridge exists.

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

V1 uses a split local model strategy:

- `qwen3:1.7b` for the outer OpenClaw cron wrapper
- `falcon3:3b` for the internal debrief router

DeepSeek handles all deeper project reasoning and recommendations only after the local router finds a safe candidate.

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
- local router prompt/template
- on-demand DeepSeek review prompt/template
- Notion comment writer
- Telegram notifier with context header plus full review

## Test Plan

- Simulate Notion debriefs with blank/New, Reviewed, Needs Repo Mapping, and No Useful Suggestions statuses.
- Confirm the local router only routes blank/New debriefs.
- Confirm the local router does not generate advice.
- Confirm missing repo mapping produces `Needs Repo Mapping`.
- Confirm useful DeepSeek output would be mirrored to both Notion comment and Telegram, with Telegram context header.
- Confirm no-useful-suggestions output updates Notion but does not Telegram.
- Confirm no full debrief/review archive is stored locally.
- Confirm Voicepal brainstorm intake stores processed digests only and does not persist raw transcripts locally or in Notion.
- Confirm Jarvis feature requests route to owner `Friday`, project `Jarvis`.
- Confirm pure personal-life context routes to owner `Jarvis`.

## Assumptions

- Notion can support a review status property and comments on debrief pages.
- Telegram integration will be used for notifications after the Notion watcher path is proven.
- Local state remains technical only and does not become the primary review archive.
- DeepSeek is already connected to Friday and handles deeper reasoning on demand.
- Friday remains suggest-only until Amit explicitly promotes him to approved writes or automatic updates.
