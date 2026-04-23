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
PROMPT_PATH = STATE_DIR / "watcher-routing-prompt.md"
NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2026-03-11"
DEFAULT_NOTION_DATA_SOURCE_ID = "33834a33-2bc2-80f5-9dd1-000bf76a48fa"
DEFAULT_NOTION_STATUS_PROPERTY = "Status"
DEFAULT_ROUTER_MODEL = "ollama/granite3.3:2b"
DEFAULT_WORKER_MODEL = "minimax/MiniMax-M2.7"
DEFAULT_EXECUTIVE_MODEL = "openai-codex/gpt-5.4"

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
    source: str = "fixture"


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
    merged["models"] = defaults["models"] | configured.get("models", {})
    merged["telegram"] = defaults["telegram"] | configured.get("telegram", {})
    return merged


def notion_api_request(method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    token = os.environ.get("NOTION_API_KEY")
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
    for name in names:
        pattern = re.compile(rf"^{re.escape(name)}\s*:?\s*(.+)$", re.IGNORECASE | re.MULTILINE)
        match = pattern.search(content)
        if match:
            return match.group(1).strip()
    return ""


def notion_page_to_debrief(page: dict[str, Any], *, status_property: str) -> Debrief:
    properties = page.get("properties", {})
    title_property = find_property_by_type(properties, "title")
    title = property_value_summary(properties.get(title_property, {})) if title_property else page.get("id", "")
    content = notion_page_content(str(page.get("id", "")))
    status = first_property_value(properties, [status_property]) or "New"
    project_name = first_property_value(properties, ["Project"])
    return Debrief(
        id=str(page.get("id", "")).strip(),
        title=title,
        review_status=status,
        project_name=project_name,
        repo_url=repo_from_text(content),
        local_repo_path=first_property_value(properties, ["Local Repo", "Local Repo Path", "Repo Path"]),
        session_summary=infer_section(content, ["Session summary", "Summary"]) or title,
        open_items=infer_section(content, ["Open items", "Open Items", "Open"]),
        next_steps=infer_section(content, ["Next steps", "Next Steps", "Next"]),
        content=content or title,
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


def normalize_status(status: str | None) -> str:
    return (status or "").strip().lower()


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
    )


def load_fixture_debriefs(path: Path = FIXTURE_PATH) -> list[Debrief]:
    data = load_json(path)
    return [parse_debrief(item) for item in data.get("debriefs", [])]


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


def granite_route(debrief: Debrief, project_map: dict[str, Any]) -> dict[str, Any]:
    """Route with Granite. Fall back to deterministic routing if JSON is invalid."""
    prompt_template = PROMPT_PATH.read_text(encoding="utf-8")
    prompt = prompt_template.replace("{{REVIEW_STATUS}}", debrief.review_status or "New")
    prompt = prompt.replace("{{DEBRIEF_TEXT}}", debrief.content)

    try:
        completed = subprocess.run(
            ["ollama", "run", "granite3.3:2b", prompt],
            cwd=str(ROOT),
            check=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120,
        )
        raw = extract_json_object(completed.stdout)
        data = json.loads(raw)
        # Merge deterministic repo mapping so the model cannot invent missing state.
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
    except Exception as exc:  # noqa: BLE001 - fallback is intentional and reported.
        route = deterministic_route(debrief, project_map)
        route["reason"] = f"Granite routing fallback used: {exc}"
        return route


def extract_json_object(text: str) -> str:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("No JSON object found in Granite output")
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

Return a single JSON object:
{{
  "result": "useful_review" | "no_useful_suggestions",
  "notion_status": "Reviewed" | "No Useful Suggestions" | "Review Failed",
  "notion_comment": "full comment to write in Notion",
  "telegram_message": "short pointer only, or empty string",
  "reason": "short reason"
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
    session = debrief.title or debrief.session_summary or debrief.id
    return (
        "Friday left a project suggestion in Notion.\n\n"
        f"Project: {project}\n"
        f"Session: {session}\n\n"
        "I kept the full suggestion in the Notion comment so you can review it when you have time."
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


def selected_route(debrief: Debrief, project_map: dict[str, Any], *, use_granite: bool) -> dict[str, Any]:
    status = normalize_status(debrief.review_status)
    if status in HANDLED_STATUSES:
        return deterministic_route(debrief, project_map)
    return granite_route(debrief, project_map) if use_granite else deterministic_route(debrief, project_map)


def process_debriefs(debriefs: list[Debrief], *, use_granite: bool, dry_run: bool) -> dict[str, Any]:
    project_map = load_project_map()
    config = load_runtime_config()
    models = config["models"]
    telegram_reply_to = str(config["telegram"].get("reply_to", "")).strip()
    results: list[dict[str, Any]] = []

    for debrief in debriefs:
        status = normalize_status(debrief.review_status)
        route = selected_route(debrief, project_map, use_granite=use_granite)

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
        "use_granite": use_granite,
        "models": models,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "results": results,
    }


def load_notion_page_debrief(page_id: str) -> Debrief:
    config = load_runtime_config()
    status_property = str(config["notion"].get("status_property") or DEFAULT_NOTION_STATUS_PROPERTY)
    page = notion_api_request("GET", f"/pages/{page_id}")
    return notion_page_to_debrief(page, status_property=status_property)


def build_page_preview(debrief: Debrief, *, use_granite: bool, telegram_reply_to: str = "") -> dict[str, Any]:
    config = load_runtime_config()
    project_map = load_project_map()
    status = normalize_status(debrief.review_status)
    route = selected_route(debrief, project_map, use_granite=use_granite)
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


def apply_page(page_id: str, *, use_granite: bool, telegram_reply_to: str = "") -> dict[str, Any]:
    debrief = load_notion_page_debrief(page_id)
    preview = build_page_preview(debrief, use_granite=use_granite, telegram_reply_to=telegram_reply_to)
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
    telegram_result = send_openclaw_telegram(telegram, telegram_target) if telegram else None
    return {
        "applied": True,
        "page_id": page_id,
        "status": next_status,
        "notion_status_result_id": status_result.get("id"),
        "notion_comment_result_id": comment_result.get("id"),
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


def auto_run(*, use_granite: bool, limit: int = 10) -> dict[str, Any]:
    state = load_processed_state()
    processed_ids = state_id_set(state.get("processedDebriefs", []))
    unresolved_ids = state_id_set(state.get("unresolvedMappings", []))
    project_map = load_project_map()
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

        route = selected_route(debrief, project_map, use_granite=use_granite)
        item["route"] = route

        if not route.get("should_launch_review"):
            if debrief.id in unresolved_ids:
                item["actions"].append({"type": "skip", "reason": "Missing mapping was already reported."})
                results.append(item)
                continue
            try:
                preview = build_page_preview(debrief, use_granite=use_granite)
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
            applied = apply_page(debrief.id, use_granite=use_granite)
            status_after = str(applied.get("status") or "")
            telegram_sent = bool(applied.get("telegram_sent"))
            outcome = "reviewed" if status_after == "Reviewed" else normalize_status(status_after).replace(" ", "_")
            mark_processed(state, debrief, outcome=outcome or "applied", status=status_after, telegram_sent=telegram_sent)
            item["actions"].append({"type": "apply_page", "applied": applied.get("applied"), "status": status_after, "telegram_sent": telegram_sent})
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
        "use_granite": use_granite,
        "limit": limit,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "results": results,
    }


def run_fixture_tests(use_granite: bool = False) -> int:
    debriefs = load_fixture_debriefs()
    result = process_debriefs(debriefs, use_granite=use_granite, dry_run=True)
    by_id = {item["id"]: item for item in result["results"]}

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


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Friday project intelligence dry-run watcher")
    parser.add_argument("--fixtures", action="store_true", help="Process local fake debrief fixtures")
    parser.add_argument("--test", action="store_true", help="Run fixture assertions")
    parser.add_argument("--use-granite", action="store_true", help="Use Ollama granite3.3:2b for routing")
    parser.add_argument("--discover-notion", action="store_true", help="Read-only discovery for the session debriefs Notion source")
    parser.add_argument("--notion-dry-run", action="store_true", help="Preview planned actions for recent Notion debriefs")
    parser.add_argument("--notion-limit", type=int, default=5, help="Recent Notion debrief rows to fetch during discovery")
    parser.add_argument("--auto-run", action="store_true", help="Run automatic Friday v1 processing for recent Notion debriefs")
    parser.add_argument("--auto-limit", type=int, default=10, help="Recent Notion debrief rows to inspect during automatic processing")
    parser.add_argument("--preview-page", help="Preview planned actions for one exact Notion page id without writes")
    parser.add_argument("--apply-page", help="Apply live Notion/Telegram actions only for this exact Notion page id")
    parser.add_argument("--telegram-reply-to", help="Telegram delivery target override for apply/preview")
    parser.add_argument("--live", action="store_true", help="Reserved for future live integrations; currently blocked")
    args = parser.parse_args(argv)

    if args.live:
        print("Use --apply-page <page_id> for the explicit one-page live write path.")
        return 2

    if args.test:
        return run_fixture_tests(use_granite=args.use_granite)

    if args.discover_notion:
        result = discover_notion_session_debriefs(limit=args.notion_limit)
        print(json.dumps(result, indent=2))
        return 0

    if args.notion_dry_run:
        debriefs = load_notion_debriefs(limit=args.notion_limit)
        result = process_debriefs(debriefs, use_granite=args.use_granite, dry_run=True)
        print(json.dumps(result, indent=2))
        return 0

    if args.auto_run:
        result = auto_run(use_granite=args.use_granite, limit=args.auto_limit)
        print(json.dumps(result, indent=2))
        return 0

    if args.preview_page:
        debrief = load_notion_page_debrief(args.preview_page)
        result = build_page_preview(debrief, use_granite=args.use_granite, telegram_reply_to=args.telegram_reply_to or "")
        print(json.dumps(result, indent=2))
        return 0

    if args.apply_page:
        result = apply_page(args.apply_page, use_granite=args.use_granite, telegram_reply_to=args.telegram_reply_to or "")
        print(json.dumps(result, indent=2))
        return 0

    if args.fixtures:
        result = process_debriefs(load_fixture_debriefs(), use_granite=args.use_granite, dry_run=True)
        print(json.dumps(result, indent=2))
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
