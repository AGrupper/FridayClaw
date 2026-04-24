# Friday v1 Implementation Status

## Completed

- Installed and verified the current local production models:
  - `qwen3:1.7b` for the OpenClaw cron wrapper
  - `falcon3:3b` for the internal Friday router
- Confirmed `NOTION_API_KEY` is present in the Windows User environment, though not inherited by the already-running OpenClaw agent process.
- Created lightweight local state files:
  - `processed-debriefs.json`
  - `project-map.json`
- Created watcher prompt and fake Notion-like fixtures.
- Added `scripts/friday_project_intelligence.py`, a conservative dry-run watcher skeleton.
- Added fixture tests for:
  - blank/New debrief routing
  - handled status skipping
  - missing repo mapping
  - one-time Telegram draft for missing mapping
  - executive review prompt packaging for safe candidates
- Added safety override so the local router cannot invent repo URLs for missing mappings.
- Confirmed OpenClaw Telegram is enabled and the CLI supports Telegram delivery with:
  - `openclaw agent --message "<message>" --deliver --reply-channel telegram --reply-to <target>`
- Confirmed OpenClaw `main` is configured on `openai-codex/gpt-5.4`.
- Confirmed `minimax/MiniMax-M2.7` is configured as a fallback model, but auth is currently missing.
- Added read-only Notion discovery to `scripts/friday_project_intelligence.py`.
- Ran read-only Notion discovery successfully with Notion API version `2026-03-11`.
- Added `runtime-config.json` for Notion IDs, model roles, and the Telegram reply target.
- Added one-page preview path guarded by `--preview-page <page_id>`.
- Added one-page live apply path guarded by `--apply-page <page_id>`.
- Added automatic v1 runner guarded by `--auto-run`.
- Configured Telegram target `8626312520` in `runtime-config.json`.
- Replaced the old DeepSeek/OpenClaw conversational executive path with direct Codex `exec` on GPT-5.4 for strict JSON executive reviews.
- Added read-only GitHub remote inspection for repo-mapped debriefs:
  - repository metadata
  - top-level files
  - recent commits
  - `CLAUDE.md`, `AGENTS.md`, and `README.md` when available
- Added a local Jarvis project mapping:
  - `Jarvis` -> `https://github.com/AGrupper/Jarvis1.0`
- Hardened local routing so placeholder values like `NOT PROVIDED` cannot override deterministic project mappings.
- Normalized local-router boolean strings before routing decisions.
- Changed useful-review Telegram behavior:
  - full GPT-5.4 suggestion stays in the Notion comment
  - Telegram sends only a short pointer with project/session context
  - the script enforces this even if GPT-5.4 returns a long Telegram body
- Proved the missing-repo-mapping live path on Notion page `34634a33-2bc2-819b-9fd0-c56a268dd374`:
  - Notion `Status` changed to `Needs Repo Mapping`
  - Notion comment write succeeded
  - raw Telegram delivery succeeded through `openclaw message send`
- Proved GPT-5.4 executive JSON generation on Notion page `33834a33-2bc2-8150-8b0c-e028608777d6`.
- Applied the same Jarvis page once:
  - Notion `Status` changed to `No Useful Suggestions`
  - Notion comment write succeeded
  - Telegram was correctly suppressed because GPT-5.4 returned `no_useful_suggestions`
- Previewed and applied Notion page `34934a33-2bc2-810e-812a-cc8649834c15`:
  - verified Jarvis project-map routing
  - verified read-only GitHub context fetch
  - GPT-5.4 returned `no_useful_suggestions`
  - Notion `Status` changed to `No Useful Suggestions`
  - Notion comment write succeeded
  - Telegram was correctly suppressed
- Ran `--auto-run` twice manually; both runs skipped handled rows and did not duplicate actions.
- Added Voicepal brainstorm intake preview/apply support:
  - `Brainstorm Digests` Notion data-source discovery and optional database creation
  - processed digest generation from transcript files
  - owner/project/domain routing for Friday, Jarvis, Mixed, and Unknown items
  - duplicate fingerprints in lightweight local state
  - explicit `--apply-brainstorm-file` live write path
  - raw transcripts intentionally excluded from Notion/local storage
- Discovered Amit-created `Brainstorm Digests` Notion data source and configured it in `runtime-config.json`:
  - data source ID: `34c34a33-2bc2-8019-a832-000b1c74ba5b`
  - database ID: `34c34a33-2bc2-8086-8ce2-c1452a8a4a50`
- Confirmed OpenClaw Telegram is enabled for the default `main`/FRIDAY agent in this workspace, with Amit's Telegram user ID allowlisted.
- Added the live `/brainstorm` OpenClaw plugin at `C:\Users\Amit\.openclaw\extensions\friday-brainstorm`, with a versioned source copy in `plugins/friday-brainstorm`.
- Restarted the local OpenClaw gateway after it was listening but closing WebSocket probes; confirmed the gateway is reachable and Telegram is running in polling mode.

## Notion Discovery

- Search query: `session debriefs`
- Found data source: `Session Debriefs`
- Data source ID: `33834a33-2bc2-80f5-9dd1-000bf76a48fa`
- Parent database ID: `33834a33-2bc2-8063-81a4-dd07fe7db184`
- Properties:
  - `Name` (`title`)
  - `Date` (`date`)
  - `Project` (`select`: `Jarvis`, `OpenClaw`)
  - `Type` (`select`: `session_debrief`)
  - `Status` (`select`: `completed`)
  - `Stat` (`select`: `Not started`, `In progress`, `Done`)
- Recent rows were fetched in dry-run/read-only mode only.
- Amit confirmed the existing Notion `Status` field can be repurposed going forward. It currently only has `completed`, so v1 should treat historical `completed` rows as already handled and add/use Friday review workflow values from this point forward.

## Live Write Status

The one-shot Notion write path has been tested successfully for both status updates and comments.

Use existing property:

- Name: `Status`
- Type: `select`
- Existing option:
  - `completed`
- Add/use options:
  - `New`
  - `Reviewed`
  - `Needs Repo Mapping`
  - `No Useful Suggestions`
  - `Review Failed`

Because Notion is the source of truth for v1, unattended live writes should stay disabled until the final automatic-run proof is completed on a safe `New` debrief.

## Model Roles

- OpenClaw cron wrapper: `ollama/qwen3:1.7b`
- Router: `ollama/falcon3:3b`
- Middle worker: `minimax/MiniMax-M2.7`
- Executive/Friday voice: `openai-codex/gpt-5.4`

## Safe Commands

```powershell
python scripts\friday_project_intelligence.py --test
python scripts\friday_project_intelligence.py --brainstorm-test
python scripts\friday_project_intelligence.py --test --use-local-router
python scripts\friday_project_intelligence.py --fixtures
python scripts\friday_project_intelligence.py --fixtures --use-local-router
python scripts\friday_project_intelligence.py --brainstorm-fixtures
python scripts\friday_project_intelligence.py --brainstorm-file <transcript.txt> --brainstorm-title "<Voicepal title>" --brainstorm-date 2026-04-24
$env:NOTION_API_KEY = [Environment]::GetEnvironmentVariable('NOTION_API_KEY','User'); python scripts\friday_project_intelligence.py --discover-notion --notion-limit 5
$env:NOTION_API_KEY = [Environment]::GetEnvironmentVariable('NOTION_API_KEY','User'); python scripts\friday_project_intelligence.py --discover-brainstorm-notion --notion-limit 5
$env:NOTION_API_KEY = [Environment]::GetEnvironmentVariable('NOTION_API_KEY','User'); python scripts\friday_project_intelligence.py --create-brainstorm-database <parent-page-id>
$env:NOTION_API_KEY = [Environment]::GetEnvironmentVariable('NOTION_API_KEY','User'); python scripts\friday_project_intelligence.py --notion-dry-run --notion-limit 5 --use-local-router
$env:NOTION_API_KEY = [Environment]::GetEnvironmentVariable('NOTION_API_KEY','User'); python scripts\friday_project_intelligence.py --preview-page <notion-page-id> --use-local-router --telegram-reply-to <target>
$env:NOTION_API_KEY = [Environment]::GetEnvironmentVariable('NOTION_API_KEY','User'); python scripts\friday_project_intelligence.py --auto-run --use-local-router
$env:NOTION_API_KEY = [Environment]::GetEnvironmentVariable('NOTION_API_KEY','User'); python scripts\friday_project_intelligence.py --apply-brainstorm-file <transcript.txt> --brainstorm-data-source-id <brainstorm-data-source-id> --telegram-reply-to <target> --send-brainstorm-telegram
```

The configured `Brainstorm Digests` data-source ID can be omitted from `--apply-brainstorm-file` unless overriding the target.

## Remaining To Finish V1

- The useful-review Telegram branch has not been triggered by GPT-5.4 yet because both safe repo-mapped live debriefs were judged `no_useful_suggestions`.
- Missing-mapping Telegram delivery has been proven, and the useful-review branch uses the same raw Telegram sender.
- Useful-review Telegram content is intentionally brief; Notion remains the full source of truth.
- Configure Minimax auth if/when the middle worker tier is first needed.
- Keep the production OpenClaw cron job on the strict single-`exec` prompt and verify it stays healthy after cleanup.

## Safety Position

The current implementation is dry-run first. It does not send Telegram, write Notion, call GPT-5.4 live, write project repos, commit, push, delete, or move user files unless `--apply-page <page_id>` or `--auto-run` is explicitly used.
