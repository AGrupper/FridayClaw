#!/usr/bin/env python3
"""Friday v1 project intelligence watcher.

This script is deliberately conservative:
- dry-run is the default
- fixtures are the default input
- live Notion/Telegram/executive review operations require explicit page apply
- no project repo writes are performed
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state" / "friday-project-intelligence"
PROCESSED_PATH = STATE_DIR / "processed-debriefs.json"
PROJECT_MAP_PATH = STATE_DIR / "project-map.json"
RUNTIME_CONFIG_PATH = STATE_DIR / "runtime-config.json"
FIXTURE_PATH = STATE_DIR / "fixture-debriefs.json"
FIXTURE_BRAINSTORM_PATH = STATE_DIR / "fixture-brainstorms.json"
PROCESSED_BRAINSTORMS_PATH = STATE_DIR / "processed-brainstorms.json"
PROMPT_PATH = STATE_DIR / "watcher-routing-prompt.md"
NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2026-03-11"
DEFAULT_NOTION_DATA_SOURCE_ID = "33834a33-2bc2-80f5-9dd1-000bf76a48fa"
DEFAULT_NOTION_STATUS_PROPERTY = "Status"
DEFAULT_NOTION_CARRYOVER_PROPERTY = "Carryover"
DEFAULT_NOTION_CARRYOVER_TOPIC_PROPERTY = "Carryover Topic"
DEFAULT_BRAINSTORM_DATA_SOURCE_ID = ""
DEFAULT_BRAINSTORM_STATUS_PROPERTY = "Status"
DEFAULT_ROUTER_MODEL = "ollama/falcon3:3b"
DEFAULT_WORKER_MODEL = "minimax/MiniMax-M2.7"
DEFAULT_EXECUTIVE_MODEL = "openai-codex/gpt-5.4"
CARRYOVER_ACTIONABLE = "Actionable"
CARRYOVER_NOT_ACTIONABLE = "Not Actionable"
CARRYOVER_RESOLVED = "Resolved"
CARRYOVER_OPTIONS = {CARRYOVER_ACTIONABLE, CARRYOVER_NOT_ACTIONABLE, CARRYOVER_RESOLVED}
COMMON_OLLAMA_PATHS = [
    Path(r"C:\Users\Amit\AppData\Local\Programs\Ollama\ollama.exe"),
    Path(r"C:\Program Files\Ollama\ollama.exe"),
]
OLLAMA_API_GENERATE = "http://127.0.0.1:11434/api/generate"
OLLAMA_ROUTE_SCHEMA = {
    "type": "object",
    "properties": {
        "project_name": {"type": ["string", "null"]},
        "repo_url": {"type": ["string", "null"]},
        "repo_hint": {"type": ["string", "null"]},
        "review_status": {"type": ["string", "null"]},
        "has_enough_context": {"type": "boolean"},
        "should_launch_review": {"type": "boolean"},
        "reason": {"type": ["string", "null"]},
    },
    "required": [
        "project_name",
        "repo_url",
        "repo_hint",
        "review_status",
        "has_enough_context",
        "should_launch_review",
        "reason",
    ],
    "additionalProperties": False,
}

HANDLED_STATUSES = {
    "completed",
    "reviewed",
    "needs repo mapping",
    "no useful suggestions",
    "review failed",
}
FRIDAY_REVIEW_STATUSES = {
    "new",
    "completed",
    "reviewed",
    "needs repo mapping",
    "no useful suggestions",
    "review failed",
}
ACTIONABLE_STATUSES = {"", "new"}


@dataclass
class Debrief:
    id: str
    title: str
    review_status: str
    project_name: str
    repo_url: str
    local_repo_path: str
    session_summary: str
    open_items: str
    next_steps: str
    content: str
    carryover: str = ""
    carryover_topic: str = ""
    source: str = "fixture"


@dataclass
class BrainstormTranscript:
    id: str
    title: str
    date: str
    transcript: str
    source_ref: str = ""
    source: str = "voicepal_telegram"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def load_runtime_config() -> dict[str, Any]:
    defaults = {
        "version": 1,
        "notion": {
            "data_source_id": DEFAULT_NOTION_DATA_SOURCE_ID,
            "status_property": DEFAULT_NOTION_STATUS_PROPERTY,
            "carryover_property": DEFAULT_NOTION_CARRYOVER_PROPERTY,
            "carryover_topic_property": DEFAULT_NOTION_CARRYOVER_TOPIC_PROPERTY,
        },
        "brainstorm": {
            "data_source_id": DEFAULT_BRAINSTORM_DATA_SOURCE_ID,
            "status_property": DEFAULT_BRAINSTORM_STATUS_PROPERTY,
        },
        "models": {
            "router_model": DEFAULT_ROUTER_MODEL,
            "worker_model": DEFAULT_WORKER_MODEL,
            "executive_model": DEFAULT_EXECUTIVE_MODEL,
        },
        "telegram": {
            "reply_to": "8626312520",
        },
    }
    if not RUNTIME_CONFIG_PATH.exists():
        return defaults
    configured = load_json(RUNTIME_CONFIG_PATH)
    merged = defaults | configured
    merged["notion"] = defaults["notion"] | configured.get("notion", {})
    merged["brainstorm"] = defaults["brainstorm"] | configured.get("brainstorm", {})
    merged["models"] = defaults["models"] | configured.get("models", {})
    merged["telegram"] = defaults["telegram"] | configured.get("telegram", {})
    return merged


def notion_api_request(method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    token = os.environ.get("NOTION_API_KEY") or read_windows_user_env("NOTION_API_KEY")
    if not token:
        raise RuntimeError("NOTION_API_KEY is not visible to this process.")

    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = Request(
        f"{NOTION_API_BASE}{path}",
        data=body,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Notion API {method} {path} failed with HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"Notion API {method} {path} failed: {exc}") from exc


def plain_text(rich_text: list[dict[str, Any]] | None) -> str:
    return "".join(str(item.get("plain_text", "")) for item in (rich_text or [])).strip()


def object_title(item: dict[str, Any]) -> str:
    return plain_text(item.get("title")) or plain_text(item.get("properties", {}).get("title", {}).get("title"))


def property_value_summary(value: dict[str, Any]) -> str:
    value_type = value.get("type")
    if value_type == "title":
        return plain_text(value.get("title"))
    if value_type == "rich_text":
        return plain_text(value.get("rich_text"))
    if value_type == "status":
        return str((value.get("status") or {}).get("name", "")).strip()
    if value_type == "select":
        return str((value.get("select") or {}).get("name", "")).strip()
    if value_type == "url":
        return str(value.get("url") or "").strip()
    if value_type == "date":
        date = value.get("date") or {}
        return str(date.get("start") or "").strip()
    if value_type == "checkbox":
        return str(value.get("checkbox"))
    return ""


def schema_options(schema: dict[str, Any]) -> list[str]:
    prop_type = str(schema.get("type", ""))
    config = schema.get(prop_type) or {}
    return [str(option.get("name", "")).strip() for option in config.get("options", []) if option.get("name")]


def schema_summary(schema: dict[str, Any]) -> dict[str, Any]:
    summary = {"id": schema.get("id"), "type": schema.get("type")}
    options = schema_options(schema)
    if options:
        summary["options"] = options
    return summary


def find_review_status_properties(properties: dict[str, Any]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for name, schema in properties.items():
        prop_type = str(schema.get("type", ""))
        normalized = name.strip().lower()
        if prop_type not in {"status", "select"}:
            continue
        options = schema_options(schema)
        normalized_options = {option.lower() for option in options}
        has_friday_options = bool(normalized_options & FRIDAY_REVIEW_STATUSES)
        has_review_name = "review" in normalized or "friday" in normalized
        is_generic_status = "status" in normalized or normalized in {"state", "triage"}
        if has_review_name or has_friday_options or is_generic_status:
            strength = "strong" if has_review_name or has_friday_options else "weak"
            candidates.append(
                {
                    "name": name,
                    "id": str(schema.get("id", "")),
                    "type": prop_type,
                    "options": options,
                    "strength": strength,
                }
            )
    return candidates


def discover_notion_session_debriefs(limit: int = 5) -> dict[str, Any]:
    search_payload = {
        "query": "session debriefs",
        "filter": {"property": "object", "value": "data_source"},
        "sort": {"direction": "descending", "timestamp": "last_edited_time"},
        "page_size": 10,
    }
    search = notion_api_request("POST", "/search", search_payload)
    data_sources = search.get("results", [])

    discovery: dict[str, Any] = {
        "dry_run": True,
        "notion_version": NOTION_VERSION,
        "query": "session debriefs",
        "matches": [],
        "selected": None,
        "status_property": None,
        "recent_debriefs": [],
        "warnings": [],
    }

    for item in data_sources:
        properties = item.get("properties", {})
        database_id = (item.get("parent") or {}).get("database_id", "")
        discovery["matches"].append(
            {
                "object": item.get("object"),
                "title": object_title(item),
                "data_source_id": item.get("id"),
                "database_id": database_id,
                "last_edited_time": item.get("last_edited_time"),
                "property_names": sorted(properties.keys()),
                "review_status_candidates": find_review_status_properties(properties),
            }
        )

    likely_matches = [
        match
        for match in discovery["matches"]
        if object_title({"title": [{"plain_text": match.get("title", "")}]}).lower() == "session debriefs"
        or "session debrief" in str(match.get("title", "")).lower()
    ]
    selected_match = likely_matches[0] if likely_matches else (discovery["matches"][0] if discovery["matches"] else None)
    if not selected_match:
        discovery["warnings"].append("No data source named like 'session debriefs' was found. Confirm the database is shared with the integration.")
        page_search = notion_api_request(
            "POST",
            "/search",
            {
                "query": "session debriefs",
                "filter": {"property": "object", "value": "page"},
                "sort": {"direction": "descending", "timestamp": "last_edited_time"},
                "page_size": 10,
            },
        )
        discovery["page_matches"] = [
            {
                "object": item.get("object"),
                "title": object_title(item),
                "page_id": item.get("id"),
                "last_edited_time": item.get("last_edited_time"),
            }
            for item in page_search.get("results", [])
        ]
        return discovery

    data_source_id = selected_match["data_source_id"]
    retrieved = notion_api_request("GET", f"/data_sources/{data_source_id}")
    properties = retrieved.get("properties", {})
    status_candidates = find_review_status_properties(properties)

    discovery["selected"] = {
        "title": object_title(retrieved) or selected_match.get("title", ""),
        "data_source_id": data_source_id,
        "database_id": (retrieved.get("parent") or {}).get("database_id") or selected_match.get("database_id", ""),
        "property_schema": {
            name: schema_summary(schema)
            for name, schema in sorted(properties.items())
        },
    }

    configured_status_candidates = [
        candidate for candidate in status_candidates if candidate.get("name") == DEFAULT_NOTION_STATUS_PROPERTY
    ]
    strong_status_candidates = [candidate for candidate in status_candidates if candidate.get("strength") == "strong"]
    if len(configured_status_candidates) == 1:
        discovery["status_property"] = configured_status_candidates[0] | {"accepted_by_config": True}
    elif len(strong_status_candidates) == 1:
        discovery["status_property"] = strong_status_candidates[0]
    elif not strong_status_candidates:
        discovery["warnings"].append(
            "No confirmed Friday review status property found. Generic status-like properties are listed as weak candidates only."
        )
        if status_candidates:
            discovery["status_property_candidates"] = status_candidates
    else:
        discovery["warnings"].append("Multiple possible Friday review status properties found; choose one before live writes.")
        discovery["status_property_candidates"] = strong_status_candidates

    query_payload: dict[str, Any] = {
        "page_size": limit,
        "sorts": [{"timestamp": "last_edited_time", "direction": "descending"}],
    }
    queried = notion_api_request("POST", f"/data_sources/{data_source_id}/query", query_payload)
    for page in queried.get("results", []):
        page_properties = page.get("properties", {})
        title = ""
        summarized_properties: dict[str, str] = {}
        for name, value in page_properties.items():
            summary = property_value_summary(value)
            if value.get("type") == "title":
                title = summary
            if summary and len(summarized_properties) < 12:
                summarized_properties[name] = summary
        discovery["recent_debriefs"].append(
            {
                "page_id": page.get("id"),
                "title": title,
                "last_edited_time": page.get("last_edited_time"),
                "review_status": summarized_properties.get((discovery["status_property"] or {}).get("name", ""), ""),
                "properties": summarized_properties,
            }
        )

    return discovery


def discover_notion_brainstorm_digests(limit: int = 5) -> dict[str, Any]:
    search_payload = {
        "query": "brainstorm digests",
        "filter": {"property": "object", "value": "data_source"},
        "sort": {"direction": "descending", "timestamp": "last_edited_time"},
        "page_size": 10,
    }
    search = notion_api_request("POST", "/search", search_payload)
    matches: list[dict[str, Any]] = []
    for item in search.get("results", []):
        properties = item.get("properties", {})
        matches.append(
            {
                "title": object_title(item),
                "data_source_id": item.get("id"),
                "database_id": (item.get("parent") or {}).get("database_id", ""),
                "last_edited_time": item.get("last_edited_time"),
                "property_schema": {name: schema_summary(schema) for name, schema in sorted(properties.items())},
            }
        )
    selected = next((match for match in matches if str(match.get("title", "")).lower() == "brainstorm digests"), None)
    selected = selected or (matches[0] if matches else None)
    recent: list[dict[str, Any]] = []
    if selected:
        data = notion_api_request(
            "POST",
            f"/data_sources/{selected['data_source_id']}/query",
            {"page_size": limit, "sorts": [{"timestamp": "last_edited_time", "direction": "descending"}]},
        )
        for page in data.get("results", []):
            props = page.get("properties", {})
            summarized = {name: property_value_summary(value) for name, value in props.items() if property_value_summary(value)}
            recent.append(
                {
                    "page_id": page.get("id"),
                    "title": next((value for name, value in summarized.items() if name.lower() == "name"), ""),
                    "last_edited_time": page.get("last_edited_time"),
                    "properties": summarized,
                }
            )
    return {
        "dry_run": True,
        "notion_version": NOTION_VERSION,
        "query": "brainstorm digests",
        "matches": matches,
        "selected": selected,
        "recent_digests": recent,
        "warnings": [] if selected else ["No Brainstorm Digests data source found. Create it or configure brainstorm.data_source_id."],
    }


def create_brainstorm_database(parent_page_id: str) -> dict[str, Any]:
    payload = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": "Brainstorm Digests"}}],
        "is_inline": False,
        "properties": {
            "Name": {"title": {}},
            "Date": {"date": {}},
            "Source": {"select": {"options": [{"name": "Voicepal Telegram", "color": "blue"}]}},
            "Owner": {
                "select": {
                    "options": [
                        {"name": "Friday", "color": "blue"},
                        {"name": "Jarvis", "color": "green"},
                        {"name": "Mixed", "color": "purple"},
                        {"name": "Unknown", "color": "gray"},
                    ]
                }
            },
            "Project": {"rich_text": {}},
            "Domain": {
                "select": {
                    "options": [
                        {"name": "Project", "color": "blue"},
                        {"name": "Personal", "color": "green"},
                        {"name": "School", "color": "yellow"},
                        {"name": "Business", "color": "orange"},
                        {"name": "Finance Module", "color": "red"},
                        {"name": "Mixed", "color": "purple"},
                    ]
                }
            },
            "Status": {
                "select": {
                    "options": [
                        {"name": "New", "color": "gray"},
                        {"name": "Processed", "color": "green"},
                        {"name": "Needs Clarification", "color": "yellow"},
                        {"name": "Linked to Debrief", "color": "blue"},
                        {"name": "Ignored", "color": "gray"},
                        {"name": "Archived", "color": "gray"},
                    ]
                }
            },
            "Confidence": {
                "select": {
                    "options": [
                        {"name": "High", "color": "green"},
                        {"name": "Medium", "color": "yellow"},
                        {"name": "Low", "color": "red"},
                    ]
                }
            },
            "Source Ref": {"rich_text": {}},
            "Proposed Actions Count": {"number": {"format": "number"}},
        },
    }
    return notion_api_request("POST", "/databases", payload)


def block_plain_text(block: dict[str, Any]) -> str:
    block_type = block.get("type")
    if not block_type:
        return ""
    value = block.get(block_type) or {}
    rich_text = value.get("rich_text") or value.get("text")
    return plain_text(rich_text)


def notion_page_content(page_id: str, limit: int = 100) -> str:
    data = notion_api_request("GET", f"/blocks/{page_id}/children?page_size={limit}")
    lines = [block_plain_text(block) for block in data.get("results", [])]
    return "\n".join(line for line in lines if line).strip()


def find_property_by_type(properties: dict[str, Any], prop_type: str) -> str:
    for name, value in properties.items():
        if value.get("type") == prop_type:
            return name
    return ""


def first_property_value(properties: dict[str, Any], names: list[str]) -> str:
    lowered = {name.lower(): name for name in properties}
    for wanted in names:
        actual = lowered.get(wanted.lower())
        if actual:
            return property_value_summary(properties[actual])
    return ""


def infer_section(content: str, names: list[str]) -> str:
    stop_headings = {
        "what was done",
        "summary",
        "session summary",
        "open",
        "open items",
        "what's open",
        "whats open",
        "next",
        "next steps",
        "what's next",
        "whats next",
    }
    for name in names:
        pattern = re.compile(rf"^{re.escape(name)}\s*:?\s*(.+)$", re.IGNORECASE | re.MULTILINE)
        match = pattern.search(content)
        if match:
            return match.group(1).strip()
    lines = content.splitlines()
    wanted = {name.strip().lower().rstrip(":") for name in names}
    for index, line in enumerate(lines):
        normalized = re.sub(r"^[#*\-\s]+", "", line).strip().lower().rstrip(":")
        if normalized not in wanted:
            continue
        section_lines: list[str] = []
        for next_line in lines[index + 1 :]:
            clean = next_line.strip()
            if not clean or clean == "---":
                continue
            next_heading = re.sub(r"^[#*\-\s]+", "", clean).strip().lower().rstrip(":")
            if clean.startswith("#") and next_heading in stop_headings:
                break
            section_lines.append(clean)
        return "\n".join(section_lines).strip()
    return ""


def notion_page_to_debrief(page: dict[str, Any], *, status_property: str) -> Debrief:
    properties = page.get("properties", {})
    title_property = find_property_by_type(properties, "title")
    title = property_value_summary(properties.get(title_property, {})) if title_property else page.get("id", "")
    content = notion_page_content(str(page.get("id", "")))
    status = first_property_value(properties, [status_property]) or "New"
    project_name = first_property_value(properties, ["Project"])
    carryover_property, carryover_topic_property = notion_carryover_property_names()
    carryover = first_property_value(properties, [carryover_property])
    carryover_topic = first_property_value(properties, [carryover_topic_property])
    return Debrief(
        id=str(page.get("id", "")).strip(),
        title=title,
        review_status=status,
        project_name=project_name,
        repo_url=repo_from_text(content),
        local_repo_path=first_property_value(properties, ["Local Repo", "Local Repo Path", "Repo Path"]),
        session_summary=infer_section(content, ["Session summary", "Summary", "What Was Done"]) or title,
        open_items=infer_section(content, ["Open items", "Open Items", "Open", "What's Open", "Whats Open"]),
        next_steps=infer_section(content, ["Next steps", "Next Steps", "Next", "What's Next", "Whats Next"]),
        content=content or title,
        carryover=carryover,
        carryover_topic=carryover_topic,
        source="notion",
    )


def load_notion_debriefs(limit: int = 5) -> list[Debrief]:
    config = load_runtime_config()
    notion_config = config["notion"]
    data_source_id = str(notion_config.get("data_source_id") or DEFAULT_NOTION_DATA_SOURCE_ID)
    status_property = str(notion_config.get("status_property") or DEFAULT_NOTION_STATUS_PROPERTY)
    payload: dict[str, Any] = {
        "page_size": limit,
        "sorts": [{"timestamp": "last_edited_time", "direction": "descending"}],
    }
    data = notion_api_request("POST", f"/data_sources/{data_source_id}/query", payload)
    return [notion_page_to_debrief(page, status_property=status_property) for page in data.get("results", [])]


def notion_property_kind(data_source_id: str, property_name: str) -> str:
    data = notion_api_request("GET", f"/data_sources/{data_source_id}")
    schema = data.get("properties", {}).get(property_name, {})
    kind = str(schema.get("type", ""))
    if kind not in {"select", "status"}:
        raise RuntimeError(f"Notion property {property_name!r} is {kind!r}, expected select or status.")
    return kind


def notion_data_source_schema(data_source_id: str) -> dict[str, Any]:
    data = notion_api_request("GET", f"/data_sources/{data_source_id}")
    return data.get("properties", {})


def notion_carryover_property_names() -> tuple[str, str]:
    config = load_runtime_config()
    notion_config = config["notion"]
    return (
        str(notion_config.get("carryover_property") or DEFAULT_NOTION_CARRYOVER_PROPERTY),
        str(notion_config.get("carryover_topic_property") or DEFAULT_NOTION_CARRYOVER_TOPIC_PROPERTY),
    )


def carryover_schema_errors(schema: dict[str, Any]) -> list[str]:
    carryover_property, carryover_topic_property = notion_carryover_property_names()
    errors: list[str] = []
    carryover_schema = schema.get(carryover_property)
    topic_schema = schema.get(carryover_topic_property)
    if not carryover_schema:
        errors.append(f"Missing Notion property {carryover_property!r}.")
    elif carryover_schema.get("type") != "select":
        errors.append(f"Notion property {carryover_property!r} must be a select property.")
    else:
        options = {
            str(option.get("name", "")).strip()
            for option in carryover_schema.get("select", {}).get("options", [])
        }
        missing = sorted(CARRYOVER_OPTIONS - options)
        if missing:
            errors.append(f"Notion property {carryover_property!r} is missing options: {', '.join(missing)}.")
    if not topic_schema:
        errors.append(f"Missing Notion property {carryover_topic_property!r}.")
    elif topic_schema.get("type") != "rich_text":
        errors.append(f"Notion property {carryover_topic_property!r} must be a rich_text property.")
    return errors


def require_carryover_schema(data_source_id: str) -> dict[str, Any]:
    schema = notion_data_source_schema(data_source_id)
    errors = carryover_schema_errors(schema)
    if errors:
        raise RuntimeError(
            "Session Debriefs carryover schema is not ready. "
            + " ".join(errors)
            + " Run --ensure-carryover-schema before live Friday cron processing."
        )
    return schema


def carryover_schema_status() -> dict[str, Any]:
    config = load_runtime_config()
    data_source_id = str(config["notion"].get("data_source_id") or DEFAULT_NOTION_DATA_SOURCE_ID)
    schema = notion_data_source_schema(data_source_id)
    errors = carryover_schema_errors(schema)
    return {"ready": not errors, "errors": errors}


def ensure_carryover_schema() -> dict[str, Any]:
    config = load_runtime_config()
    data_source_id = str(config["notion"].get("data_source_id") or DEFAULT_NOTION_DATA_SOURCE_ID)
    carryover_property, carryover_topic_property = notion_carryover_property_names()
    schema = notion_data_source_schema(data_source_id)
    properties: dict[str, Any] = {}
    carryover_schema = schema.get(carryover_property)
    if not carryover_schema or carryover_schema.get("type") == "select":
        existing_options = {
            str(option.get("name", "")).strip()
            for option in (carryover_schema or {}).get("select", {}).get("options", [])
        }
        if not carryover_schema or CARRYOVER_OPTIONS - existing_options:
            properties[carryover_property] = {
                "select": {
                    "options": [
                        {"name": CARRYOVER_ACTIONABLE, "color": "green"},
                        {"name": CARRYOVER_NOT_ACTIONABLE, "color": "gray"},
                        {"name": CARRYOVER_RESOLVED, "color": "blue"},
                    ]
                }
            }
    if carryover_topic_property not in schema:
        properties[carryover_topic_property] = {"rich_text": {}}
    if properties:
        schema = notion_api_request("PATCH", f"/data_sources/{data_source_id}", {"properties": properties}).get(
            "properties", {}
        )
    errors = carryover_schema_errors(schema)
    return {
        "data_source_id": data_source_id,
        "changed": bool(properties),
        "properties_added": list(properties),
        "ready": not errors,
        "errors": errors,
    }


def notion_update_page_properties(page_id: str, values: dict[str, Any]) -> dict[str, Any]:
    config = load_runtime_config()
    data_source_id = str(config["notion"].get("data_source_id") or DEFAULT_NOTION_DATA_SOURCE_ID)
    schema = require_carryover_schema(data_source_id)
    lower_schema = {name.lower(): name for name in schema}
    properties: dict[str, Any] = {}
    for wanted_name, value in values.items():
        actual = lower_schema.get(wanted_name.lower())
        if not actual:
            raise RuntimeError(f"Notion property {wanted_name!r} does not exist.")
        property_value = notion_property_value(schema[actual], value)
        if property_value is not None:
            properties[actual] = property_value
    if not properties:
        return {"skipped": True, "reason": "No non-empty property values to update."}
    return notion_api_request("PATCH", f"/pages/{page_id}", {"properties": properties})


def notion_update_carryover(page_id: str, carryover: str, topic: str) -> dict[str, Any]:
    carryover_property, carryover_topic_property = notion_carryover_property_names()
    return notion_update_page_properties(
        page_id,
        {
            carryover_property: carryover,
            carryover_topic_property: topic,
        },
    )


def notion_update_status(page_id: str, status: str) -> dict[str, Any]:
    config = load_runtime_config()
    notion_config = config["notion"]
    data_source_id = str(notion_config.get("data_source_id") or DEFAULT_NOTION_DATA_SOURCE_ID)
    property_name = str(notion_config.get("status_property") or DEFAULT_NOTION_STATUS_PROPERTY)
    property_kind = notion_property_kind(data_source_id, property_name)
    payload = {"properties": {property_name: {property_kind: {"name": status}}}}
    return notion_api_request("PATCH", f"/pages/{page_id}", payload)


def notion_add_comment(page_id: str, body: str) -> dict[str, Any]:
    chunks = [body[index : index + 1900] for index in range(0, len(body), 1900)] or [body]
    rich_text = [{"type": "text", "text": {"content": chunk}} for chunk in chunks]
    payload = {"parent": {"page_id": page_id}, "rich_text": rich_text}
    return notion_api_request("POST", "/comments", payload)


def notion_property_value(schema: dict[str, Any], value: Any) -> dict[str, Any] | None:
    kind = str(schema.get("type", ""))
    text = str(value or "").strip()
    if kind == "title":
        return {"title": notion_rich_text_chunks(text[:2000])}
    if kind == "rich_text":
        return {"rich_text": notion_rich_text_chunks(text[:2000])}
    if kind in {"select", "status"}:
        if not text:
            return None
        return {kind: {"name": text}}
    if kind == "date":
        if not text:
            return None
        return {"date": {"start": text}}
    if kind == "number":
        try:
            return {"number": int(value)}
        except (TypeError, ValueError):
            return None
    if kind == "url":
        return {"url": text or None}
    return None


def build_brainstorm_properties(digest: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    project_value = digest["project"]
    project_schema_name = {name.lower(): name for name in schema}.get("project")
    if project_schema_name and schema[project_schema_name].get("type") in {"select", "status"}:
        projects = digest.get("projects", [])
        project_value = projects[0] if projects else ""
    wanted = {
        "Name": digest["name"],
        "Date": digest["date"],
        "Source": digest["source"],
        "Owner": digest["owner"],
        "Project": project_value,
        "Domain": digest["domain"],
        "Status": digest["status"],
        "Confidence": digest["confidence"],
        "Source Ref": digest["source_ref"],
        "Proposed Actions Count": len(digest.get("proposed_actions", [])),
    }
    properties: dict[str, Any] = {}
    lower_schema = {name.lower(): name for name in schema}
    for wanted_name, value in wanted.items():
        actual = lower_schema.get(wanted_name.lower())
        if not actual:
            continue
        property_value = notion_property_value(schema[actual], value)
        if property_value is not None:
            properties[actual] = property_value
    title_property = find_schema_property_by_type(schema, "title")
    if title_property and title_property not in properties:
        properties[title_property] = {"title": notion_rich_text_chunks(str(digest["name"])[:2000])}
    return properties


def find_schema_property_by_type(schema: dict[str, Any], prop_type: str) -> str:
    for name, value in schema.items():
        if value.get("type") == prop_type:
            return name
    return ""


def build_brainstorm_children(digest: dict[str, Any]) -> list[dict[str, Any]]:
    children: list[dict[str, Any]] = [
        notion_text_block("heading_2", "Summary"),
        notion_text_block("paragraph", digest.get("summary", "")),
        notion_text_block("heading_2", "Routing"),
        notion_text_block(
            "paragraph",
            f"Owner: {digest.get('owner', '')}\nProject: {digest.get('project', '') or 'Unmatched'}\nDomain: {digest.get('domain', '')}\nOutcome: {digest.get('main_outcome', '')}\nConfidence: {digest.get('confidence', '')}",
        ),
        notion_text_block("heading_2", "Key Decisions"),
        *notion_bullets(digest.get("decisions", [])),
        notion_text_block("heading_2", "Proposed Actions"),
        *notion_bullets(digest.get("proposed_actions", [])),
        notion_text_block("heading_2", "Project Ideas"),
        *notion_bullets(digest.get("project_ideas", [])),
        notion_text_block("heading_2", "Open Questions"),
        *notion_bullets(digest.get("open_questions", [])),
        notion_text_block("heading_2", "Handoff Notes"),
        *notion_bullets(digest.get("handoff_notes", [])),
        notion_text_block("heading_2", "Routed Items"),
    ]
    routed = [
        f"{item.get('owner')} / {item.get('project') or 'Unmatched'} / {item.get('domain')} / {item.get('type')}: {item.get('text')}"
        for item in digest.get("routed_items", [])
    ]
    children.extend(notion_bullets(routed))
    children.extend(
        [
            notion_text_block("heading_2", "Why This May Matter Later"),
            notion_text_block("paragraph", digest.get("why_it_matters_later", "")),
            notion_text_block("paragraph", "Raw transcript intentionally not stored here. Voicepal remains the raw source archive."),
        ]
    )
    return children[:95]


def notion_create_brainstorm_digest(digest: dict[str, Any], data_source_id: str) -> dict[str, Any]:
    schema = notion_data_source_schema(data_source_id)
    payload = {
        "parent": {"type": "data_source_id", "data_source_id": data_source_id},
        "properties": build_brainstorm_properties(digest, schema),
        "children": build_brainstorm_children(digest),
    }
    return notion_api_request("POST", "/pages", payload)


def notion_rich_text_chunks(text: str, chunk_size: int = 1900) -> list[dict[str, Any]]:
    chunks = [text[index : index + chunk_size] for index in range(0, len(text), chunk_size)] or [""]
    return [{"type": "text", "text": {"content": chunk}} for chunk in chunks]


def notion_text_block(block_type: str, text: str) -> dict[str, Any]:
    return {
        "object": "block",
        "type": block_type,
        block_type: {"rich_text": notion_rich_text_chunks(text)},
    }


def notion_bullets(items: list[str]) -> list[dict[str, Any]]:
    return [notion_text_block("bulleted_list_item", item) for item in items if item.strip()]


def normalize_status(status: str | None) -> str:
    return (status or "").strip().lower()


def meaningful_text(value: str) -> bool:
    text = clean_model_text(value)
    if not text:
        return False
    lowered = text.lower()
    empty_markers = {
        "none",
        "no open items",
        "no open item",
        "nothing open",
        "nothing to do",
        "n/a",
        "not applicable",
        "complete",
        "completed",
    }
    return lowered not in empty_markers


def debrief_has_actionable_carryover(debrief: Debrief) -> bool:
    if meaningful_text(debrief.open_items) or meaningful_text(debrief.next_steps):
        return True
    lowered = f"{debrief.session_summary}\n{debrief.content}".lower()
    action_patterns = [
        "what's next",
        "whats next",
        "next:",
        "next steps",
        "still need",
        "needs ",
        "todo",
        "to do",
        "open item",
        "follow up",
        "follow-up",
        "continue ",
        "unresolved",
    ]
    return any(pattern in lowered for pattern in action_patterns)


def normalize_carryover(value: Any, *, debrief: Debrief, result: str) -> str:
    text = str(value or "").strip()
    if text.lower().replace("-", " ") in {"actionable", "open"}:
        return CARRYOVER_ACTIONABLE
    if text.lower().replace("-", " ") in {"not actionable", "not relevant", "none", "closed"}:
        if debrief_has_actionable_carryover(debrief):
            return CARRYOVER_ACTIONABLE
        return CARRYOVER_NOT_ACTIONABLE
    if text.lower() == "resolved":
        return CARRYOVER_RESOLVED
    if result == "useful_review" or debrief_has_actionable_carryover(debrief):
        return CARRYOVER_ACTIONABLE
    return CARRYOVER_NOT_ACTIONABLE


def topic_is_specific(topic: str, project_name: str = "") -> bool:
    text = clean_model_text(topic)
    if not text or ":" not in text:
        return False
    generic = {"cron job", "cron", "brainstorm", "telegram", "notion", "friday", "project intelligence"}
    lowered = text.lower().strip()
    if lowered in generic or lowered == project_name.lower().strip():
        return False
    words = re.findall(r"[A-Za-z0-9]+", text)
    return len(words) >= 5


def concise_phrase(value: str, max_words: int = 5) -> str:
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9_.-]*", clean_model_text(value))
    return " ".join(words[:max_words]) if words else "follow-up work"


def infer_carryover_topic(debrief: Debrief, route: dict[str, Any], proposed_topic: str = "") -> str:
    project = route.get("project_name") or debrief.project_name or "Friday"
    if topic_is_specific(proposed_topic, project):
        return clean_model_text(proposed_topic)

    text = f"{debrief.title}\n{debrief.session_summary}\n{debrief.open_items}\n{debrief.next_steps}\n{debrief.content}".lower()
    if "voicepal" in text or "brainstorm" in text:
        module = "Voicepal brainstorm intake"
        if "digest" in text and ("quality" in text or "extraction" in text):
            capability = "digest quality extraction"
        elif "transcript" in text or "filing" in text or "telegram" in text:
            capability = "Telegram transcript filing"
        else:
            capability = concise_phrase(debrief.next_steps or debrief.open_items or debrief.session_summary)
    elif "cron" in text or "auto-run" in text or "watcher" in text or "project intelligence" in text:
        module = "project-intelligence cron"
        if "telegram" in text and ("context" in text or "suggestion" in text or "comment" in text):
            capability = "useful-review Telegram context"
        elif "useful-review" in text and ("live" in text or "trigger" in text or "verify" in text):
            capability = "useful-review live path verification"
        elif "nameerror" in text or "config" in text:
            capability = "auto-run NameError recovery"
        else:
            capability = concise_phrase(debrief.next_steps or debrief.open_items or debrief.session_summary)
    else:
        module = concise_phrase(debrief.session_summary or debrief.title, max_words=4)
        capability = concise_phrase(debrief.next_steps or debrief.open_items or debrief.session_summary)

    return f"{project} {module}: {capability}"


def carryover_metadata(
    debrief: Debrief,
    route: dict[str, Any],
    executive_result: dict[str, Any],
) -> dict[str, str]:
    result = str(executive_result.get("result") or "").strip()
    carryover = normalize_carryover(executive_result.get("carryover"), debrief=debrief, result=result)
    topic = infer_carryover_topic(debrief, route, str(executive_result.get("carryover_topic") or ""))
    reason = clean_model_text(executive_result.get("carryover_reason")) or (
        "Debrief has open items or next steps."
        if debrief_has_actionable_carryover(debrief)
        else "No clear next-session carryover found."
    )
    return {
        "carryover": carryover,
        "carryover_topic": topic,
        "carryover_reason": reason,
    }


def parse_debrief(raw: dict[str, Any]) -> Debrief:
    return Debrief(
        id=str(raw.get("id", "")).strip(),
        title=str(raw.get("title", "")).strip(),
        review_status=str(raw.get("review_status", "")).strip(),
        project_name=str(raw.get("project_name", "")).strip(),
        repo_url=str(raw.get("repo_url", "")).strip(),
        local_repo_path=str(raw.get("local_repo_path", "")).strip(),
        session_summary=str(raw.get("session_summary", "")).strip(),
        open_items=str(raw.get("open_items", "")).strip(),
        next_steps=str(raw.get("next_steps", "")).strip(),
        content=str(raw.get("content", "")).strip(),
        carryover=str(raw.get("carryover", "")).strip(),
        carryover_topic=str(raw.get("carryover_topic", "")).strip(),
    )


def load_fixture_debriefs(path: Path = FIXTURE_PATH) -> list[Debrief]:
    data = load_json(path)
    return [parse_debrief(item) for item in data.get("debriefs", [])]


def parse_brainstorm(raw: dict[str, Any]) -> BrainstormTranscript:
    title = str(raw.get("title", "")).strip() or "Untitled Brainstorm"
    transcript = str(raw.get("transcript", "") or raw.get("content", "")).strip()
    date = str(raw.get("date", "")).strip() or datetime.now(timezone.utc).date().isoformat()
    source_ref = str(raw.get("source_ref", "") or raw.get("sourceRef", "")).strip()
    fingerprint = brainstorm_fingerprint(title, date, transcript)
    return BrainstormTranscript(
        id=str(raw.get("id", "")).strip() or fingerprint,
        title=title,
        date=date,
        transcript=transcript,
        source_ref=source_ref or title,
        source=str(raw.get("source", "")).strip() or "voicepal_telegram",
    )


def load_fixture_brainstorms(path: Path = FIXTURE_BRAINSTORM_PATH) -> list[BrainstormTranscript]:
    data = load_json(path)
    return [parse_brainstorm(item) for item in data.get("brainstorms", [])]


def load_brainstorm_file(path: Path, *, title: str = "", date: str = "", source_ref: str = "") -> BrainstormTranscript:
    text = path.read_text(encoding="utf-8")
    return load_brainstorm_text(text, title=title or path.stem, date=date, source_ref=source_ref or str(path))


def load_brainstorm_text(text: str, *, title: str = "", date: str = "", source_ref: str = "") -> BrainstormTranscript:
    detected_title, transcript = split_brainstorm_title(text)
    return parse_brainstorm(
        {
            "title": title or detected_title or "Untitled Brainstorm",
            "date": date or datetime.now(timezone.utc).date().isoformat(),
            "source_ref": source_ref or title or detected_title or "stdin",
            "transcript": transcript,
        }
    )


def split_brainstorm_title(text: str) -> tuple[str, str]:
    lines = [line.rstrip() for line in text.splitlines()]
    non_empty = [line.strip() for line in lines if line.strip()]
    if not non_empty:
        return "", ""
    first = non_empty[0]
    if len(first) <= 120 and not first.lower().startswith(("assistant:", "you:", "user:")):
        rest = "\n".join(lines[1:]).strip()
        return first, rest or text.strip()
    return "", text.strip()


def brainstorm_fingerprint(title: str, date: str, transcript: str) -> str:
    digest = hashlib.sha256()
    normalized = "\n".join(line.strip().lower() for line in transcript.splitlines() if line.strip())
    digest.update(f"{title.strip().lower()}\n{date.strip()}\n{normalized}".encode("utf-8", errors="replace"))
    return digest.hexdigest()[:16]


def load_project_map() -> dict[str, Any]:
    if not PROJECT_MAP_PATH.exists():
        return {"version": 1, "projects": []}
    return load_json(PROJECT_MAP_PATH)


def load_processed_state() -> dict[str, Any]:
    defaults = {
        "version": 1,
        "lastCheckedAt": None,
        "processedDebriefs": [],
        "unresolvedMappings": [],
    }
    if not PROCESSED_PATH.exists():
        return defaults
    data = load_json(PROCESSED_PATH)
    return defaults | data


def load_processed_brainstorm_state() -> dict[str, Any]:
    defaults = {
        "version": 1,
        "processedBrainstorms": [],
    }
    if not PROCESSED_BRAINSTORMS_PATH.exists():
        return defaults
    data = load_json(PROCESSED_BRAINSTORMS_PATH)
    return defaults | data


def state_id_set(items: list[Any]) -> set[str]:
    ids: set[str] = set()
    for item in items:
        if isinstance(item, str):
            ids.add(item)
        elif isinstance(item, dict) and item.get("id"):
            ids.add(str(item["id"]))
    return ids


def append_state_record(state: dict[str, Any], key: str, record: dict[str, Any]) -> None:
    existing = state_id_set(state.get(key, []))
    if str(record["id"]) not in existing:
        state.setdefault(key, []).append(record)


def mark_processed(
    state: dict[str, Any],
    debrief: Debrief,
    *,
    outcome: str,
    status: str,
    telegram_sent: bool = False,
    error: str = "",
) -> None:
    append_state_record(
        state,
        "processedDebriefs",
        {
            "id": debrief.id,
            "title": debrief.title,
            "outcome": outcome,
            "status": status,
            "telegramSent": telegram_sent,
            "error": error,
            "processedAt": datetime.now(timezone.utc).isoformat(),
        },
    )


def mark_unresolved_mapping(state: dict[str, Any], debrief: Debrief, route: dict[str, Any]) -> None:
    append_state_record(
        state,
        "unresolvedMappings",
        {
            "id": debrief.id,
            "title": debrief.title,
            "project": route.get("project_name") or debrief.project_name,
            "recordedAt": datetime.now(timezone.utc).isoformat(),
        },
    )


def mark_brainstorm_processed(
    state: dict[str, Any],
    brainstorm: BrainstormTranscript,
    *,
    fingerprint: str,
    outcome: str,
    status: str,
    notion_page_id: str = "",
) -> None:
    append_state_record(
        state,
        "processedBrainstorms",
        {
            "id": fingerprint,
            "title": brainstorm.title,
            "date": brainstorm.date,
            "sourceRef": brainstorm.source_ref,
            "outcome": outcome,
            "status": status,
            "notionPageId": notion_page_id,
            "processedAt": datetime.now(timezone.utc).isoformat(),
        },
    )


def project_map_lookup(project_name: str, project_map: dict[str, Any]) -> dict[str, str]:
    wanted = project_name.strip().lower()
    for project in project_map.get("projects", []):
        names = [project.get("name", ""), *project.get("aliases", [])]
        if any(str(name).strip().lower() == wanted for name in names):
            return {
                "repo_url": str(project.get("repo_url", "")).strip(),
                "local_repo_path": str(project.get("local_repo_path", "")).strip(),
            }
    return {"repo_url": "", "local_repo_path": ""}


def clean_model_text(value: Any) -> str:
    text = str(value or "").strip()
    if text.lower() in {"not provided", "none", "null", "n/a", "unknown", "not specified"}:
        return ""
    return text


def model_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "1"}
    return bool(value)


def repo_from_text(text: str) -> str:
    match = re.search(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", text)
    return match.group(0) if match else ""


def sentence_chunks(text: str, max_items: int = 18) -> list[str]:
    chunks: list[str] = []
    for line in text.splitlines():
        cleaned = re.sub(r"\s+", " ", line).strip()
        if not cleaned:
            continue
        chunks.extend(re.split(r"(?<=[.!?])\s+", cleaned))
    return [chunk.strip() for chunk in chunks if len(chunk.strip()) > 20][:max_items]


def brainstorm_signal_text(text: str) -> str:
    """Prefer Amit's Voicepal answers over interviewer prompts."""
    normalized = text.replace("\r\n", "\n")
    matches = re.findall(
        r"(?:^|\b)(?:You|User)\s*:\s*(.*?)(?=\s*(?:Assistant|You|User)\s*:|\Z)",
        normalized,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if matches:
        return "\n".join(match.strip() for match in matches if match.strip())
    lines = []
    for line in normalized.splitlines():
        stripped = line.strip()
        if not stripped or stripped.lower().startswith("assistant:"):
            continue
        lines.append(stripped)
    return "\n".join(lines).strip()


def first_matching_sentences(text: str, patterns: list[str], *, max_items: int = 6) -> list[str]:
    matches: list[str] = []
    lowered_patterns = [pattern.lower() for pattern in patterns]
    for sentence in sentence_chunks(text, max_items=80):
        lowered = sentence.lower()
        if any(pattern in lowered for pattern in lowered_patterns):
            matches.append(sentence)
        if len(matches) >= max_items:
            break
    return matches


def classify_brainstorm_owner(text: str) -> str:
    lowered = text.lower()
    friday_hits = sum(
        1
        for token in [
            "friday",
            "project",
            "github",
            "repo",
            "software",
            "feature",
            "build",
            "business",
            "school",
            "trading",
            "stock",
            "agent",
            "openclaw",
        ]
        if token in lowered
    )
    jarvis_hits = sum(
        1
        for token in [
            "jarvis",
            "personal",
            "journal",
            "health",
            "garmin",
            "calendar",
            "morning briefing",
            "evening review",
            "routine",
            "weather",
            "readwise",
        ]
        if token in lowered
    )
    if friday_hits and jarvis_hits:
        return "Mixed"
    if friday_hits:
        return "Friday"
    if jarvis_hits:
        return "Jarvis"
    return "Unknown"


def classify_brainstorm_domain(text: str) -> str:
    lowered = text.lower()
    domains: list[str] = []
    if any(token in lowered for token in ["stock", "trading", "portfolio", "finance", "buy", "sell"]):
        domains.append("Finance Module")
    if any(token in lowered for token in ["school", "exam", "math", "computer science", "literature"]):
        domains.append("School")
    if any(token in lowered for token in ["business", "startup", "sell", "software idea"]):
        domains.append("Business")
    if any(token in lowered for token in ["journal", "health", "garmin", "calendar", "personal", "routine", "felt", "feeling", "stressed"]):
        domains.append("Personal")
    if any(token in lowered for token in ["project", "github", "repo", "feature", "build", "openclaw", "agent"]):
        domains.append("Project")
    unique = list(dict.fromkeys(domains))
    if len(unique) > 1:
        return "Mixed"
    return unique[0] if unique else "Project"


def infer_brainstorm_projects(text: str, project_map: dict[str, Any]) -> list[str]:
    lowered = text.lower()
    projects: list[str] = []
    known = [project.get("name", "") for project in project_map.get("projects", [])]
    for name in ["Friday", "Jarvis", "Jarvis-Friday Bridge", *known]:
        if name and name.lower() in lowered and name not in projects:
            projects.append(str(name))
    if "morning briefing" in lowered and "Jarvis" not in projects:
        projects.append("Jarvis")
    if ("voicepal" in lowered or "brainstorm" in lowered) and "Friday" not in projects:
        projects.append("Friday")
    if ("stock" in lowered or "trading" in lowered) and "Friday" not in projects:
        projects.append("Friday")
    return projects


def item_route(sentence: str, overall_owner: str, projects: list[str]) -> dict[str, str]:
    lowered = sentence.lower()
    owner = overall_owner if overall_owner != "Unknown" else "Unknown"
    project = projects[0] if projects else ""
    domain = classify_brainstorm_domain(sentence)
    item_type = "Context"

    build_terms = ["build", "feature", "add", "improve", "fix", "design", "create", "module", "agent", "openclaw", "learn"]
    personal_context_terms = ["felt", "feeling", "bothering me", "my day", "journal", "health", "routine"]
    if any(term in lowered for term in personal_context_terms) and not re.search(r"\bjarvis\s+should\b", lowered):
        owner = "Jarvis"
        project = project if project != "Friday" else ""
        item_type = "Personal Context"
    elif "jarvis" in lowered and (any(term in lowered for term in build_terms) or re.search(r"\bjarvis\s+should\b", lowered)):
        owner = "Friday"
        project = "Jarvis"
        item_type = "Feature Idea"
    elif "friday" in lowered or any(term in lowered for term in ["project", "repo", "github", "software"]):
        owner = "Friday"
        item_type = "Project Context"
    elif "jarvis" in lowered:
        owner = "Jarvis"
        project = "Jarvis"

    if "stock" in lowered or "trading" in lowered or "finance" in lowered:
        owner = "Friday"
        project = "Friday"
        domain = "Finance Module"
        item_type = "Future Module"
    if "jarvis" in lowered and "friday" in lowered:
        owner = "Mixed"
        project = "Jarvis-Friday Bridge"
        item_type = "Cross-Agent Idea"

    return {"owner": owner, "project": project, "domain": domain, "type": item_type}


def extract_brainstorm_decisions(text: str) -> list[str]:
    patterns = ["i want", "should", "need", "would like", "going to", "don't need", "do not", "raw", "notion", "telegram"]
    return first_matching_sentences(text, patterns, max_items=8)


def extract_brainstorm_actions(text: str) -> list[str]:
    patterns = ["create", "add", "build", "implement", "configure", "send", "store", "link", "route", "extract", "process"]
    return first_matching_sentences(text, patterns, max_items=10)


def extract_brainstorm_questions(text: str) -> list[str]:
    questions = re.findall(r"[^?]{12,160}\?", text)
    return [question.strip() for question in questions[:8]]


def build_brainstorm_digest(brainstorm: BrainstormTranscript) -> dict[str, Any]:
    project_map = load_project_map()
    text = brainstorm.transcript
    signal_text = brainstorm_signal_text(text)
    fingerprint = brainstorm_fingerprint(brainstorm.title, brainstorm.date, text)
    owner = classify_brainstorm_owner(signal_text)
    domain = classify_brainstorm_domain(signal_text)
    projects = infer_brainstorm_projects(signal_text, project_map)
    decisions = extract_brainstorm_decisions(signal_text)
    actions = extract_brainstorm_actions(signal_text)
    questions = extract_brainstorm_questions(signal_text)
    idea_sentences = first_matching_sentences(
        signal_text,
        ["idea", "feature", "module", "software", "project", "could", "maybe"],
        max_items=8,
    )
    personal_sentences = first_matching_sentences(
        signal_text,
        ["i felt", "i feel", "my journal", "my day", "health", "routine", "personal"],
        max_items=6,
    )
    routed_items = [
        {"text": item, **item_route(item, owner, projects)}
        for item in list(dict.fromkeys([*decisions, *actions, *idea_sentences, *personal_sentences]))[:18]
    ]
    handoff_notes = [
        item["text"]
        for item in routed_items
        if item.get("owner") == "Jarvis" and item.get("type") == "Personal Context"
    ][:6]
    status = "Needs Clarification" if owner == "Unknown" else "Processed"
    confidence = "High" if projects and owner != "Unknown" else ("Medium" if owner != "Unknown" else "Low")
    main_outcome = "Ask clarification" if status == "Needs Clarification" else ("Link to latest debrief" if projects else "Store digest only")
    name = f"{brainstorm.title} - {brainstorm.date}"

    return {
        "fingerprint": fingerprint,
        "name": name,
        "title": brainstorm.title,
        "date": brainstorm.date,
        "source": "Voicepal Telegram",
        "source_ref": brainstorm.source_ref,
        "owner": owner,
        "domain": domain,
        "projects": projects,
        "project": ", ".join(projects),
        "status": status,
        "confidence": confidence,
        "main_outcome": main_outcome,
        "summary": summarize_brainstorm(signal_text, owner, projects),
        "decisions": decisions,
        "proposed_actions": actions,
        "project_ideas": idea_sentences,
        "open_questions": questions,
        "handoff_notes": handoff_notes,
        "routed_items": routed_items,
        "why_it_matters_later": why_brainstorm_matters(owner, projects, actions, decisions),
        "raw_transcript_stored": False,
    }


def summarize_brainstorm(text: str, owner: str, projects: list[str]) -> str:
    first_sentences = sentence_chunks(text, max_items=3)
    project_text = ", ".join(projects) if projects else "no confident project"
    if first_sentences:
        return f"Voicepal brainstorm classified as {owner} with {project_text}. Main thread: {' '.join(first_sentences)[:500]}"
    return f"Voicepal brainstorm classified as {owner} with {project_text}."


def why_brainstorm_matters(owner: str, projects: list[str], actions: list[str], decisions: list[str]) -> str:
    if owner == "Unknown":
        return "Friday needs a clarification before this can become reliable project intelligence."
    pieces = [f"It records {owner.lower()}-owned intent"]
    if projects:
        pieces.append(f"for {', '.join(projects)}")
    if actions:
        pieces.append(f"with {len(actions)} possible follow-up actions")
    if decisions:
        pieces.append(f"and {len(decisions)} decisions/preferences to preserve")
    return " ".join(pieces) + "."


def preview_brainstorm(brainstorm: BrainstormTranscript) -> dict[str, Any]:
    digest = build_brainstorm_digest(brainstorm)
    state = load_processed_brainstorm_state()
    processed = state_id_set(state.get("processedBrainstorms", []))
    duplicate = digest["fingerprint"] in processed
    telegram = draft_brainstorm_telegram_reply(digest, duplicate=duplicate)
    return {
        "dry_run": True,
        "duplicate": duplicate,
        "raw_transcript_stored": False,
        "digest": digest,
        "telegram_message": telegram,
        "planned_actions": [{"type": "skip", "reason": "Duplicate brainstorm fingerprint."}]
        if duplicate
        else brainstorm_planned_actions(digest),
    }


def brainstorm_planned_actions(digest: dict[str, Any]) -> list[dict[str, Any]]:
    actions = [
        {"type": "notion_page", "database": "Brainstorm Digests", "name": digest["name"]},
        {"type": "notion_body", "stores_raw_transcript": False},
    ]
    if digest.get("main_outcome") == "Ask clarification":
        actions.append({"type": "telegram_clarification", "body": "I need one clarification before routing this brainstorm."})
    else:
        actions.append({"type": "telegram_summary", "body": draft_brainstorm_telegram_reply(digest)})
    if digest.get("projects"):
        actions.append({"type": "project_link_candidate", "projects": digest.get("projects", [])})
    return actions


def draft_brainstorm_telegram_reply(digest: dict[str, Any], *, duplicate: bool = False) -> str:
    if duplicate:
        return f"I already filed `{digest['name']}`. I skipped the duplicate."
    projects = digest.get("project") or "Unmatched"
    decisions = len(digest.get("decisions", []))
    actions = len(digest.get("proposed_actions", []))
    future_modules = sum(1 for item in digest.get("routed_items", []) if item.get("type") == "Future Module")
    if digest.get("main_outcome") == "Ask clarification":
        return (
            f"Filed a draft digest for `{digest['name']}`, but I need one clarification before routing it. "
            "Is this for Friday, Jarvis, or both?"
        )
    extra = f", and {future_modules} future modules" if future_modules else ""
    return (
        f"Filed `{digest['name']}`. Owner: {digest.get('owner')}. Projects: {projects}. "
        f"I found {decisions} decisions, {actions} proposed actions{extra}."
    )


def apply_brainstorm(
    brainstorm: BrainstormTranscript,
    *,
    data_source_id: str = "",
    telegram_reply_to: str = "",
    send_telegram: bool = False,
) -> dict[str, Any]:
    config = load_runtime_config()
    target_data_source_id = data_source_id or str(config["brainstorm"].get("data_source_id", "")).strip()
    if not target_data_source_id:
        raise RuntimeError("Brainstorm Digests data source ID is missing. Run discovery/create first or pass --brainstorm-data-source-id.")

    preview = preview_brainstorm(brainstorm)
    digest = preview["digest"]
    if preview["duplicate"]:
        return {"applied": False, "duplicate": True, "preview": preview}

    page = notion_create_brainstorm_digest(digest, target_data_source_id)
    state = load_processed_brainstorm_state()
    mark_brainstorm_processed(
        state,
        brainstorm,
        fingerprint=digest["fingerprint"],
        outcome=digest["main_outcome"],
        status=digest["status"],
        notion_page_id=str(page.get("id", "")),
    )
    save_json(PROCESSED_BRAINSTORMS_PATH, state)

    telegram_result = None
    if send_telegram:
        target = telegram_reply_to or str(config["telegram"].get("reply_to", "")).strip()
        if not target:
            raise RuntimeError("Telegram reply target is missing.")
        telegram_result = send_openclaw_telegram(preview["telegram_message"], target)

    return {
        "applied": True,
        "page_id": page.get("id"),
        "page_url": page.get("url"),
        "telegram_sent": bool(telegram_result),
        "telegram_result": telegram_result,
        "preview": preview,
    }


def deterministic_route(debrief: Debrief, project_map: dict[str, Any]) -> dict[str, Any]:
    status = normalize_status(debrief.review_status)
    project_name = debrief.project_name or infer_project_name(debrief)
    repo_url = debrief.repo_url or repo_from_text(debrief.content)
    local_repo_path = debrief.local_repo_path

    if not repo_url and not local_repo_path and project_name:
        mapped = project_map_lookup(project_name, project_map)
        repo_url = mapped["repo_url"]
        local_repo_path = mapped["local_repo_path"]

    if status in HANDLED_STATUSES:
        return {
            "project_name": project_name,
            "repo_url": repo_url,
            "repo_hint": local_repo_path or "",
            "review_status": debrief.review_status,
            "has_enough_context": False,
            "should_launch_review": False,
            "reason": f"Skipped because status is {debrief.review_status}.",
        }

    has_repo = bool(repo_url or local_repo_path)
    return {
        "project_name": project_name,
        "repo_url": repo_url,
        "repo_hint": local_repo_path or ("explicit repo URL found" if repo_url else ""),
        "review_status": debrief.review_status or "New",
        "has_enough_context": has_repo,
        "should_launch_review": has_repo,
        "reason": "Safe repo match found." if has_repo else "No repository URL, local path, or confirmed mapping found.",
    }


def infer_project_name(debrief: Debrief) -> str:
    text = f"{debrief.title}\n{debrief.content}"
    match = re.search(r"Project:\s*([^\n.]+)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return debrief.title.replace(" session", "").strip()


def discover_ollama_command() -> list[str]:
    found = shutil.which("ollama")
    if found:
        return [found]
    for candidate in COMMON_OLLAMA_PATHS:
        if candidate.exists():
            return [str(candidate)]
    raise RuntimeError("Ollama CLI was not found in PATH or common install locations.")


def normalize_ollama_model_tag(model_tag: str) -> str:
    tag = str(model_tag or "").strip()
    if tag.startswith("ollama/"):
        return tag.split("/", 1)[1]
    return tag or "falcon3:3b"


def ollama_generate_json(model_tag: str, prompt: str, *, timeout_seconds: int) -> dict[str, Any]:
    payload = json.dumps(
        {
            "model": normalize_ollama_model_tag(model_tag),
            "prompt": prompt,
            "stream": False,
            "format": OLLAMA_ROUTE_SCHEMA,
            "options": {
                "temperature": 0,
            },
        }
    ).encode("utf-8")
    request = Request(
        OLLAMA_API_GENERATE,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Friday-Project-Intelligence/1.0",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            body = response.read().decode("utf-8", errors="replace")
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(detail or str(exc)) from exc
    payload_json = json.loads(body)
    if "error" in payload_json:
        raise RuntimeError(str(payload_json["error"]))
    return json.loads(extract_json_object(str(payload_json.get("response", ""))))


def build_router_prompt(debrief: Debrief) -> str:
    prompt_template = PROMPT_PATH.read_text(encoding="utf-8")
    prompt = prompt_template.replace("{{REVIEW_STATUS}}", debrief.review_status or "New")
    return prompt.replace("{{DEBRIEF_TEXT}}", debrief.content)


def merge_model_route(debrief: Debrief, project_map: dict[str, Any], data: dict[str, Any]) -> dict[str, Any]:
    deterministic = deterministic_route(debrief, project_map)
    data["project_name"] = deterministic["project_name"] or clean_model_text(data.get("project_name"))
    data["review_status"] = deterministic["review_status"]
    data["repo_url"] = clean_model_text(data.get("repo_url"))
    data["repo_hint"] = clean_model_text(data.get("repo_hint"))
    data["has_enough_context"] = model_bool(data.get("has_enough_context"))
    data["should_launch_review"] = model_bool(data.get("should_launch_review"))
    if deterministic["repo_url"]:
        data["repo_url"] = deterministic["repo_url"]
    if deterministic["repo_hint"]:
        data["repo_hint"] = deterministic["repo_hint"]
    if not deterministic["has_enough_context"]:
        data["has_enough_context"] = False
        data["should_launch_review"] = False
        data["repo_url"] = deterministic["repo_url"]
        data["repo_hint"] = deterministic["repo_hint"]
        data["reason"] = deterministic["reason"]
    elif deterministic["has_enough_context"]:
        data["has_enough_context"] = True
        data["should_launch_review"] = True
        if not clean_model_text(data.get("reason")):
            data["reason"] = deterministic["reason"]
    return data


def ollama_route(
    debrief: Debrief,
    project_map: dict[str, Any],
    *,
    model_tag: str,
    timeout_seconds: int = 120,
) -> dict[str, Any]:
    try:
        prompt = build_router_prompt(debrief)
        data = ollama_generate_json(model_tag, prompt, timeout_seconds=timeout_seconds)
        return merge_model_route(debrief, project_map, data)
    except Exception as exc:  # noqa: BLE001 - fallback is intentional and reported.
        route = deterministic_route(debrief, project_map)
        route["reason"] = f"{normalize_ollama_model_tag(model_tag)} routing fallback used: {exc}"
        return route


def configured_local_router_route(
    debrief: Debrief,
    project_map: dict[str, Any],
    *,
    model_tag: str,
) -> dict[str, Any]:
    """Route with the configured local Ollama router and deterministic guardrails."""
    return ollama_route(debrief, project_map, model_tag=model_tag, timeout_seconds=120)


def extract_json_object(text: str) -> str:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("No JSON object found in router output")
    return text[start : end + 1]


def extract_first_json_object(text: str) -> str:
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            _, end = decoder.raw_decode(text[index:])
            return text[index : index + end]
        except json.JSONDecodeError:
            continue
    raise ValueError("No JSON object found in text")


def parse_github_repo_url(repo_url: str) -> tuple[str, str] | None:
    parsed = urlparse(repo_url)
    if parsed.netloc.lower() not in {"github.com", "www.github.com"}:
        return None
    parts = [part for part in parsed.path.strip("/").split("/") if part]
    if len(parts) < 2:
        return None
    owner = parts[0]
    repo = re.sub(r"\.git$", "", parts[1])
    return owner, repo


def github_api_get(path: str) -> Any:
    request = Request(
        f"https://api.github.com{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "Friday-Project-Intelligence/1.0",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def read_windows_user_env(name: str) -> str:
    if os.name != "nt":
        return ""
    powershell = shutil.which("powershell") or shutil.which("pwsh")
    if not powershell:
        return ""
    try:
        result = subprocess.run(
            [
                powershell,
                "-NoProfile",
                "-Command",
                f"[Environment]::GetEnvironmentVariable('{name}','User')",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def decode_github_text_file(file_info: dict[str, Any], max_chars: int = 6000) -> str:
    if file_info.get("encoding") != "base64" or not file_info.get("content"):
        return ""
    raw = base64.b64decode(str(file_info["content"])).decode("utf-8", errors="replace")
    return raw[:max_chars]


def inspect_github_remote(repo_url: str) -> dict[str, Any]:
    parsed = parse_github_repo_url(repo_url)
    if not parsed:
        return {"available": True, "kind": "remote", "repo_url": repo_url, "note": "Remote repo URL available; no clone/write performed."}

    owner, repo = parsed
    context: dict[str, Any] = {
        "available": True,
        "kind": "remote-github",
        "repo_url": repo_url,
        "owner": owner,
        "repo": repo,
        "write_mode": "none",
    }
    try:
        metadata = github_api_get(f"/repos/{owner}/{repo}")
        default_branch = metadata.get("default_branch") or "main"
        context.update(
            {
                "description": metadata.get("description") or "",
                "default_branch": default_branch,
                "updated_at": metadata.get("updated_at") or "",
                "pushed_at": metadata.get("pushed_at") or "",
            }
        )
        root_contents = github_api_get(f"/repos/{owner}/{repo}/contents?ref={default_branch}")
        if isinstance(root_contents, list):
            context["top_level_files"] = [
                {"name": item.get("name"), "type": item.get("type")}
                for item in root_contents[:60]
            ]
        commits = github_api_get(f"/repos/{owner}/{repo}/commits?per_page=8&sha={default_branch}")
        if isinstance(commits, list):
            context["recent_commits"] = [
                {
                    "sha": str(commit.get("sha", ""))[:7],
                    "date": (((commit.get("commit") or {}).get("committer") or {}).get("date") or ""),
                    "message": str(((commit.get("commit") or {}).get("message") or "")).splitlines()[0],
                }
                for commit in commits[:8]
            ]
        docs: dict[str, str] = {}
        for filename in ("CLAUDE.md", "AGENTS.md", "README.md"):
            try:
                info = github_api_get(f"/repos/{owner}/{repo}/contents/{filename}?ref={default_branch}")
                if isinstance(info, dict):
                    text = decode_github_text_file(info)
                    if text:
                        docs[filename] = text
            except (HTTPError, URLError, TimeoutError):
                continue
        if docs:
            context["documents"] = docs
    except HTTPError as error:
        context.update({"available": False, "reason": f"GitHub API returned {error.code}: {error.reason}"})
    except (URLError, TimeoutError) as error:
        context.update({"available": False, "reason": f"GitHub API request failed: {error}"})
    return context


def inspect_repo_context(route: dict[str, Any], fetch_remote: bool = False) -> dict[str, Any]:
    """Inspect repo context without cloning or writing project repositories."""
    repo_url = str(route.get("repo_url", "")).strip()
    local_path = str(route.get("repo_hint", "")).strip()
    if repo_url:
        if fetch_remote:
            return inspect_github_remote(repo_url)
        return {"available": True, "kind": "remote-github", "repo_url": repo_url, "note": "Remote repo URL available; no clone/write performed."}
    if local_path.lower() in {"explicit repo url found", "not specified", "n/a", "none", "null"}:
        local_path = ""
    if local_path:
        path = Path(local_path)
        if not path.is_absolute():
            path = (ROOT / path).resolve()
        if not path.exists():
            return {"available": False, "kind": "local", "reason": f"Local path does not exist: {path}"}
        if not path.is_dir():
            return {"available": False, "kind": "local", "reason": f"Local path is not a directory: {path}"}
        files = sorted(p.name for p in path.iterdir() if p.name not in {".git", "node_modules", ".venv"})[:40]
        return {"available": True, "kind": "local", "path": str(path), "top_level_files": files}
    return {"available": False, "kind": "none", "reason": "No repo context available."}


def draft_worker_prompt(debrief: Debrief, route: dict[str, Any], repo_context: dict[str, Any]) -> str:
    config = load_runtime_config()
    worker_model = config["models"].get("worker_model", DEFAULT_WORKER_MODEL)
    return f"""You are Friday's middle worker using {worker_model}.

Clean up this debrief into structured facts only. Do not write the final message to Amit.
Return concise JSON with:
- project_name
- repo_evidence
- session_summary
- open_items
- next_steps
- risks_or_gaps
- should_escalate_to_executive

Project: {route.get("project_name", "")}
Route: {json.dumps(route, indent=2)}
Repo context: {json.dumps(repo_context, indent=2)}

Debrief:
{debrief.content}
"""


def draft_executive_review_prompt(
    debrief: Debrief,
    route: dict[str, Any],
    repo_context: dict[str, Any],
    worker_output: str = "",
) -> str:
    config = load_runtime_config()
    executive_model = config["models"].get("executive_model", DEFAULT_EXECUTIVE_MODEL)
    return f"""You are Friday reviewing a work session for Amit.

You are the executive layer running on {executive_model}. You are also the face of the agent.
Use the session debrief and repo context to decide if there is extra value worth sending.
Do not rewrite the session summary/open items/next steps unless they are missing or clearly wrong.
Before suggesting anything, verify from repo context whether it already exists or is already in progress.
For useful reviews, write the full suggestion only in notion_comment.
The Telegram message must be only a short notification: project name, session title/date if available, and that a suggestion was left in Notion.
Do not include the actual suggestion or detailed reasoning in Telegram.
Separately decide carryover for future start-session resume targeting.
No useful extra suggestion does not mean not actionable; if the debrief itself has open items, next steps, unfinished work, or a clear feature thread to resume, carryover must be Actionable.
Carryover Topic must be specific enough to distinguish related future work. Use "{{project/module}}: {{specific capability or problem}}".
Bad topics: "cron job", "brainstorm", "Telegram", "Notion", "Friday".
Good topics: "Friday project-intelligence cron: useful-review Telegram context", "Friday Voicepal brainstorm intake: Telegram transcript filing".

Return a single JSON object:
{{
  "result": "useful_review" | "no_useful_suggestions",
  "notion_status": "Reviewed" | "No Useful Suggestions" | "Review Failed",
  "notion_comment": "full comment to write in Notion",
  "telegram_message": "short pointer only, or empty string",
  "reason": "short reason",
  "carryover": "Actionable" | "Not Actionable",
  "carryover_topic": "specific feature-thread label",
  "carryover_reason": "short reason for carryover decision"
}}

Project: {route.get("project_name", "")}
Repo URL: {route.get("repo_url", "")}
Repo hint/path: {route.get("repo_hint", "")}

Session summary: {debrief.session_summary}
Open items: {debrief.open_items}
Next steps: {debrief.next_steps}

Full debrief:
{debrief.content}

Repo context:
{json.dumps(repo_context, indent=2)}

Worker output, if any:
{worker_output}
"""


def draft_missing_mapping_comment(debrief: Debrief, route: dict[str, Any]) -> str:
    project = route.get("project_name") or debrief.project_name or debrief.title
    return (
        "Friday could not safely match this session debrief to a GitHub/local repo.\n\n"
        f"Project: {project}\n"
        f"Session: {debrief.session_summary or debrief.title}\n\n"
        "How to fix: add the GitHub repo link or local repo path to the Notion debrief, "
        f"or tell Friday: \"{project} = <repo url or local path>\"."
    )


def draft_telegram_missing_mapping(debrief: Debrief, route: dict[str, Any]) -> str:
    return "Project mapping needed\n\n" + draft_missing_mapping_comment(debrief, route)


def draft_telegram_review_notice(debrief: Debrief, route: dict[str, Any]) -> str:
    project = route.get("project_name") or debrief.project_name or "Unknown project"
    title = debrief.title or debrief.session_summary or debrief.id
    content = debrief.content.strip()
    context = debrief.session_summary or (content.splitlines()[0] if content else title)
    if len(context) > 240:
        context = context[:237].rstrip() + "..."
    return (
        f"Friday commented on debrief: {title}\n\n"
        f"Project: {project}\n"
        f"Context: {context}\n\n"
        "Full suggestion is in the Notion comment."
    )


def draft_telegram_review(project_name: str, session_summary: str, full_review: str) -> str:
    return (
        f"Project: {project_name}\n"
        f"Session: {session_summary}\n"
        "Why I'm messaging: I found a useful suggestion after checking the debrief and repo context.\n\n"
        f"{full_review}"
    )


def draft_openclaw_telegram_command(message: str, reply_to: str | None) -> list[str] | None:
    if not reply_to:
        return None
    return [
        *openclaw_command_base(),
        "message",
        "send",
        "--channel",
        "telegram",
        "--target",
        reply_to,
        "--message",
        message,
    ]


def openclaw_command_base() -> list[str]:
    for executable in ("openclaw.cmd", "openclaw"):
        found = shutil.which(executable)
        if found:
            return [found]
    appdata = os.environ.get("APPDATA")
    if appdata:
        npm_dir = Path(appdata) / "npm"
        cmd_path = npm_dir / "openclaw.cmd"
        if cmd_path.exists():
            return [str(cmd_path)]
        ps1_path = npm_dir / "openclaw.ps1"
        if ps1_path.exists():
            return ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps1_path)]
    raise RuntimeError("OpenClaw CLI was not found in PATH or APPDATA\\npm.")


def codex_model_name(model: str) -> str:
    if model.startswith("openai-codex/"):
        return model.split("/", 1)[1]
    return model


def call_openclaw_executive(prompt: str) -> dict[str, Any]:
    """Call GPT-5.4 through Codex exec for a strict JSON executive review.

    OpenClaw agent/infer routes are conversational in this runtime, so the
    executive review uses Codex directly and parses the first JSON object from
    stdout. Codex may emit plugin warnings after the answer; those are ignored.
    """
    codex = shutil.which("codex")
    if not codex:
        raise RuntimeError("Codex CLI was not found in PATH; cannot run GPT-5.4 executive review.")

    completed = subprocess.run(
        [
            codex,
            "exec",
            "--ephemeral",
            "--sandbox",
            "read-only",
            "--model",
            codex_model_name(DEFAULT_EXECUTIVE_MODEL),
            "-",
        ],
        input=prompt,
        cwd=str(ROOT),
        check=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=660,
    )
    return normalize_executive_result(json.loads(extract_first_json_object(completed.stdout)))


def normalize_executive_result(result: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(result)
    raw_result = str(normalized.get("result") or normalized.get("outcome") or "").strip().lower()
    comment = str(
        normalized.get("notion_comment")
        or normalized.get("comment")
        or normalized.get("review")
        or normalized.get("full_review")
        or normalized.get("message")
        or ""
    ).strip()
    telegram = str(
        normalized.get("telegram_message")
        or normalized.get("telegram")
        or normalized.get("summary")
        or ""
    ).strip()
    status = str(normalized.get("notion_status") or normalized.get("status") or "").strip()

    if raw_result in {"no_useful_suggestions", "no useful suggestions", "none", "no"}:
        normalized["result"] = "no_useful_suggestions"
        normalized["notion_status"] = status or "No Useful Suggestions"
        normalized["notion_comment"] = comment or str(normalized.get("reason") or "Friday found no useful extra suggestions.")
        normalized["telegram_message"] = ""
        return normalized

    normalized["result"] = "useful_review"
    normalized["notion_status"] = status or "Reviewed"
    normalized["notion_comment"] = comment
    normalized["telegram_message"] = telegram or comment
    return normalized


def send_openclaw_telegram(message: str, reply_to: str) -> dict[str, Any]:
    command = draft_openclaw_telegram_command(message, reply_to)
    if not command:
        raise RuntimeError("Telegram reply target is missing.")
    completed = subprocess.run(
        [*command, "--json"],
        cwd=str(ROOT),
        check=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=660,
    )
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {"raw": completed.stdout.strip()}


def selected_route(
    debrief: Debrief,
    project_map: dict[str, Any],
    *,
    use_local_router: bool,
    ollama_model: str | None = None,
) -> dict[str, Any]:
    status = normalize_status(debrief.review_status)
    if status in HANDLED_STATUSES:
        return deterministic_route(debrief, project_map)
    if not use_local_router:
        return deterministic_route(debrief, project_map)
    return configured_local_router_route(
        debrief,
        project_map,
        model_tag=normalize_ollama_model_tag(ollama_model or DEFAULT_ROUTER_MODEL),
    )


def process_debriefs(
    debriefs: list[Debrief],
    *,
    use_local_router: bool,
    dry_run: bool,
    ollama_model: str | None = None,
) -> dict[str, Any]:
    project_map = load_project_map()
    config = load_runtime_config()
    models = config["models"]
    telegram_reply_to = str(config["telegram"].get("reply_to", "")).strip()
    results: list[dict[str, Any]] = []

    for debrief in debriefs:
        status = normalize_status(debrief.review_status)
        route = selected_route(
            debrief,
            project_map,
            use_local_router=use_local_router,
            ollama_model=ollama_model or models.get("router_model"),
        )

        item: dict[str, Any] = {
            "id": debrief.id,
            "title": debrief.title,
            "route": route,
            "planned_actions": [],
        }

        if status in HANDLED_STATUSES:
            item["planned_actions"].append({"type": "skip", "reason": route.get("reason")})
            results.append(item)
            continue

        if not route.get("should_launch_review"):
            comment = draft_missing_mapping_comment(debrief, route)
            telegram = draft_telegram_missing_mapping(debrief, route)
            item["planned_actions"].extend(
                [
                    {"type": "notion_status", "status": "Needs Repo Mapping", "dry_run": dry_run},
                    {"type": "notion_comment", "body": comment, "dry_run": dry_run},
                    {
                        "type": "telegram_message",
                        "body": telegram,
                        "openclaw_command_shape": draft_openclaw_telegram_command(
                            telegram, telegram_reply_to or "<telegram-chat-id>"
                        ),
                        "dry_run": dry_run,
                    },
                ]
            )
            results.append(item)
            continue

        repo_context = inspect_repo_context(route)
        worker_prompt = draft_worker_prompt(debrief, route, repo_context)
        prompt = draft_executive_review_prompt(debrief, route, repo_context)
        item["repo_context"] = repo_context
        if debrief.source == "notion":
            schema_status = carryover_schema_status()
            item["carryover_schema"] = schema_status
            if not schema_status["ready"]:
                item["planned_actions"].append(
                    {
                        "type": "carryover_schema_error",
                        "errors": schema_status["errors"],
                        "fix": "Run --ensure-carryover-schema before live Friday cron processing.",
                    }
                )
        item["planned_actions"].append(
            {
                "type": "worker_prompt",
                "model": models.get("worker_model", DEFAULT_WORKER_MODEL),
                "body": worker_prompt,
                "dry_run": True,
                "optional": True,
            }
        )
        item["planned_actions"].append(
            {
                "type": "executive_review_prompt",
                "model": models.get("executive_model", DEFAULT_EXECUTIVE_MODEL),
                "body": prompt,
                "dry_run": True,
            }
        )
        item["planned_actions"].append(
            {
                "type": "pending_live_review",
                "reason": "GPT-5.4 executive call and Notion/Telegram writes require explicit --apply-page.",
            }
        )
        results.append(item)

    return {
        "dry_run": dry_run,
        "use_local_router": use_local_router,
        "models": models,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "results": results,
    }


def load_notion_page_debrief(page_id: str) -> Debrief:
    config = load_runtime_config()
    status_property = str(config["notion"].get("status_property") or DEFAULT_NOTION_STATUS_PROPERTY)
    page = notion_api_request("GET", f"/pages/{page_id}")
    return notion_page_to_debrief(page, status_property=status_property)


def build_page_preview(
    debrief: Debrief,
    *,
    use_local_router: bool,
    telegram_reply_to: str = "",
    ollama_model: str | None = None,
) -> dict[str, Any]:
    config = load_runtime_config()
    project_map = load_project_map()
    status = normalize_status(debrief.review_status)
    route = selected_route(
        debrief,
        project_map,
        use_local_router=use_local_router,
        ollama_model=ollama_model or config["models"].get("router_model"),
    )
    repo_context = inspect_repo_context(route, fetch_remote=True) if route.get("should_launch_review") else {}
    telegram_target = telegram_reply_to or str(config["telegram"].get("reply_to", "")).strip()

    preview: dict[str, Any] = {
        "dry_run": True,
        "page_id": debrief.id,
        "title": debrief.title,
        "current_status": debrief.review_status or "New",
        "route": route,
        "repo_context": repo_context,
        "models": config["models"],
        "model_tier_used": "router",
        "gpt54_would_be_called": False,
        "telegram_target": telegram_target or "<missing>",
        "planned_actions": [],
    }

    if normalize_status(debrief.review_status) in HANDLED_STATUSES:
        preview["planned_actions"].append({"type": "skip", "reason": route.get("reason")})
        return preview

    if not route.get("should_launch_review"):
        comment = draft_missing_mapping_comment(debrief, route)
        telegram = draft_telegram_missing_mapping(debrief, route)
        preview["next_status"] = "Needs Repo Mapping"
        preview["notion_comment"] = comment
        preview["telegram_message"] = telegram
        preview["planned_actions"].extend(
            [
                {"type": "notion_status", "status": "Needs Repo Mapping"},
                {"type": "notion_comment", "body": comment},
                {"type": "telegram_message", "body": telegram, "target": telegram_target or "<missing>"},
            ]
        )
        return preview

    worker_prompt = draft_worker_prompt(debrief, route, repo_context)
    executive_prompt = draft_executive_review_prompt(debrief, route, repo_context)
    preview["model_tier_used"] = "executive"
    preview["gpt54_would_be_called"] = True
    if debrief.source == "notion":
        schema_status = carryover_schema_status()
        preview["carryover_schema"] = schema_status
        if not schema_status["ready"]:
            preview["planned_actions"].append(
                {
                    "type": "carryover_schema_error",
                    "errors": schema_status["errors"],
                    "fix": "Run --ensure-carryover-schema before live Friday cron processing.",
                }
            )
    preview["worker_prompt"] = worker_prompt
    preview["executive_prompt"] = executive_prompt
    preview["planned_actions"].extend(
        [
            {"type": "optional_worker_prompt", "model": config["models"].get("worker_model", DEFAULT_WORKER_MODEL)},
            {"type": "executive_review", "model": config["models"].get("executive_model", DEFAULT_EXECUTIVE_MODEL)},
            {"type": "notion_status", "status": "<from executive result>"},
            {"type": "notion_comment", "body": "<from executive result>"},
            {"type": "telegram_message", "body": "<from executive result if useful>", "target": telegram_target or "<missing>"},
        ]
    )
    return preview


def apply_page(
    page_id: str,
    *,
    use_local_router: bool,
    telegram_reply_to: str = "",
    ollama_model: str | None = None,
) -> dict[str, Any]:
    debrief = load_notion_page_debrief(page_id)
    preview = build_page_preview(
        debrief,
        use_local_router=use_local_router,
        telegram_reply_to=telegram_reply_to,
        ollama_model=ollama_model,
    )
    if preview["planned_actions"] and preview["planned_actions"][0]["type"] == "skip":
        return {"applied": False, "preview": preview, "reason": "Page is already handled."}

    next_status = preview.get("next_status")
    comment = preview.get("notion_comment")
    telegram = preview.get("telegram_message", "")

    if preview.get("gpt54_would_be_called"):
        executive_result = call_openclaw_executive(str(preview["executive_prompt"]))
        next_status = str(executive_result.get("notion_status") or "").strip()
        comment = str(executive_result.get("notion_comment") or "").strip()
        telegram = str(executive_result.get("telegram_message") or "").strip()
        if executive_result.get("result") == "no_useful_suggestions":
            next_status = next_status or "No Useful Suggestions"
            telegram = ""
        elif not next_status:
            next_status = "Reviewed"
        carryover = carryover_metadata(debrief, preview.get("route", {}), executive_result)
        config = load_runtime_config()
        require_carryover_schema(str(config["notion"].get("data_source_id") or DEFAULT_NOTION_DATA_SOURCE_ID))
        preview["carryover"] = carryover
        preview["executive_result"] = executive_result

    if not next_status:
        raise RuntimeError("Apply blocked: no next Notion status was produced.")
    if not comment:
        raise RuntimeError("Apply blocked: no Notion comment was produced.")

    telegram_target = str(preview.get("telegram_target") or "").strip()
    if telegram and telegram_target == "<missing>":
        raise RuntimeError("Apply blocked: Telegram message exists but no reply target is configured.")
    if telegram and preview.get("gpt54_would_be_called"):
        telegram = draft_telegram_review_notice(debrief, preview.get("route", {}))

    status_result = notion_update_status(page_id, next_status)
    comment_result = notion_add_comment(page_id, comment)
    carryover_result = None
    if preview.get("carryover"):
        carryover_result = notion_update_carryover(
            page_id,
            str(preview["carryover"]["carryover"]),
            str(preview["carryover"]["carryover_topic"]),
        )
    telegram_result = send_openclaw_telegram(telegram, telegram_target) if telegram else None
    return {
        "applied": True,
        "page_id": page_id,
        "status": next_status,
        "carryover": preview.get("carryover", {}).get("carryover", ""),
        "carryover_topic": preview.get("carryover", {}).get("carryover_topic", ""),
        "notion_status_result_id": status_result.get("id"),
        "notion_comment_result_id": comment_result.get("id"),
        "notion_carryover_result_id": carryover_result.get("id") if carryover_result else None,
        "telegram_sent": bool(telegram_result),
        "telegram_result": telegram_result,
        "preview": preview,
    }


def mark_review_failed(page_id: str, message: str) -> dict[str, Any]:
    status_result = notion_update_status(page_id, "Review Failed")
    comment_result = notion_add_comment(page_id, f"Friday review failed.\n\n{message[:1800]}")
    return {
        "status": "Review Failed",
        "notion_status_result_id": status_result.get("id"),
        "notion_comment_result_id": comment_result.get("id"),
    }


def auto_run(*, use_local_router: bool, limit: int = 10, ollama_model: str | None = None) -> dict[str, Any]:
    state = load_processed_state()
    processed_ids = state_id_set(state.get("processedDebriefs", []))
    unresolved_ids = state_id_set(state.get("unresolvedMappings", []))
    project_map = load_project_map()
    config = load_runtime_config()
    debriefs = load_notion_debriefs(limit=limit)
    results: list[dict[str, Any]] = []

    for debrief in debriefs:
        status = normalize_status(debrief.review_status)
        item: dict[str, Any] = {
            "id": debrief.id,
            "title": debrief.title,
            "status": debrief.review_status or "New",
            "actions": [],
        }

        if debrief.id in processed_ids:
            item["actions"].append({"type": "skip", "reason": "Already recorded in processed state."})
            results.append(item)
            continue

        if status in HANDLED_STATUSES:
            item["actions"].append({"type": "skip", "reason": f"Status is already handled: {debrief.review_status}."})
            results.append(item)
            continue

        if status not in ACTIONABLE_STATUSES:
            item["actions"].append({"type": "skip", "reason": f"Status is not blank/New: {debrief.review_status}."})
            results.append(item)
            continue

        route = selected_route(
            debrief,
            project_map,
            use_local_router=use_local_router,
            ollama_model=ollama_model or config["models"].get("router_model"),
        )
        item["route"] = route

        if not route.get("should_launch_review"):
            if debrief.id in unresolved_ids:
                item["actions"].append({"type": "skip", "reason": "Missing mapping was already reported."})
                results.append(item)
                continue
            try:
                preview = build_page_preview(debrief, use_local_router=use_local_router, ollama_model=ollama_model)
                next_status = str(preview.get("next_status") or "Needs Repo Mapping")
                comment = str(preview.get("notion_comment") or draft_missing_mapping_comment(debrief, route))
                telegram = str(preview.get("telegram_message") or draft_telegram_missing_mapping(debrief, route))
                telegram_target = str(preview.get("telegram_target") or "").strip()
                if telegram_target == "<missing>":
                    raise RuntimeError("Telegram target is missing.")
                notion_update_status(debrief.id, next_status)
                notion_add_comment(debrief.id, comment)
                send_openclaw_telegram(telegram, telegram_target)
                mark_unresolved_mapping(state, debrief, route)
                mark_processed(state, debrief, outcome="needs_repo_mapping", status=next_status, telegram_sent=True)
                item["actions"].extend(
                    [
                        {"type": "notion_status", "status": next_status},
                        {"type": "notion_comment"},
                        {"type": "telegram_message", "sent": True},
                    ]
                )
            except Exception as exc:  # noqa: BLE001 - auto-run reports and continues.
                item["error"] = str(exc)
                try:
                    failure = mark_review_failed(debrief.id, str(exc))
                    item["actions"].append({"type": "notion_status", "status": failure["status"]})
                except Exception as failure_exc:  # noqa: BLE001
                    item["failure_mark_error"] = str(failure_exc)
                mark_processed(state, debrief, outcome="failed", status="Review Failed", error=str(exc))
            results.append(item)
            continue

        try:
            applied = apply_page(debrief.id, use_local_router=use_local_router, ollama_model=ollama_model)
            status_after = str(applied.get("status") or "")
            telegram_sent = bool(applied.get("telegram_sent"))
            outcome = "reviewed" if status_after == "Reviewed" else normalize_status(status_after).replace(" ", "_")
            mark_processed(state, debrief, outcome=outcome or "applied", status=status_after, telegram_sent=telegram_sent)
            item["actions"].append(
                {
                    "type": "apply_page",
                    "applied": applied.get("applied"),
                    "status": status_after,
                    "carryover": applied.get("carryover"),
                    "carryover_topic": applied.get("carryover_topic"),
                    "telegram_sent": telegram_sent,
                }
            )
        except Exception as exc:  # noqa: BLE001 - auto-run reports and continues.
            item["error"] = str(exc)
            try:
                failure = mark_review_failed(debrief.id, str(exc))
                item["actions"].append({"type": "notion_status", "status": failure["status"]})
            except Exception as failure_exc:  # noqa: BLE001
                item["failure_mark_error"] = str(failure_exc)
            mark_processed(state, debrief, outcome="failed", status="Review Failed", error=str(exc))
        results.append(item)

    state["lastCheckedAt"] = datetime.now(timezone.utc).isoformat()
    save_json(PROCESSED_PATH, state)
    return {
        "auto_run": True,
        "use_local_router": use_local_router,
        "limit": limit,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "results": results,
    }


def run_fixture_tests(use_local_router: bool = False, ollama_model: str | None = None) -> int:
    debriefs = load_fixture_debriefs()
    result = process_debriefs(
        debriefs,
        use_local_router=use_local_router,
        dry_run=True,
        ollama_model=ollama_model,
    )
    by_id = {item["id"]: item for item in result["results"]}
    fixture_debriefs = {debrief.id: debrief for debrief in debriefs}
    review_notice = draft_telegram_review_notice(
        fixture_debriefs["fixture-clear-repo"],
        by_id["fixture-clear-repo"]["route"],
    )
    useful_carryover = carryover_metadata(
        fixture_debriefs["fixture-clear-repo"],
        by_id["fixture-clear-repo"]["route"],
        {
            "result": "useful_review",
            "carryover_topic": "cron job",
            "carryover_reason": "Model gave a generic topic.",
        },
    )
    no_suggestion_open_carryover = carryover_metadata(
        fixture_debriefs["fixture-clear-repo"],
        by_id["fixture-clear-repo"]["route"],
        {"result": "no_useful_suggestions", "carryover": "Not Actionable", "carryover_topic": "brainstorm"},
    )
    no_suggestion_closed_carryover = carryover_metadata(
        fixture_debriefs["fixture-reviewed"],
        by_id["fixture-reviewed"]["route"],
        {
            "result": "no_useful_suggestions",
            "carryover": "Not Actionable",
            "carryover_topic": "Sleep.io cleanup: already reviewed session",
        },
    )

    assertions = [
        ("clear repo should route to review", by_id["fixture-clear-repo"]["route"]["should_launch_review"] is True),
        ("reviewed status should skip", by_id["fixture-reviewed"]["planned_actions"][0]["type"] == "skip"),
        ("completed status should skip", by_id["fixture-completed"]["planned_actions"][0]["type"] == "skip"),
        (
            "missing mapping should not launch review",
            by_id["fixture-missing-mapping"]["route"]["should_launch_review"] is False,
        ),
        (
            "missing mapping should not keep invented repo",
            not by_id["fixture-missing-mapping"]["route"].get("repo_url"),
        ),
        (
            "missing mapping drafts telegram",
            any(action["type"] == "telegram_message" for action in by_id["fixture-missing-mapping"]["planned_actions"]),
        ),
        (
            "clear repo drafts executive review prompt",
            any(action["type"] == "executive_review_prompt" for action in by_id["fixture-clear-repo"]["planned_actions"]),
        ),
        (
            "clear repo includes optional worker tier",
            any(action["type"] == "worker_prompt" and action.get("optional") for action in by_id["fixture-clear-repo"]["planned_actions"]),
        ),
        ("review notice names exact debrief", "Friday commented on debrief: Sleep.io session" in review_notice),
        ("review notice includes project", "Project: Sleep.io" in review_notice),
        ("review notice includes context", "Context: Fixed auth redirects and left payment settings unresolved." in review_notice),
        ("review notice points to Notion", "Full suggestion is in the Notion comment." in review_notice),
        ("review notice does not include full review body", "Why I'm messaging:" not in review_notice),
        ("useful review sets actionable carryover", useful_carryover["carryover"] == CARRYOVER_ACTIONABLE),
        (
            "no useful suggestion with open work stays actionable",
            no_suggestion_open_carryover["carryover"] == CARRYOVER_ACTIONABLE,
        ),
        (
            "no useful suggestion with no open work is not actionable",
            no_suggestion_closed_carryover["carryover"] == CARRYOVER_NOT_ACTIONABLE,
        ),
        (
            "generic carryover topic is rewritten",
            useful_carryover["carryover_topic"] != "cron job" and topic_is_specific(useful_carryover["carryover_topic"]),
        ),
    ]

    failed = [name for name, ok in assertions if not ok]
    if failed:
        print("Fixture tests failed:")
        for name in failed:
            print(f"- {name}")
        print(json.dumps(result, indent=2))
        return 1

    print("Fixture tests passed.")
    print(json.dumps(result, indent=2))
    return 0


def run_brainstorm_fixture_tests() -> int:
    brainstorms = load_fixture_brainstorms()
    previews = [preview_brainstorm(brainstorm) for brainstorm in brainstorms]
    by_id = {preview["digest"]["title"]: preview for preview in previews}
    sample = by_id["Enhancing Personal and Work Agents with OpenClaw"]
    digest = sample["digest"]
    routed = digest["routed_items"]

    assertions = [
        ("sample should classify as mixed", digest["owner"] == "Mixed"),
        ("sample should not store raw transcript", digest["raw_transcript_stored"] is False),
        ("name should use title plus date", digest["name"] == "Enhancing Personal and Work Agents with OpenClaw - 2026-04-24"),
        (
            "Jarvis feature-building routes to Friday/Jarvis",
            any(
                item["owner"] == "Friday"
                and item["project"] == "Jarvis"
                and "learn from my journal" in item["text"]
                for item in routed
            ),
        ),
        (
            "pure personal context routes to Jarvis",
            any(
                item["owner"] == "Jarvis"
                and item["type"] == "Personal Context"
                and item["domain"] == "Personal"
                for item in routed
            ),
        ),
        (
            "finance module routes as future Friday module",
            any(item["owner"] == "Friday" and item["domain"] == "Finance Module" and item["type"] == "Future Module" for item in routed),
        ),
        ("telegram summary is concise", len(sample["telegram_message"]) < 350),
    ]

    failed = [name for name, ok in assertions if not ok]
    if failed:
        print("Brainstorm fixture tests failed:")
        for name in failed:
            print(f"- {name}")
        print(json.dumps(previews, indent=2))
        return 1

    print("Brainstorm fixture tests passed.")
    print(json.dumps(previews, indent=2))
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Friday project intelligence dry-run watcher")
    parser.add_argument("--fixtures", action="store_true", help="Process local fake debrief fixtures")
    parser.add_argument("--test", action="store_true", help="Run fixture assertions")
    parser.add_argument(
        "--use-local-router",
        "--use-granite",
        dest="use_local_router",
        action="store_true",
        help="Use the configured local Ollama router instead of deterministic routing. --use-granite remains as a deprecated alias.",
    )
    parser.add_argument("--ollama-model", help="Override the local Ollama router tag (for example falcon3:3b)")
    parser.add_argument("--discover-notion", action="store_true", help="Read-only discovery for the session debriefs Notion source")
    parser.add_argument("--discover-brainstorm-notion", action="store_true", help="Read-only discovery for the Brainstorm Digests Notion source")
    parser.add_argument("--ensure-carryover-schema", action="store_true", help="Create/update Session Debriefs carryover properties")
    parser.add_argument("--create-brainstorm-database", help="Create Brainstorm Digests under this Notion parent page id")
    parser.add_argument("--notion-dry-run", action="store_true", help="Preview planned actions for recent Notion debriefs")
    parser.add_argument("--notion-limit", type=int, default=5, help="Recent Notion debrief rows to fetch during discovery")
    parser.add_argument("--auto-run", action="store_true", help="Run automatic Friday v1 processing for recent Notion debriefs")
    parser.add_argument("--auto-limit", type=int, default=10, help="Recent Notion debrief rows to inspect during automatic processing")
    parser.add_argument("--brainstorm-fixtures", action="store_true", help="Preview local Voicepal brainstorm fixtures")
    parser.add_argument("--brainstorm-test", action="store_true", help="Run brainstorm fixture assertions")
    parser.add_argument("--brainstorm-file", help="Preview one Voicepal brainstorm transcript file without writes")
    parser.add_argument("--apply-brainstorm-file", help="Create one Brainstorm Digests Notion page from a transcript file")
    parser.add_argument("--brainstorm-stdin", action="store_true", help="Preview one Voicepal brainstorm transcript from stdin without writes")
    parser.add_argument("--apply-brainstorm-stdin", action="store_true", help="Create one Brainstorm Digests Notion page from stdin")
    parser.add_argument("--brainstorm-title", help="Override detected Voicepal title")
    parser.add_argument("--brainstorm-date", help="Override brainstorm date, YYYY-MM-DD")
    parser.add_argument("--brainstorm-source-ref", help="Telegram message id/date or Voicepal title reference")
    parser.add_argument("--brainstorm-data-source-id", help="Brainstorm Digests data source ID override")
    parser.add_argument("--send-brainstorm-telegram", action="store_true", help="Send the concise brainstorm filing reply over Telegram during apply")
    parser.add_argument("--preview-page", help="Preview planned actions for one exact Notion page id without writes")
    parser.add_argument("--apply-page", help="Apply live Notion/Telegram actions only for this exact Notion page id")
    parser.add_argument("--telegram-reply-to", help="Telegram delivery target override for apply/preview")
    parser.add_argument("--live", action="store_true", help="Reserved for future live integrations; currently blocked")
    args = parser.parse_args(argv)

    if args.live:
        print("Use --apply-page <page_id> for the explicit one-page live write path.")
        return 2

    if args.test:
        return run_fixture_tests(use_local_router=args.use_local_router, ollama_model=args.ollama_model)

    if args.brainstorm_test:
        return run_brainstorm_fixture_tests()

    if args.discover_notion:
        result = discover_notion_session_debriefs(limit=args.notion_limit)
        print(json.dumps(result, indent=2))
        return 0

    if args.discover_brainstorm_notion:
        result = discover_notion_brainstorm_digests(limit=args.notion_limit)
        print(json.dumps(result, indent=2))
        return 0

    if args.ensure_carryover_schema:
        result = ensure_carryover_schema()
        print(json.dumps(result, indent=2))
        return 0

    if args.create_brainstorm_database:
        result = create_brainstorm_database(args.create_brainstorm_database)
        print(json.dumps(result, indent=2))
        return 0

    if args.brainstorm_fixtures:
        result = [preview_brainstorm(brainstorm) for brainstorm in load_fixture_brainstorms()]
        print(json.dumps(result, indent=2))
        return 0

    if args.brainstorm_file:
        brainstorm = load_brainstorm_file(
            Path(args.brainstorm_file),
            title=args.brainstorm_title or "",
            date=args.brainstorm_date or "",
            source_ref=args.brainstorm_source_ref or "",
        )
        print(json.dumps(preview_brainstorm(brainstorm), indent=2))
        return 0

    if args.brainstorm_stdin:
        brainstorm = load_brainstorm_text(
            sys.stdin.read(),
            title=args.brainstorm_title or "",
            date=args.brainstorm_date or "",
            source_ref=args.brainstorm_source_ref or "telegram stdin",
        )
        print(json.dumps(preview_brainstorm(brainstorm), indent=2))
        return 0

    if args.apply_brainstorm_file:
        brainstorm = load_brainstorm_file(
            Path(args.apply_brainstorm_file),
            title=args.brainstorm_title or "",
            date=args.brainstorm_date or "",
            source_ref=args.brainstorm_source_ref or "",
        )
        result = apply_brainstorm(
            brainstorm,
            data_source_id=args.brainstorm_data_source_id or "",
            telegram_reply_to=args.telegram_reply_to or "",
            send_telegram=args.send_brainstorm_telegram,
        )
        print(json.dumps(result, indent=2))
        return 0

    if args.apply_brainstorm_stdin:
        brainstorm = load_brainstorm_text(
            sys.stdin.read(),
            title=args.brainstorm_title or "",
            date=args.brainstorm_date or "",
            source_ref=args.brainstorm_source_ref or "telegram stdin",
        )
        result = apply_brainstorm(
            brainstorm,
            data_source_id=args.brainstorm_data_source_id or "",
            telegram_reply_to=args.telegram_reply_to or "",
            send_telegram=args.send_brainstorm_telegram,
        )
        print(json.dumps(result, indent=2))
        return 0

    if args.notion_dry_run:
        debriefs = load_notion_debriefs(limit=args.notion_limit)
        result = process_debriefs(
            debriefs,
            use_local_router=args.use_local_router,
            dry_run=True,
            ollama_model=args.ollama_model,
        )
        print(json.dumps(result, indent=2))
        return 0

    if args.auto_run:
        result = auto_run(use_local_router=args.use_local_router, limit=args.auto_limit, ollama_model=args.ollama_model)
        print(json.dumps(result, indent=2))
        return 0

    if args.preview_page:
        debrief = load_notion_page_debrief(args.preview_page)
        result = build_page_preview(
            debrief,
            use_local_router=args.use_local_router,
            telegram_reply_to=args.telegram_reply_to or "",
            ollama_model=args.ollama_model,
        )
        print(json.dumps(result, indent=2))
        return 0

    if args.apply_page:
        result = apply_page(
            args.apply_page,
            use_local_router=args.use_local_router,
            telegram_reply_to=args.telegram_reply_to or "",
            ollama_model=args.ollama_model,
        )
        print(json.dumps(result, indent=2))
        return 0

    if args.fixtures:
        result = process_debriefs(
            load_fixture_debriefs(),
            use_local_router=args.use_local_router,
            dry_run=True,
            ollama_model=args.ollama_model,
        )
        print(json.dumps(result, indent=2))
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
