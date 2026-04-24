# Friday Project Intelligence Scripts

`friday_project_intelligence.py` is the conservative dry-run skeleton for Friday v1.

Safe commands:

```powershell
python scripts\friday_project_intelligence.py --test
python scripts\friday_project_intelligence.py --test --use-local-router
python scripts\friday_project_intelligence.py --fixtures
python scripts\friday_project_intelligence.py --fixtures --use-local-router
python scripts\friday_project_intelligence.py --brainstorm-test
python scripts\friday_project_intelligence.py --brainstorm-fixtures
python scripts\friday_project_intelligence.py --brainstorm-file <transcript.txt> --brainstorm-title "<Voicepal title>" --brainstorm-date 2026-04-24
Get-Content <transcript.txt> -Raw | python scripts\friday_project_intelligence.py --brainstorm-stdin --brainstorm-title "<Voicepal title>" --brainstorm-date 2026-04-24
$env:NOTION_API_KEY = [Environment]::GetEnvironmentVariable('NOTION_API_KEY','User'); python scripts\friday_project_intelligence.py --discover-notion --notion-limit 5
$env:NOTION_API_KEY = [Environment]::GetEnvironmentVariable('NOTION_API_KEY','User'); python scripts\friday_project_intelligence.py --discover-brainstorm-notion --notion-limit 5
$env:NOTION_API_KEY = [Environment]::GetEnvironmentVariable('NOTION_API_KEY','User'); python scripts\friday_project_intelligence.py --create-brainstorm-database <parent-page-id>
$env:NOTION_API_KEY = [Environment]::GetEnvironmentVariable('NOTION_API_KEY','User'); python scripts\friday_project_intelligence.py --notion-dry-run --notion-limit 5 --use-local-router
$env:NOTION_API_KEY = [Environment]::GetEnvironmentVariable('NOTION_API_KEY','User'); python scripts\friday_project_intelligence.py --preview-page <notion-page-id> --use-local-router --telegram-reply-to <target>
$env:NOTION_API_KEY = [Environment]::GetEnvironmentVariable('NOTION_API_KEY','User'); python scripts\friday_project_intelligence.py --auto-run --use-local-router
```

Live writes are intentionally limited to one explicit page:

```powershell
$env:NOTION_API_KEY = [Environment]::GetEnvironmentVariable('NOTION_API_KEY','User'); python scripts\friday_project_intelligence.py --apply-page <notion-page-id> --use-local-router --telegram-reply-to <target>
$env:NOTION_API_KEY = [Environment]::GetEnvironmentVariable('NOTION_API_KEY','User'); python scripts\friday_project_intelligence.py --apply-brainstorm-file <transcript.txt> --telegram-reply-to <target> --send-brainstorm-telegram
$env:NOTION_API_KEY = [Environment]::GetEnvironmentVariable('NOTION_API_KEY','User'); Get-Content <transcript.txt> -Raw | python scripts\friday_project_intelligence.py --apply-brainstorm-stdin --brainstorm-title "<Voicepal title>" --brainstorm-date 2026-04-24 --telegram-reply-to <target> --send-brainstorm-telegram
```

Friday uses `falcon3:3b` for the internal local router, `qwen3:1.7b` for the outer OpenClaw cron wrapper, optional MiniMax M2.7 for middle-worker prompts, and GPT-5.4 as the executive reviewer/Telegram voice.

Brainstorm intake stores processed digests only. Raw Voicepal transcripts remain in Voicepal; local state stores only fingerprints and Notion page IDs for duplicate prevention.

The live Telegram `/brainstorm` command is installed as an OpenClaw plugin at `C:\Users\Amit\.openclaw\extensions\friday-brainstorm`. A repo copy is kept in `plugins/friday-brainstorm` so the command source is versioned.
