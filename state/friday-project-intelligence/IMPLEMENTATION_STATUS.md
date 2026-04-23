# Friday v1 Implementation Status

## Completed

- Installed and verified Ollama `granite3.3:2b`.
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
- Added safety override so Granite cannot invent repo URLs for missing mappings.
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
- Hardened Granite routing so placeholder values like `NOT PROVIDED` cannot override deterministic project mappings.
- Normalized Granite boolean strings before routing decisions.
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

- Router: `ollama/granite3.3:2b`
- Middle worker: `minimax/MiniMax-M2.7`
- Executive/Friday voice: `openai-codex/gpt-5.4`

## Safe Commands

```powershell
python scripts\friday_project_intelligence.py --test
python scripts\friday_project_intelligence.py --test --use-granite
python scripts\friday_project_intelligence.py --fixtures
python scripts\friday_project_intelligence.py --fixtures --use-granite
$env:NOTION_API_KEY = [Environment]::GetEnvironmentVariable('NOTION_API_KEY','User'); python scripts\friday_project_intelligence.py --discover-notion --notion-limit 5
$env:NOTION_API_KEY = [Environment]::GetEnvironmentVariable('NOTION_API_KEY','User'); python scripts\friday_project_intelligence.py --notion-dry-run --notion-limit 5 --use-granite
$env:NOTION_API_KEY = [Environment]::GetEnvironmentVariable('NOTION_API_KEY','User'); python scripts\friday_project_intelligence.py --preview-page <notion-page-id> --use-granite --telegram-reply-to <target>
$env:NOTION_API_KEY = [Environment]::GetEnvironmentVariable('NOTION_API_KEY','User'); python scripts\friday_project_intelligence.py --auto-run --use-granite
```

## Remaining To Finish V1

- The useful-review Telegram branch has not been triggered by GPT-5.4 yet because both safe repo-mapped live debriefs were judged `no_useful_suggestions`.
- Missing-mapping Telegram delivery has been proven, and the useful-review branch uses the same raw Telegram sender.
- Useful-review Telegram content is intentionally brief; Notion remains the full source of truth.
- Configure Minimax auth if/when the middle worker tier is first needed.
- Enable the prepared OpenClaw cron job when Amit accepts that the only untriggered live branch is "useful review sends Telegram"; the rest of v1 is end-to-end verified.

## Safety Position

The current implementation is dry-run first. It does not send Telegram, write Notion, call GPT-5.4 live, write project repos, commit, push, delete, or move user files unless `--apply-page <page_id>` or `--auto-run` is explicitly used.
