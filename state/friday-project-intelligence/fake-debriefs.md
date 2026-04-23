# Fake Debriefs For Watcher Testing

These are fake local fixtures for testing Friday's watcher/router. They are not real Notion content.

## Clear Repo Link

Session debrief for Project: Sleep.io.

Repo: https://github.com/AGrupper/sleep.io

Today I fixed auth redirects and left payment settings unresolved.

Expected routing:

- `project_name`: `Sleep.io`
- `repo_url`: `https://github.com/AGrupper/sleep.io`
- `has_enough_context`: `true`
- `should_launch_review`: `true`

## Missing Repo Context

Worked a bit on the school helper app today. Fixed some UI bugs. Not sure which repository this belongs to.

Expected routing:

- `project_name`: `School Helper App`
- `repo_url`: ``
- `has_enough_context`: `false`
- `should_launch_review`: `false`

## Ambiguous Project

Worked on Jarvis today. Updated some prompts and checked memory behavior.

Expected routing:

- `project_name`: `Jarvis`
- `repo_url`: ``
- `has_enough_context`: `false`
- `should_launch_review`: `false`
