# Friday Project Intelligence Scripts

`friday_project_intelligence.py` is the conservative dry-run skeleton for Friday v1.

Safe commands:

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

Live writes are intentionally limited to one explicit page:

```powershell
$env:NOTION_API_KEY = [Environment]::GetEnvironmentVariable('NOTION_API_KEY','User'); python scripts\friday_project_intelligence.py --apply-page <notion-page-id> --use-granite --telegram-reply-to <target>
```

Friday uses Granite for low-cost routing, optional Minimax M2.7 for middle-worker prompts, and GPT-5.4 as the executive reviewer/Telegram voice.
