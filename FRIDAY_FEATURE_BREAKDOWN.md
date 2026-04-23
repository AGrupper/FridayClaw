# Friday v1 Feature Breakdown

## Summary

Friday v1 is a Notion-first automated project intelligence pipeline. Ollama `granite3.3:2b` runs every roughly 30 minutes as the watcher/router, checks Notion session debriefs, routes safe candidates to the correct project/repo, and invokes DeepSeek only when there is a valid review candidate.

Notion is the source of truth for debriefs, review statuses, and Friday review comments. Local state stays lightweight and technical. Telegram receives the full useful review with a short context header.

## Milestone 1: Local Model Setup

Goal: prepare the local watcher model.

Features:

- Pull `granite3.3:2b` through Ollama.
- Verify Ollama can run the model locally.
- Test strict JSON output for routing tasks.
- Do not install Qwen for v1.
- Treat `gemma4:e2b` as a later fallback only.

Acceptance criteria:

- `granite3.3:2b` responds locally.
- Given a sample debrief, Granite returns structured routing data.
- Granite does not produce project advice.

## Milestone 2: Lightweight Local State

Goal: create only the local technical checkpoint state Friday needs.

Features:

- Store last checked timestamp.
- Store processed/dealt-with Notion page IDs if needed.
- Store project-to-repo mappings.
- Store unresolved mapping IDs if useful.
- Do not store full debriefs or full review archives locally.

Likely artifacts:

- `state/friday-project-intelligence/processed-debriefs.json`
- `state/friday-project-intelligence/project-map.json`
- `state/friday-project-intelligence/watcher-routing-prompt.md`

Acceptance criteria:

- Friday can avoid duplicate processing.
- Confirmed project mappings can be reused.
- Local state remains technical and lightweight.

## Milestone 3: Granite Notion Debrief Watcher

Goal: detect new reviewable session debriefs from Notion.

Features:

- Fetch recent Notion session debriefs.
- Check the review status property.
- Process only `New` or blank-status debriefs.
- Ignore debriefs already marked `Reviewed`, `Needs Repo Mapping`, or `No Useful Suggestions`.
- Stay quiet when there is nothing new.
- Log watcher errors without spamming Amit.

Acceptance criteria:

- A new/blank-status debrief is detected once.
- Already handled statuses are skipped.
- The same debrief is not reviewed twice.
- No notification is sent when there are no new reviewable debriefs.

## Milestone 4: Project And Repo Resolver

Goal: match each debrief to the correct GitHub/local project.

Features:

- Prefer explicit GitHub repo links or local paths in the debrief.
- Extract project names and repo hints using `granite3.3:2b`.
- Reuse confirmed mappings from local project map.
- If no safe repo match exists, set Notion status to `Needs Repo Mapping`.
- Add a Notion comment explaining what could not be resolved.
- Ask Amit only when a match is needed and cannot be resolved safely.

Acceptance criteria:

- Clear repo links resolve directly.
- Known project names resolve through the project map.
- Ambiguous matches are not guessed.
- Missing project context does not trigger DeepSeek review.
- Missing mapping is reflected in Notion.

## Milestone 5: On-Demand DeepSeek Review Agent

Goal: produce useful project intelligence from the debrief and repo context only after Granite finds a valid candidate.

Features:

- Package the full Notion debrief.
- Include matched repo URL/path.
- Include recent git activity if available.
- Include relevant prior Notion review context if available.
- Ask DeepSeek for:
  - what the session/debrief was about
  - what changed
  - what remains open
  - recommended next-session prompt
  - one or two high-signal suggestions
  - risks or cleanup opportunities
  - feature/product ideas
  - no-useful-suggestions result when appropriate

Acceptance criteria:

- Review output is grounded in debrief and repo context.
- Output separates next action, improvement idea, risk, and long-term direction.
- Friday does not invent advice when context is weak.
- Friday remains suggest-only.

## Milestone 6: Notion Comment And Status Writer

Goal: make Notion the human-facing source of truth for Friday reviews.

Features:

- If useful suggestions exist:
  - set Notion status to `Reviewed`
  - write the full Friday review as a Notion comment
- If no useful suggestions exist:
  - set Notion status to `No Useful Suggestions`
  - optionally add a short comment saying no strong suggestions were found
- If review fails:
  - set Notion status to `Review Failed`
  - add a short diagnostic comment when useful

Acceptance criteria:

- Useful reviews appear as comments on the original debrief.
- No-useful-suggestions cases do not create noise.
- Notion stores the review result; local files do not become the review archive.

## Milestone 7: Telegram Notification

Goal: notify Amit only when Friday finds useful review output.

Features:

- Send Telegram only for useful suggestions.
- Telegram message includes:
  - project name
  - short summary of what the session/debrief was about
  - why Friday is messaging
  - full Friday review
- Do not send Telegram for no-useful-suggestions cases.
- Send Telegram for missing repo mapping only if it blocks repeated reviews or appears important.

Acceptance criteria:

- Telegram provides enough context to understand the review immediately.
- Telegram contains the same substantive review as the Notion comment.
- No-op cases stay quiet.

## Cross-Cutting Rules

- Granite watcher/router runs on heartbeat and does not generate project advice.
- DeepSeek runs only on valid review candidates and handles all deeper reasoning.
- Friday does not edit code, tasks, project docs, or repos automatically in v1.
- Notion comment/status updates and Telegram messages are communication actions.
- Keep Jarvis personal context out unless explicitly shared or summarized.

## Test Scenarios

Use fixture-style tests or simulated Notion debriefs for:

- blank/New status
- Reviewed status
- Needs Repo Mapping status
- No Useful Suggestions status
- clear GitHub repo link
- project name with known mapping
- ambiguous project name
- missing project context
- useful DeepSeek review
- no-useful-suggestions review
- Telegram context header plus full review

## Later Upgrades

Potential future improvements:

- evaluate `gemma4:e2b` if Granite routing quality is poor
- add approved project-memory updates
- allow automatic project-memory updates after enough trust
- add a weekly project intelligence digest
- add Jarvis-Friday planning bridge
