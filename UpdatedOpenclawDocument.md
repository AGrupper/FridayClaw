### Install LiteLLM and Start Proxy

Source: https://docs.openclaw.ai/providers/litellm

Install the LiteLLM proxy and start it with a specified model. Ensure you have the necessary dependencies installed.

```bash
pip install 'litellm[proxy]'
litellm --model claude-opus-4-6
```

--------------------------------

### Update Installed Skills (Workflow Example)

Source: https://docs.openclaw.ai/tools/clawhub

Example of updating all installed skills using the CLI.

```bash
clawhub update --all
```

--------------------------------

### Onboard and Install OpenClaw Service

Source: https://docs.openclaw.ai/

Run the onboarding command to set up and install the OpenClaw service as a daemon. This command guides you through the initial setup and configuration.

```bash
openclaw onboard --install-daemon

```

--------------------------------

### OpenClaw Development Setup from Source

Source: https://docs.openclaw.ai/help/faq

Clones the OpenClaw repository, installs dependencies, builds the project and UI assets, and then runs the onboarding process. This is suitable for contributors and developers.

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm build
pnpm ui:build
openclaw onboard
```

--------------------------------

### Install OpenClaw

Source: https://docs.openclaw.ai/platforms/windows

Clones and builds the OpenClaw project for first-time setup.

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm build
pnpm ui:build
pnpm openclaw onboard --install-daemon
```

--------------------------------

### Install and Setup Honcho Plugin

Source: https://docs.openclaw.ai/concepts/memory-honcho

Install the Honcho plugin, run its setup, and restart the OpenClaw gateway. The setup command prompts for API credentials and can migrate existing workspace memory.

```bash
openclaw plugins install @honcho-ai/openclaw-honcho
openclaw honcho setup
openclaw gateway --force
```

--------------------------------

### Generate QR and Setup Codes

Source: https://docs.openclaw.ai/cli/qr

Basic usage examples for generating pairing information with various configuration overrides.

```bash
openclaw qr
openclaw qr --setup-code-only
openclaw qr --json
openclaw qr --remote
openclaw qr --url wss://gateway.example/ws
```

--------------------------------

### Create Optional Channel Setup Surface

Source: https://docs.openclaw.ai/plugins/sdk-channel-plugins

Prefer `createOptionalChannelSetupSurface` when a channel only needs to advertise "install this plugin first" in setup surfaces. The generated adapter/wizard fail closed on config writes and finalization.

```javascript
createOptionalChannelSetupSurface(...)
```

--------------------------------

### Installation with Flags

Source: https://docs.openclaw.ai/install/installer

Provides examples of installing Openclaw AI with various command-line flags to customize the installation process.

```APIDOC
## Installation with Flags

### Description
These examples demonstrate how to use flags with the install script to modify the installation behavior.

### Method
GET

### Endpoint
https://openclaw.ai/install.sh

### Flags Reference
| Flag                                  | Description                                                |
| ------------------------------------- | ---------------------------------------------------------- |
| `--install-method npm|git`           | Choose install method (default: `npm`). Alias: `--method`  |
| `--npm`                               | Shortcut for npm method                                    |
| `--git`                               | Shortcut for git method. Alias: `--github`                 |
| `--version <version|dist-tag|spec>` | npm version, dist-tag, or package spec (default: `latest`) |
| `--beta`                              | Use beta dist-tag if available, else fallback to `latest`  |
| `--git-dir <path>`                    | Checkout directory (default: `~/openclaw`). Alias: `--dir` |
| `--no-git-update`                     | Skip `git pull` for existing checkout                      |
| `--no-prompt`                         | Disable prompts                                            |
| `--no-onboard`                        | Skip onboarding                                            |
| `--onboard`                           | Enable onboarding                                          |
| `--dry-run`                           | Print actions without applying changes                     |
| `--verbose`                           | Enable debug output (`set -x`, npm notice-level logs)      |
| `--help`                              | Show usage (`-h`)                                          |

### Examples

#### Skip onboarding
```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --no-onboard
```

#### Git install
```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --install-method git
```

#### GitHub main via npm
```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --version main
```

#### Dry run
```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --dry-run
```

### Request Example (Skip onboarding)
```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --no-onboard
```

### Response
(Output of the bash script execution)
```

--------------------------------

### Install and initialize Tailscale on VPS

Source: https://docs.openclaw.ai/help/faq

Standard installation and authentication commands for Tailscale on a Linux VPS.

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

--------------------------------

### Setup Metadata

Source: https://docs.openclaw.ai/plugins/manifest

Defines onboarding and setup surfaces for plugin-owned metadata.

```APIDOC
## Setup Metadata

### Description
Provides metadata for setup and onboarding surfaces before the full runtime is loaded.

### Parameters
#### Request Body
- **providers** (array) - Optional - List of provider configurations including id, authMethods, and envVars.
- **cliBackends** (string[]) - Optional - Setup-specific descriptor surface for control-plane/setup flows.
- **configMigrations** (string[]) - Optional - List of configuration migrations.
- **requiresRuntime** (boolean) - Optional - Flag indicating if setup requires richer runtime hooks.

### Request Example
{
  "setup": {
    "providers": [
      {
        "id": "openai",
        "authMethods": ["api-key"],
        "envVars": ["OPENAI_API_KEY"]
      }
    ],
    "cliBackends": ["openai-cli"],
    "configMigrations": ["legacy-openai-auth"],
    "requiresRuntime": false
  }
}
```

--------------------------------

### Configure Setup Metadata

Source: https://docs.openclaw.ai/plugins/manifest

The 'setup' object provides metadata for setup and onboarding surfaces, including providers, CLI backends, and configuration migrations. Set 'requiresRuntime: true' if runtime hooks are needed.

```json
{
  "setup": {
    "providers": [
      {
        "id": "openai",
        "authMethods": ["api-key"],
        "envVars": ["OPENAI_API_KEY"]
      }
    ],
    "cliBackends": ["openai-cli"],
    "configMigrations": ["legacy-openai-auth"],
    "requiresRuntime": false
  }
}
```

--------------------------------

### Complete Broadcast Group Configuration Example

Source: https://docs.openclaw.ai/channels/broadcast-groups

A comprehensive configuration example demonstrating agent definitions and broadcast group setup for multiple WhatsApp group IDs and direct messages, including parallel processing strategy.

```json
{
  "agents": {
    "list": [
      {
        "id": "code-reviewer",
        "name": "Code Reviewer",
        "workspace": "/path/to/code-reviewer",
        "sandbox": { "mode": "all" }
      },
      {
        "id": "security-auditor",
        "name": "Security Auditor",
        "workspace": "/path/to/security-auditor",
        "sandbox": { "mode": "all" }
      },
      {
        "id": "docs-generator",
        "name": "Documentation Generator",
        "workspace": "/path/to/docs-generator",
        "sandbox": { "mode": "all" }
      }
    ]
  },
  "broadcast": {
    "strategy": "parallel",
    "120363403215116621@g.us": ["code-reviewer", "security-auditor", "docs-generator"],
    "120363424282127706@g.us": ["support-en", "support-de"],
    "+15555550123": ["assistant", "logger"]
  }
}
```

--------------------------------

### Skill Installer Configuration

Source: https://docs.openclaw.ai/tools/skills

Define installation methods for a skill using the `metadata.openclaw.install` field. This example shows how to configure Homebrew as an installer for the Gemini CLI.

```markdown
---
name: gemini
description: Use Gemini CLI for coding assistance and Google search lookups.
metadata:
  {
    "openclaw":
      {
        "emoji": "♊️",
        "requires": { "bins": ["gemini"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "gemini-cli",
              "bins": ["gemini"],
              "label": "Install Gemini CLI (brew)",
            },
          ],
      },
  }
---

```

--------------------------------

### Channel Setup Primitives Example

Source: https://docs.openclaw.ai/plugins/sdk-channel-plugins

Includes primitives like `DEFAULT_ACCOUNT_ID`, `createTopLevelChannelDmPolicy`, `setSetupChannelEnabled`, and `splitSetupEntries` within `openclaw/plugin-sdk/channel-setup`.

```javascript
DEFAULT_ACCOUNT_ID
```

```javascript
createTopLevelChannelDmPolicy
```

```javascript
setSetupChannelEnabled
```

```javascript
splitSetupEntries
```

--------------------------------

### Install OpenClaw via script

Source: https://docs.openclaw.ai/install

Use the recommended installer script to automatically detect the OS, install Node, and launch onboarding.

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

--------------------------------

### Download New Skills (Workflow Example)

Source: https://docs.openclaw.ai/tools/clawhub

Example of downloading a skill pack named 'my-skill-pack' using the CLI.

```bash
clawhub install my-skill-pack
```

--------------------------------

### Import Setup Runtime Helpers

Source: https://docs.openclaw.ai/plugins/sdk-channel-plugins

Use `openclaw/plugin-sdk/setup-runtime` for import-safe setup patch adapters, lookup-note output, prompt resolution, and delegated setup-proxy builders.

```javascript
import {
  createPatchedAccountSetupAdapter,
  createEnvPatchedAccountSetupAdapter,
  createSetupInputPresenceValidator,
} from "openclaw/plugin-sdk/setup-runtime";
```

--------------------------------

### Start LM Studio Server

Source: https://docs.openclaw.ai/providers/lmstudio

Commands to initialize the daemon or start the local server instance.

```bash
lms daemon up
```

```bash
lms server start --port 1234
```

--------------------------------

### Installation with Environment Variables

Source: https://docs.openclaw.ai/install/installer

Details on how to configure the installation using environment variables.

```APIDOC
## Environment Variables for Installation

### Description
Environment variables can be used to control the installation process, providing an alternative to command-line flags.

### Environment Variables Reference
| Variable                                                | Description                                   |
| ------------------------------------------------------- | --------------------------------------------- |
| `OPENCLAW_INSTALL_METHOD=git|npm`                      | Install method                                |
| `OPENCLAW_VERSION=latest|next|main|<semver>|<spec>` | npm version, dist-tag, or package spec        |
| `OPENCLAW_BETA=0|1`                                    | Use beta if available                         |
| `OPENCLAW_GIT_DIR=<path>`                               | Checkout directory                            |
| `OPENCLAW_GIT_UPDATE=0|1`                              | Toggle git updates                            |
| `OPENCLAW_NO_PROMPT=1`                                  | Disable prompts                               |
| `OPENCLAW_NO_ONBOARD=1`                                 | Skip onboarding                               |
| `OPENCLAW_DRY_RUN=1`                                    | Dry run mode                                  |
| `OPENCLAW_VERBOSE=1`                                    | Debug mode                                    |
| `OPENCLAW_NPM_LOGLEVEL=error|warn|notice`             | npm log level                                 |
| `SHARP_IGNORE_GLOBAL_LIBVIPS=0|1`                      | Control sharp/libvips behavior (default: `1`) |

### Example Usage
```bash
export OPENCLAW_INSTALL_METHOD=git
export OPENCLAW_GIT_DIR=~/my-openclaw-repo
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
```

### Response
(Output of the bash script execution)
```

--------------------------------

### Run Interactive Onboarding

Source: https://docs.openclaw.ai/providers/opencode-go

Initiates the interactive setup process for the Go provider.

```bash
openclaw onboard --auth-choice opencode-go
```

--------------------------------

### Install and restart node host

Source: https://docs.openclaw.ai/nodes/index

Install the node as a service and restart it.

```bash
openclaw node install --host <gateway-host> --port 18789 --display-name "Build Node"
openclaw node restart
```

--------------------------------

### Install Docker and Dependencies

Source: https://docs.openclaw.ai/install/hetzner

Installs necessary packages like git and curl, then installs Docker. Verify the installation by checking the Docker and Docker Compose versions.

```bash
apt-get update
apt-get install -y git curl ca-certificates
curl -fsSL https://get.docker.com | sh
```

```bash
docker --version
docker compose version
```

--------------------------------

### Install from source

Source: https://docs.openclaw.ai/install

Clone the repository and build the project locally for development purposes.

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install && pnpm build && pnpm ui:build
pnpm link --global
openclaw onboard --install-daemon
```

--------------------------------

### Perform non-interactive setup

Source: https://docs.openclaw.ai/providers/deepseek

Configures the environment for headless or scripted installations by passing all required flags directly.

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice deepseek-api-key \
  --deepseek-api-key "$DEEPSEEK_API_KEY" \
  --skip-health \
  --accept-risk
```

--------------------------------

### Install Node.js on Ubuntu/Debian

Source: https://docs.openclaw.ai/install/node

Install Node.js on Ubuntu or Debian-based systems using NodeSource setup script and apt.

```bash
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt-get install -y nodejs
```

--------------------------------

### OpenCode Configuration Example

Source: https://docs.openclaw.ai/providers/opencode

A JSON5 configuration example showing environment variables and default agent model settings for OpenCode.

```json5
{
  env: { OPENCODE_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "opencode/claude-opus-4-6" } } },
}
```

--------------------------------

### Define Setup Entry Point

Source: https://docs.openclaw.ai/plugins/sdk-channel-plugins

Create a lightweight setup entry to avoid loading heavy runtime code when the channel is disabled or unconfigured.

```typescript
import { defineSetupPluginEntry } from "openclaw/plugin-sdk/channel-core";
import { acmeChatPlugin } from "./src/channel.js";

export default defineSetupPluginEntry(acmeChatPlugin);
```

--------------------------------

### Install OpenClaw

Source: https://docs.openclaw.ai/install/exe-dev

Execute the official installation script to set up OpenClaw.

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

--------------------------------

### Openclaw Wiki Get Command Examples

Source: https://docs.openclaw.ai/cli/wiki

Examples of using the `openclaw wiki get` command to retrieve specific wiki pages by ID or path. Use `--from` and `--lines` to control the output.

```bash
openclaw wiki get entity.alpha
```

```bash
openclaw wiki get syntheses/alpha-summary.md --from 1 --lines 80
```

--------------------------------

### Setup Runtime and Adapter Imports

Source: https://docs.openclaw.ai/plugins/sdk-channel-plugins

Prefer `openclaw/plugin-sdk/setup-runtime` and `openclaw/plugin-sdk/setup-adapter-runtime` for setup-specific functionalities when the broader surface is not needed.

```javascript
openclaw/plugin-sdk/setup-runtime
```

```javascript
openclaw/plugin-sdk/setup-adapter-runtime
```

--------------------------------

### Install OpenClaw (Skip Onboarding PowerShell)

Source: https://docs.openclaw.ai/install/installer

Installs OpenClaw using PowerShell while skipping the onboarding process. This is useful for automated setups where user interaction is not desired.

```powershell
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard
```

--------------------------------

### Install from Marketplace using Shorthand

Source: https://docs.openclaw.ai/cli/plugins

Installs a plugin from a marketplace using a shorthand notation, provided the marketplace is listed in `~/.claude/plugins/known_marketplaces.json`.

```bash
openclaw plugins install <plugin-name>@<marketplace-name>
```

--------------------------------

### Install via package managers

Source: https://docs.openclaw.ai/install

Install the global CLI using npm, pnpm, or bun, followed by daemon initialization.

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

```bash
pnpm add -g openclaw@latest
pnpm approve-builds -g
openclaw onboard --install-daemon
```

```bash
bun add -g openclaw@latest
openclaw onboard --install-daemon
```

--------------------------------

### Run interactive onboarding

Source: https://docs.openclaw.ai/providers/deepseek

Initiates the interactive setup process to configure the DeepSeek API key and set the default model.

```bash
openclaw onboard --auth-choice deepseek-api-key
```

--------------------------------

### Install Plugins with OpenClaw CLI

Source: https://docs.openclaw.ai/cli/plugins

Demonstrates various ways to install plugins using the `openclaw plugins install` command. Supports installation from ClawHub, npm, local paths, and marketplaces with options for forcing installation and pinning versions.

```bash
openclaw plugins install <package>                      # ClawHub first, then npm
openclaw plugins install clawhub:<package>              # ClawHub only
openclaw plugins install <package> --force              # overwrite existing install
openclaw plugins install <package> --pin                # pin version
openclaw plugins install <package> --dangerously-force-unsafe-install
openclaw plugins install <path>                         # local path
openclaw plugins install <plugin>@<marketplace>         # marketplace
openclaw plugins install <plugin> --marketplace <name>  # marketplace (explicit)
openclaw plugins install <plugin> --marketplace https://github.com/<owner>/<repo>
```

--------------------------------

### Run OpenClaw onboarding

Source: https://docs.openclaw.ai/install/digitalocean

Initializes the gateway configuration and installs the systemd daemon.

```bash
openclaw onboard --install-daemon
```

--------------------------------

### Initialize OpenClaw Setup

Source: https://docs.openclaw.ai/cli/setup

Run the setup command with various flags to configure the workspace, onboarding mode, or remote gateway connection.

```bash
openclaw setup
openclaw setup --workspace ~/.openclaw/workspace
openclaw setup --wizard
openclaw setup --non-interactive --mode remote --remote-url wss://gateway-host:18789 --remote-token <token>
```

--------------------------------

### Sync and Backup Multiple Skills (Workflow Example)

Source: https://docs.openclaw.ai/tools/clawhub

Example of syncing and backing up multiple skills at once using the `--all` flag for non-interactive upload.

```bash
clawhub sync --all
```

--------------------------------

### Channel Setup Builders and Primitives

Source: https://docs.openclaw.ai/plugins/sdk-channel-plugins

Use `openclaw/plugin-sdk/channel-setup` for optional-install setup builders and setup-safe primitives like `createOptionalChannelSetupSurface` and `createOptionalChannelSetupAdapter`.

```javascript
openclaw/plugin-sdk/channel-setup
```

```javascript
createOptionalChannelSetupSurface
```

```javascript
createOptionalChannelSetupAdapter
```

--------------------------------

### Run Onboarding Inside Container

Source: https://docs.openclaw.ai/install/podman

Launch the container and run the setup process for onboarding. Access the UI at http://127.0.0.1:18789/ and use the token from ~/.openclaw/.env.

```bash
./scripts/run-openclaw-podman.sh launch setup
```

--------------------------------

### Run interactive onboarding for Hugging Face

Source: https://docs.openclaw.ai/providers/huggingface

Initiates the interactive setup process to configure the Hugging Face API key.

```bash
openclaw onboard --auth-choice huggingface-api-key
```

--------------------------------

### Install Prerequisites

Source: https://docs.openclaw.ai/install/exe-dev

Install necessary system packages on the VM before running the OpenClaw installer.

```bash
sudo apt-get update
sudo apt-get install -y git curl jq ca-certificates openssl
```

--------------------------------

### Quick start browser commands

Source: https://docs.openclaw.ai/cli/browser

Initial commands to list profiles, start a browser, navigate to a URL, and take a snapshot.

```bash
openclaw browser profiles
openclaw browser --browser-profile openclaw start
openclaw browser --browser-profile openclaw open https://example.com
openclaw browser --browser-profile openclaw snapshot
```

--------------------------------

### Onboard Kimi Coding

Source: https://docs.openclaw.ai/providers/moonshot

Run this command to start the onboarding process for Kimi Coding API key authentication.

```bash
openclaw onboard --auth-choice kimi-code-api-key
```

--------------------------------

### Location Get Command CLI Usage

Source: https://docs.openclaw.ai/nodes/location-command

Example of how to invoke the location get command using the OpenClaw CLI. Requires specifying the node ID.

```bash
openclaw nodes location get --node <id>
```

--------------------------------

### Run Onboarding Wizard

Source: https://docs.openclaw.ai/cli/setup

Execute the interactive onboarding process to configure the environment.

```bash
openclaw setup --wizard
```

--------------------------------

### Create an Optional Channel Setup Surface

Source: https://docs.openclaw.ai/plugins/sdk-setup

Initializes a setup surface that only appears in specific contexts, returning both an adapter and a wizard.

```typescript
import { createOptionalChannelSetupSurface } from "openclaw/plugin-sdk/channel-setup";

const setupSurface = createOptionalChannelSetupSurface({
  channel: "my-channel",
  label: "My Channel",
  npmSpec: "@myorg/openclaw-my-channel",
  docsPath: "/channels/my-channel",
});
// Returns { setupAdapter, setupWizard }
```

--------------------------------

### Manage Gateway Service Lifecycle

Source: https://docs.openclaw.ai/cli/gateway

Commands to install, start, stop, restart, or uninstall the OpenClaw Gateway service.

```bash
openclaw gateway install
openclaw gateway start
openclaw gateway stop
openclaw gateway restart
openclaw gateway uninstall
```

--------------------------------

### Install Plugin Bundles

Source: https://docs.openclaw.ai/plugins/bundles

Install bundles from local directories, archives, or the Claude marketplace.

```bash
# Local directory
openclaw plugins install ./my-bundle

# Archive
openclaw plugins install ./my-bundle.tgz

# Claude marketplace
openclaw plugins marketplace list <marketplace-name>
openclaw plugins install <plugin-name>@<marketplace-name>
```

--------------------------------

### Plan or Apply CoreDNS Setup

Source: https://docs.openclaw.ai/cli/dns

Use `openclaw dns setup` to plan or apply CoreDNS configuration for discovery. The `--apply` flag installs or updates the CoreDNS config and restarts the service, requiring sudo on macOS.

```bash
openclaw dns setup
```

```bash
openclaw dns setup --domain openclaw.internal
```

```bash
openclaw dns setup --apply
```

--------------------------------

### List WSL distributions

Source: https://docs.openclaw.ai/platforms/windows

Lists all installed WSL distributions and their states. Use this to find the correct name for your distribution when scheduling WSL to start at boot.

```powershell
wsl --list --verbose
```

--------------------------------

### Stop and Start OpenClaw Gateway Service

Source: https://docs.openclaw.ai/help/faq

Commands to stop and start the OpenClaw Gateway when it's installed as a supervised service. This is typically used for background daemon operations.

```bash
openclaw gateway stop
openclaw gateway start
```

--------------------------------

### Install from GitHub main

Source: https://docs.openclaw.ai/install

Install the latest version directly from the main branch of the GitHub repository.

```bash
npm install -g github:openclaw/openclaw#main
```

--------------------------------

### Split Setup Entries

Source: https://docs.openclaw.ai/plugins/sdk-migration

Use `splitSetupEntries` to split setup entries.

```typescript
splitSetupEntries
```

--------------------------------

### Check Openclaw Installation and Gateway Status

Source: https://docs.openclaw.ai/gateway/troubleshooting

Run these commands to verify your Openclaw installation, check the doctor status, and confirm the gateway is operational. These are useful for initial setup and troubleshooting.

```bash
openclaw --version
openclaw doctor
openclaw gateway status
```

--------------------------------

### Full QMD configuration example

Source: https://docs.openclaw.ai/reference/memory-config

Comprehensive configuration for the QMD backend, including citation settings, update intervals, and path definitions.

```json5
{
  memory: {
    backend: "qmd",
    citations: "auto",
    qmd: {
      includeDefaultMemory: true,
      update: { interval: "5m", debounceMs: 15000 },
      limits: { maxResults: 6, timeoutMs: 4000 },
      scope: {
        default: "deny",
        rules: [{ action: "allow", match: { chatType: "direct" } }],
      },
      paths: [{ name: "docs", path: "~/notes", pattern: "**/*.md" }],
    },
  },
}
```

--------------------------------

### Example of Multi-Language Support Group

Source: https://docs.openclaw.ai/channels/broadcast-groups

Demonstrates a broadcast group setup for 'International Support', with separate agents configured to respond in English, German, and Spanish.

```yaml
Group: "International Support"
Agents:
  - Agent_EN (responds in English)
  - Agent_DE (responds in German)
  - Agent_ES (responds in Spanish)
```

--------------------------------

### Slack Native Command Example

Source: https://docs.openclaw.ai/channels/slack

Example of a Slack native command. This command is '/help'.

```text
/help
```

--------------------------------

### Publish a Single Skill (Workflow Example)

Source: https://docs.openclaw.ai/tools/clawhub

Example of publishing a single skill from a local directory, including slug, name, version, and tags.

```bash
clawhub skill publish ./my-skill --slug my-skill --name "My Skill" --version 1.0.0 --tags latest
```

--------------------------------

### Search for Skills (Workflow Example)

Source: https://docs.openclaw.ai/tools/clawhub

Example of searching for skills related to 'postgres backups' using the CLI.

```bash
clawhub search "postgres backups"
```

--------------------------------

### Start the server

Source: https://docs.openclaw.ai/providers/claude-max-api-proxy

Launch the proxy server, which defaults to running at http://localhost:3456.

```bash
claude-max-api
# Server runs at http://localhost:3456
```

--------------------------------

### Install and verify imsg CLI

Source: https://docs.openclaw.ai/channels/imessage

Installs the imsg CLI using Homebrew and verifies the installation by checking the help command. Ensure Homebrew is installed and configured.

```bash
brew install steipete/tap/imsg
imsg rpc --help
```

--------------------------------

### Switch from Git to npm Installation

Source: https://docs.openclaw.ai/help/faq

Use these commands to switch from a git installation to an npm installation. Ensure you run `openclaw doctor` and `openclaw gateway restart` after installation to update the gateway service.

```bash
npm install -g openclaw@latest
openclaw doctor
openclaw gateway restart
```

--------------------------------

### Switch from npm to Git Installation

Source: https://docs.openclaw.ai/help/faq

Use these commands to switch from an npm installation to a git installation. Ensure you run `openclaw doctor` and `openclaw gateway restart` after installation to update the gateway service.

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm build
openclaw doctor
openclaw gateway restart
```

--------------------------------

### Example /btw Command Usage

Source: https://docs.openclaw.ai/tools/btw

Use the /btw command followed by your question to get a quick answer about the current session. This command is ephemeral and does not affect session history.

```text
/btw what changed?
```

```text
/btw what file are we editing?
```

```text
/btw what does this error mean?
```

```text
/btw summarize the current task in one sentence
```

```text
/btw what is 17 * 19?
```

--------------------------------

### Initialize Feishu channel

Source: https://docs.openclaw.ai/channels/feishu

Run the setup wizard to authenticate and create a bot, then restart the gateway to apply changes.

```bash
openclaw channels login --channel feishu
```

```bash
openclaw gateway restart
```

--------------------------------

### OpenAI Configuration Example

Source: https://docs.openclaw.ai/providers/openai

Example configuration file for OpenAI API key authentication.

```json5
{
  env: { OPENAI_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "openai/gpt-5.4" } } },
}
```

--------------------------------

### Install Zalo Personal Plugin from npm

Source: https://docs.openclaw.ai/plugins/zalouser

Use this command to install the Zalo Personal plugin from npm. Restart the Gateway after installation.

```bash
openclaw plugins install @openclaw/zalouser
```

--------------------------------

### setup Fields Reference

Source: https://docs.openclaw.ai/plugins/manifest

General setup fields for OpenClaw AI plugins.

```APIDOC
## setup Fields Reference

### Description
General setup fields for OpenClaw AI plugins.

### Parameters
#### Request Body
- **providers** (object[]) - Optional - Provider setup descriptors exposed during setup and onboarding.
- **cliBackends** (string[]) - Optional - Setup-time backend ids used for descriptor-first setup lookup. Keep normalized ids globally unique.
- **configMigrations** (string[]) - Optional - Config migration ids owned by this plugin's setup surface.
- **requiresRuntime** (boolean) - Optional - Whether setup still needs `setup-api` execution after descriptor lookup.
```

--------------------------------

### Groq Configuration File Example

Source: https://docs.openclaw.ai/providers/groq

An example configuration file demonstrating how to set the Groq API key and default model. This file should be placed in the appropriate OpenClaw configuration directory.

```json5
{
  env: { GROQ_API_KEY: "gsk_..." },
  agents: {
    defaults: {
      model: { primary: "groq/llama-3.3-70b-versatile" },
    },
  },
}
```

--------------------------------

### Automate onboarding with baseline configuration

Source: https://docs.openclaw.ai/start/wizard-cli-automation

Use this command for a standard non-interactive setup. Ensure required environment variables like ANTHROPIC_API_KEY are set before execution.

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice apiKey \
  --anthropic-api-key "$ANTHROPIC_API_KEY" \
  --secret-input-mode plaintext \
  --gateway-port 18789 \
  --gateway-bind loopback \
  --install-daemon \
  --daemon-runtime node \
  --skip-skills
```

--------------------------------

### Run basic OpenClaw CLI commands on Windows

Source: https://docs.openclaw.ai/platforms/windows

Examples of basic OpenClaw CLI commands that work on native Windows. These commands are useful for checking installation and plugin status.

```powershell
openclaw --version
```

```powershell
openclaw doctor
```

```powershell
openclaw plugins list --json
```

--------------------------------

### Bootstrap OpenClaw Setup

Source: https://docs.openclaw.ai/start/setup

Initializes the local configuration and workspace for OpenClaw.

```bash
openclaw setup
```

```bash
openclaw setup
```

--------------------------------

### Enable and Restart WeChat Plugin

Source: https://docs.openclaw.ai/channels/wechat

If a channel shows as installed but not connecting, enable the associated plugin and restart the OpenClaw gateway. This is often necessary after initial setup or configuration changes.

```bash
openclaw config set plugins.entries.openclaw-weixin.enabled true
```

```bash
openclaw gateway restart
```

--------------------------------

### Install Prerequisites

Source: https://docs.openclaw.ai/install/ansible

Updates the package list and installs Ansible and Git on the host system.

```bash
sudo apt update && sudo apt install -y ansible git
```

--------------------------------

### Verify OpenClaw CLI and Gateway

Source: https://docs.openclaw.ai/platforms/mac/bundled-gateway

Checks the installed CLI version and starts the Gateway in local mode, binding to a specific port and interface. Use this to ensure the CLI is functional and the Gateway can be launched.

```bash
openclaw --version
```

```bash
OPENCLAW_SKIP_CHANNELS=1 \
OPENCLAW_SKIP_CANVAS_HOST=1 \
openclaw gateway --port 18999 --bind loopback
```

--------------------------------

### Install LM Studio

Source: https://docs.openclaw.ai/providers/lmstudio

Use this command to install the LM Studio headless daemon.

```bash
curl -fsSL https://lmstudio.ai/install.sh | bash
```

--------------------------------

### Search and Install Skills on Linux

Source: https://docs.openclaw.ai/help/faq

Commands for searching, installing, and managing skills on Linux systems. Native installation writes to the active workspace.

```bash
openclaw skills search "calendar"
```

```bash
openclaw skills search --limit 20
```

```bash
openclaw skills install <skill-slug>
```

```bash
openclaw skills install <skill-slug> --version <version>
```

```bash
openclaw skills install <skill-slug> --force
```

```bash
openclaw skills update --all
```

```bash
openclaw skills list --eligible
```

```bash
openclaw skills check
```

--------------------------------

### Start and open browser via CLI

Source: https://docs.openclaw.ai/tools/browser-login

Commands to initialize the browser and navigate to a specific URL using the CLI.

```bash
openclaw browser start
openclaw browser open https://x.com
```

--------------------------------

### Run Gmail Watcher

Source: https://docs.openclaw.ai/cli/index

Starts the local Gmail watcher and renew loop. Allows runtime overrides for setup flags.

```bash
openclaw webhooks gmail run
```

--------------------------------

### Define a lightweight setup entry

Source: https://docs.openclaw.ai/plugins/sdk-entrypoints

Use this for setup-only files to avoid loading full runtime or CLI wiring.

```typescript
import { defineSetupPluginEntry } from "openclaw/plugin-sdk/channel-core";

export default defineSetupPluginEntry(myChannelPlugin);
```

--------------------------------

### Install OpenClaw

Source: https://docs.openclaw.ai/install/azure

Download and execute the OpenClaw installation script within the VM shell.

```bash
curl -fsSL https://openclaw.ai/install.sh -o /tmp/install.sh
bash /tmp/install.sh
rm -f /tmp/install.sh
```

--------------------------------

### Configure Remote Mac iMessage Channel

Source: https://docs.openclaw.ai/channels/imessage

Example configuration for a remote Mac setup using SSH and SCP for attachment fetching.

```json5
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "~/.openclaw/scripts/imsg-ssh",
      remoteHost: "bot@mac-mini.tailnet-1234.ts.net",
      includeAttachments: true,
      dbPath: "/Users/bot/Library/Messages/chat.db",
    },
  },
}
```

```bash
#!/usr/bin/env bash
exec ssh -T bot@mac-mini.tailnet-1234.ts.net imsg "$@"
```

--------------------------------

### Display Detailed Context Breakdown (Example)

Source: https://docs.openclaw.ai/concepts/context

This is an example output from the `/context detail` command, showing a deeper dive into context usage, particularly for skills and tool schemas.

```text
🧠 Context breakdown (detailed)
…
Top skills (prompt entry size):
- frontend-design: 412 chars (~103 tok)
- oracle: 401 chars (~101 tok)
… (+10 more skills)

Top tools (schema size):
- browser: 9,812 chars (~2,453 tok)
- exec: 6,240 chars (~1,560 tok)
… (+N more tools)
```

--------------------------------

### Create Optional Channel Setup Wizard

Source: https://docs.openclaw.ai/plugins/sdk-migration

Use `createOptionalChannelSetupWizard` to create a wizard for optional channel setup.

```typescript
createOptionalChannelSetupWizard
```

--------------------------------

### Configure Skills Loading and Installation

Source: https://docs.openclaw.ai/tools/skills-config

Defines directories for extra skills, enables watching for changes, and sets preferences for package managers and installers. Use this to manage how and where skills are loaded and installed.

```json5
{
  skills: {
    allowBundled: ["gemini", "peekaboo"],
    load: {
      extraDirs: ["~/Projects/agent-scripts/skills", "~/Projects/oss/some-skill-pack/skills"],
      watch: true,
      watchDebounceMs: 250,
    },
    install: {
      preferBrew: true,
      nodeManager: "npm", // npm | pnpm | yarn | bun (Gateway runtime still Node; bun not recommended)
    },
    entries: {
      "image-lab": {
        enabled: true,
        apiKey: { source: "env", provider: "default", id: "GEMINI_API_KEY" }, // or plaintext string
        env: {
          GEMINI_API_KEY: "GEMINI_KEY_HERE",
        },
      },
      peekaboo: { enabled: true },
      sag: { enabled: false },
    },
  },
}
```

--------------------------------

### Display Context Breakdown (Example)

Source: https://docs.openclaw.ai/concepts/context

This is an example output from the `/context list` command, illustrating how context is broken down by workspace, system prompt, injected files, and skills.

```text
🧠 Context breakdown
Workspace: <workspaceDir>
Bootstrap max/file: 12,000 chars
Sandbox: mode=non-main sandboxed=false
System prompt (run): 38,412 chars (~9,603 tok) (Project Context 23,901 chars (~5,976 tok))

Injected workspace files:
- AGENTS.md: OK | raw 1,742 chars (~436 tok) | injected 1,742 chars (~436 tok)
- SOUL.md: OK | raw 912 chars (~228 tok) | injected 912 chars (~228 tok)
- TOOLS.md: TRUNCATED | raw 54,210 chars (~13,553 tok) | injected 20,962 chars (~5,241 tok)
- IDENTITY.md: OK | raw 211 chars (~53 tok) | injected 211 chars (~53 tok)
- USER.md: OK | raw 388 chars (~97 tok) | injected 388 chars (~97 tok)
- HEARTBEAT.md: MISSING | raw 0 | injected 0
- BOOTSTRAP.md: OK | raw 0 chars (~0 tok) | injected 0 chars (~0 tok)

Skills list (system prompt text): 2,184 chars (~546 tok) (12 skills)
Tools: read, edit, write, exec, process, browser, message, sessions_send, …
Tool list (system prompt text): 1,032 chars (~258 tok)
Tool schemas (JSON): 31,988 chars (~7,997 tok) (counts toward context; not shown as text)
Tools: (same as above)

Session tokens (cached): 14,250 total / ctx=32,000
```

--------------------------------

### Install acpx Plugin

Source: https://docs.openclaw.ai/tools/acp-agents

Install the acpx backend plugin using the OpenClaw CLI. Use this command for fresh installs or when switching to a local development checkout. Verify the installation with '/acp doctor'.

```bash
openclaw plugins install acpx
openclaw config set plugins.entries.acpx.enabled true
```

--------------------------------

### Run OpenClaw installer with verbose output

Source: https://docs.openclaw.ai/help/faq

Use these commands to debug installation issues by enabling verbose logging. The beta and git-based installation methods are also provided for specific use cases.

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --verbose
```

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --beta --verbose
```

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git --verbose
```

--------------------------------

### Get Google Chat Channel Configuration

Source: https://docs.openclaw.ai/channels/googlechat

Retrieve the current configuration for the Google Chat channel. Use this to verify if the channel is configured in your Openclaw setup.

```bash
openclaw config get channels.googlechat
```

--------------------------------

### Install OpenClaw (install-cli.sh)

Source: https://docs.openclaw.ai/install/installer

Installs OpenClaw CLI using the install-cli.sh script. This command downloads and executes the script for a local prefix installation.

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash
```

--------------------------------

### Verify Binary Installation

Source: https://docs.openclaw.ai/install/docker-vm-runtime

Check if the installed binaries are accessible within the running container. This confirms that the installation steps in the Dockerfile were successful.

```bash
docker compose exec openclaw-gateway which gog
docker compose exec openclaw-gateway which goplaces
docker compose exec openclaw-gateway which wacli
```

--------------------------------

### Install Voice Call Plugin from npm

Source: https://docs.openclaw.ai/plugins/voice-call

Use this command to install the Voice Call plugin from npm. Ensure you restart the Gateway after installation.

```bash
openclaw plugins install @openclaw/voice-call
```

--------------------------------

### Example of Task Automation Group

Source: https://docs.openclaw.ai/channels/broadcast-groups

Presents a broadcast group setup for 'Project Management', assigning agents to tasks such as updating databases, logging time, and generating reports.

```yaml
Group: "Project Management"
Agents:
  - TaskTracker (updates task database)
  - TimeLogger (logs time spent)
  - ReportGenerator (creates summaries)
```

--------------------------------

### Install OpenClaw CLI

Source: https://docs.openclaw.ai/install/installer

Use these commands to install the OpenClaw CLI. The script supports various flags for custom installation paths, methods, and post-installation onboarding.

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash
```

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --prefix /opt/openclaw --version latest
```

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --install-method git --git-dir ~/openclaw
```

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --json --prefix /opt/openclaw
```

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --onboard
```

--------------------------------

### Install Homebrew on Linux

Source: https://docs.openclaw.ai/help/faq

Commands to install and configure Homebrew on a Linux system.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.profile
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
brew install <formula>
```

--------------------------------

### Onboard OpenClaw with LiteLLM

Source: https://docs.openclaw.ai/providers/litellm

Use this command for a quick setup of OpenClaw with LiteLLM using an API key.

```bash
openclaw onboard --auth-choice litellm-api-key
```

--------------------------------

### Run onboarding for Synthetic

Source: https://docs.openclaw.ai/providers/synthetic

Execute the onboarding command to configure the Synthetic provider using an API key.

```bash
openclaw onboard --auth-choice synthetic-api-key
```

--------------------------------

### Install OpenClaw

Source: https://docs.openclaw.ai/

Install the OpenClaw package globally using npm. Ensure you have Node.js 24 or Node.js 22 LTS installed.

```bash
npm install -g openclaw@latest

```

--------------------------------

### Start the Gateway Service

Source: https://docs.openclaw.ai/gateway

Use these commands to start the Gateway service locally. The `--verbose` flag mirrors debug/trace output to stdio. `--force` can be used to kill an existing listener on the selected port before starting.

```bash
openclaw gateway --port 18789
# debug/trace mirrored to stdio
openclaw gateway --port 18789 --verbose
# force-kill listener on selected port, then start
openclaw gateway --force
```

--------------------------------

### Show Help for install.sh

Source: https://docs.openclaw.ai/install/installer

Displays the help message for the install.sh script, showing available options and usage instructions.

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --help
```

--------------------------------

### Default Installation

Source: https://docs.openclaw.ai/install/installer

Installs Openclaw AI using the default settings.

```APIDOC
## curl https://openclaw.ai/install.sh | bash

### Description
Installs Openclaw AI using the default method and settings.

### Method
GET

### Endpoint
https://openclaw.ai/install.sh

### Request Example
```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
```

### Response
(Output of the bash script execution)
```

--------------------------------

### Configure OpenCode Go via JSON5

Source: https://docs.openclaw.ai/providers/opencode-go

Example configuration file structure for setting the API key and default model.

```json5
{
  env: { OPENCODE_API_KEY: "YOUR_API_KEY_HERE" }, // pragma: allowlist secret
  agents: { defaults: { model: { primary: "opencode-go/kimi-k2.5" } } },
}
```

--------------------------------

### Create Optional Channel Setup Adapter

Source: https://docs.openclaw.ai/plugins/sdk-migration

Use `createOptionalChannelSetupAdapter` for optional channel setup adapters.

```typescript
createOptionalChannelSetupAdapter
```

--------------------------------

### Update Setup Command

Source: https://docs.openclaw.ai/cli/sandbox

Recreate runtimes globally or for a specific agent after changing the setup command.

```bash
openclaw sandbox recreate --all
# or just one agent:
openclaw sandbox recreate --agent family
```

--------------------------------

### Install Node Host as Service

Source: https://docs.openclaw.ai/cli/node

Command to install the node host as a background user service.

```bash
openclaw node install --host <gateway-host> --port 18789
```

--------------------------------

### Install and Configure Gateway via CLI

Source: https://docs.openclaw.ai/platforms/linux

Commands to initialize the gateway service or configure settings. Select the Gateway service option when prompted by the interactive CLI.

```bash
openclaw onboard --install-daemon
```

```bash
openclaw gateway install
```

```bash
openclaw configure
```

--------------------------------

### Connect and install OpenClaw on Droplet

Source: https://docs.openclaw.ai/install/digitalocean

Updates the system, installs Node.js 24, and sets up the OpenClaw environment.

```bash
ssh root@YOUR_DROPLET_IP

apt update && apt upgrade -y

# Install Node.js 24
curl -fsSL https://deb.nodesource.com/setup_24.x | bash -
apt install -y nodejs

# Install OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw --version
```

--------------------------------

### Configure Skills Loading and Installation

Source: https://docs.openclaw.ai/gateway/configuration-reference

Manage skill loading, including extra directories and installation preferences. Set API keys for specific skills or disable them. The `preferBrew` option prioritizes Homebrew for installations.

```json5
{
  skills: {
    allowBundled: ["gemini", "peekaboo"],
    load: {
      extraDirs: ["~/Projects/agent-scripts/skills"],
    },
    install: {
      preferBrew: true,
      nodeManager: "npm", // npm | pnpm | yarn | bun
    },
    entries: {
      "image-lab": {
        apiKey: { source: "env", provider: "default", id: "GEMINI_API_KEY" }, // or plaintext string
        env: { GEMINI_API_KEY: "GEMINI_KEY_HERE" },
      },
      peekaboo: { enabled: true },
      sag: { enabled: false },
    },
  },
}
```

--------------------------------

### setup.providers Reference

Source: https://docs.openclaw.ai/plugins/manifest

Defines the parameters for provider setup and authentication.

```APIDOC
## setup.providers Reference

### Description
Defines the parameters for provider setup and authentication.

### Parameters
#### Request Body
- **id** (string) - Required - Provider id exposed during setup or onboarding. Keep normalized ids globally unique.
- **authMethods** (string[]) - Optional - Setup/auth method ids this provider supports without loading full runtime.
- **envVars** (string[]) - Optional - Env vars that generic setup/status surfaces can check before plugin runtime loads.
```

--------------------------------

### Install from Marketplace Explicitly

Source: https://docs.openclaw.ai/cli/plugins

Installs a plugin from a marketplace by explicitly specifying the marketplace source. This can be a known marketplace name, a local path, a GitHub repository shorthand, a URL, or a git URL.

```bash
openclaw plugins install <plugin-name> --marketplace <marketplace-name>
openclaw plugins install <plugin-name> --marketplace <owner/repo>
openclaw plugins install <plugin-name> --marketplace https://github.com/<owner>/<repo>
openclaw plugins install <plugin-name> --marketplace ./my-marketplace
```

--------------------------------

### Install a Skill using OpenClaw CLI

Source: https://docs.openclaw.ai/tools/clawhub

Install a skill into your active workspace using its slug. The `<skill-slug>` should be replaced with the actual identifier of the skill you wish to install.

```bash
openclaw skills install <skill-slug>
```

--------------------------------

### Install OpenClaw CLI

Source: https://docs.openclaw.ai/platforms/mac/bundled-gateway

Installs the OpenClaw CLI globally using npm. Ensure Node.js (v24 recommended, v22 LTS compatible) is installed.

```bash
npm install -g openclaw@<version>
```

--------------------------------

### Create macOS VM with Lume

Source: https://docs.openclaw.ai/install/macos-vm

Creates a new macOS virtual machine named 'openclaw' using the latest available IPSW image. A VNC window will open to guide you through the initial setup.

```bash
lume create openclaw --os macos --ipsw latest
```

--------------------------------

### Install and manage OpenClaw Gateway on Windows

Source: https://docs.openclaw.ai/platforms/windows

Installs the OpenClaw gateway service and checks its status. This is for native Windows installations where managed startup is desired.

```powershell
openclaw gateway install
```

```powershell
openclaw gateway status --json
```

--------------------------------

### Install Matrix Plugin

Source: https://docs.openclaw.ai/channels/matrix

Commands to install the Matrix plugin from npm or a local directory.

```bash
openclaw plugins install @openclaw/matrix
```

```bash
openclaw plugins install ./path/to/local/matrix-plugin
```

--------------------------------

### Configure Global Setup Command

Source: https://docs.openclaw.ai/gateway/sandboxing

Define a one-time setup command that runs after the sandbox container is created. This command executes via 'sh -lc' inside the container.

```json
agents.defaults.sandbox.docker.setupCommand
```

--------------------------------

### Setup and Run Gmail Webhooks

Source: https://docs.openclaw.ai/cli/webhooks

Basic commands to initialize and execute the Gmail webhook integration.

```bash
openclaw webhooks gmail setup --account you@example.com
openclaw webhooks gmail run
```

--------------------------------

### Install the proxy

Source: https://docs.openclaw.ai/providers/claude-max-api-proxy

Install the package globally and verify that the Claude Code CLI is authenticated.

```bash
npm install -g claude-max-api-proxy

# Verify Claude CLI is authenticated
claude --version
```

--------------------------------

### Install WhatsApp Plugin

Source: https://docs.openclaw.ai/channels/whatsapp

Use this command to manually install the WhatsApp plugin if it's not automatically handled during onboarding or channel addition.

```bash
openclaw plugins install @openclaw/whatsapp
```

--------------------------------

### OpenRouter Configuration Example

Source: https://docs.openclaw.ai/providers/openrouter

This JSON5 configuration example shows how to set up the OpenRouter API key in environment variables and specify the default model for agents.

```json5
{
  env: { OPENROUTER_API_KEY: "sk-or-..." },
  agents: {
    defaults: {
      model: { primary: "openrouter/auto" },
    },
  },
}
```

--------------------------------

### Install Gemini CLI

Source: https://docs.openclaw.ai/providers/google

Installation commands for the Gemini CLI required for OAuth-based authentication.

```bash
# Homebrew
brew install gemini-cli

# or npm
npm install -g @google/gemini-cli
```

--------------------------------

### Install Zalo Plugin from Source

Source: https://docs.openclaw.ai/channels/zalo

Install the Zalo plugin manually from a local source checkout using this command.

```bash
openclaw plugins install ./path/to/local/zalo-plugin
```

--------------------------------

### Install and Configure Tailscale

Source: https://docs.openclaw.ai/install/oracle

Installs Tailscale and configures it to use the specified hostname. Subsequent connections can be made via Tailscale.

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up --ssh --hostname=openclaw
```

--------------------------------

### Non-interactive Setup (Direct)

Source: https://docs.openclaw.ai/providers/arcee

Perform a non-interactive onboarding for Arcee AI direct access. Requires setting the ARCEEAI_API_KEY environment variable.

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice arceeai-api-key \
  --arceeai-api-key "$ARCEEAI_API_KEY"
```

--------------------------------

### Install Node.js on Fedora/RHEL

Source: https://docs.openclaw.ai/install/node

Install Node.js on Fedora or RHEL-based systems using dnf.

```bash
sudo dnf install nodejs
```

--------------------------------

### Verify Plugin Installation

Source: https://docs.openclaw.ai/plugins/bundles

List installed plugins and inspect specific bundle details to confirm format detection.

```bash
openclaw plugins list
openclaw plugins inspect <id>
```

--------------------------------

### Check OpenClaw Install and Status

Source: https://docs.openclaw.ai/channels/wechat

Use these commands to verify your OpenClaw installation, list installed plugins, check channel connectivity, and view the OpenClaw version.

```bash
openclaw plugins list
```

```bash
openclaw channels status --probe
```

```bash
openclaw --version
```

--------------------------------

### Install and Update OpenClaw Skills

Source: https://docs.openclaw.ai/help/faq

Commands to install a new skill by its slug and update all installed skills. Native installs are placed in the active workspace's `skills/` directory.

```bash
openclaw skills install <skill-slug>
```

```bash
openclaw skills update --all
```

--------------------------------

### Onboard OpenCode

Source: https://docs.openclaw.ai/start/wizard-cli-automation

Use this command to onboard with OpenCode. Ensure the OPENCODE_API_KEY environment variable is set. For the Go catalog, swap to `--auth-choice opencode-go --opencode-go-api-key "$OPENCODE_API_KEY"`.

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice opencode-zen \
  --opencode-zen-api-key "$OPENCODE_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

--------------------------------

### Install signal-cli on Linux

Source: https://docs.openclaw.ai/channels/signal

Installs the latest version of signal-cli from GitHub releases. Ensure you have curl and tar installed. This script downloads, extracts, and links the binary to /usr/local/bin.

```bash
VERSION=$(curl -Ls -o /dev/null -w %{url_effective} https://github.com/AsamK/signal-cli/releases/latest | sed -e 's/^.*\/v//')
curl -L -O "https://github.com/AsamK/signal-cli/releases/download/v${VERSION}/signal-cli-${VERSION}-Linux-native.tar.gz"
sudo tar xf "signal-cli-${VERSION}-Linux-native.tar.gz" -C /opt
sudo ln -sf /opt/signal-cli /usr/local/bin/
signal-cli --version
```

--------------------------------

### Install Nextcloud Talk Plugin via CLI

Source: https://docs.openclaw.ai/channels/nextcloud-talk

Use this command to install the Nextcloud Talk plugin from the npm registry using the OpenClaw CLI. Ensure you have the CLI installed and configured.

```bash
openclaw plugins install @openclaw/nextcloud-talk
```

--------------------------------

### Install WSL2 and Distribution

Source: https://docs.openclaw.ai/platforms/windows

Installs the WSL2 subsystem and a specific Linux distribution.

```powershell
wsl --install
# Or pick a distro explicitly:
wsl --list --online
wsl --install -d Ubuntu-24.04
```

--------------------------------

### Install OpenClaw CLI (JSON Bash)

Source: https://docs.openclaw.ai/install/installer

Installs the OpenClaw CLI using a bash script, specifying a JSON prefix for the installation directory. This is often used for custom deployments.

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --json --prefix /opt/openclaw
```

--------------------------------

### Install Project Dependencies

Source: https://docs.openclaw.ai/platforms/mac/dev-setup

Run this command in your project's root directory to install all necessary dependencies using pnpm.

```bash
pnpm install
```

--------------------------------

### Install Node.js 24

Source: https://docs.openclaw.ai/install/raspberry-pi

Configures the NodeSource repository and installs Node.js version 24.

```bash
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt install -y nodejs
node --version
```

--------------------------------

### Install OpenClaw (Dry Run PowerShell)

Source: https://docs.openclaw.ai/install/installer

Performs a dry run of the OpenClaw installation, printing the actions that would be taken without actually executing them. Useful for verifying the installation plan.

```powershell
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -DryRun
```

--------------------------------

### Simple OpenProse Program Example

Source: https://docs.openclaw.ai/prose

An example of a basic `.prose` file that sets up two agents to research and write in parallel, then merges their outputs.

```prose
# Research + synthesis with two agents running in parallel.

input topic: "What should we research?"

agent researcher:
  model: sonnet
  prompt: "You research thoroughly and cite sources."

agent writer:
  model: opus
  prompt: "You write a concise summary."

parallel:
  findings = session: researcher
    prompt: "Research {topic}."
  draft = session: writer
    prompt: "Summarize {topic}."

session "Merge the findings + draft into a final answer."
context: { findings, draft }
```

--------------------------------

### Install Docker on VM

Source: https://docs.openclaw.ai/install/gcp

Install Docker and necessary packages on the VM. After adding the user to the docker group, log out and back in for changes to take effect.

```bash
sudo apt-get update
sudo apt-get install -y git curl ca-certificates
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
```

```bash
exit
```

```bash
gcloud compute ssh openclaw-gateway --zone=us-central1-a
```

```bash
docker --version
docker compose version
```

--------------------------------

### Perform Non-Interactive Onboarding

Source: https://docs.openclaw.ai/providers/lmstudio

Automate setup for CI or remote provisioning environments.

```bash
openclaw onboard \
  --non-interactive \
  --accept-risk \
  --auth-choice lmstudio
```

```bash
openclaw onboard \
  --non-interactive \
  --accept-risk \
  --auth-choice lmstudio \
  --custom-base-url http://localhost:1234/v1 \
  --lmstudio-api-key "$LM_API_TOKEN" \
  --custom-model-id qwen/qwen3.5-9b
```

--------------------------------

### Install plugins via CLI

Source: https://docs.openclaw.ai/tools/plugin

Installs plugins from npm, local directories, or archive files.

```bash
# From npm
openclaw plugins install @openclaw/voice-call

# From a local directory or archive
openclaw plugins install ./my-plugin
openclaw plugins install ./my-plugin.tgz
```

--------------------------------

### Install Synology Chat plugin

Source: https://docs.openclaw.ai/channels/synology-chat

Use this command to install the plugin from a local source checkout if it is not already bundled.

```bash
openclaw plugins install ./path/to/local/synology-chat-plugin
```

--------------------------------

### Install OpenClaw (install.ps1)

Source: https://docs.openclaw.ai/install/installer

Installs OpenClaw using the install.ps1 script on Windows PowerShell. This command downloads and executes the script for installation.

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

--------------------------------

### Install Microsoft Teams Plugin

Source: https://docs.openclaw.ai/channels/msteams

Commands to install the plugin from a package or a local directory.

```bash
openclaw plugins install @openclaw/msteams
```

```bash
openclaw plugins install ./path/to/local/msteams-plugin
```

--------------------------------

### Lightweight State Checker Examples

Source: https://docs.openclaw.ai/plugins/manifest

Examples of configuring persisted auth and configured state checkers.

```APIDOC
### Persisted Auth State Example
```json
{
  "openclaw": {
    "channel": {
      "id": "whatsapp",
      "persistedAuthState": {
        "specifier": "./auth-presence",
        "exportName": "hasAnyWhatsAppAuth"
      }
    }
  }
}
```

### Configured State Example
```json
{
  "openclaw": {
    "channel": {
      "id": "telegram",
      "configuredState": {
        "specifier": "./configured-state",
        "exportName": "hasTelegramConfiguredState"
      }
    }
  }
}
```
```

--------------------------------

### Check Installation Status

Source: https://docs.openclaw.ai/install/development-channels

Displays the active channel, installation type, current version, and source information.

```bash
openclaw update status
```

--------------------------------

### Configure Gmail Webhooks

Source: https://docs.openclaw.ai/cli/webhooks

Examples for setting up Gmail webhooks with various project, JSON, and URL configurations.

```bash
openclaw webhooks gmail setup --account you@example.com
openclaw webhooks gmail setup --account you@example.com --project my-gcp-project --json
openclaw webhooks gmail setup --account you@example.com --hook-url https://gateway.example.com/hooks/gmail
```

--------------------------------

### Execute Common Follow-up Commands

Source: https://docs.openclaw.ai/cli/onboard

Standard commands for updating configuration or adding new agents after initial setup.

```bash
openclaw configure
openclaw agents add <name>
```

--------------------------------

### Start Development Gateway

Source: https://docs.openclaw.ai/start/setup

Commands to initialize and run the gateway in watch mode for development.

```bash
pnpm install
# First run only (or after resetting local OpenClaw config/workspace)
pnpm openclaw setup
pnpm gateway:watch
```

```bash
bun install
# First run only (or after resetting local OpenClaw config/workspace)
bun run openclaw setup
bun run gateway:watch
```

--------------------------------

### Install Default Matrix Plugin

Source: https://docs.openclaw.ai/install/migrating-matrix

Revert to the standard Matrix package when a custom path installation is no longer desired.

```bash
openclaw plugins install @openclaw/matrix
```

--------------------------------

### Show Help for install-cli.sh

Source: https://docs.openclaw.ai/install/installer

Displays the help message for the install-cli.sh script, showing available options and usage instructions for CLI installation.

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --help
```

--------------------------------

### Onboard with OAuth

Source: https://docs.openclaw.ai/providers/minimax

Run the onboarding command to authenticate with MiniMax using OAuth. Choose between international and China-specific endpoints.

```bash
openclaw onboard --auth-choice minimax-global-oauth
```

```bash
openclaw onboard --auth-choice minimax-cn-oauth
```

--------------------------------

### Setup and Run Gateways with Profiles

Source: https://docs.openclaw.ai/gateway/multiple-gateways

Use profiles to manage separate configurations and state directories for multiple gateway instances. Ensure unique ports for each instance to avoid conflicts.

```bash
# main
openclaw --profile main setup
openclaw --profile main gateway --port 18789

# rescue
openclaw --profile rescue setup
openclaw --profile rescue gateway --port 19001
```

--------------------------------

### Recommended OpenClaw Installation

Source: https://docs.openclaw.ai/help/faq

Installs OpenClaw using the recommended method and initiates the onboarding process, which may include building UI assets. The Gateway typically runs on port 18789 after onboarding.

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard --install-daemon
```

--------------------------------

### Create Optional Channel Setup Surface

Source: https://docs.openclaw.ai/plugins/sdk-migration

Use `createOptionalChannelSetupSurface` to create a surface for optional channel setup.

```typescript
createOptionalChannelSetupSurface
```

--------------------------------

### Add, Login, and Setup Auth Profiles

Source: https://docs.openclaw.ai/cli/models

Use these commands to manage authentication for model providers. `models auth add` is an interactive helper. `models auth login` runs a provider's auth flow. `models auth setup-token` and `models auth paste-token` are for token-based authentication.

```bash
openclaw models auth add
openclaw models auth login --provider <id>
openclaw models auth setup-token --provider <id>
openclaw models auth paste-token
```

--------------------------------

### Kimi Coding Configuration Example

Source: https://docs.openclaw.ai/providers/moonshot

Example configuration for Kimi Coding, including API key, default model, and model aliases.

```json
{
  env: { KIMI_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "kimi/kimi-code" },
      models: {
        "kimi/kimi-code": { alias: "Kimi" },
      },
    },
  },
}
```

--------------------------------

### Initialize development profile and gateway

Source: https://docs.openclaw.ai/help/debugging

Commands to spin up an isolated, disposable development environment.

```bash
pnpm gateway:dev
OPENCLAW_PROFILE=dev openclaw tui
```

```bash
pnpm gateway:dev:reset
```

```bash
OPENCLAW_PROFILE=dev openclaw gateway --dev --reset
```

```bash
openclaw gateway stop
```

--------------------------------

### Run non-interactive setup

Source: https://docs.openclaw.ai/providers/huggingface

Configures the provider and default model automatically without user prompts.

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice huggingface-api-key \
  --huggingface-api-key "$HF_TOKEN"
```

--------------------------------

### Install OpenClaw without onboarding

Source: https://docs.openclaw.ai/install

Run the installer script while skipping the interactive onboarding process.

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard
```

```powershell
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard
```

--------------------------------

### Onboard with API Key

Source: https://docs.openclaw.ai/providers/minimax

Run the onboarding command to configure the Anthropic-compatible API. Select the appropriate endpoint for your region.

```bash
openclaw onboard --auth-choice minimax-global-api
```

```bash
openclaw onboard --auth-choice minimax-cn-api
```

--------------------------------

### Start Codex App-Server Locally

Source: https://docs.openclaw.ai/plugins/codex-harness

Use this command to start the Codex app-server locally with standard input/output communication.

```bash
codex app-server --listen stdio://

```

--------------------------------

### Start inferrs Server

Source: https://docs.openclaw.ai/providers/inferrs

Use this command to start the inferrs server with a specified model, host, port, and device.

```bash
inferrs serve google/gemma-4-E2B-it \
  --host 127.0.0.1 \
  --port 8080 \
  --device metal
```

--------------------------------

### Verify Go Models

Source: https://docs.openclaw.ai/providers/opencode

List available models from the OpenCode-go provider to verify successful setup.

```bash
openclaw models list --provider opencode-go
```

--------------------------------

### Install Voice Call Plugin from Local Folder

Source: https://docs.openclaw.ai/plugins/voice-call

Install the Voice Call plugin from a local directory for development purposes. This avoids copying files and allows direct modification. Remember to restart the Gateway after installation.

```bash
PLUGIN_SRC=./path/to/local/voice-call-plugin
openclaw plugins install "$PLUGIN_SRC"
cd "$PLUGIN_SRC" && pnpm install
```

--------------------------------

### Setup DNS Server for Gateway

Source: https://docs.openclaw.ai/gateway/bonjour

Initialize the DNS server configuration on the gateway host.

```bash
openclaw dns setup --apply
```

--------------------------------

### Install OpenClaw CLI only on Windows

Source: https://docs.openclaw.ai/platforms/windows

Installs the OpenClaw CLI without the gateway service. Use `--skip-health` if you do not need to check gateway health during installation.

```powershell
openclaw onboard --non-interactive --skip-health
```

```powershell
openclaw gateway run
```

--------------------------------

### Launch the configuration wizard

Source: https://docs.openclaw.ai/providers/minimax

Use the interactive CLI wizard to configure MiniMax authentication and model settings without manual JSON editing.

```bash
openclaw configure
```

--------------------------------

### Update System and Install Dependencies

Source: https://docs.openclaw.ai/install/raspberry-pi

Updates the package list and installs essential tools for the gateway.

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl build-essential

# Set timezone (important for cron and reminders)
sudo timedatectl set-timezone America/Chicago
```

--------------------------------

### Run onboarding

Source: https://docs.openclaw.ai/providers/together

Executes the interactive onboarding process to configure the Together API key.

```bash
openclaw onboard --auth-choice together-api-key
```

--------------------------------

### List Installed Skills in ClawHub CLI

Source: https://docs.openclaw.ai/tools/clawhub

List all installed skills by reading the `.clawhub/lock.json` file.

```bash
clawhub list
```

--------------------------------

### Install from ClawHub

Source: https://docs.openclaw.ai/cli/plugins

Installs a plugin directly from ClawHub, optionally specifying a version. This is the preferred method for ClawHub packages.

```bash
openclaw plugins install clawhub:openclaw-codex-app-server
openclaw plugins install clawhub:openclaw-codex-app-server@1.2.3
```

--------------------------------

### Install Context Engine Plugin

Source: https://docs.openclaw.ai/concepts/context-engine

Commands to install a context engine plugin from npm or a local development path.

```bash
# Install from npm
openclaw plugins install @martian-engineering/lossless-claw

# Or install from a local path (for development)
openclaw plugins install -l ./my-context-engine
```

--------------------------------

### Install Nostr Plugin

Source: https://docs.openclaw.ai/channels/nostr

Commands to install the Nostr plugin from the registry or a local development path.

```bash
openclaw plugins install @openclaw/nostr
```

```bash
openclaw plugins install --link <path-to-local-nostr-plugin>
```

--------------------------------

### Install ClawDock Helpers

Source: https://docs.openclaw.ai/install/clawdock

Downloads the helper script and adds it to the shell configuration file.

```bash
mkdir -p ~/.clawdock && curl -sL https://raw.githubusercontent.com/openclaw/openclaw/main/scripts/clawdock/clawdock-helpers.sh -o ~/.clawdock/clawdock-helpers.sh
echo 'source ~/.clawdock/clawdock-helpers.sh' >> ~/.zshrc && source ~/.zshrc
```

--------------------------------

### Verify OpenClaw Installation

Source: https://docs.openclaw.ai/install

Run these commands to confirm the OpenClaw CLI is installed and the gateway is running.

```bash
openclaw --version      # confirm the CLI is available
openclaw doctor         # check for config issues
openclaw gateway status # verify the Gateway is running
```

--------------------------------

### Install WeChat Plugin

Source: https://docs.openclaw.ai/channels/wechat

Commands to install the WeChat plugin via CLI or manual configuration.

```bash
npx -y @tencent-weixin/openclaw-weixin-cli install
```

```bash
openclaw plugins install "@tencent-weixin/openclaw-weixin"
openclaw config set plugins.entries.openclaw-weixin.enabled true
```

--------------------------------

### Minimal remote setup configuration

Source: https://docs.openclaw.ai/gateway/openshell

Configures a basic remote OpenShell sandbox environment.

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "all",
        backend: "openshell",
      },
    },
  },
  plugins: {
    entries: {
      openshell: {
        enabled: true,
        config: {
          from: "openclaw",
          mode: "remote",
        },
      },
    },
  },
}
```

--------------------------------

### Start a Voice Call (Alias) via CLI

Source: https://docs.openclaw.ai/plugins/voice-call

The `start` command is an alias for `call` to initiate a voice call.

```bash
openclaw voicecall start --to "+15555550123"   # alias for call
```

--------------------------------

### Initialize NVIDIA API Authentication

Source: https://docs.openclaw.ai/providers/nvidia

Sets the required environment variable and runs the onboarding process.

```bash
export NVIDIA_API_KEY="nvapi-..."
openclaw onboard --auth-choice skip
```

--------------------------------

### Start OpenCLAW Gateway

Source: https://docs.openclaw.ai/platforms/ios

Use this command to start the OpenCLAW Gateway. Ensure the port is accessible.

```bash
openclaw gateway --port 18789
```

--------------------------------

### Run Control UI Development Server

Source: https://docs.openclaw.ai/web/control-ui

Starts the local development server for the Control UI.

```bash
pnpm ui:dev
```

--------------------------------

### Run Onboarding for Z.AI

Source: https://docs.openclaw.ai/providers/zai

Initializes the OpenClaw environment with Z.AI authentication.

```bash
openclaw onboard --auth-choice zai-api-key
```

--------------------------------

### Verify Zen Models

Source: https://docs.openclaw.ai/providers/opencode

List available models from the OpenCode provider to verify successful setup.

```bash
openclaw models list --provider opencode
```

--------------------------------

### Setup Virtual Network and Subnets

Source: https://docs.openclaw.ai/install/azure

Creates the VNet, attaches the NSG to the VM subnet, and provisions the required AzureBastionSubnet.

```bash
az network vnet create \
  -g "${RG}" -n "${VNET_NAME}" -l "${LOCATION}" \
  --address-prefixes "${VNET_PREFIX}" \
  --subnet-name "${VM_SUBNET_NAME}" \
  --subnet-prefixes "${VM_SUBNET_PREFIX}"

# Attach the NSG to the VM subnet
az network vnet subnet update \
  -g "${RG}" --vnet-name "${VNET_NAME}" \
  -n "${VM_SUBNET_NAME}" --nsg "${NSG_NAME}"

# AzureBastionSubnet — name is required by Azure
az network vnet subnet create \
  -g "${RG}" --vnet-name "${VNET_NAME}" \
  -n AzureBastionSubnet \
  --address-prefixes "${BASTION_SUBNET_PREFIX}"
```

--------------------------------

### Create Fly.io App and Volume

Source: https://docs.openclaw.ai/install/fly

Initialize the application and provision persistent storage on Fly.io.

```bash
# Clone the repo
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# Create a new Fly app (pick your own name)
fly apps create my-openclaw

# Create a persistent volume (1GB is usually enough)
fly volumes create openclaw_data --size 1 --region iad
```

--------------------------------

### Install OpenClaw (Custom Git Directory PowerShell)

Source: https://docs.openclaw.ai/install/installer

Installs OpenClaw from Git into a specified custom directory. This allows for managing multiple OpenClaw installations or custom build locations.

```powershell
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -InstallMethod git -GitDir "C:\openclaw"
```

--------------------------------

### ACP Harness Spawn Examples

Source: https://docs.openclaw.ai/tools/acp-agents

Basic commands to initiate specific ACP harness adapters.

```text
/acp spawn codex
```

```text
/acp spawn claude
```

--------------------------------

### Install OpenClaw via shell script

Source: https://docs.openclaw.ai/install/installer

Execute the installation script with various configuration flags to customize the deployment process.

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
```

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --no-onboard
```

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --install-method git
```

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --version main
```

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --dry-run
```

--------------------------------

### Gmail PubSub Integration Wizard Setup

Source: https://docs.openclaw.ai/automation/cron-jobs

Initiates the setup for Gmail PubSub integration using a CLI command. This configures hooks, enables the Gmail preset, and sets up a Tailscale Funnel endpoint.

```bash
openclaw webhooks gmail setup --account openclaw@gmail.com
```

--------------------------------

### Explain Sandbox Configuration

Source: https://docs.openclaw.ai/cli/sandbox

Inspect effective sandbox settings, tool policies, and elevated gates.

```bash
openclaw sandbox explain
openclaw sandbox explain --session agent:main:main
openclaw sandbox explain --agent work
openclaw sandbox explain --json
```

--------------------------------

### Install OpenClaw Plugin with Link

Source: https://docs.openclaw.ai/cli/plugins

Install a local plugin by linking to its directory instead of copying. This adds the path to `plugins.load.paths` and avoids copying files.

```bash
openclaw plugins install -l ./my-plugin
```

--------------------------------

### Define Skill Metadata and Instructions

Source: https://docs.openclaw.ai/tools/creating-skills

Create the SKILL.md file to define your skill's name, description, and provide instructions for the agent. This example uses YAML frontmatter and markdown.

```markdown
---
name: hello_world
description: A simple skill that says hello.
---

# Hello World Skill

When the user asks for a greeting, use the `echo` tool to say
"Hello from your custom skill!".

```

--------------------------------

### Define a setup plugin entry

Source: https://docs.openclaw.ai/plugins/sdk-setup

Use this pattern in setup-entry.ts to register a channel plugin for setup flows without triggering full runtime initialization.

```typescript
// setup-entry.ts
import { defineSetupPluginEntry } from "openclaw/plugin-sdk/channel-core";
import { myChannelPlugin } from "./src/channel.js";

export default defineSetupPluginEntry(myChannelPlugin);
```

--------------------------------

### Start OpenClaw Gateway

Source: https://docs.openclaw.ai/channels/imessage

Command to start the OpenClaw gateway service. This command should be run after configuring the gateway.

```bash
openclaw gateway
```

--------------------------------

### Uninstall command usage examples

Source: https://docs.openclaw.ai/cli/uninstall

Demonstrates various ways to invoke the uninstall command, including flags for specific components and non-interactive modes.

```bash
openclaw backup create
openclaw uninstall
openclaw uninstall --service --yes --non-interactive
openclaw uninstall --state --workspace --yes --non-interactive
openclaw uninstall --all --yes
openclaw uninstall --dry-run
```

--------------------------------

### Install Hook Packs

Source: https://docs.openclaw.ai/cli/hooks

Use the unified plugins installer to add hook packs from npm, local paths, or archives.

```bash
openclaw plugins install <package>        # ClawHub first, then npm
openclaw plugins install <package> --pin  # pin version
openclaw plugins install <path>           # local path
```

```bash
# Local directory
openclaw plugins install ./my-hook-pack

# Local archive
openclaw plugins install ./my-hook-pack.zip

# NPM package
openclaw plugins install @openclaw/my-hook-pack

# Link a local directory without copying
openclaw plugins install -l ./my-hook-pack
```

--------------------------------

### Install Node.js LTS with winget (Windows)

Source: https://docs.openclaw.ai/install/node

Install the Node.js LTS version on Windows using the winget package manager.

```powershell
winget install OpenJS.NodeJS.LTS
```

--------------------------------

### Onboard with Mistral API Key

Source: https://docs.openclaw.ai/providers/mistral

Use this command to onboard with Mistral, either interactively or by providing the API key directly.

```bash
openclaw onboard --auth-choice mistral-api-key
```

```bash
openclaw onboard --mistral-api-key "$MISTRAL_API_KEY"
```

--------------------------------

### Start Ollama Service

Source: https://docs.openclaw.ai/providers/ollama

Launch the Ollama server process to enable API access.

```bash
ollama serve
```

--------------------------------

### Install Gateway Service with Profiles

Source: https://docs.openclaw.ai/gateway/multiple-gateways

Install the gateway service for each profile to ensure they run independently. This command registers the gateway as a service for its respective profile.

```bash
openclaw --profile main gateway install
openclaw --profile rescue gateway install
```

--------------------------------

### Install OpenClaw Beta or Git Version

Source: https://docs.openclaw.ai/help/faq

Use these commands on macOS or Linux to install specific release channels via the shell script.

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --beta
```

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --install-method git
```

--------------------------------

### Install and Use Node.js with fnm

Source: https://docs.openclaw.ai/install/node

Manage Node.js versions using fnm. Install a specific version and set it as the current version.

```bash
fnm install 24
fnm use 24
```

--------------------------------

### Install Zalo Personal Plugin from Local Folder (Development)

Source: https://docs.openclaw.ai/plugins/zalouser

Install the Zalo Personal plugin from a local folder for development purposes. Ensure you restart the Gateway afterwards.

```bash
PLUGIN_SRC=./path/to/local/zalouser-plugin
openclaw plugins install "$PLUGIN_SRC"
cd "$PLUGIN_SRC" && pnpm install
```

--------------------------------

### Slack Slash Command Example

Source: https://docs.openclaw.ai/channels/slack

Example of a basic Slack slash command configuration. The command name is set to 'openclaw'.

```text
/openclaw /help
```

--------------------------------

### Interactive Configuration Commands

Source: https://docs.openclaw.ai/configuration

Commands to launch the onboarding flow or the configuration wizard.

```bash
openclaw onboard       # full onboarding flow
openclaw configure     # config wizard
```

--------------------------------

### Example: Lobster Workflow Step

Source: https://docs.openclaw.ai/tools/llm-task

An example demonstrating how to use the `llm-task` tool within a Lobster workflow to process an email and generate an intent and draft.

```APIDOC
## Example: Lobster workflow step

This example shows how to invoke the `llm-task` tool in a Lobster workflow:

```lobster
openclaw.invoke --tool llm-task --action json --args-json '{ 
  "prompt": "Given the input email, return intent and draft.",
  "thinking": "low",
  "input": {
    "subject": "Hello",
    "body": "Can you help?"
  },
  "schema": {
    "type": "object",
    "properties": {
      "intent": { "type": "string" },
      "draft": { "type": "string" }
    },
    "required": ["intent", "draft"],
    "additionalProperties": false
  }
}'
```
```

--------------------------------

### Execute x_search queries

Source: https://docs.openclaw.ai/tools/web

Examples for performing keyword searches with filters and targeted lookups for specific posts.

```javascript
await x_search({
  query: "dinner recipes",
  allowed_x_handles: ["nytfood"],
  from_date: "2026-03-01",
});
```

```javascript
// Per-post stats: use the exact status URL or status ID when possible
await x_search({
  query: "https://x.com/huntharo/status/1905678901234567890",
});
```

--------------------------------

### Configure channel settings

Source: https://docs.openclaw.ai/plugins/sdk-setup

Example of defining channel-specific configuration settings.

```json5
{
  channels: {
    "my-channel": {
      token: "bot-token",
      allowFrom: ["user1", "user2"],
    },
  },
}
```

--------------------------------

### Install OpenClaw

Source: https://docs.openclaw.ai/install/oracle

Installs OpenClaw and sources the bashrc to make commands available. Select 'Do this later' when prompted to hatch a bot.

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
source ~/.bashrc
```

--------------------------------

### install-cli.sh

Source: https://docs.openclaw.ai/install/installer

Information about the install-cli.sh script, designed for local prefix installations without system Node dependencies.

```APIDOC
## install-cli.sh

### Description
This script is designed for environments where you want all Openclaw AI components installed under a local prefix (defaulting to `~/.openclaw`) and do not want a system-wide Node.js dependency. It supports both npm installations and git-checkout installations within the same prefix flow.

### Usage
(Refer to the general installation examples above for usage patterns, as install-cli.sh is typically invoked via the main install script with specific flags or environment variables.)

### Key Features
- Installs under a local prefix (default `~/.openclaw`).
- No system Node dependency required.
- Supports npm and git-checkout installation methods.

### Response
(Output of the bash script execution)
```

--------------------------------

### Install and Configure Ollama

Source: https://docs.openclaw.ai/concepts/model-providers

Commands and configuration for setting up Ollama models locally.

```bash
# Install Ollama, then pull a model:
ollama pull llama3.3
```

```json5
{
  agents: {
    defaults: { model: { primary: "ollama/llama3.3" } },
  },
}
```

--------------------------------

### Install Dependencies with Bun

Source: https://docs.openclaw.ai/install/bun

Installs project dependencies using Bun. `bun.lock` files are gitignored. Use `--no-save` to skip lockfile writes.

```sh
bun install
```

```sh
bun install --no-save
```

--------------------------------

### Install Playwright browsers in container

Source: https://docs.openclaw.ai/install/docker

Installs Chromium browser binaries within the running container environment.

```bash
docker compose run --rm openclaw-cli \
  node /app/node_modules/playwright-core/cli.js install chromium
```

--------------------------------

### Non-interactive Setup (OpenRouter)

Source: https://docs.openclaw.ai/providers/arcee

Perform a non-interactive onboarding for Arcee AI via OpenRouter. Requires setting the OPENROUTER_API_KEY environment variable.

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice arceeai-openrouter \
  --openrouter-api-key "$OPENROUTER_API_KEY"
```

--------------------------------

### Install via local prefix

Source: https://docs.openclaw.ai/install

Keep OpenClaw and Node isolated under a local directory without affecting system-wide installations.

```bash
curl -fsSL https://openclaw.ai/install-cli.sh | bash
```

--------------------------------

### Install Zalo Personal Plugin

Source: https://docs.openclaw.ai/channels/zalouser

Commands to install the Zalo Personal plugin via CLI or from a local source checkout.

```bash
openclaw plugins install @openclaw/zalouser
```

```bash
openclaw plugins install ./path/to/local/zalouser-plugin
```

--------------------------------

### Troubleshoot Service Startup

Source: https://docs.openclaw.ai/install/ansible

Commands to inspect logs, verify file permissions, and test the gateway service manually.

```bash
# Check logs
sudo journalctl -u openclaw -n 100

# Verify permissions
sudo ls -la /opt/openclaw

# Test manual start
sudo -i -u openclaw
cd ~/openclaw
openclaw gateway run
```

--------------------------------

### Install OpenClaw and Onboard

Source: https://docs.openclaw.ai/install/macos-vm

Installs the latest version of OpenClaw globally within the macOS VM and initiates the onboarding process to configure model providers.

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

--------------------------------

### Configure default and alias models

Source: https://docs.openclaw.ai/help/faq

Example configuration for setting a default model and defining aliases for session switching.

```json5
{
  env: { MINIMAX_API_KEY: "sk-...", OPENAI_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "minimax/MiniMax-M2.7" },
      models: {
        "minimax/MiniMax-M2.7": { alias: "minimax" },
        "openai/gpt-5.4": { alias: "gpt" },
      },
    },
  },
}
```

--------------------------------

### Install OpenClaw (install.sh)

Source: https://docs.openclaw.ai/install/installer

Installs OpenClaw using the install.sh script. This command downloads and executes the script to set up OpenClaw on macOS, Linux, or WSL.

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
```

--------------------------------

### Initialize OpenClaw Gateway

Source: https://docs.openclaw.ai/install/clawdock

Standard sequence for starting the gateway, configuring the token, and accessing the dashboard.

```bash
clawdock-start
clawdock-fix-token
clawdock-dashboard
```

--------------------------------

### Gateway Discovery Options and Output

Source: https://docs.openclaw.ai/cli/gateway

Examples for configuring discovery timeouts and parsing machine-readable JSON output.

```bash
openclaw gateway discover --timeout 4000
openclaw gateway discover --json | jq '.beacons[].wsUrl'
```

--------------------------------

### MCP Client Configuration Example

Source: https://docs.openclaw.ai/cli/mcp

Example stdio client configuration for the OpenClaw MCP bridge. This JSON defines how to connect to the Gateway server.

```json
{
  "mcpServers": {
    "openclaw": {
      "command": "openclaw",
      "args": [
        "mcp",
        "serve",
        "--url",
        "wss://gateway-host:18789",
        "--token-file",
        "/path/to/gateway.token"
      ]
    }
  }
}
```

--------------------------------

### Install Ansible Collections

Source: https://docs.openclaw.ai/install/ansible

Installs required Ansible collections defined in the requirements file.

```bash
ansible-galaxy collection install -r requirements.yml
```

--------------------------------

### Create and Connect to VM

Source: https://docs.openclaw.ai/install/exe-dev

Commands to provision a new VM and establish an SSH connection.

```bash
ssh exe.dev new
```

```bash
ssh <vm-name>.exe.xyz
```

--------------------------------

### Start OpenClaw Gateway Container

Source: https://docs.openclaw.ai/install/podman

Use this script to launch the OpenClaw Gateway container. It starts the container as your current uid/gid with `--userns=keep-id` and bind-mounts your OpenClaw state into the container.

```bash
./scripts/run-openclaw-podman.sh launch
```

--------------------------------

### Onboard Qwen Standard Plan

Source: https://docs.openclaw.ai/providers/qwen

Commands to initialize authentication for the Qwen Standard pay-as-you-go plan.

```bash
openclaw onboard --auth-choice qwen-standard-api-key
```

```bash
openclaw onboard --auth-choice qwen-standard-api-key-cn
```

--------------------------------

### Install Mattermost Plugin from Local Checkout

Source: https://docs.openclaw.ai/channels/mattermost

Install the Mattermost plugin from a local git repository checkout. Ensure the path points to the plugin's directory.

```bash
openclaw plugins install ./path/to/local/mattermost-plugin
```

--------------------------------

### Install Twitch Plugin from Local Checkout

Source: https://docs.openclaw.ai/channels/twitch

Install the Twitch plugin by providing a local path to the plugin's directory, useful when running from a git repository.

```bash
openclaw plugins install ./path/to/local/twitch-plugin
```

--------------------------------

### Perform Non-interactive Onboarding

Source: https://docs.openclaw.ai/providers/opencode-go

Configures the provider by passing the API key directly via environment variable.

```bash
openclaw onboard --opencode-go-api-key "$OPENCODE_API_KEY"
```

--------------------------------

### Set Setup Channel Enabled

Source: https://docs.openclaw.ai/plugins/sdk-migration

Use `setSetupChannelEnabled` to enable or disable channel setup.

```typescript
setSetupChannelEnabled
```

--------------------------------

### Install Node.js with Homebrew (macOS)

Source: https://docs.openclaw.ai/install/node

Use Homebrew to install Node.js on macOS. This is the recommended method for macOS users.

```bash
brew install node
```

--------------------------------

### CLI Command: onboard

Source: https://docs.openclaw.ai/cli

Interactive onboarding for gateway, workspace, and skills.

```APIDOC
## CLI Command: onboard

### Description
Interactive onboarding for gateway, workspace, and skills.

### Parameters
#### Options
- **--workspace** (dir) - Optional - Path to workspace directory
- **--reset** (boolean) - Optional - Reset config, credentials, and sessions before onboarding
- **--reset-scope** (string) - Optional - Scope of reset (config|config+creds+sessions|full)
- **--non-interactive** (boolean) - Optional - Run without interactive prompts
- **--mode** (string) - Optional - Mode of operation (local|remote)
- **--flow** (string) - Optional - Onboarding flow (quickstart|advanced|manual)
- **--auth-choice** (string) - Optional - Authentication provider choice
- **--secret-input-mode** (string) - Optional - Mode for secret input (plaintext|ref)
- **--gateway-port** (number) - Optional - Port for the gateway
- **--gateway-bind** (string) - Optional - Gateway bind interface (loopback|lan|tailnet|auto|custom)
- **--gateway-auth** (string) - Optional - Gateway authentication method (token|password)
- **--gateway-token** (string) - Optional - Gateway authentication token
- **--gateway-password** (string) - Optional - Gateway authentication password
- **--remote-url** (string) - Optional - Remote URL for connection
- **--remote-token** (string) - Optional - Remote token for connection
- **--tailscale** (string) - Optional - Tailscale configuration (off|serve|funnel)
- **--install-daemon** (boolean) - Optional - Install the daemon
- **--daemon-runtime** (string) - Optional - Runtime for the daemon (node|bun)
- **--node-manager** (string) - Optional - Node manager for skills (npm|pnpm|bun)
- **--json** (boolean) - Optional - Output in JSON format
```

--------------------------------

### Install OpenClaw from Git Checkout

Source: https://docs.openclaw.ai/help/faq

Installs OpenClaw directly from a git repository, allowing the AI agent to access the source code and documentation for better context. This method is recommended for local AI agent interaction. To revert to a stable version, re-run the installer without the --install-method git flag.

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git
```

--------------------------------

### Install Google Chrome on Linux

Source: https://docs.openclaw.ai/tools/browser-linux-troubleshooting

Commands to install the official Google Chrome .deb package to avoid snap confinement issues.

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install -y  # if there are dependency errors
```

--------------------------------

### Markdown Input Example

Source: https://docs.openclaw.ai/concepts/markdown-formatting

Example of raw Markdown input used for IR conversion.

```markdown
Hello **world** — see [docs](https://docs.openclaw.ai).
```

--------------------------------

### dns setup

Source: https://docs.openclaw.ai/cli/index

Configures wide-area discovery DNS helpers using CoreDNS and Tailscale.

```APIDOC
## dns setup

### Description
Installs or updates CoreDNS configuration for wide-area discovery.

### Parameters
#### Query Parameters
- **--domain** (string) - Optional - The domain to configure.
- **--apply** (boolean) - Optional - Install/update CoreDNS config (requires sudo; macOS only).
```

--------------------------------

### Manual Docker deployment

Source: https://docs.openclaw.ai/install/docker

Performs the build, onboarding, configuration, and startup steps manually without the setup script.

```bash
docker build -t openclaw:local -f Dockerfile .
docker compose run --rm --no-deps --entrypoint node openclaw-gateway \
  dist/index.js onboard --mode local --no-install-daemon
docker compose run --rm --no-deps --entrypoint node openclaw-gateway \
  dist/index.js config set --batch-json '[{"path":"gateway.mode","value":"local"},{"path":"gateway.bind","value":"lan"},{"path":"gateway.controlUi.allowedOrigins","value":["http://localhost:18789","http://127.0.0.1:18789"]}]'
docker compose up -d openclaw-gateway
```

--------------------------------

### Install OpenClaw with Ansible Quick-Start Script

Source: https://docs.openclaw.ai/install/ansible

Execute this command to automatically install OpenClaw and its dependencies using the official Ansible playbook. Ensure you have internet access for package downloads.

```bash
curl -fsSL https://raw.githubusercontent.com/openclaw/openclaw-ansible/main/install.sh | bash
```

--------------------------------

### Install Hook Packs via CLI

Source: https://docs.openclaw.ai/automation/hooks

Use this command to install hook packs distributed as npm packages.

```bash
openclaw plugins install <path-or-spec>
```

--------------------------------

### Install Nextcloud Talk Plugin from Local Checkout

Source: https://docs.openclaw.ai/channels/nextcloud-talk

Install the Nextcloud Talk plugin by providing a local path to the plugin's directory. This is useful when working with a git checkout of the plugin.

```bash
openclaw plugins install ./path/to/local/nextcloud-talk-plugin
```

--------------------------------

### Install OpenClaw with Options (install.ps1)

Source: https://docs.openclaw.ai/install/installer

Installs OpenClaw using the install.ps1 script with specific options like beta tag, no onboarding, and dry run. This is useful for testing or specific deployment scenarios.

```powershell
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -Tag beta -NoOnboard -DryRun
```

--------------------------------

### Automate onboarding with environment-backed references

Source: https://docs.openclaw.ai/start/wizard-cli-automation

Use this command to store references in auth profiles instead of plaintext. Provider environment variables must be present in the process environment.

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice openai-api-key \
  --secret-input-mode ref \
  --accept-risk
```

--------------------------------

### Install OpenClaw (Git Method PowerShell)

Source: https://docs.openclaw.ai/install/installer

Installs OpenClaw by cloning the Git repository. If Git is missing, the script will exit with a link to Git for Windows.

```powershell
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -InstallMethod git
```

--------------------------------

### Install Local acpx Plugin

Source: https://docs.openclaw.ai/tools/acp-agents

Install a local development version of the acpx plugin by providing the path to its directory. This is useful for development and testing.

```bash
openclaw plugins install ./path/to/local/acpx-plugin
```

--------------------------------

### Define a bundled channel setup entry

Source: https://docs.openclaw.ai/plugins/sdk-entrypoints

Use this contract when setup flows require a lightweight runtime setter before the full channel entry loads.

```typescript
import { defineBundledChannelSetupEntry } from "openclaw/plugin-sdk/channel-entry-contract";

export default defineBundledChannelSetupEntry({
  importMetaUrl: import.meta.url,
  plugin: {
    specifier: "./channel-plugin-api.js",
    exportName: "myChannelPlugin",
  },
  runtime: {
    specifier: "./runtime-api.js",
    exportName: "setMyChannelRuntime",
  },
});
```

--------------------------------

### Install Node.js LTS with Chocolatey (Windows)

Source: https://docs.openclaw.ai/install/node

Install the Node.js LTS version on Windows using the Chocolatey package manager.

```powershell
choco install nodejs-lts
```

--------------------------------

### Install OpenClaw Plugin

Source: https://docs.openclaw.ai/plugins/community

Use this command to install any community plugin from ClawHub or npm. Replace `<package-name>` with the actual plugin package name.

```bash
openclaw plugins install <package-name>
```

--------------------------------

### Onboard Volcengine API Key

Source: https://docs.openclaw.ai/providers/volcengine

Run interactive onboarding to register both general and coding providers using a single API key.

```bash
openclaw onboard --auth-choice volcengine-api-key
```

--------------------------------

### Access Control UI via Tailscale Serve

Source: https://docs.openclaw.ai/install/digitalocean

Installs Tailscale and configures the gateway to serve the UI over the tailnet.

```bash
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up
openclaw config set gateway.tailscale.mode serve
openclaw gateway restart
```

--------------------------------

### Deploy and Verify Application

Source: https://docs.openclaw.ai/install/fly

Execute the deployment and check the status of the running application.

```bash
fly deploy
```

```bash
fly status
fly logs
```

--------------------------------

### Start OpenClaw Gateway (Basic)

Source: https://docs.openclaw.ai/platforms/android

Launches the OpenClaw Gateway on a specified port with verbose logging enabled. Ensure this command is run on the machine designated as the Gateway host.

```bash
openclaw gateway --port 18789 --verbose
```

--------------------------------

### Troubleshoot sharp build errors

Source: https://docs.openclaw.ai/install

Bypass globally installed libvips dependencies during npm installation.

```bash
SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install -g openclaw@latest
```

--------------------------------

### Setup DNS Configuration

Source: https://docs.openclaw.ai/cli/index

Helper for wide-area discovery DNS configuration using CoreDNS and Tailscale. Without --apply, it prints the recommended config.

```bash
openclaw dns setup [--domain <domain>] [--apply]
```

--------------------------------

### Onboard Z.AI API Key

Source: https://docs.openclaw.ai/start/wizard-cli-automation

Use this command to onboard with a Z.AI API key. Ensure the ZAI_API_KEY environment variable is set.

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice zai-api-key \
  --zai-api-key "$ZAI_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

--------------------------------

### Install Binaries in Dockerfile

Source: https://docs.openclaw.ai/install/docker-vm-runtime

Use this pattern to install required binaries like CLIs into your Docker image during the build process. Ensure you use the correct architecture-specific download URLs.

```dockerfile
FROM node:24-bookworm

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

# Example binary 1: Gmail CLI
RUN curl -L https://github.com/steipete/gog/releases/latest/download/gog_Linux_x86_64.tar.gz 
  | tar -xz -C /usr/local/bin && chmod +x /usr/local/bin/gog

# Example binary 2: Google Places CLI
RUN curl -L https://github.com/steipete/goplaces/releases/latest/download/goplaces_Linux_x86_64.tar.gz 
  | tar -xz -C /usr/local/bin && chmod +x /usr/local/bin/goplaces

# Example binary 3: WhatsApp CLI
RUN curl -L https://github.com/steipete/wacli/releases/latest/download/wacli_Linux_x86_64.tar.gz 
  | tar -xz -C /usr/local/bin && chmod +x /usr/local/bin/wacli

# Add more binaries below using the same pattern

WORKDIR /app
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml .npmrc ./
COPY ui/package.json ./ui/package.json
COPY scripts ./scripts

RUN corepack enable
RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm build
RUN pnpm ui:install
RUN pnpm ui:build

ENV NODE_ENV=production

CMD ["node","dist/index.js"]
```

--------------------------------

### Install Zalo Plugin via CLI

Source: https://docs.openclaw.ai/channels/zalo

Use this command to install the Zalo plugin if it's not bundled with your OpenClaw release.

```bash
openclaw plugins install @openclaw/zalo
```

--------------------------------

### Run OpenClaw Development Loop

Source: https://docs.openclaw.ai/platforms/windows

Starts the development environment for OpenClaw.

```bash
pnpm install
# First run only (or after resetting local OpenClaw config/workspace)
pnpm openclaw setup
pnpm gateway:watch
```

--------------------------------

### Verify Lume Installation

Source: https://docs.openclaw.ai/install/macos-vm

Checks if the Lume command-line tool is installed and accessible by printing its version.

```bash
lume --version
```

--------------------------------

### Install OpenClaw (GitHub Main via npm PowerShell)

Source: https://docs.openclaw.ai/install/installer

Installs OpenClaw from the 'main' branch on GitHub using npm. This is useful for testing the latest development version.

```powershell
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -Tag main
```

--------------------------------

### Run OpenClaw Onboarding with pnpm

Source: https://docs.openclaw.ai/help/faq

Executes the OpenClaw onboarding process using pnpm, useful if you do not have a global installation of OpenClaw.

```bash
pnpm openclaw onboard
```

--------------------------------

### Configure deferred channel loading

Source: https://docs.openclaw.ai/plugins/architecture

Advanced configuration to defer full plugin loading until after the gateway starts listening, using the setupEntry for essential startup capabilities.

```json
{
  "name": "@scope/my-channel",
  "openclaw": {
    "extensions": ["./index.ts"],
    "setupEntry": "./setup-entry.ts",
    "startup": {
      "deferConfiguredChannelFullLoadUntilAfterListen": true
    }
  }
}
```

--------------------------------

### Start and Control OpenClaw Browser

Source: https://docs.openclaw.ai/tools/browser

Use these commands to manage the status, start, and open URLs in the OpenClaw browser profile. Ensure the Gateway is running and the browser is enabled.

```bash
openclaw browser --browser-profile openclaw status
openclaw browser --browser-profile openclaw start
openclaw browser --browser-profile openclaw open https://example.com
openclaw browser --browser-profile openclaw snapshot
```

--------------------------------

### Setup Quadlet for Podman

Source: https://docs.openclaw.ai/install/podman

Run this script to set up Quadlet for Podman. Quadlet is a Linux-only option that depends on systemd user services.

```bash
./scripts/podman/setup.sh --quadlet
```

--------------------------------

### Install LINE Plugin from Local Checkout

Source: https://docs.openclaw.ai/channels/line

Install the LINE plugin from a local Git repository checkout using the OpenClaw CLI. Specify the path to the local plugin directory.

```bash
openclaw plugins install ./path/to/local/line-plugin
```

--------------------------------

### Agent Startup and Context Limits

Source: https://docs.openclaw.ai/gateway/configuration-reference

Configuration for startup context preludes and runtime context budget limits.

```APIDOC
## Agent Startup and Context Limits

### Description
Configures the startup prelude for new sessions and sets limits for runtime context surfaces like memory and tool results.

### Request Body
- **agents.defaults.startupContext** (object) - Optional - Settings for startup prelude on /new and /reset.
  - **enabled** (boolean) - Whether startup context is enabled.
  - **applyOn** (array) - Events to trigger startup context.
  - **dailyMemoryDays** (integer) - Days of memory to include.
  - **maxFileBytes** (integer) - Max bytes per file.
  - **maxFileChars** (integer) - Max characters per file.
  - **maxTotalChars** (integer) - Max total characters.
- **agents.defaults.contextLimits** (object) - Optional - Shared limits for runtime context.
  - **memoryGetMaxChars** (integer) - Cap for memory_get excerpts.
  - **memoryGetDefaultLines** (integer) - Default line window for memory_get.
  - **toolResultMaxChars** (integer) - Cap for live tool results.
  - **postCompactionMaxChars** (integer) - Cap for AGENTS.md excerpts during compaction.
```

--------------------------------

### Install Skills in ClawHub CLI

Source: https://docs.openclaw.ai/tools/clawhub

Install a skill by its slug. Use `--version` to specify a particular version and `--force` to overwrite existing files.

```bash
clawhub install <slug>
```

```bash
clawhub install <slug> --version <version>
```

```bash
clawhub install <slug> --force
```

--------------------------------

### Generate QR Code and Setup Code

Source: https://docs.openclaw.ai/cli/qr

Generates a mobile pairing QR code and setup code from the current Gateway configuration.

```APIDOC
## POST /qr

### Description
Generate a mobile pairing QR and setup code from your current Gateway configuration.

### Method
POST

### Endpoint
/qr

### Parameters
#### Query Parameters
- **setup-code-only** (boolean) - Optional - Print only setup code
- **json** (boolean) - Optional - Emit JSON (`setupCode`, `gatewayUrl`, `auth`, `urlSource`)
- **remote** (boolean) - Optional - Prefer `gateway.remote.url`; if it is unset, `gateway.tailscale.mode=serve|funnel` can still provide the remote public URL
- **url** (string) - Optional - Override gateway URL used in payload
- **public-url** (string) - Optional - Override public URL used in payload
- **token** (string) - Optional - Override which gateway token the bootstrap flow authenticates against
- **password** (string) - Optional - Override which gateway password the bootstrap flow authenticates against
- **no-ascii** (boolean) - Optional - Skip ASCII QR rendering

### Request Example
```bash
openclaw qr
openclaw qr --setup-code-only
openclaw qr --json
openclaw qr --remote
openclaw qr --url wss://gateway.example/ws
```

### Response
#### Success Response (200)
- **setupCode** (string) - The setup code for pairing.
- **gatewayUrl** (string) - The URL of the gateway.
- **auth** (object) - Authentication details.
- **urlSource** (string) - The source of the gateway URL.

#### Response Example
```json
{
  "setupCode": "123456",
  "gatewayUrl": "wss://gateway.openclaw.ai/ws",
  "auth": {
    "token": "<token>",
    "password": "<password>"
  },
  "urlSource": "config"
}
```
```

--------------------------------

### Onboard Go Catalog

Source: https://docs.openclaw.ai/providers/opencode

Run the onboarding process for the Go catalog. You can choose to authenticate interactively or provide the API key directly.

```bash
openclaw onboard --auth-choice opencode-go
```

```bash
openclaw onboard --opencode-go-api-key "$OPENCODE_API_KEY"
```

--------------------------------

### Start OpenClaw Managed Browser

Source: https://docs.openclaw.ai/tools/browser-linux-troubleshooting

Use this command to start OpenClaw's managed browser profile, which is recommended for consistent behavior. Alternatively, configure `browser.defaultProfile: "openclaw"` in your settings.

```bash
openclaw browser start --browser-profile openclaw
```

--------------------------------

### Flow Status Example

Source: https://docs.openclaw.ai/automation/taskflow

This example illustrates the state progression of a weekly report flow in managed mode, showing task creation and success.

```text
Flow: weekly-report
  Step 1: gather-data     → task created → succeeded
  Step 2: generate-report → task created → succeeded
  Step 3: deliver         → task created → running
```

--------------------------------

### Create and Configure GCP Project

Source: https://docs.openclaw.ai/install/gcp

Create a new GCP project and set it as the default. Billing must be enabled for Compute Engine usage.

```bash
gcloud projects create my-openclaw-project --name="OpenClaw Gateway"
gcloud config set project my-openclaw-project
```

```bash
gcloud services enable compute.googleapis.com
```

--------------------------------

### Start Local Relay with Docker

Source: https://docs.openclaw.ai/channels/nostr

Launch a local strfry relay instance for testing purposes.

```bash
# Start strfry
docker run -p 7777:7777 ghcr.io/hoytech/strfry
```

--------------------------------

### Manage Chat Channels via CLI

Source: https://docs.openclaw.ai/cli

Examples for adding, removing, and checking the status of chat channel accounts.

```bash
openclaw channels add --channel telegram --account alerts --name "Alerts Bot" --token $TELEGRAM_BOT_TOKEN
openclaw channels add --channel discord --account work --name "Work Bot" --token $DISCORD_BOT_TOKEN
openclaw channels remove --channel discord --account work --delete
openclaw channels status --probe
openclaw status --deep
```

--------------------------------

### NVIDIA Provider Configuration

Source: https://docs.openclaw.ai/providers/nvidia

Example configuration file defining the NVIDIA provider and default model settings.

```json5
{
  env: { NVIDIA_API_KEY: "nvapi-..." },
  models: {
    providers: {
      nvidia: {
        baseUrl: "https://integrate.api.nvidia.com/v1",
        api: "openai-completions",
      },
    },
  },
  agents: {
    defaults: {
      model: { primary: "nvidia/nvidia/nemotron-3-super-120b-a12b" },
    },
  },
}
```

--------------------------------

### Install ClawHub CLI using npm

Source: https://docs.openclaw.ai/tools/clawhub

Install the ClawHub CLI globally using npm. This is required for registry-authenticated workflows like publishing and syncing.

```bash
npm i -g clawhub
```

--------------------------------

### Non-interactive Onboarding

Source: https://docs.openclaw.ai/providers/cloudflare-ai-gateway

Configures gateway settings via command line arguments for CI or scripted environments.

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice cloudflare-ai-gateway-api-key \
  --cloudflare-ai-gateway-account-id "your-account-id" \
  --cloudflare-ai-gateway-gateway-id "your-gateway-id" \
  --cloudflare-ai-gateway-api-key "$CLOUDFLARE_AI_GATEWAY_API_KEY"
```

--------------------------------

### Install LINE Plugin with OpenClaw CLI

Source: https://docs.openclaw.ai/channels/line

Install the LINE plugin using the OpenClaw command-line interface. This command is used for packaged builds.

```bash
openclaw plugins install @openclaw/line
```

--------------------------------

### List installed plugins

Source: https://docs.openclaw.ai/tools/plugin

Displays all currently loaded plugins in the OpenClaw environment.

```bash
openclaw plugins list
```

--------------------------------

### OpenClaw Configuration Example

Source: https://docs.openclaw.ai/tools/acp-agents

A comprehensive OpenClaw configuration demonstrating agent runtime defaults, persistent ACP bindings for Discord and Telegram, and route bindings. This example shows how to set up ACP sessions for different channels and agents.

```json
{
  agents: {
    list: [
      {
        id: "codex",
        runtime: {
          type: "acp",
          acp: {
            agent: "codex",
            backend: "acpx",
            mode: "persistent",
            cwd: "/workspace/openclaw",
          },
        },
      },
      {
        id: "claude",
        runtime: {
          type: "acp",
          acp: { agent: "claude", backend: "acpx", mode: "persistent" },
        },
      },
    ],
  },
  bindings: [
    {
      type: "acp",
      agentId: "codex",
      match: {
        channel: "discord",
        accountId: "default",
        peer: { kind: "channel", id: "222222222222222222" },
      },
      acp: { label: "codex-main" },
    },
    {
      type: "acp",
      agentId: "claude",
      match: {
        channel: "telegram",
        accountId: "default",
        peer: { kind: "group", id: "-1001234567890:topic:42" },
      },
      acp: { cwd: "/workspace/repo-b" },
    },
    {
      type: "route",
      agentId: "main",
      match: { channel: "discord", accountId: "default" },
    },
    {
      type: "route",
      agentId: "main",
      match: { channel: "telegram", accountId: "default" },
    },
  ],
  channels: {
    discord: {
      guilds: {
        "111111111111111111": {
          channels: {
            "222222222222222222": { requireMention: false },
          },
        },
      },
    },
    telegram: {
      groups: {
        "-1001234567890": {
          topics: { "42": { requireMention: false } },
        },
      },
    },
  },
}
```

--------------------------------

### OpenClaw Configuration Example

Source: https://docs.openclaw.ai/

Example JSON configuration for OpenClaw. This configuration specifies rules for WhatsApp channel access, including allowed senders and mention requirements for group chats.

```json
{
  channels: {
    whatsapp: {
      allowFrom: ["+15555550123"],
      groups: { "*": { requireMention: true } },
    },
  },
  messages: { groupChat: { mentionPatterns: ["@openclaw"] } },
}

```

--------------------------------

### Onboard Gemini API Key

Source: https://docs.openclaw.ai/start/wizard-cli-automation

Use this command to onboard with a Gemini API key. Ensure the GEMINI_API_KEY environment variable is set.

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice gemini-api-key \
  --gemini-api-key "$GEMINI_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

--------------------------------

### Start Node Host in Foreground

Source: https://docs.openclaw.ai/nodes/index

Initiate a node host process on the node machine to connect to the Gateway. Specify the Gateway host and port, and provide a display name for the node.

```bash
openclaw node run --host <gateway-host> --port 18789 --display-name "Build Node"
```

--------------------------------

### Run OpenClaw Onboarding

Source: https://docs.openclaw.ai/concepts/models

Execute the onboarding command to set up model and authentication for common providers. This is recommended if you prefer not to manually edit configuration files.

```bash
openclaw onboard
```

--------------------------------

### Install Legacy Plugin

Source: https://docs.openclaw.ai/channels/wechat

Command to install the legacy version of the WeChat plugin for older OpenClaw versions.

```bash
openclaw plugins install @tencent-weixin/openclaw-weixin@legacy
```

--------------------------------

### Initialize and Authenticate gcloud CLI

Source: https://docs.openclaw.ai/install/gcp

Use these commands to initialize and log in to the Google Cloud SDK. Ensure you have the gcloud CLI installed.

```bash
gcloud init
gcloud auth login
```

--------------------------------

### Onboard with OpenRouter API Key

Source: https://docs.openclaw.ai/providers/openrouter

Run this command to onboard with OpenRouter using your API key. Ensure you have created an API key at openrouter.ai/keys.

```bash
openclaw onboard --auth-choice openrouter-api-key
```

--------------------------------

### Checking model status with authentication

Source: https://docs.openclaw.ai/concepts/models

Example workflow for logging into a provider and verifying the current model status.

```bash
claude auth login
openclaw models status
```

--------------------------------

### Configure plugin entries

Source: https://docs.openclaw.ai/plugins/sdk-setup

Example of defining plugin configuration within the entries object.

```json5
{
  plugins: {
    entries: {
      "my-plugin": {
        config: {
          webhookSecret: "abc123",
        },
      },
    },
  },
}
```

--------------------------------

### Configure Per-Agent Setup Command

Source: https://docs.openclaw.ai/gateway/sandboxing

Define a one-time setup command specific to an agent, which runs after its sandbox container is created. This command executes via 'sh -lc' inside the container.

```json
agents.list[].sandbox.docker.setupCommand
```

--------------------------------

### Manage VM Power State

Source: https://docs.openclaw.ai/install/azure

Deallocate or start the VM to manage compute costs.

```bash
az vm deallocate -g "${RG}" -n "${VM_NAME}"
az vm start -g "${RG}" -n "${VM_NAME}"   # restart later
```

--------------------------------

### Minimal OpenClaw Configuration

Source: https://docs.openclaw.ai/configuration

A basic JSON5 configuration example defining workspace paths and channel access.

```json5
// ~/.openclaw/openclaw.json
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}
```

--------------------------------

### Message envelope examples

Source: https://docs.openclaw.ai/date-time

Examples of how message envelopes appear with different timezone and elapsed time settings.

```text
[WhatsApp +1555 2026-01-18 00:19 PST] hello
```

```text
[WhatsApp +1555 2026-01-18 00:19 CST] hello
```

```text
[WhatsApp +1555 +30s 2026-01-18T05:19Z] follow-up
```

--------------------------------

### Install Opik Plugin for OpenClaw

Source: https://docs.openclaw.ai/plugins/community

Install the Opik plugin to export agent traces for monitoring. This plugin helps in observing agent behavior, costs, tokens, and errors.

```bash
openclaw plugins install @opik/opik-openclaw
```

--------------------------------

### Run the Gateway Process

Source: https://docs.openclaw.ai/cli/gateway

Starts the local Gateway process. Requires gateway.mode=local in the configuration file unless --allow-unconfigured is used.

```bash
openclaw gateway
```

```bash
openclaw gateway run
```

--------------------------------

### Enable PowerShell Debug Tracing for Installer

Source: https://docs.openclaw.ai/install/installer

Run this PowerShell script to enable detailed tracing for the Openclaw AI installer script. This is helpful for diagnosing issues when the standard installer output is insufficient. Remember to disable tracing afterwards.

```powershell
Set-PSDebug -Trace 1
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard
Set-PSDebug -Trace 0
```

--------------------------------

### Qianfan Configuration Example

Source: https://docs.openclaw.ai/providers/qianfan

Example JSON5 configuration for the Qianfan provider. This includes setting the API key, default model, and provider-specific model metadata like base URL and capabilities.

```json5
{
  env: { QIANFAN_API_KEY: "bce-v3/ALTAK-..." },
  agents: {
    defaults: {
      model: { primary: "qianfan/deepseek-v3.2" },
      models: {
        "qianfan/deepseek-v3.2": { alias: "QIANFAN" },
      },
    },
  },
  models: {
    providers: {
      qianfan: {
        baseUrl: "https://qianfan.baidubce.com/v2",
        api: "openai-completions",
        models: [
          {
            id: "deepseek-v3.2",
            name: "DEEPSEEK V3.2",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 98304,
            maxTokens: 32768,
          },
          {
            id: "ernie-5.0-thinking-preview",
            name: "ERNIE-5.0-Thinking-Preview",
            reasoning: true,
            input: ["text", "image"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 119000,
            maxTokens: 64000,
          },
        ],
      },
    },
  },
}
```

--------------------------------

### Moonshot API Configuration Example

Source: https://docs.openclaw.ai/providers/moonshot

A comprehensive configuration example for the Moonshot API, including environment variables, default agent settings, model aliases, and provider-specific model details.

```json5
{
  env: { MOONSHOT_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "moonshot/kimi-k2.6" },
      models: {
        // moonshot-kimi-k2-aliases:start
        "moonshot/kimi-k2.6": { alias: "Kimi K2.6" },
        "moonshot/kimi-k2.5": { alias: "Kimi K2.5" },
        "moonshot/kimi-k2-thinking": { alias: "Kimi K2 Thinking" },
        "moonshot/kimi-k2-thinking-turbo": { alias: "Kimi K2 Thinking Turbo" },
        "moonshot/kimi-k2-turbo": { alias: "Kimi K2 Turbo" },
        // moonshot-kimi-k2-aliases:end
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      moonshot: {
        baseUrl: "https://api.moonshot.ai/v1",
        apiKey: "${MOONSHOT_API_KEY}",
        api: "openai-completions",
        models: [
          // moonshot-kimi-k2-models:start
          {
            id: "kimi-k2.6",
            name: "Kimi K2.6",
            reasoning: false,
            input: ["text", "image"],
            cost: { input: 0.95, output: 4, cacheRead: 0.16, cacheWrite: 0 },
            contextWindow: 262144,
            maxTokens: 262144,
          },
          {
            id: "kimi-k2.5",
            name: "Kimi K2.5",
            reasoning: false,
            input: ["text", "image"],
            cost: { input: 0.6, output: 3, cacheRead: 0.1, cacheWrite: 0 },
            contextWindow: 262144,
            maxTokens: 262144,
          },
          {
            id: "kimi-k2-thinking",
            name: "Kimi K2 Thinking",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 262144,
            maxTokens: 262144,
          },
          {
            id: "kimi-k2-thinking-turbo",
            name: "Kimi K2 Thinking Turbo",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 262144,
            maxTokens: 262144,
          },
          {
            id: "kimi-k2-turbo",
            name: "Kimi K2 Turbo",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 16384,
          },
          // moonshot-kimi-k2-models:end
        ],
      },
    },
  },
}
```

--------------------------------

### Execute agent commands via CLI

Source: https://docs.openclaw.ai/cli/agent

Examples of running agent turns with various routing, delivery, and configuration options.

```bash
openclaw agent --to +15555550123 --message "status update" --deliver
openclaw agent --agent ops --message "Summarize logs"
openclaw agent --session-id 1234 --message "Summarize inbox" --thinking medium
openclaw agent --to +15555550123 --message "Trace logs" --verbose on --json
openclaw agent --agent ops --message "Generate report" --deliver --reply-channel slack --reply-to "#reports"
openclaw agent --agent ops --message "Run locally" --local
```

--------------------------------

### Install External Plugin Explicitly from ClawHub

Source: https://docs.openclaw.ai/plugins/sdk-setup

Force OpenClaw to install a plugin exclusively from ClawHub, ignoring npm.

```bash
openclaw plugins install clawhub:@myorg/openclaw-my-plugin   # ClawHub only
```

--------------------------------

### List Available Models (API Key)

Source: https://docs.openclaw.ai/providers/minimax

Verify model availability after API key onboarding using the minimax provider.

```bash
openclaw models list --provider minimax
```

--------------------------------

### Configure Model Variants (Cheapest, Fastest)

Source: https://docs.openclaw.ai/providers/huggingface

Configure different variants of a model, such as the cheapest or fastest, by appending policy suffixes. This example uses Qwen3 8B.

```json5
{
  agents: {
    defaults: {
      model: { primary: "huggingface/Qwen/Qwen3-8B" },
      models: {
        "huggingface/Qwen/Qwen3-8B": { alias: "Qwen3 8B" },
        "huggingface/Qwen/Qwen3-8B:cheapest": { alias: "Qwen3 8B (cheapest)" },
        "huggingface/Qwen/Qwen3-8B:fastest": { alias: "Qwen3 8B (fastest)" },
      },
    },
  },
}
```

--------------------------------

### Install ClawHub CLI using pnpm

Source: https://docs.openclaw.ai/tools/clawhub

Install the ClawHub CLI globally using pnpm. This is an alternative to npm for managing packages and is needed for authenticated registry operations.

```bash
pnpm add -g clawhub
```

--------------------------------

### Install from ClawHub (Bare Package Name)

Source: https://docs.openclaw.ai/cli/plugins

Installs a plugin using its bare package name. OpenClaw first checks ClawHub and falls back to npm if the package is not found on ClawHub.

```bash
openclaw plugins install openclaw-codex-app-server
```

--------------------------------

### Update and Install Build Essentials

Source: https://docs.openclaw.ai/install/oracle

Updates the package list and installs build-essential, which is required for ARM compilation of some dependencies.

```bash
ssh ubuntu@YOUR_PUBLIC_IP

sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential
```

--------------------------------

### Run Onboarding or Configure Model

Source: https://docs.openclaw.ai/providers/sglang

Commands and configuration for initializing OpenClaw or manually defining a model.

```bash
openclaw onboard
```

```json5
{
  agents: {
    defaults: {
      model: { primary: "sglang/your-model-id" },
    },
  },
}
```

--------------------------------

### HEARTBEAT.md Checklist Example

Source: https://docs.openclaw.ai/gateway/heartbeat

An example of a HEARTBEAT.md file content, providing a simple checklist for daily or periodic tasks. This content is used by the agent as guidance during heartbeat runs.

```markdown
# Heartbeat checklist

- Quick scan: anything urgent in inboxes?
- If it’s daytime, do a lightweight check-in if nothing else is pending.
- If a task is blocked, write down _what is missing_ and ask Peter next time.

```

--------------------------------

### Install a Plugin from ClawHub using OpenClaw CLI

Source: https://docs.openclaw.ai/tools/clawhub

Install a plugin from ClawHub by specifying its package name. The format `clawhub:<package>` is used, where `<package>` is the plugin's identifier on ClawHub.

```bash
openclaw plugins install clawhub:<package>
```

--------------------------------

### Hardened Exec Provider Example

Source: https://docs.openclaw.ai/cli/config

Example of configuring a hardened exec provider for secrets. This includes security-focused flags like `--provider-json-only` and `--provider-trusted-dir`.

```bash
openclaw config set secrets.providers.vault \
  --provider-source exec \
  --provider-command /usr/local/bin/openclaw-vault \
  --provider-arg read \
  --provider-arg openai/api-key \
  --provider-json-only \
  --provider-pass-env VAULT_TOKEN \
  --provider-trusted-dir /usr/local/bin \
  --provider-timeout-ms 5000
```

--------------------------------

### Common CLI usage pitfalls

Source: https://docs.openclaw.ai/cli/infer

Examples of incorrect versus correct command syntax for media and audio operations.

```bash
# Bad
openclaw infer media image generate --prompt "friendly lobster"

# Good
openclaw infer image generate --prompt "friendly lobster"
```

```bash
# Bad
openclaw infer audio transcribe --file ./memo.m4a --model whisper-1 --json

# Good
openclaw infer audio transcribe --file ./memo.m4a --model openai/whisper-1 --json
```

--------------------------------

### Invoke Music Generation Tool

Source: https://docs.openclaw.ai/providers/comfy

Example command to trigger music generation using the shared music_generate tool.

```text
/tool music_generate prompt="Warm ambient synth loop with soft tape texture"
```

--------------------------------

### Configure Slash Commands

Source: https://docs.openclaw.ai/tools/slash-commands

Example configuration object for the commands system, defining permissions, enabled features, and owner access.

```json5
{
  commands: {
    native: "auto",
    nativeSkills: "auto",
    text: true,
    bash: false,
    bashForegroundMs: 2000,
    config: false,
    mcp: false,
    plugins: false,
    debug: false,
    restart: true,
    ownerAllowFrom: ["discord:123456789012345678"],
    ownerDisplay: "raw",
    ownerDisplaySecret: "${OWNER_ID_HASH_SECRET}",
    allowFrom: {
      "*": ["user1"],
      discord: ["user:123"],
    },
    useAccessGroups: true,
  },
}
```

--------------------------------

### Clone and run formal models

Source: https://docs.openclaw.ai/security/formal-verification

Initial setup for the formal models repository. Requires Java 11+ to execute the TLC model checker.

```bash
git clone https://github.com/vignesh07/openclaw-formal-models
cd openclaw-formal-models

# Java 11+ required (TLC runs on the JVM).
# The repo vendors a pinned `tla2tools.jar` (TLA+ tools) and provides `bin/tlc` + Make targets.

make <target>
```

--------------------------------

### Publishing and Installing External Plugins

Source: https://docs.openclaw.ai/plugins/building-plugins

Commands for validating, publishing a plugin to ClawHub, and installing it into an OpenClaw instance. OpenClaw prioritizes ClawHub over npm for package resolution.

```bash
clawhub package publish your-org/your-plugin --dry-run
clawhub package publish your-org/your-plugin
openclaw plugins install clawhub:@myorg/openclaw-my-plugin
```

--------------------------------

### Install QQbot Plugin for OpenClaw

Source: https://docs.openclaw.ai/plugins/community

Install the QQbot plugin to connect OpenClaw with QQ via the QQ Bot API. It supports various chat features and rich media.

```bash
openclaw plugins install @tencent-connect/openclaw-qqbot
```

--------------------------------

### Rich OpenClaw Plugin Manifest Example

Source: https://docs.openclaw.ai/plugins/manifest

A comprehensive example of an OpenClaw plugin manifest, demonstrating various configuration options for identity, model support, authentication, and UI hints.

```json
{
  "id": "openrouter",
  "name": "OpenRouter",
  "description": "OpenRouter provider plugin",
  "version": "1.0.0",
  "providers": ["openrouter"],
  "modelSupport": {
    "modelPrefixes": ["router-"]
  },
  "providerEndpoints": [
    {
      "endpointClass": "xai-native",
      "hosts": ["api.x.ai"]
    }
  ],
  "cliBackends": ["openrouter-cli"],
  "syntheticAuthRefs": ["openrouter-cli"],
  "providerAuthEnvVars": {
    "openrouter": ["OPENROUTER_API_KEY"]
  },
  "providerAuthAliases": {
    "openrouter-coding": "openrouter"
  },
  "channelEnvVars": {
    "openrouter-chatops": ["OPENROUTER_CHATOPS_TOKEN"]
  },
  "providerAuthChoices": [
    {
      "provider": "openrouter",
      "method": "api-key",
      "choiceId": "openrouter-api-key",
      "choiceLabel": "OpenRouter API key",
      "groupId": "openrouter",
      "groupLabel": "OpenRouter",
      "optionKey": "openrouterApiKey",
      "cliFlag": "--openrouter-api-key",
      "cliOption": "--openrouter-api-key <key>",
      "cliDescription": "OpenRouter API key",
      "onboardingScopes": ["text-inference"]
    }
  ],
  "uiHints": {
    "apiKey": {
      "label": "API key",
      "placeholder": "sk-or-v1-…",
      "sensitive": true
    }
  },
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "apiKey": {
        "type": "string"
      }
    }
  }
}
```

--------------------------------

### Configure group policies

Source: https://docs.openclaw.ai/channels/feishu

JSON configuration examples for controlling group access and mention requirements.

```json5
{
  channels: {
    feishu: {
      groupPolicy: "open",
    },
  },
}
```

```json5
{
  channels: {
    feishu: {
      groupPolicy: "open",
      requireMention: true,
    },
  },
}
```

```json5
{
  channels: {
    feishu: {
      groupPolicy: "allowlist",
      // Group IDs look like: oc_xxx
      groupAllowFrom: ["oc_xxx", "oc_yyy"],
    },
  },
}
```

```json5
{
  channels: {
    feishu: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["oc_xxx"],
      groups: {
        oc_xxx: {
          // User open_ids look like: ou_xxx
          allowFrom: ["ou_user1", "ou_user2"],
        },
      },
    },
  },
}
```

--------------------------------

### Custom systemd Unit Configuration

Source: https://docs.openclaw.ai/gateway

Example configuration for a manual systemd user-unit.

```ini
[Unit]
Description=OpenClaw Gateway
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/local/bin/openclaw gateway --port 18789
Restart=always
RestartSec=5
TimeoutStopSec=30
TimeoutStartSec=30
SuccessExitStatus=0 143
KillMode=control-group

[Install]
WantedBy=default.target
```

--------------------------------

### Configure Exec Path Prepend in JSON5

Source: https://docs.openclaw.ai/tools/exec

Example configuration for adding custom directories to the PATH for exec runs.

```json5
{
  tools: {
    exec: {
      pathPrepend: ["~/bin", "/opt/oss/bin"],
    },
  },
}
```

--------------------------------

### Install Tlon Plugin from Local Checkout

Source: https://docs.openclaw.ai/channels/tlon

Install the Tlon plugin from a local Git repository checkout using the OpenClaw CLI. This is useful when developing or testing the plugin locally.

```bash
openclaw plugins install ./path/to/local/tlon-plugin
```

--------------------------------

### Verify NPM Post-Publish Installation

Source: https://docs.openclaw.ai/reference/RELEASING

Run the post-publish verification script to check the published registry install path in a fresh temporary prefix. Use tsx for running TypeScript files.

```bash
node --import tsx scripts/openclaw-npm-postpublish-verify.ts YYYY.M.D
```

--------------------------------

### Run basic onboarding flows

Source: https://docs.openclaw.ai/cli/onboard

Execute standard onboarding workflows using different flow modes or remote gateway targets.

```bash
openclaw onboard
openclaw onboard --flow quickstart
openclaw onboard --flow manual
openclaw onboard --mode remote --remote-url wss://gateway-host:18789
```

--------------------------------

### Manual Environment Setup for Multiple Gateways

Source: https://docs.openclaw.ai/gateway/multiple-gateways

Manually set environment variables for configuration path and state directory to run multiple gateway instances with distinct configurations. Ensure unique ports are assigned.

```bash
OPENCLAW_CONFIG_PATH=~/.openclaw/main.json \
OPENCLAW_STATE_DIR=~/.openclaw-main \
openclaw gateway --port 18789

OPENCLAW_CONFIG_PATH=~/.openclaw/rescue.json \
OPENCLAW_STATE_DIR=~/.openclaw-rescue \
openclaw gateway --port 19001
```

--------------------------------

### Set Configuration in Batch Mode with JSON

Source: https://docs.openclaw.ai/cli/config

Configure multiple settings at once using batch mode with a JSON payload. This example sets a default provider and a Discord token.

```bash
openclaw config set --batch-json '[
  {
    "path": "secrets.providers.default",
    "provider": { "source": "env" }
  },
  {
    "path": "channels.discord.token",
    "ref": { "source": "env", "provider": "default", "id": "DISCORD_BOT_TOKEN" }
  }
]'
```

--------------------------------

### Run Interactive Vydra Onboarding

Source: https://docs.openclaw.ai/providers/vydra

Initiates interactive onboarding for Vydra API key authentication. Alternatively, set the VYDRA_API_KEY environment variable directly.

```bash
openclaw onboard --auth-choice vydra-api-key
```

```bash
export VYDRA_API_KEY="vydra_live_..."
```

--------------------------------

### openclaw.install Package Metadata

Source: https://docs.openclaw.ai/plugins/sdk-setup

Metadata fields for package installation and configuration.

```APIDOC
## openclaw.install Package Metadata

`openclaw.install` is package metadata, not manifest metadata.

| Field                        | Type                 | What it means                                                                    |
| ---------------------------- | -------------------- | -------------------------------------------------------------------------------- |
| `npmSpec`                    | `string`             | Canonical npm spec for install/update flows.                                     |
| `localPath`                  | `string`             | Local development or bundled install path.                                       |
| `defaultChoice`              | `"npm"` | `"local"` | Preferred install source when both are available.                                |
| `minHostVersion`             | `string`             | Minimum supported OpenClaw version in the form `>=x.y.z`.                        |
| `allowInvalidConfigRecovery` | `boolean`            | Lets bundled-plugin reinstall flows recover from specific stale-config failures. |

If `minHostVersion` is set, install and manifest-registry loading both enforce
it. Older hosts skip the plugin; invalid version strings are rejected.

`allowInvalidConfigRecovery` is not a general bypass for broken configs. It is
for narrow bundled-plugin recovery only, so reinstall/setup can repair known
upgrade leftovers like a missing bundled plugin path or stale `channels.<id>`
entry for that same plugin. If config is broken for unrelated reasons, install
still fails closed and tells the operator to run `openclaw doctor --fix`.
```

--------------------------------

### Update or Install OpenClaw via CLI and Git

Source: https://docs.openclaw.ai/help/faq

Commands for switching update channels or performing a manual source-based installation.

```bash
openclaw update --channel dev
```

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git
```

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm build
```

--------------------------------

### Onboard Zen Catalog

Source: https://docs.openclaw.ai/providers/opencode

Run the onboarding process for the Zen catalog. You can choose to authenticate interactively or provide the API key directly.

```bash
openclaw onboard --auth-choice opencode-zen
```

```bash
openclaw onboard --opencode-zen-api-key "$OPENCODE_API_KEY"
```

--------------------------------

### Setup Gmail Pub/Sub Hook

Source: https://docs.openclaw.ai/cli/index

Configures the Gmail watch and the OpenClaw-facing push path. Requires account email.

```bash
openclaw webhooks gmail setup --account <email>
```

--------------------------------

### Initialize Configuration File

Source: https://docs.openclaw.ai/install/fly

Access the remote machine via SSH to create the application configuration file.

```bash
fly ssh console
```

```bash
mkdir -p /data
cat > /data/openclaw.json << 'EOF'
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-opus-4-6",
        "fallbacks": ["anthropic/claude-sonnet-4-6", "openai/gpt-5.4"]
      },
      "maxConcurrent": 4
    },
    "list": [
      {
        "id": "main",
        "default": true
      }
    ]
  },
  "auth": {
    "profiles": {
      "anthropic:default": { "mode": "token", "provider": "anthropic" },
      "openai:default": { "mode": "token", "provider": "openai" }
```

--------------------------------

### Configure Compaction Model (JSON5)

Source: https://docs.openclaw.ai/concepts/compaction

Use a more capable model for improved summaries by specifying it in the 'agents.defaults.compaction.model' setting. This example uses JSON5 syntax.

```json5
{
  agents: {
    defaults: {
      compaction: {
        model: "openrouter/anthropic/claude-sonnet-4-6",
      },
    },
  },
}
```

--------------------------------

### Build and Test with Bun

Source: https://docs.openclaw.ai/install/bun

Executes build and test scripts using the Bun runtime. Ensure Bun is installed and configured for your project.

```sh
bun run build
```

```sh
bun run vitest run
```

--------------------------------

### Initialize OpenClaw Workspace

Source: https://docs.openclaw.ai/start/openclaw

This command sets up the default OpenClaw workspace directory and creates essential starter files like AGENTS.md, SOUL.md, etc. It's recommended for new setups.

```bash
openclaw setup
```

--------------------------------

### Runway Configuration Example

Source: https://docs.openclaw.ai/providers/runway

This JSON configuration snippet shows how to set the default video generation model to Runway.

```json
{
  agents: {
    defaults: {
      videoGenerationModel: {
        primary: "runway/gen4.5",
      },
    },
  },
}
```

--------------------------------

### Configure Teams and Channel Allowlist

Source: https://docs.openclaw.ai/channels/msteams

Example of scoping replies to specific teams and channels with mention requirements.

```json5
{
  channels: {
    msteams: {
      groupPolicy: "allowlist",
      teams: {
        "My Team": {
          channels: {
            General: { requireMention: true },
          },
        },
      },
    },
  },
}
```

--------------------------------

### Install Rescue Bot Gateway

Source: https://docs.openclaw.ai/gateway/multiple-gateways

Onboard and install the rescue bot gateway using a separate profile and ensuring a distinct port range. This provides an isolated environment for the rescue bot.

```bash
# Main bot (existing or fresh, without --profile param)
# Runs on port 18789 + Chrome CDC/Canvas/... Ports
openclaw onboard
openclaw gateway install

# Rescue bot (isolated profile + ports)
openclaw --profile rescue onboard
# Notes:
# - workspace name will be postfixed with -rescue per default
# - Port should be at least 18789 + 20 Ports,
#   better choose completely different base port, like 19789,
# - rest of the onboarding is the same as normal

# To install the service (if not happened automatically during setup)
openclaw --profile rescue gateway install
```

--------------------------------

### Install Lume Script

Source: https://docs.openclaw.ai/install/macos-vm

Execute this bash script to install the Lume environment on your macOS system. Ensure your ~/.local/bin is in your PATH.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/trycua/cua/main/libs/lume/scripts/install.sh)"
```

--------------------------------

### Configure Matrix with access token

Source: https://docs.openclaw.ai/channels/matrix

Use an access token for authentication, which is the preferred method for non-interactive setups.

```json5
{
  channels: {
    matrix: {
      enabled: true,
      homeserver: "https://matrix.example.org",
      accessToken: "syt_xxx",
      dm: { policy: "pairing" },
    },
  },
}
```

--------------------------------

### Example Music Generation Prompt

Source: https://docs.openclaw.ai/tools/music-generation

Use this prompt to generate a cinematic piano track with soft strings and no vocals.

```text
Generate a cinematic piano track with soft strings and no vocals.
```

--------------------------------

### Onboard Alibaba Provider

Source: https://docs.openclaw.ai/providers/alibaba

Use this command to onboard the Alibaba provider and set up authentication. It configures the shared DashScope credential.

```bash
openclaw onboard --auth-choice qwen-standard-api-key
```

--------------------------------

### Install Lossless Claw (LCM) Plugin

Source: https://docs.openclaw.ai/plugins/community

Install the Lossless Claw plugin for advanced conversation summarization and context management. It uses a DAG-based approach to preserve context fidelity while reducing token usage.

```bash
openclaw plugins install @martian-engineering/lossless-claw
```

--------------------------------

### Run SearXNG via Docker

Source: https://docs.openclaw.ai/tools/searxng-search

Starts a local SearXNG instance on port 8888.

```bash
docker run -d -p 8888:8080 searxng/searxng
```

--------------------------------

### Run OpenClaw configuration commands

Source: https://docs.openclaw.ai/cli/configure

Execute the interactive configuration wizard for general setup or specific functional sections.

```bash
openclaw configure
openclaw configure --section web
openclaw configure --section model --section channels
openclaw configure --section gateway --section daemon
```

--------------------------------

### PDF Tool - Configuration

Source: https://docs.openclaw.ai/tools/pdf

Example configuration for the PDF tool.

```APIDOC
## PDF Tool - Configuration

```json5
{
  "agents": {
    "defaults": {
      "pdfModel": {
        "primary": "anthropic/claude-opus-4-6",
        "fallbacks": ["openai/gpt-5.4-mini"]
      },
      "pdfMaxBytesMb": 10,
      "pdfMaxPages": 20
    }
  }
}
```
```

--------------------------------

### openclaw webhooks gmail setup

Source: https://docs.openclaw.ai/cli/webhooks

Configure Gmail watch, Pub/Sub, and OpenClaw webhook delivery.

```APIDOC
## openclaw webhooks gmail setup

### Description
Configure Gmail watch, Pub/Sub, and OpenClaw webhook delivery.

### Method
CLI Command

### Endpoint
N/A

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None

#### Command Line Arguments
- **--account** (string) - Required - The email account to configure.
- **--project** (string) - Optional - The GCP project ID.
- **--topic** (string) - Optional - The Pub/Sub topic name.
- **--subscription** (string) - Optional - The Pub/Sub subscription name.
- **--label** (string) - Optional - The Gmail label to watch.
- **--hook-url** (string) - Optional - The URL for webhook delivery.
- **--hook-token** (string) - Optional - A token for webhook authentication.
- **--push-token** (string) - Optional - A token for push notifications.
- **--bind** (string) - Optional - The host to bind the webhook server to.
- **--port** (integer) - Optional - The port for the webhook server.
- **--path** (string) - Optional - The path for the webhook endpoint.
- **--include-body** (boolean) - Optional - Whether to include the email body in notifications.
- **--max-bytes** (integer) - Optional - Maximum bytes for email content.
- **--renew-minutes** (integer) - Optional - Minutes to renew the watch subscription.
- **--tailscale** (string) - Optional - Tailscale mode (funnel, serve, off).
- **--tailscale-path** (string) - Optional - Path for Tailscale.
- **--tailscale-target** (string) - Optional - Target for Tailscale.
- **--push-endpoint** (string) - Optional - The push notification endpoint URL.
- **--json** (boolean) - Optional - Output in JSON format.

### Request Example
```bash
openclaw webhooks gmail setup --account you@example.com
openclaw webhooks gmail setup --account you@example.com --project my-gcp-project --json
openclaw webhooks gmail setup --account you@example.com --hook-url https://gateway.example.com/hooks/gmail
```

### Response
#### Success Response (200)
Output depends on the `--json` flag. Typically, a success message or JSON confirmation.

#### Response Example
```json
{
  "status": "success",
  "message": "Gmail webhook configured successfully."
}
```
```

--------------------------------

### Enable Systemd Service

Source: https://docs.openclaw.ai/platforms/linux

Command to enable and start the configured systemd user service.

```bash
systemctl --user enable --now openclaw-gateway[-<profile>].service
```

--------------------------------

### Example Energetic Chiptune Prompt

Source: https://docs.openclaw.ai/tools/music-generation

Use this prompt to generate an energetic chiptune loop about launching a rocket at sunrise.

```text
Generate an energetic chiptune loop about launching a rocket at sunrise.
```

--------------------------------

### Onboard with Xiaomi API Key

Source: https://docs.openclaw.ai/providers/xiaomi

Use this command to onboard with Xiaomi MiMo using an API key. The key can be provided during the onboarding process or passed directly as an argument.

```bash
openclaw onboard --auth-choice xiaomi-api-key
```

```bash
openclaw onboard --auth-choice xiaomi-api-key --xiaomi-api-key "$XIAOMI_API_KEY"
```

--------------------------------

### Configure agent access profiles

Source: https://docs.openclaw.ai/gateway/security

Examples of defining agent sandbox and tool permissions in the configuration file.

```json5
{
  agents: {
    list: [
      {
        id: "personal",
        workspace: "~/.openclaw/workspace-personal",
        sandbox: { mode: "off" },
      },
    ],
  },
}
```

```json5
{
  agents: {
    list: [
      {
        id: "family",
        workspace: "~/.openclaw/workspace-family",
        sandbox: {
          mode: "all",
          scope: "agent",
          workspaceAccess: "ro",
        },
        tools: {
          allow: ["read"],
          deny: ["write", "edit", "apply_patch", "exec", "process", "browser"],
        },
      },
    ],
  },
}
```

```json5
{
  agents: {
    list: [
      {
        id: "public",
        workspace: "~/.openclaw/workspace-public",
        sandbox: {
          mode: "all",
          scope: "agent",
          workspaceAccess: "none",
        },
        // Session tools can reveal sensitive data from transcripts. By default OpenClaw limits these tools
        // to the current session + spawned subagent sessions, but you can clamp further if needed.
        // See `tools.sessions.visibility` in the configuration reference.
        tools: {
          sessions: { visibility: "tree" }, // self | tree | agent | all
          allow: [
            "sessions_list",
            "sessions_history",
            "sessions_send",
            "sessions_spawn",
            "session_status",
            "whatsapp",
            "telegram",
            "slack",
            "discord",
          ],
          deny: [
            "read",
            "write",
            "edit",
            "apply_patch",
            "exec",
            "process",
            "browser",
            "canvas",
            "nodes",
            "cron",
            "gateway",
            "image",
          ],
        },
      },
    ],
  },
}
```

--------------------------------

### Start Chromium Manually

Source: https://docs.openclaw.ai/tools/browser-linux-troubleshooting

Command to launch Chromium with the necessary flags for remote debugging.

```bash
chromium-browser --headless --no-sandbox --disable-gpu \
  --remote-debugging-port=18800 \
  --user-data-dir=$HOME/.openclaw/browser/openclaw/user-data \
  about:blank &
```

--------------------------------

### Execute command with specific profile

Source: https://docs.openclaw.ai/cli/browser

Example of running a command using a named browser profile.

```bash
openclaw browser --browser-profile work tabs
```

--------------------------------

### Install Gateway Service

Source: https://docs.openclaw.ai/help/faq

Installs the Openclaw Gateway as a system service for a specific profile. Ensure a unique port is configured for each profile.

```bash
openclaw --profile <name> gateway install
```

--------------------------------

### Migrate Single Agent Configuration

Source: https://docs.openclaw.ai/tools/multi-agent-sandbox-tools

Examples showing the transition from legacy single-agent configuration to the modern multi-agent list structure.

```json
{
  "agents": {
    "defaults": {
      "workspace": "~/.openclaw/workspace",
      "sandbox": {
        "mode": "non-main"
      }
    }
  },
  "tools": {
    "sandbox": {
      "tools": {
        "allow": ["read", "write", "apply_patch", "exec"],
        "deny": []
      }
    }
  }
}
```

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "default": true,
        "workspace": "~/.openclaw/workspace",
        "sandbox": { "mode": "off" }
      }
    ]
  }
}
```

--------------------------------

### Remove OpenClaw CLI (bun)

Source: https://docs.openclaw.ai/install/uninstall

Removes the OpenClaw CLI installed globally using bun. Use this if you installed via bun.

```bash
bun remove -g openclaw
```

--------------------------------

### Onboard Qwen Coding Plan

Source: https://docs.openclaw.ai/providers/qwen

Commands to initialize authentication for the Qwen Coding Plan subscription.

```bash
openclaw onboard --auth-choice qwen-api-key
```

```bash
openclaw onboard --auth-choice qwen-api-key-cn
```

--------------------------------

### Remove OpenClaw CLI (pnpm)

Source: https://docs.openclaw.ai/install/uninstall

Removes the OpenClaw CLI installed globally using pnpm. Use this if you installed via pnpm.

```bash
pnpm remove -g openclaw
```

--------------------------------

### Run Kilo Gateway Onboarding

Source: https://docs.openclaw.ai/providers/kilocode

Execute the onboarding command for Kilo Gateway using the kilocode-api-key authentication choice. Alternatively, set the KILOCODE_API_KEY environment variable directly.

```bash
openclaw onboard --auth-choice kilocode-api-key
```

```bash
export KILOCODE_API_KEY="<your-kilocode-api-key>"
```

--------------------------------

### Configure ComfyUI with Multiple Capabilities

Source: https://docs.openclaw.ai/providers/comfy

Example configuration for ComfyUI provider supporting image, video, and music generation with distinct workflows and node IDs for each capability.

```json
{
  models: {
    providers: {
      comfy: {
        mode: "local",
        baseUrl: "http://127.0.0.1:8188",
        image: {
          workflowPath: "./workflows/flux-api.json",
          promptNodeId: "6",
          outputNodeId: "9",
        },
        video: {
          workflowPath: "./workflows/video-api.json",
          promptNodeId: "12",
          outputNodeId: "21",
        },
        music: {
          workflowPath: "./workflows/music-api.json",
          promptNodeId: "3",
          outputNodeId: "18",
        },
      },
    },
  },
}
```

--------------------------------

### Configure QMD with bridge mode

Source: https://docs.openclaw.ai/plugins/memory-wiki

Example configuration for integrating QMD for recall while using memory-wiki in bridge mode for knowledge management.

```json5
{
  memory: {
    backend: "qmd",
      "memory-wiki": {
        enabled: true,
        config: {
          vaultMode: "bridge",
          bridge: {
            enabled: true,
            readMemoryArtifacts: true,
            indexDreamReports: true,
            indexDailyNotes: true,
            indexMemoryRoot: true,
            followMemoryEvents: true,
          },
          search: {
            backend: "shared",
            corpus: "all",
          },
          context: {
            includeCompiledDigestPrompt: false,
          },
        },
      },
    },
  },
}
```

--------------------------------

### Remove OpenClaw CLI (npm)

Source: https://docs.openclaw.ai/install/uninstall

Removes the OpenClaw CLI installed globally using npm. Use this if you installed via npm.

```bash
npm rm -g openclaw
```

--------------------------------

### Configure Default Startup Context

Source: https://docs.openclaw.ai/gateway/configuration-reference

Controls the initial prelude injected on bare '/new' and '/reset' runs. Includes settings for enabling, application triggers, memory days, and character limits.

```json5
{
  agents: {
    defaults: {
      startupContext: {
        enabled: true,
        applyOn: ["new", "reset"],
        dailyMemoryDays: 2,
        maxFileBytes: 16384,
        maxFileChars: 1200,
        maxTotalChars: 2800,
      },
    },
  },
}
```

--------------------------------

### Plugin Runtime Registration

Source: https://docs.openclaw.ai/plugins/sdk-runtime

Example of how to access the runtime object during plugin registration.

```APIDOC
## Register Plugin Runtime

### Description
Access the `api.runtime` object within the `register` function.

### Method
`register(api)`

### Parameters
- **api** (object) - The API object provided during plugin registration.

### Request Example
```typescript
register(api) {
  const runtime = api.runtime;
}
```

### Response
- **runtime** (object) - The runtime object for plugin interaction.
```

--------------------------------

### List Available Providers and Models

Source: https://docs.openclaw.ai/tools/image-generation

Use the tool command to inspect available providers and models at runtime.

```text
/tool image_generate action=list
```

--------------------------------

### Run non-interactive onboarding

Source: https://docs.openclaw.ai/providers/ollama

Automates the onboarding process using command-line flags for configuration.

```bash
openclaw onboard --non-interactive \
  --auth-choice ollama \
  --accept-risk
```

```bash
openclaw onboard --non-interactive \
  --auth-choice ollama \
  --custom-base-url "http://ollama-host:11434" \
  --custom-model-id "qwen3.5:27b" \
  --accept-risk
```

--------------------------------

### Configure OpenClaw for Google Chrome

Source: https://docs.openclaw.ai/tools/browser-linux-troubleshooting

JSON configuration to point OpenClaw to the installed Google Chrome binary.

```json
{
  "browser": {
    "enabled": true,
    "executablePath": "/usr/bin/google-chrome-stable",
    "headless": true,
    "noSandbox": true
  }
}
```

--------------------------------

### Verify ComfyUI Provider

Source: https://docs.openclaw.ai/providers/comfy

Use this command to list available models from the ComfyUI provider and verify the setup.

```bash
openclaw models list --provider comfy
```

--------------------------------

### Configure Active Memory with a fast provider

Source: https://docs.openclaw.ai/concepts/active-memory

Full configuration example for enabling Active Memory with a dedicated Cerebras model.

```json5
models: {
  providers: {
    cerebras: {
      baseUrl: "https://api.cerebras.ai/v1",
      apiKey: "${CEREBRAS_API_KEY}",
      api: "openai-completions",
      models: [{ id: "gpt-oss-120b", name: "GPT OSS 120B (Cerebras)" }],
    },
  },
},
plugins: {
  entries: {
    "active-memory": {
      enabled: true,
      config: {
        model: "cerebras/gpt-oss-120b",
      },
    },
  },
}
```

--------------------------------

### Default Codex App-Server Start

Source: https://docs.openclaw.ai/plugins/codex-harness

This snippet shows the default command to start the Codex app-server locally using stdio transport.

```APIDOC
## Start Codex App-Server Locally

### Description
Starts the Codex app-server locally using standard input/output (stdio) for communication.

### Method
Command Line

### Endpoint
N/A

### Request Example
```bash
codex app-server --listen stdio://
```

### Response
N/A
```

--------------------------------

### List available models via CLI

Source: https://docs.openclaw.ai/help/faq

Command to display all available models for troubleshooting provider configuration.

```bash
openclaw models list
```

--------------------------------

### Start Gmail Watcher

Source: https://docs.openclaw.ai/automation/cron-jobs

Starts the Gmail watcher service to monitor for new emails and push notifications to a specified Pub/Sub topic.

```bash
gog gmail watch start \
  --account openclaw@gmail.com \
  --label INBOX \
  --topic projects/<project-id>/topics/gog-gmail-watch
```

--------------------------------

### Patch Format Example

Source: https://docs.openclaw.ai/tools/apply-patch

Illustrates the structured patch format for applying changes to files, including adding, updating, and deleting.

```plaintext
*** Begin Patch
*** Add File: path/to/file.txt
+line 1
+line 2
*** Update File: src/app.ts
@@
-old line
+new line
*** Delete File: obsolete.txt
*** End Patch
```

--------------------------------

### Broader Setup Seam Usage

Source: https://docs.openclaw.ai/plugins/sdk-channel-plugins

Use the broader `openclaw/plugin-sdk/setup` seam only when heavier shared setup/config helpers, such as `moveSingleAccountChannelSectionToDefaultAccount`, are also needed.

```javascript
openclaw/plugin-sdk/setup
```

```javascript
moveSingleAccountChannelSectionToDefaultAccount(...)
```

--------------------------------

### List Step Plan Models

Source: https://docs.openclaw.ai/providers/stepfun

Verify available models for the Step Plan provider.

```bash
openclaw models list --provider stepfun-plan
```

--------------------------------

### Run gateway in watch mode

Source: https://docs.openclaw.ai/help/debugging

Commands to start the gateway with file watching enabled for rapid development iteration.

```bash
pnpm gateway:watch
```

```bash
node scripts/watch-node.mjs gateway --force
```

--------------------------------

### Browser lifecycle management

Source: https://docs.openclaw.ai/cli/browser

Commands to check status, start, stop, and reset browser profiles.

```bash
openclaw browser status
openclaw browser start
openclaw browser stop
openclaw browser --browser-profile openclaw reset-profile
```

--------------------------------

### Configure Brave Web Search Plugin

Source: https://docs.openclaw.ai/help/faq

Example configuration for the Brave web search plugin, requiring an API key.

```json5
{
  plugins: {
    entries: {
      brave: {
        config: {
          webSearch: {

```

--------------------------------

### Initialize development profile

Source: https://docs.openclaw.ai/gateway

Use the --dev flag to automatically configure isolated state, configuration, and the default gateway port.

```bash
openclaw --dev setup
openclaw --dev gateway --allow-unconfigured
openclaw --dev status
```

--------------------------------

### Install Mattermost Plugin via CLI

Source: https://docs.openclaw.ai/channels/mattermost

Use this command to install the Mattermost plugin from the npm registry when not using a bundled OpenClaw release.

```bash
openclaw plugins install @openclaw/mattermost
```

--------------------------------

### Timeout Recommendation for Full Context

Source: https://docs.openclaw.ai/concepts/active-memory

Illustrates the recommended timeout progression for different context modes. For 'full' mode, start with a timeout of 15000 ms or higher, increasing with context size.

```text
message < recent < full
```

--------------------------------

### Run Media Live Harness

Source: https://docs.openclaw.ai/help/testing

Execute the unified media test suite for images, music, and video with various filtering options.

```bash
pnpm test:live:media
```

```bash
pnpm test:live:media image video --providers openai,google,minimax
```

```bash
pnpm test:live:media video --video-providers openai,runway --all-providers
```

```bash
pnpm test:live:media music --quiet
```

--------------------------------

### List Agents and Bindings

Source: https://docs.openclaw.ai/concepts/multi-agent

Verify the current agent configuration and routing bindings.

```bash
openclaw agents list --bindings
```

--------------------------------

### Perform non-interactive onboarding

Source: https://docs.openclaw.ai/providers/fireworks

Configures the provider for scripted or CI environments by passing all required values via command line arguments.

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice fireworks-api-key \
  --fireworks-api-key "$FIREWORKS_API_KEY" \
  --skip-health \
  --accept-risk
```

--------------------------------

### Configure Model Fallback Strategy

Source: https://docs.openclaw.ai/providers/minimax

Example configuration for setting a primary model with a fallback to MiniMax M2.7.

```json5
{
  env: { MINIMAX_API_KEY: "sk-..." },
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-6": { alias: "primary" },
        "minimax/MiniMax-M2.7": { alias: "minimax" },
      },
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["minimax/MiniMax-M2.7"],
      },
    },
  },
}
```

--------------------------------

### Run Node Host in Foreground

Source: https://docs.openclaw.ai/cli/node

Command to start the node host process in the foreground, connecting to a specified gateway.

```bash
openclaw node run --host <gateway-host> --port 18789
```

--------------------------------

### package.json openclaw metadata

Source: https://docs.openclaw.ai/plugins/manifest

Overview of the fields used for plugin discovery, installation, and startup optimization.

```APIDOC
## package.json openclaw metadata

### Description
Defines metadata for OpenClaw plugins directly within the package.json file to facilitate discovery and lightweight state checking without loading the full plugin runtime.

### Fields
- **openclaw.extensions** (string) - Declares native plugin entrypoints.
- **openclaw.setupEntry** (string) - Lightweight setup-only entrypoint for onboarding.
- **openclaw.channel** (object) - Metadata for channel catalog including labels, docs, and aliases.
- **openclaw.channel.configuredState** (object) - Metadata for checking if env-only setup exists.
- **openclaw.channel.persistedAuthState** (object) - Metadata for checking if auth is present.
- **openclaw.install.npmSpec** / **openclaw.install.localPath** (string) - Install/update hints.
- **openclaw.install.defaultChoice** (string) - Preferred install path.
- **openclaw.install.minHostVersion** (string) - Minimum supported OpenClaw host version (semver).
- **openclaw.install.allowInvalidConfigRecovery** (boolean) - Allows recovery for specific bundled-plugin upgrade failures.
- **openclaw.startup.deferConfiguredChannelFullLoadUntilAfterListen** (boolean) - Defers full channel load.
```

--------------------------------

### Onboard with fal API Key

Source: https://docs.openclaw.ai/providers/fal

Use this command to set up your OpenClaw environment with the 'fal' provider and authenticate using your API key.

```bash
openclaw onboard --auth-choice fal-api-key
```

--------------------------------

### Start Gateway and Approve Pairing

Source: https://docs.openclaw.ai/channels/telegram

Start the gateway and then list and approve the Telegram pairing code. Pairing codes expire after 1 hour.

```bash
openclaw gateway
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
```

--------------------------------

### Show Exec Policy and Presets

Source: https://docs.openclaw.ai/cli/approvals

Inspect the local requested policy, host approvals file, and effective merge. Apply local presets like YOLO or deny-all. Use --json for machine-readable output.

```bash
openclaw exec-policy show
```

```bash
openclaw exec-policy show --json
```

```bash
openclaw exec-policy preset yolo
```

```bash
openclaw exec-policy preset cautious --json
```

```bash
openclaw exec-policy set --host gateway --security full --ask off --ask-fallback full
```

--------------------------------

### Run Initial Troubleshooting Commands

Source: https://docs.openclaw.ai/help/troubleshooting

Execute this sequence of commands for a rapid assessment of your OpenClaw setup. Ensure each command produces expected output to confirm basic functionality.

```bash
openclaw status
openclaw status --all
openclaw gateway probe
openclaw gateway status
openclaw doctor
openclaw channels status --probe
openclaw logs --follow
```

--------------------------------

### Install External Plugin from ClawHub or npm

Source: https://docs.openclaw.ai/plugins/sdk-setup

Use this command to install a plugin, which OpenClaw will attempt to find on ClawHub first and then fall back to npm.

```bash
openclaw plugins install @myorg/openclaw-my-plugin
```

--------------------------------

### Onboard Synthetic API Key

Source: https://docs.openclaw.ai/start/wizard-cli-automation

Use this command to onboard with a Synthetic API key. Ensure the SYNTHETIC_API_KEY environment variable is set.

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice synthetic-api-key \
  --synthetic-api-key "$SYNTHETIC_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

--------------------------------

### Configuring Approval Policy and Guardian Integration

Source: https://docs.openclaw.ai/plugins/codex-harness

This configuration example demonstrates how to set a stricter approval policy and route reviews through a guardian subagent.

```APIDOC
## Configure Approval Policy and Guardian

### Description
Configures the Codex app-server to use an 'untrusted' approval policy and route reviews to the 'guardian_subagent'. It also specifies the sandbox and service tier.

### Method
Configuration (JSON)

### Endpoint
N/A

### Request Body
```json
{
  "plugins": {
    "entries": {
      "codex": {
        "enabled": true,
        "config": {
          "appServer": {
            "approvalPolicy": "untrusted",
            "approvalsReviewer": "guardian_subagent",
            "sandbox": "workspace-write",
            "serviceTier": "priority"
          }
        }
      }
    }
  }
}
```

### Response
N/A
```

--------------------------------

### Run Music Generation Live Tests via Repo Wrapper

Source: https://docs.openclaw.ai/tools/music-generation

Use the repository wrapper script to trigger live tests for music generation.

```bash
pnpm test:live:media music
```

--------------------------------

### Run Live Tests

Source: https://docs.openclaw.ai/tools/video-generation

Commands to execute live integration tests for video generation providers.

```bash
OPENCLAW_LIVE_TEST=1 pnpm test:live -- extensions/video-generation-providers.live.test.ts
```

```bash
pnpm test:live:media video
```

```bash
pnpm test:live:media video --video-providers fal
```

--------------------------------

### Multi-Account QQ Bot Setup

Source: https://docs.openclaw.ai/channels/qqbot

This configuration allows running multiple QQ bots under a single OpenClaw instance. Each account requires its own AppID and AppSecret.

```json
{ "channels": { "qqbot": { "enabled": true, "appId": "111111111", "clientSecret": "secret-of-bot-1", "accounts": { "bot2": { "enabled": true, "appId": "222222222", "clientSecret": "secret-of-bot-2" } } } } }
```

--------------------------------

### Run OpenClaw MCP Server

Source: https://docs.openclaw.ai/cli/mcp

Commands for starting the MCP server with various configurations for local or remote Gateway connections and logging.

```bash
# Local Gateway
openclaw mcp serve

# Remote Gateway
openclaw mcp serve --url wss://gateway-host:18789 --token-file ~/.openclaw/gateway.token

# Remote Gateway with password auth
openclaw mcp serve --url wss://gateway-host:18789 --password-file ~/.openclaw/gateway.password

# Enable verbose bridge logs
openclaw mcp serve --verbose

# Disable Claude-specific push notifications
openclaw mcp serve --claude-channel-mode off
```

--------------------------------

### Active Memory Diagnostic Flow Example

Source: https://docs.openclaw.ai/concepts/active-memory

A sample interaction demonstrating how to trigger and view active memory diagnostics.

```text
/verbose on
/trace on
what wings should i order?
```

```text
...normal assistant reply...

🧩 Active Memory: status=ok elapsed=842ms query=recent summary=34 chars
🔎 Active Memory Debug: Lemon pepper wings with blue cheese.
```

--------------------------------

### Verify Available ZAI Models

Source: https://docs.openclaw.ai/providers/glm

List all models available from the Z.AI provider to confirm successful setup and model accessibility.

```bash
openclaw models list --provider zai
```

--------------------------------

### Login and Session Configuration

Source: https://docs.openclaw.ai/channels/wechat

Commands to initiate QR login and configure session scoping for multiple accounts.

```bash
openclaw channels login --channel openclaw-weixin
```

```bash
openclaw config set session.dmScope per-account-channel-peer
```

--------------------------------

### Map Input to Tool Calls

Source: https://docs.openclaw.ai/tools/lobster

Example of mapping search results to individual tool invocations using Lobster piping.

```bash
gog.gmail.search --query 'newer_than:1d' \
  | openclaw.invoke --tool message --action send --each --item-key message --args-json '{"provider":"telegram","to":"..."}'
```

--------------------------------

### Install Twitch Plugin via CLI

Source: https://docs.openclaw.ai/channels/twitch

Use this command to install the Twitch plugin from the npm registry when using an older or custom OpenClaw build.

```bash
openclaw plugins install @openclaw/twitch
```

--------------------------------

### Open Dashboard

Source: https://docs.openclaw.ai/start/getting-started

Launch the Control UI in the default web browser.

```bash
openclaw dashboard
```

--------------------------------

### Manage Ollama Models

Source: https://docs.openclaw.ai/providers/ollama

List installed models and pull new ones to ensure they are available for use.

```bash
ollama list  # See what's installed
ollama pull gemma4
ollama pull gpt-oss:20b
ollama pull llama3.3     # Or another model
```

--------------------------------

### Build and Launch Docker Compose

Source: https://docs.openclaw.ai/install/docker-vm-runtime

Execute these commands to build your Docker image and start the specified service in detached mode. Ensure sufficient memory is available during the build process.

```bash
docker compose build
docker compose up -d openclaw-gateway
```

--------------------------------

### Configure VM Resources

Source: https://docs.openclaw.ai/install/azure

Set VM size and disk parameters, and query available SKUs or usage quotas.

```bash
VM_SIZE="Standard_B2as_v2"
OS_DISK_SIZE_GB=64
```

```bash
az vm list-skus --location "${LOCATION}" --resource-type virtualMachines -o table
```

```bash
az vm list-usage --location "${LOCATION}" -o table
```

--------------------------------

### Web Fetch Tool Usage

Source: https://docs.openclaw.ai/tools/web-fetch

Demonstrates how to use the web_fetch tool to retrieve content from a given URL. The tool is enabled by default and requires no special configuration to start using.

```APIDOC
## POST /tools/web_fetch

### Description
Fetches readable content from a given URL using an HTTP GET request. It does not execute JavaScript and is suitable for extracting text or markdown from static HTML.

### Method
POST

### Endpoint
/tools/web_fetch

### Parameters
#### Request Body
- **url** (string) - Required - The URL to fetch (http/https only).
- **extractMode** (string) - Optional - The extraction mode. Can be "markdown" (default) or "text".
- **maxChars** (number) - Optional - Truncates the output to this many characters.

### Request Example
```json
{
  "url": "https://example.com/article"
}
```

### Response
#### Success Response (200)
- **content** (string) - The extracted content from the URL.

#### Response Example
```json
{
  "content": "<h1>Article Title</h1><p>This is the article content...</p>"
}

```

--------------------------------

### Run Live Tests for Music Generation Providers

Source: https://docs.openclaw.ai/tools/music-generation

Execute live integration tests for bundled music generation providers using the specified test file.

```bash
OPENCLAW_LIVE_TEST=1 pnpm test:live -- extensions/music-generation-providers.live.test.ts
```

--------------------------------

### Automated Shelley Prompt

Source: https://docs.openclaw.ai/install/exe-dev

Use this prompt with the Shelley agent to perform a non-interactive installation and configuration of OpenClaw.

```text
Set up OpenClaw (https://docs.openclaw.ai/install) on this VM. Use the non-interactive and accept-risk flags for openclaw onboarding. Add the supplied auth or token as needed. Configure nginx to forward from the default port 18789 to the root location on the default enabled site config, making sure to enable Websocket support. Pairing is done by "openclaw devices list" and "openclaw devices approve <request id>". Make sure the dashboard shows that OpenClaw's health is OK. exe.dev handles forwarding from port 8000 to port 80/443 and HTTPS for us, so the final "reachable" should be <vm-name>.exe.xyz, without port specification.
```

--------------------------------

### OpenClaw Configuration for Z.AI

Source: https://docs.openclaw.ai/providers/glm

Example configuration file snippet showing environment variables and default agent model settings for Z.AI integration.

```json5
{ env: { ZAI_API_KEY: "sk-..." }, agents: { defaults: { model: { primary: "zai/glm-5.1" } } } }
```

--------------------------------

### Onboard Vercel AI Gateway API Key

Source: https://docs.openclaw.ai/start/wizard-cli-automation

Use this command to onboard with a Vercel AI Gateway API key. Ensure the AI_GATEWAY_API_KEY environment variable is set.

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice ai-gateway-api-key \
  --ai-gateway-api-key "$AI_GATEWAY_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

--------------------------------

### Set Session-Level Exec Overrides

Source: https://docs.openclaw.ai/tools/exec

Example of using the /exec command to configure host, security, ask, and node settings for the current session.

```text
/exec host=auto security=allowlist ask=on-miss node=mac-1
```

--------------------------------

### Switch to Nix Configuration

Source: https://docs.openclaw.ai/install/nix

After configuring secrets and filling in template placeholders, switch to your new Nix configuration using home-manager.

```bash
home-manager switch
```

--------------------------------

### Build the OpenClaw gateway image

Source: https://docs.openclaw.ai/install/docker

Builds the gateway image locally using the setup script. Optionally, set the OPENCLAW_IMAGE environment variable to use a pre-built image from the GitHub Container Registry.

```bash
./scripts/docker/setup.sh
```

```bash
export OPENCLAW_IMAGE="ghcr.io/openclaw/openclaw:latest"
./scripts/docker/setup.sh
```

--------------------------------

### Install OpenClaw (Debug Trace PowerShell)

Source: https://docs.openclaw.ai/install/installer

Enables PowerShell debug tracing for the OpenClaw installation script to diagnose issues. Remember to disable tracing afterwards.

```powershell
# install.ps1 has no dedicated -Verbose flag yet.
Set-PSDebug -Trace 1
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard
Set-PSDebug -Trace 0
```

--------------------------------

### Generate and describe video

Source: https://docs.openclaw.ai/cli/infer

Video commands support generation and description. Video describe requires the --model flag to be in <provider/model> format.

```bash
openclaw infer video generate --prompt "cinematic sunset over the ocean" --json
openclaw infer video generate --prompt "slow drone shot over a forest lake" --json
openclaw infer video describe --file ./clip.mp4 --json
openclaw infer video describe --file ./clip.mp4 --model openai/gpt-4.1-mini --json
```

--------------------------------

### Configure Heartbeat Settings

Source: https://docs.openclaw.ai/gateway/heartbeat

Example JSON5 configuration for setting up heartbeat intervals, delivery targets, and context options. Ensure `agents.defaults.heartbeat.every` is set to `0m` to disable.

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        target: "last", // explicit delivery to last contact (default is "none")
        directPolicy: "allow", // default: allow direct/DM targets; set "block" to suppress
        lightContext: true, // optional: only inject HEARTBEAT.md from bootstrap files
        isolatedSession: true, // optional: fresh session each run (no conversation history)
        // activeHours: { start: "08:00", end: "24:00" },
        // includeReasoning: true, // optional: send separate `Reasoning:` message too
      },
    },
  },
}
```

--------------------------------

### Onboard Mistral API Key

Source: https://docs.openclaw.ai/start/wizard-cli-automation

Use this command to onboard with a Mistral API key. Ensure the MISTRAL_API_KEY environment variable is set.

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice mistral-api-key \
  --mistral-api-key "$MISTRAL_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

--------------------------------

### Repro (Node-only) Command

Source: https://docs.openclaw.ai/debug/node-issue

Run this command in the repository root to reproduce the crash. Ensure you have installed dependencies with pnpm first.

```bash
node --version
pnpm install
node --import tsx src/entry.ts status
```

--------------------------------

### Configure Notification Forwarding Settings

Source: https://docs.openclaw.ai/platforms/android

Example JSON configuration for defining allowed packages, quiet hours, and rate limits for forwarded notifications.

```json5
{
  notifications: {
    allowPackages: ["com.slack", "com.whatsapp"],
    denyPackages: ["com.android.systemui"],
    quietHours: {
      start: "22:00",
      end: "07:00",
    },
    rateLimit: 5,
  },
}
```

--------------------------------

### Add New Agent

Source: https://docs.openclaw.ai/cli/agents

Add a new agent with a specified workspace. Use '--non-interactive' for automated setup. The agent name 'main' is reserved.

```bash
openclaw agents add work --workspace ~/.openclaw/workspace-work
```

```bash
openclaw agents add ops --workspace ~/.openclaw/workspace-ops --bind telegram:ops --non-interactive
```

--------------------------------

### Onboard with OpenAI API Key

Source: https://docs.openclaw.ai/providers/openai

Initialize OpenClaw using an OpenAI API key for direct platform access.

```bash
openclaw onboard --auth-choice openai-api-key
```

```bash
openclaw onboard --openai-api-key "$OPENAI_API_KEY"
```

--------------------------------

### Inspect Context List

Source: https://docs.openclaw.ai/concepts/context

Use the `/context list` command to get a quick overview of your current context window usage, including injected workspace files and their sizes.

```bash
/context list
```

--------------------------------

### View Wizard Metadata

Source: https://docs.openclaw.ai/gateway/configuration-reference

Represents the metadata generated by CLI setup flows like onboard, configure, and doctor.

```json5
{
  wizard: {
    lastRunAt: "2026-01-01T00:00:00.000Z",
    lastRunVersion: "2026.1.4",
    lastRunCommit: "abc1234",
    lastRunCommand: "configure",
    lastRunMode: "local",
  },
}
```

--------------------------------

### Manage OpenClaw plugins via CLI

Source: https://docs.openclaw.ai/tools/plugin

Use these commands to list, inspect, install, update, and configure plugins. Note that some flags like --pin and --dangerously-force-unsafe-install have specific constraints regarding marketplace sources and security scanning.

```bash
openclaw plugins list                       # compact inventory
openclaw plugins list --enabled            # only loaded plugins
openclaw plugins list --verbose            # per-plugin detail lines
openclaw plugins list --json               # machine-readable inventory
openclaw plugins inspect <id>              # deep detail
openclaw plugins inspect <id> --json       # machine-readable
openclaw plugins inspect --all             # fleet-wide table
openclaw plugins info <id>                 # inspect alias
openclaw plugins doctor                    # diagnostics

openclaw plugins install <package>         # install (ClawHub first, then npm)
openclaw plugins install clawhub:<pkg>     # install from ClawHub only
openclaw plugins install <spec> --force    # overwrite existing install
openclaw plugins install <path>            # install from local path
openclaw plugins install -l <path>         # link (no copy) for dev
openclaw plugins install <plugin> --marketplace <source>
openclaw plugins install <plugin> --marketplace https://github.com/<owner>/<repo>
openclaw plugins install <spec> --pin      # record exact resolved npm spec
openclaw plugins install <spec> --dangerously-force-unsafe-install
openclaw plugins update <id>             # update one plugin
openclaw plugins update <id> --dangerously-force-unsafe-install
openclaw plugins update --all            # update all
openclaw plugins uninstall <id>          # remove config/install records
openclaw plugins uninstall <id> --keep-files
openclaw plugins marketplace list <source>
openclaw plugins marketplace list <source> --json

openclaw plugins enable <id>
openclaw plugins disable <id>
```

--------------------------------

### Troubleshoot Gateway Onboarding

Source: https://docs.openclaw.ai/help/faq

Diagnostic and management commands to resolve issues when the Gateway fails to initialize or respond.

```bash
openclaw gateway restart
```

```bash
openclaw status
openclaw models status
openclaw logs --follow
```

```bash
openclaw doctor
```

--------------------------------

### Configure Deferred Loading for Channel Plugins

Source: https://docs.openclaw.ai/plugins/sdk-setup

Enable deferred loading to delay full plugin entry loading until after the gateway starts listening. Ensure setupEntry registers all essential gateway requirements before enabling.

```json
{
  "openclaw": {
    "extensions": ["./index.ts"],
    "setupEntry": "./setup-entry.ts",
    "startup": {
      "deferConfiguredChannelFullLoadUntilAfterListen": true
    }
  }
}
```

--------------------------------

### Install DingTalk Plugin for OpenClaw

Source: https://docs.openclaw.ai/plugins/community

Install the DingTalk plugin for enterprise robot integration. It supports various message types and communication modes via DingTalk clients.

```bash
openclaw plugins install @largezhou/ddingtalk
```

--------------------------------

### Install OpenClaw (Non-interactive Git Bash)

Source: https://docs.openclaw.ai/install/installer

Installs OpenClaw using the Git method in a non-interactive mode via a bash script, setting environment variables for configuration.

```bash
OPENCLAW_INSTALL_METHOD=git OPENCLAW_NO_PROMPT=1 \
  curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
```

--------------------------------

### Configure Hybrid Search and Memory Features

Source: https://docs.openclaw.ai/reference/memory-config

Example configuration for hybrid search, MMR, and temporal decay settings within the agent defaults.

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        query: {
          hybrid: {
            vectorWeight: 0.7,
            textWeight: 0.3,
            mmr: { enabled: true, lambda: 0.7 },
            temporalDecay: { enabled: true, halfLifeDays: 30 },
          },
        },
      },
    },
  },
}
```

--------------------------------

### Define OpenClaw extensions in package.json

Source: https://docs.openclaw.ai/plugins/architecture

Basic configuration for a plugin pack, specifying extension files and an optional setup entry point.

```json
{
  "name": "my-pack",
  "openclaw": {
    "extensions": ["./src/safety.ts", "./src/tools.ts"],
    "setupEntry": "./src/setup-entry.ts"
  }
}
```

--------------------------------

### Manage Skills via CLI

Source: https://docs.openclaw.ai/tools/skills

Common commands for installing, updating, and syncing skills using the OpenClaw and ClawHub CLI tools.

```bash
openclaw skills install <skill-slug>
```

```bash
openclaw skills update --all
```

```bash
clawhub sync --all
```

--------------------------------

### Onboard with AI Gateway Auth

Source: https://docs.openclaw.ai/providers/vercel-ai-gateway

Run the onboarding process and select the AI Gateway authentication option. This sets up your project to use the Vercel AI Gateway.

```bash
openclaw onboard --auth-choice ai-gateway-api-key
```

--------------------------------

### Configure Agent Access Profiles

Source: https://docs.openclaw.ai/gateway/configuration-reference

Examples of defining agent configurations with varying levels of sandbox restrictions and tool permissions.

```json5
{
  agents: {
    list: [
      {
        id: "personal",
        workspace: "~/.openclaw/workspace-personal",
        sandbox: { mode: "off" },
      },
    ],
  },
}
```

```json5
{
  agents: {
    list: [
      {
        id: "family",
        workspace: "~/.openclaw/workspace-family",
        sandbox: { mode: "all", scope: "agent", workspaceAccess: "ro" },
        tools: {
          allow: [
            "read",
            "sessions_list",
            "sessions_history",
            "sessions_send",
            "sessions_spawn",
            "session_status",
          ],
          deny: ["write", "edit", "apply_patch", "exec", "process", "browser"],
        },
      },
    ],
  },
}
```

```json5
{
  agents: {
    list: [
      {
        id: "public",
        workspace: "~/.openclaw/workspace-public",
        sandbox: { mode: "all", scope: "agent", workspaceAccess: "none" },
        tools: {
          allow: [
            "sessions_list",
            "sessions_history",
            "sessions_send",
            "sessions_spawn",
            "session_status",
            "whatsapp",
            "telegram",
            "slack",
            "discord",
            "gateway",
          ],
          deny: [
            "read",
            "write",
            "edit",
            "apply_patch",
            "exec",
            "process",
            "browser",
            "canvas",
            "nodes",
            "cron",
            "gateway",
            "image",
          ],
        },
      },
    ],
  },
}
```

--------------------------------

### POST /sessions/spawn - Start New ACP Session

Source: https://docs.openclaw.ai/tools/acp-agents

Initiates a new ACP session. This is the primary method for starting an ACP session from an agent turn or tool call.

```APIDOC
## POST /sessions/spawn

### Description
Starts a new ACP (Agent Communication Protocol) session.

### Method
POST

### Endpoint
/sessions/spawn

### Parameters
#### Request Body
- **task** (string) - Required - The initial prompt or task to be sent to the ACP session.
- **runtime** (string) - Required - Must be set to "acp" to initiate an ACP session. Defaults to "subagent".
- **agentId** (string) - Optional - The target harness ID for the ACP session. If omitted, OpenClaw uses the configured `acp.defaultAgent`.
- **thread** (boolean) - Optional (default `false`) - Requests thread binding for a persistent conversation if supported by the runtime.
- **mode** (string) - Optional (default `"run"`) - Specifies the session mode. Can be `"run"` (one-shot) or `"session"` (persistent). `"session"` mode requires `thread: true`.
- **cwd** (string) - Optional - The requested runtime working directory. If omitted, ACP spawn inherits the target agent workspace or falls back to backend defaults.
- **label** (string) - Optional - An operator-facing label for the session.
- **resumeSessionId** (string) - Optional - The ID of an existing ACP session to resume. Requires `runtime: "acp"`.
- **streamTo** (string) - Optional - If set to `"parent"`, streams initial ACP run progress summaries back to the requester as system events. May provide `streamLogPath` for tailing.

### Request Example
```json
{
  "task": "Open the repo and summarize failing tests",
  "runtime": "acp",
  "agentId": "codex",
  "thread": true,
  "mode": "session"
}
```

### Response
#### Success Response (200)
- **childSessionKey** (string) - A key identifying the newly spawned child session.
- **accepted** (string) - Indicates if the session spawn was accepted ('yes' or 'no').
- **error** (string) - Any error message encountered during session spawning.

#### Response Example
```json
{
  "accepted": "yes",
  "childSessionKey": "<session-key>",
  "error": null
}
```
```

--------------------------------

### Install WeCom Plugin for OpenClaw

Source: https://docs.openclaw.ai/plugins/community

Install the WeCom plugin for integration with WeCom. It supports direct messages, group chats, streaming replies, and various message processing capabilities.

```bash
openclaw plugins install @wecom/wecom-openclaw-plugin
```

--------------------------------

### Manual Compaction with Instructions

Source: https://docs.openclaw.ai/concepts/compaction

Manually trigger compaction in a chat by typing '/compact' followed by specific instructions to guide the summarization process.

```text
/compact Focus on the API design decisions
```

--------------------------------

### Xiaomi MiMo Configuration Example

Source: https://docs.openclaw.ai/providers/xiaomi

This JSON configuration sets up the Xiaomi MiMo provider, including environment variables, default model settings, and detailed model metadata. It's useful for overriding default behavior or specifying custom model parameters.

```json5
{
  env: { XIAOMI_API_KEY: "your-key" },
  agents: { defaults: { model: { primary: "xiaomi/mimo-v2-flash" } } },
  models: {
    mode: "merge",
    providers: {
      xiaomi: {
        baseUrl: "https://api.xiaomimimo.com/v1",
        api: "openai-completions",
        apiKey: "XIAOMI_API_KEY",
        models: [
          {
            id: "mimo-v2-flash",
            name: "Xiaomi MiMo V2 Flash",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 262144,
            maxTokens: 8192,
          },
          {
            id: "mimo-v2-pro",
            name: "Xiaomi MiMo V2 Pro",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 1048576,
            maxTokens: 32000,
          },
          {
            id: "mimo-v2-omni",
            name: "Xiaomi MiMo V2 Omni",
            reasoning: true,
            input: ["text", "image"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 262144,
            maxTokens: 32000,
          },
        ],
      },
    },
  },
}
```

--------------------------------

### Install Prometheus Avatar Plugin

Source: https://docs.openclaw.ai/plugins/community

Install the Prometheus Avatar plugin to integrate a Live2D avatar with real-time lip-sync and text-to-speech capabilities for your OpenClaw agent. This plugin is currently in alpha.

```bash
openclaw plugins install @prometheusavatar/openclaw-plugin
```

--------------------------------

### Apply Patch Tool Usage

Source: https://docs.openclaw.ai/tools/apply-patch

Example of how to invoke the apply_patch tool with a specific file update. Ensure the input string correctly formats the patch content.

```json
{
  "tool": "apply_patch",
  "input": "*** Begin Patch\n*** Update File: src/index.ts\n@@\n-const foo = 1\n+const foo = 2\n*** End Patch"
}
```

--------------------------------

### Non-interactive Standard Onboarding

Source: https://docs.openclaw.ai/providers/stepfun

Perform onboarding without interactive prompts by providing the API key directly.

```bash
openclaw onboard --auth-choice stepfun-standard-api-key-intl \
  --stepfun-api-key "$STEPFUN_API_KEY"
```

--------------------------------

### Install Apify Plugin for OpenClaw

Source: https://docs.openclaw.ai/plugins/community

Install the Apify plugin to enable web scraping capabilities within OpenClaw. This plugin allows agents to extract data from various websites.

```bash
openclaw plugins install @apify/apify-openclaw-plugin
```

--------------------------------

### Per-Channel vs Per-Account Heartbeat Configuration Example

Source: https://docs.openclaw.ai/gateway/heartbeat

Demonstrates how to set default heartbeat settings and then apply specific overrides for Slack and Telegram channels, including account-specific settings for suppressing alerts.

```yaml
channels:
  defaults:
    heartbeat:
      showOk: false
      showAlerts: true
      useIndicator: true
  slack:
    heartbeat:
      showOk: true # all Slack accounts
    accounts:
      ops:
        heartbeat:
          showAlerts: false # suppress alerts for the ops account only
  telegram:
    heartbeat:
      showOk: true

```

--------------------------------

### Configure custom providers non-interactively

Source: https://docs.openclaw.ai/cli/onboard

Automate onboarding for custom API providers by specifying base URLs, model IDs, and authentication keys.

```bash
openclaw onboard --non-interactive \
  --auth-choice custom-api-key \
  --custom-base-url "https://llm.example.com/v1" \
  --custom-model-id "foo-large" \
  --custom-api-key "$CUSTOM_API_KEY" \
  --secret-input-mode plaintext \
  --custom-compatibility openai
```

--------------------------------

### Enable private data logging for OpenClaw

Source: https://docs.openclaw.ai/platforms/mac/logging

Creates and installs a plist file to disable privacy redaction for the ai.openclaw subsystem. Requires root privileges to install the configuration file.

```bash
cat <<'EOF' >/tmp/ai.openclaw.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>DEFAULT-OPTIONS</key>
    <dict>
        <key>Enable-Private-Data</key>
        <true/>
    </dict>
</dict>
</plist>
EOF
sudo install -m 644 -o root -g wheel /tmp/ai.openclaw.plist /Library/Preferences/Logging/Subsystems/ai.openclaw.plist
```

--------------------------------

### Install OpenClaw (Non-interactive npm Bash)

Source: https://docs.openclaw.ai/install/installer

Installs OpenClaw using npm in a non-interactive mode via a bash script. This is suitable for automated environments like CI/CD pipelines.

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --no-prompt --no-onboard
```

--------------------------------

### Onboard with Z.AI for GLM Models

Source: https://docs.openclaw.ai/providers/glm

Use these commands to onboard with Z.AI, choosing an authentication route that matches your plan and region. The `zai-api-key` choice enables automatic endpoint detection.

```bash
openclaw onboard --auth-choice zai-api-key
```

```bash
openclaw onboard --auth-choice zai-coding-global
```

--------------------------------

### Agent and Binding Configuration

Source: https://docs.openclaw.ai/channels/channel-routing

Define agents with their workspace and configure bindings to map inbound channels and peers to specific agents. This example sets up a 'support' agent and binds Slack and Telegram channels to it.

```json5
{
  agents: {
    list: [{ id: "support", name: "Support", workspace: "~/.openclaw/workspace-support" }],
  },
  bindings: [
    { match: { channel: "slack", teamId: "T123" }, agentId: "support" },
    { match: { channel: "telegram", peer: { kind: "group", id: "-100123" } }, agentId: "support" },
  ],
}
```

--------------------------------

### Configure npm Global Prefix for Permissions (Linux)

Source: https://docs.openclaw.ai/install/node

Change npm's global installation directory to a user-writable location to avoid EACCES permission errors during global installs.

```bash
mkdir -p "$HOME/.npm-global"
npm config set prefix "$HOME/.npm-global"
export PATH="$HOME/.npm-global/bin:$PATH"
```

--------------------------------

### Configure macOS LaunchAgent for Proxy Auto-start

Source: https://docs.openclaw.ai/providers/claude-max-api-proxy

Creates a LaunchAgent plist file and bootstraps it with launchctl to ensure the proxy service runs automatically on macOS.

```bash
cat > ~/Library/LaunchAgents/com.claude-max-api.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.claude-max-api</string>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/local/bin/node</string>
    <string>/usr/local/lib/node_modules/claude-max-api-proxy/dist/server/standalone.js</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>/usr/local/bin:/opt/homebrew/bin:~/.local/bin:/usr/bin:/bin</string>
  </dict>
</dict>
</plist>
EOF

launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.claude-max-api.plist
```

--------------------------------

### Run QA and Environment Tests

Source: https://docs.openclaw.ai/help/testing

Commands for launching Docker-backed or Linux VM-backed QA environments.

```bash
pnpm qa:lab:up
```

```bash
pnpm openclaw qa suite --runner multipass --scenario channel-chat-baseline
```

--------------------------------

### Isolated Session Context Examples

Source: https://docs.openclaw.ai/channels/broadcast-groups

Displays the distinct session, history, workspace, and tool configurations for two separate agents in the same group.

```text
Session: agent:alfred:whatsapp:group:120363403215116621@g.us
History: [user message, alfred's previous responses]
Workspace: /Users/user/openclaw-alfred/
Tools: read, write, exec
```

```text
Session: agent:baerbel:whatsapp:group:120363403215116621@g.us
History: [user message, baerbel's previous responses]
Workspace: /Users/user/openclaw-baerbel/
Tools: read only
```

--------------------------------

### CLI Command: configure

Source: https://docs.openclaw.ai/cli

Interactive configuration wizard for models, channels, skills, and gateway.

```APIDOC
## CLI Command: configure

### Description
Interactive configuration wizard for models, channels, skills, and gateway.

### Parameters
#### Options
- **--section** (string) - Optional - Repeatable; limit the wizard to specific sections
```

--------------------------------

### Direct Music Generation Example

Source: https://docs.openclaw.ai/tools/music-generation

Generate a dreamy lo-fi hip hop track with vinyl texture and gentle rain, specifying instrumental output.

```text
/tool music_generate prompt="Dreamy lo-fi hip hop with vinyl texture and gentle rain" instrumental=true
```

--------------------------------

### Build and Run macOS App

Source: https://docs.openclaw.ai/platforms/macos

Standard commands for building the native macOS application and packaging the app.

```bash
cd apps/macos && swift build
swift run OpenClaw
scripts/package-mac-app.sh
```

--------------------------------

### Execute OpenClaw CLI commands

Source: https://docs.openclaw.ai/concepts/model-providers

Common commands for onboarding, setting the active model, and listing available models.

```bash
openclaw onboard --auth-choice opencode-zen
openclaw models set opencode/claude-opus-4-6
openclaw models list
```

--------------------------------

### Install Playwright Browsers in Docker

Source: https://docs.openclaw.ai/help/faq

Use this command to install Playwright browsers within a Docker container for full feature support. Ensure the path is persisted and set via PLAYWRIGHT_BROWSERS_PATH.

```bash
node /app/node_modules/playwright-core/cli.js install chromium
```

--------------------------------

### Brave Search API Configuration

Source: https://docs.openclaw.ai/tools/brave-search

Configuration example for setting up Brave Search as a web search provider. This includes API key, search mode, and general web search tool settings.

```APIDOC
## Brave Search API Configuration

### Description
Configuration for integrating Brave Search as a web search provider. This example shows how to set the API key, choose the search mode (`web` or `llm-context`), and define general web search tool parameters like `maxResults` and `timeoutSeconds`.

### Config Example
```json5
{
  plugins: {
    entries: {
      brave: {
        config: {
          webSearch: {
            apiKey: "BRAVE_API_KEY_HERE",
            mode: "web", // or "llm-context"
          },
        },
      },
    },
  },
  tools: {
    web: {
      search: {
        provider: "brave",
        maxResults: 5,
        timeoutSeconds: 30,
      },
    },
  },
}
```

### Notes
- Provider-specific Brave search settings are located under `plugins.entries.brave.config.webSearch.*`.
- Legacy `tools.web.search.apiKey` is supported for compatibility but is no longer the canonical path.
- `webSearch.mode` determines the Brave transport: `web` for standard search results, `llm-context` for grounded text chunks and sources.
```

--------------------------------

### Apply Full Configuration via RPC

Source: https://docs.openclaw.ai/configuration

Use `config.apply` to validate and write the entire configuration, followed by a Gateway restart. Provide the full JSON5 payload in `raw` and the `baseHash` from `config.get` if the config already exists. Optional parameters include `sessionKey`, `note`, and `restartDelayMs`.

```bash
openclaw gateway call config.get --params '{}'  # capture payload.hash
```

```bash
openclaw gateway call config.apply --params '{
  "raw": "{ agents: { defaults: { workspace: \"~/.openclaw/workspace\" } } }",
  "baseHash": "<hash>",
  "sessionKey": "agent:main:whatsapp:direct:+15555550123"
}'

```

--------------------------------

### OpenClaw Configuration Structure

Source: https://docs.openclaw.ai/install/fly

Example JSON configuration for the OpenClaw gateway, including Discord channel bindings and gateway mode settings.

```json
        }
      },
      "bindings": [
        {
          "agentId": "main",
          "match": { "channel": "discord" }
        }
      ],
      "channels": {
        "discord": {
          "enabled": true,
          "groupPolicy": "allowlist",
          "guilds": {
            "YOUR_GUILD_ID": {
              "channels": { "general": { "allow": true } },
              "requireMention": false
            }
          }
        }
      },
      "gateway": {
        "mode": "local",
        "bind": "auto"
      },
      "meta": {}
    }
    EOF
```

--------------------------------

### Install Tlon Plugin via CLI

Source: https://docs.openclaw.ai/channels/tlon

Install the Tlon plugin from the npm registry using the OpenClaw CLI. This is for users who need to add the plugin to older or custom OpenClaw builds.

```bash
openclaw plugins install @openclaw/tlon
```

--------------------------------

### Import Account Core Helpers

Source: https://docs.openclaw.ai/plugins/sdk-channel-plugins

Use `openclaw/plugin-sdk/account-core`, `openclaw/plugin-sdk/account-id`, `openclaw/plugin-sdk/account-resolution`, and `openclaw/plugin-sdk/account-helpers` for multi-account configuration and default-account fallback.

```javascript
openclaw/plugin-sdk/account-core
```

```javascript
openclaw/plugin-sdk/account-id
```

```javascript
openclaw/plugin-sdk/account-resolution
```

```javascript
openclaw/plugin-sdk/account-helpers
```

--------------------------------

### Configure Gemini as Active Memory Provider

Source: https://docs.openclaw.ai/concepts/active-memory

Example configuration to set Gemini as the memory search provider. After changing the provider, restart the gateway and run a test with `/trace on` to verify the new embedding path.

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        provider: "gemini",
      },
    },
  },
}
```

--------------------------------

### Run OpenShell Backend E2E Smoke Test

Source: https://docs.openclaw.ai/help/testing

Starts an isolated OpenShell gateway via Docker, creates a sandbox, and exercises the OpenShell backend using SSH exec. Requires a local `openshell` CLI and Docker daemon.

```bash
pnpm test:e2e:openshell
```

--------------------------------

### Run Live Provider Tests

Source: https://docs.openclaw.ai/help/testing

Commands for debugging real-world model and provider integrations using live credentials.

```bash
pnpm test:live
```

```bash
pnpm test:live -- src/agents/models.profiles.live.test.ts
```

--------------------------------

### Outbound Media Attachment Example

Source: https://docs.openclaw.ai/start/openclaw

Include `MEDIA:<path-or-url>` on a new line to send attachments like images or documents from the agent. This example shows sending a PNG image from a URL.

```text
Here’s the screenshot.
MEDIA:https://example.com/screenshot.png
```

--------------------------------

### Install OpenClaw Gateway with Force Option

Source: https://docs.openclaw.ai/help/faq

Use this command to reinstall the OpenClaw Gateway, forcing the installation. This is useful for resolving configuration mismatches or ensuring the service uses the intended profile and environment.

```bash
openclaw gateway install --force
```

--------------------------------

### Configure UFW DOCKER-USER Firewall Rules

Source: https://docs.openclaw.ai/gateway/security

Append these rules to /etc/ufw/after.rules to manage Docker traffic alignment with firewall policies. This example creates a minimal allowlist for IPv4 traffic.

```bash
# /etc/ufw/after.rules (append as its own *filter section)
*filter
:DOCKER-USER - [0:0]
-A DOCKER-USER -m conntrack --ctstate ESTABLISHED,RELATED -j RETURN
-A DOCKER-USER -s 127.0.0.0/8 -j RETURN
-A DOCKER-USER -s 10.0.0.0/8 -j RETURN
-A DOCKER-USER -s 172.16.0.0/12 -j RETURN
-A DOCKER-USER -s 192.168.0.0/16 -j RETURN
-A DOCKER-USER -s 100.64.0.0/10 -j RETURN
-A DOCKER-USER -p tcp --dport 80 -j RETURN
-A DOCKER-USER -p tcp --dport 443 -j RETURN
-A DOCKER-USER -m conntrack --ctstate NEW -j DROP
-A DOCKER-USER -j RETURN
COMMIT

```

--------------------------------

### Configure tool parameters for run and resume

Source: https://docs.openclaw.ai/tools/lobster

Advanced execution parameters including pipeline strings, working directories, and argument passing.

```json
{
  "action": "run",
  "pipeline": "gog.gmail.search --query 'newer_than:1d' | email.triage",
  "cwd": "workspace",
  "timeoutMs": 30000,
  "maxStdoutBytes": 512000
}
```

```json
{
  "action": "run",
  "pipeline": "/path/to/inbox-triage.lobster",
  "argsJson": "{\"tag\":\"family\"}"
}
```

```json
{
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

--------------------------------

### Status Output Example for Media Processing

Source: https://docs.openclaw.ai/nodes/media-understanding

This is an example of the status output line generated when media understanding runs. It summarizes the outcome for each capability (e.g., 'ok', 'skipped') and indicates the provider and model used.

```text
📎 Media: image ok (openai/gpt-5.4-mini) · audio skipped (maxBytes)
```

--------------------------------

### Schedule WSL to start at Windows boot

Source: https://docs.openclaw.ai/platforms/windows

Configures Windows Task Scheduler to launch WSL automatically when the system boots. Replace 'Ubuntu' with your specific WSL distribution name.

```powershell
schtasks /create /tn "WSL Boot" /tr "wsl.exe -d Ubuntu --exec /bin/true" /sc onstart /ru SYSTEM
```

--------------------------------

### Openclaw Wiki Apply Synthesis Command

Source: https://docs.openclaw.ai/cli/wiki

Example of using `openclaw wiki apply synthesis` to create or update a synthesis page. Requires a title, body, and source ID.

```bash
openclaw wiki apply synthesis "Alpha Summary" \
  --body "Short synthesis body" \
  --source-id source.alpha
```

--------------------------------

### Perplexity Search API Usage Examples

Source: https://docs.openclaw.ai/tools/perplexity-search

Demonstrates various configurations for the web_search function, including geographic filtering, time-based constraints, domain filtering, and token budget management.

```javascript
// Country and language-specific search
await web_search({
  query: "renewable energy",
  country: "DE",
  language: "de",
});

// Recent results (past week)
await web_search({
  query: "AI news",
  freshness: "week",
});

// Date range search
await web_search({
  query: "AI developments",
  date_after: "2024-01-01",
  date_before: "2024-06-30",
});

// Domain filtering (allowlist)
await web_search({
  query: "climate research",
  domain_filter: ["nature.com", "science.org", ".edu"],
});

// Domain filtering (denylist - prefix with -)
await web_search({
  query: "product reviews",
  domain_filter: ["-reddit.com", "-pinterest.com"],
});

// More content extraction
await web_search({
  query: "detailed AI research",
  max_tokens: 50000,
  max_tokens_per_page: 4096,
});
```

--------------------------------

### Onboard Moonshot API Key

Source: https://docs.openclaw.ai/start/wizard-cli-automation

Use this command to onboard with a Moonshot API key. Ensure the MOONSHOT_API_KEY environment variable is set.

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice moonshot-api-key \
  --moonshot-api-key "$MOONSHOT_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

--------------------------------

### GET /chat.history

Source: https://docs.openclaw.ai/web/control-ui

Retrieves the chat transcript history for a session.

```APIDOC
## GET /chat.history

### Description
Retrieves the chat transcript history. Responses are size-bounded for UI safety; large messages may be truncated or replaced with placeholders.

### Method
GET

### Endpoint
/chat.history
```

--------------------------------

### GET /hooks/info

Source: https://docs.openclaw.ai/cli/hooks

Show detailed information about a specific hook.

```APIDOC
## GET /hooks/info

### Description
Show detailed information about a specific hook.

### Method
GET

### Endpoint
openclaw hooks info <name>

### Parameters
#### Path Parameters
- **name** (string) - Required - Hook name or hook key

#### Query Parameters
- **--json** (flag) - Optional - Output as JSON
```

--------------------------------

### Implement Channel Plugin with createChatChannelPlugin

Source: https://docs.openclaw.ai/plugins/sdk-channel-plugins

Build a chat channel plugin by providing configuration options to `createChatChannelPlugin`. This example sets up account resolution, security policies, pairing, threading, and outbound message sending.

```typescript
import {
  createChatChannelPlugin,
  createChannelPluginBase,
} from "openclaw/plugin-sdk/channel-core";
import type { OpenClawConfig } from "openclaw/plugin-sdk/channel-core";
import { acmeChatApi } from "./client.js"; // your platform API client

type ResolvedAccount = {
  accountId: string | null;
  token: string;
  allowFrom: string[];
  dmPolicy: string | undefined;
};

function resolveAccount(
  cfg: OpenClawConfig,
  accountId?: string | null,
): ResolvedAccount {
  const section = (cfg.channels as Record<string, any>)?.["acme-chat"];
  const token = section?.token;
  if (!token) throw new Error("acme-chat: token is required");
  return {
    accountId: accountId ?? null,
    token,
    allowFrom: section?.allowFrom ?? [],
    dmPolicy: section?.dmSecurity,
  };
}

export const acmeChatPlugin = createChatChannelPlugin<ResolvedAccount>({
  base: createChannelPluginBase({
    id: "acme-chat",
    setup: {
      resolveAccount,
      inspectAccount(cfg, accountId) {
        const section =
          (cfg.channels as Record<string, any>)?.["acme-chat"];
        return {
          enabled: Boolean(section?.token),
          configured: Boolean(section?.token),
          tokenStatus: section?.token ? "available" : "missing",
        };
      },
    },
  }),

  // DM security: who can message the bot
  security: {
    dm: {
      channelKey: "acme-chat",
      resolvePolicy: (account) => account.dmPolicy,
      resolveAllowFrom: (account) => account.allowFrom,
      defaultPolicy: "allowlist",
    },
  },

  // Pairing: approval flow for new DM contacts
  pairing: {
    text: {
      idLabel: "Acme Chat username",
      message: "Send this code to verify your identity:",
      notify: async ({ target, code }) => {
        await acmeChatApi.sendDm(target, `Pairing code: ${code}`);
      },
    },
  },

  // Threading: how replies are delivered
  threading: { topLevelReplyToMode: "reply" },

  // Outbound: send messages to the platform
  outbound: {
    attachedResults: {
      sendText: async (params) => {
        const result = await acmeChatApi.sendMessage(
          params.to,
          params.text,
        );
        return { messageId: result.id };
      },
    },
    base: {
      sendMedia: async (params) => {
        await acmeChatApi.sendFile(params.to, params.filePath);
      },
    },
  },
});

```

--------------------------------

### List Available Models (OAuth)

Source: https://docs.openclaw.ai/providers/minimax

Verify model availability after OAuth onboarding using the minimax-portal provider.

```bash
openclaw models list --provider minimax-portal
```

--------------------------------

### Onboard Gemini API Key

Source: https://docs.openclaw.ai/providers/google

Commands to initialize the Gemini provider using an API key, either interactively or by passing the key directly.

```bash
openclaw onboard --auth-choice gemini-api-key
```

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice gemini-api-key \
  --gemini-api-key "$GEMINI_API_KEY"
```

--------------------------------

### Build Control UI Static Files

Source: https://docs.openclaw.ai/web/control-ui

Commands to build the static assets for the Control UI.

```bash
pnpm ui:build
```

```bash
OPENCLAW_CONTROL_UI_BASE_PATH=/openclaw/ pnpm ui:build
```

--------------------------------

### GET /health

Source: https://docs.openclaw.ai/cli/health

Fetches the health status of the running OpenClaw Gateway.

```APIDOC
## GET /health

### Description
Fetch health status from the running Gateway. By default, it returns a cached snapshot if available, otherwise it performs a fresh probe.

### Method
GET

### Endpoint
openclaw health

### Parameters
#### Query Parameters
- **--json** (flag) - Optional - Returns machine-readable output.
- **--timeout** (integer) - Optional - Connection timeout in milliseconds (default 10000).
- **--verbose** (flag) - Optional - Forces a live probe and prints detailed gateway connection info.
- **--debug** (flag) - Optional - Alias for --verbose.

### Request Example
openclaw health --json --timeout 2500

### Response
#### Success Response (200)
- **status** (object) - Health snapshot of the gateway, including per-agent session stores if multiple agents are configured.
```

--------------------------------

### Example TTS Directives in Reply Payload

Source: https://docs.openclaw.ai/tools/tts

This example shows how to use `[[tts:...]]` directives within a reply payload to override voice and provide expressive text for audio output. The `[[tts:text]]...[[/tts:text]]` block is for expressive tags like laughter or singing cues.

```text
Here you go.

[[tts:voiceId=pMsXgVXv3BLzUgSXRplE model=eleven_v3 speed=1.1]]
[[tts:text]](laughs) Read the song once more.[[/tts:text]]
```

--------------------------------

### PDF Tool Configuration Example

Source: https://docs.openclaw.ai/tools/pdf

This JSON configuration sets default models and limits for the PDF tool, including primary and fallback PDF models, maximum bytes per PDF, and maximum pages for extraction.

```json
{
  agents: {
    defaults: {
      pdfModel: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["openai/gpt-5.4-mini"],
      },
      pdfMaxBytesMb: 10,
      pdfMaxPages: 20,
    },
  },
}
```

--------------------------------

### Run Full Gate Tests

Source: https://docs.openclaw.ai/help/testing

Execute the complete suite of build, type checking, and tests required before pushing code.

```bash
pnpm build && pnpm check && pnpm check:test-types && pnpm test
```

--------------------------------

### Gateway RPC: Get Status

Source: https://docs.openclaw.ai/plugins/voice-call

The `voicecall.status` RPC method. Requires `callId`.

```rpc
voicecall.status (`callId`)
```

--------------------------------

### Snap Package Warning

Source: https://docs.openclaw.ai/tools/browser-linux-troubleshooting

Output indicating that the installed chromium package is a snap wrapper.

```text
Note, selecting 'chromium-browser' instead of 'chromium'
chromium-browser is already the newest version (2:1snap1-0ubuntu2).
```

--------------------------------

### List Kimi Models

Source: https://docs.openclaw.ai/providers/moonshot

Verify that Kimi models are available by listing them using the 'kimi' provider.

```bash
openclaw models list --provider kimi
```

--------------------------------

### Skills Management API

Source: https://docs.openclaw.ai/cli

Endpoints for searching, installing, updating, and inspecting workspace skills.

```APIDOC
## GET /skills

### Description
List available skills in the workspace.

### Parameters
#### Query Parameters
- **json** (boolean) - Optional - Emit machine-readable output.
- **verbose** (boolean) - Optional - Include missing requirements in the table.

## POST /skills/install

### Description
Install a skill from ClawHub into the active workspace.

### Parameters
#### Request Body
- **slug** (string) - Required - The skill identifier.
- **version** (string) - Optional - Specific version to install.
- **force** (boolean) - Optional - Overwrite existing skill folder.
```

--------------------------------

### Skills Management API

Source: https://docs.openclaw.ai/cli/index

Commands for searching, installing, updating, and inspecting workspace skills.

```APIDOC
## skills

### Description
List and inspect available skills plus readiness info.

### Subcommands
- **skills search [query...]**: search ClawHub skills.
- **skills install <slug>**: install a skill from ClawHub into the active workspace.
- **skills update <slug|--all>**: update tracked ClawHub skills.
- **skills list**: list skills.
- **skills info <name>**: show details for one skill.
- **skills check**: summary of ready vs missing requirements.
```

--------------------------------

### Configure OpenClaw Models

Source: https://docs.openclaw.ai/providers/lmstudio

Commands to run onboarding or manually set the active model.

```bash
openclaw onboard
```

```bash
openclaw models set lmstudio/qwen/qwen3.5-9b
```

--------------------------------

### Onboard Custom Provider

Source: https://docs.openclaw.ai/start/wizard-cli-automation

Use this command to onboard a custom AI provider. The `--custom-api-key` is optional and defaults to the CUSTOM_API_KEY environment variable if omitted. The ref-mode variant stores the API key as a reference.

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice custom-api-key \
  --custom-base-url "https://llm.example.com/v1" \
  --custom-model-id "foo-large" \
  --custom-api-key "$CUSTOM_API_KEY" \
  --custom-provider-id "my-custom" \
  --custom-compatibility anthropic \
  --gateway-port 18789 \
  --gateway-bind loopback
```

```bash
export CUSTOM_API_KEY="your-key"
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice custom-api-key \
  --custom-base-url "https://llm.example.com/v1" \
  --custom-model-id "foo-large" \
  --secret-input-mode ref \
  --custom-provider-id "my-custom" \
  --custom-compatibility anthropic \
  --gateway-port 18789 \
  --gateway-bind loopback
```

--------------------------------

### Create Nextcloud Talk Bot

Source: https://docs.openclaw.ai/channels/nextcloud-talk

Command to install a bot on your Nextcloud server. Replace placeholders with your bot name, shared secret, and webhook URL. The `--feature reaction` flag enables reaction support.

```bash
./occ talk:bot:install "OpenClaw" "<shared-secret>" "<webhook-url>" --feature reaction
```

--------------------------------

### ACP Command Examples

Source: https://docs.openclaw.ai/tools/acp-agents

Commonly used ACP commands for session management and configuration.

```text
/acp spawn codex --bind here --cwd /repo
```

```text
/acp cancel agent:codex:acp:<uuid>
```

```text
/acp steer --session support inbox prioritize failing tests
```

```text
/acp close
```

```text
/acp status
```

```text
/acp set-mode plan
```

```text
/acp set model openai/gpt-5.4
```

```text
/acp cwd /Users/user/Projects/repo
```

```text
/acp permissions strict
```

```text
/acp timeout 120
```

```text
/acp model anthropic/claude-opus-4-6
```

```text
/acp reset-options
```

```text
/acp sessions
```

```text
/acp doctor
```

```text
/acp install
```

--------------------------------

### CLI command to enable Tailscale Serve

Source: https://docs.openclaw.ai/gateway/tailscale

Use this command to enable Tailscale Serve mode for the OpenClaw Gateway via the command line. Ensure the `tailscale` CLI is installed and logged in.

```bash
openclaw gateway --tailscale serve
```

--------------------------------

### Task Status Summary Output

Source: https://docs.openclaw.ai/automation/tasks

Example output format for the openclaw status command.

```text
Tasks: 3 queued · 2 running · 1 issues
```

--------------------------------

### Location Caption Formatting

Source: https://docs.openclaw.ai/channels/location

Example of how a location pin is rendered when accompanied by a user-provided caption.

```text
📍 48.858844, 2.294351 ±12m
Meet here
```

--------------------------------

### Verify system readiness

Source: https://docs.openclaw.ai/gateway

Run these commands to check the status of the gateway, channels, and overall system health.

```bash
openclaw gateway status
openclaw channels status --probe
openclaw health
```

--------------------------------

### Configure Update Settings

Source: https://docs.openclaw.ai/gateway/configuration-reference

Set the release channel, enable update checks on startup, and configure auto-update behavior.

```json5
{
  update: {
    channel: "stable", // stable | beta | dev
    checkOnStart: true,

    auto: {
      enabled: false,
      stableDelayHours: 6,
      stableJitterHours: 12,
      betaCheckIntervalHours: 1,
    },
  },
}
```

--------------------------------

### Onboard Runway API Key

Source: https://docs.openclaw.ai/providers/runway

Use this command to set up authentication for the Runway provider by providing your API key.

```bash
openclaw onboard --auth-choice runway-api-key
```

--------------------------------

### Manage Hooks via CLI

Source: https://docs.openclaw.ai/automation/hooks

Use these commands to list, enable, verify, and inspect hook configurations.

```bash
# List available hooks
openclaw hooks list

# Enable a hook
openclaw hooks enable session-memory

# Check hook status
openclaw hooks check

# Get detailed information
openclaw hooks info session-memory
```

--------------------------------

### Execute Gmail Webhook Watcher

Source: https://docs.openclaw.ai/cli/webhooks

Command to start the Gmail watch and auto-renew loop.

```bash
openclaw webhooks gmail run --account you@example.com
```

--------------------------------

### Run a simple agent turn

Source: https://docs.openclaw.ai/tools/agent-send

Sends a message through the Gateway and prints the reply.

```bash
openclaw agent --message "What is the weather today?"
```

--------------------------------

### CLI Configuration Management

Source: https://docs.openclaw.ai/configuration

Commands for getting, setting, or unsetting specific configuration keys.

```bash
openclaw config get agents.defaults.workspace
openclaw config set agents.defaults.heartbeat.every "2h"
openclaw config unset plugins.entries.brave.config.webSearch.apiKey
```

--------------------------------

### Get OpenClaw Plugin Info

Source: https://docs.openclaw.ai/cli/plugins

Retrieve information about a specific plugin using its ID.

```bash
openclaw plugins info <id>
```

--------------------------------

### Run Playbook

Source: https://docs.openclaw.ai/install/ansible

Executes the deployment playbook. Includes an alternative method for manual execution.

```bash
./run-playbook.sh
```

```bash
ansible-playbook playbook.yml --ask-become-pass
# Then run: /tmp/openclaw-setup.sh
```

--------------------------------

### GET /permissions_list_open

Source: https://docs.openclaw.ai/cli/mcp

Lists pending exec/plugin approval requests observed since connection.

```APIDOC
## GET /permissions_list_open

### Description
Lists pending exec/plugin approval requests the bridge has observed since it connected to the Gateway.

### Method
GET

### Endpoint
/permissions_list_open
```

--------------------------------

### Onboard Anthropic API Key

Source: https://docs.openclaw.ai/start/wizard-cli-automation

Use this command to onboard with an Anthropic API key. Ensure the ANTHROPIC_API_KEY environment variable is set.

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice apiKey \
  --anthropic-api-key "$ANTHROPIC_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

--------------------------------

### GET /hooks/list

Source: https://docs.openclaw.ai/cli/hooks

List all discovered hooks from workspace, managed, extra, and bundled directories.

```APIDOC
## GET /hooks/list

### Description
List all discovered hooks from workspace, managed, extra, and bundled directories.

### Method
GET

### Endpoint
openclaw hooks list

### Parameters
#### Query Parameters
- **--eligible** (flag) - Optional - Show only eligible hooks (requirements met)
- **--json** (flag) - Optional - Output as JSON
- **-v, --verbose** (flag) - Optional - Show detailed information including missing requirements
```

--------------------------------

### Get hook information

Source: https://docs.openclaw.ai/cli/hooks

Displays detailed information about a specific hook by name or key.

```bash
openclaw hooks info <name>
```

```bash
openclaw hooks info session-memory
```

--------------------------------

### Build and Test Plugin

Source: https://docs.openclaw.ai/plugins/sdk-migration

Execute the build and test commands to verify migration changes.

```bash
pnpm build
pnpm test -- my-plugin/
```

--------------------------------

### POST /act

Source: https://docs.openclaw.ai/tools/browser

Executes an action within the browser context. This endpoint requires Playwright to be installed.

```APIDOC
## POST /act

### Description
Executes a specific action in the browser. Requires Playwright to be installed; otherwise, returns a 501 error.

### Method
POST

### Endpoint
/act

### Query Parameters
- **profile** (string) - Optional - The profile name to use for the request.

### Response
#### Error Response (400/403/501)
- **error** (string) - A descriptive error message.
- **code** (string) - A specific error code (e.g., ACT_KIND_REQUIRED, ACT_INVALID_REQUEST, ACT_SELECTOR_UNSUPPORTED, ACT_EVALUATE_DISABLED, ACT_TARGET_ID_MISMATCH, ACT_EXISTING_SESSION_UNSUPPORTED).
```

--------------------------------

### Optimize Dockerfile for faster builds

Source: https://docs.openclaw.ai/install/docker

Structures the Dockerfile to leverage layer caching for dependency installation.

```dockerfile
FROM node:24-bookworm
RUN curl -fsSL https://bun.sh/install | bash
ENV PATH="/root/.bun/bin:${PATH}"
RUN corepack enable
WORKDIR /app
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml .npmrc ./
COPY ui/package.json ./ui/package.json
COPY scripts ./scripts
RUN pnpm install --frozen-lockfile
COPY . .
RUN pnpm build
RUN pnpm ui:install
RUN pnpm ui:build
ENV NODE_ENV=production
CMD ["node","dist/index.js"]
```

--------------------------------

### Manage Node Host Service

Source: https://docs.openclaw.ai/cli/node

Commands for controlling the lifecycle of the installed node host service.

```bash
openclaw node status
openclaw node stop
openclaw node restart
openclaw node uninstall
```

--------------------------------

### Configure Ollama authentication

Source: https://docs.openclaw.ai/providers/ollama

Sets the API key for cloud access or a placeholder for local-only setups.

```bash
# Cloud
export OLLAMA_API_KEY="your-ollama-api-key"

# Local-only
export OLLAMA_API_KEY="ollama-local"

# Or configure in your config file
openclaw config set models.providers.ollama.apiKey "OLLAMA_API_KEY"
```

--------------------------------

### Organize configuration with $include

Source: https://docs.openclaw.ai/configuration

Use the $include directive to split large configuration files into smaller, manageable components.

```json
// ~/.openclaw/openclaw.json
{
  gateway: { port: 18789 },
  agents: { $include: "./agents.json5" },
  broadcast: {
    $include: ["./clients/a.json5", "./clients/b.json5"],
  },
}
```

--------------------------------

### Request Analysis Tasks

Source: https://docs.openclaw.ai/tools/code-execution

Examples of natural language prompts for triggering code execution tasks.

```text
Use code_execution to calculate the 7-day moving average for these numbers: ...
```

```text
Use x_search to find posts mentioning OpenClaw this week, then use code_execution to count them by day.
```

```text
Use web_search to gather the latest AI benchmark numbers, then use code_execution to compare percent changes.
```

--------------------------------

### Error Message Example

Source: https://docs.openclaw.ai/tools/browser-linux-troubleshooting

The error message encountered when the browser control server fails to launch.

```json
{"error":"Error: Failed to start Chrome CDP on port 18800 for profile \"openclaw\"."}
```

--------------------------------

### List Available Xiaomi Models

Source: https://docs.openclaw.ai/providers/xiaomi

Verify that the Xiaomi models are available after onboarding by listing them using this command.

```bash
openclaw models list --provider xiaomi
```

--------------------------------

### Slack Command for AI Interaction

Source: https://docs.openclaw.ai/channels/slack

Example of a Slack command '/think' used for AI interactions.

```text
/think
```

--------------------------------

### Configure OpenShell Plugin

Source: https://docs.openclaw.ai/gateway/openshell

Enable the OpenShell plugin and set the sandbox backend in the OpenClaw configuration file.

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "all",
        backend: "openshell",
        scope: "session",
        workspaceAccess: "rw",
      },
    },
  },
  plugins: {
    entries: {
      openshell: {
        enabled: true,
        config: {
          from: "openclaw",
          mode: "remote",
        },
      },
    },
  },
}
```

--------------------------------

### Protocol Frame Examples

Source: https://docs.openclaw.ai/concepts/typebox

Standard JSON frames for connection requests, responses, and event notifications.

```json
{
  "type": "req",
  "id": "c1",
  "method": "connect",
  "params": {
    "minProtocol": 3,
    "maxProtocol": 3,
    "client": {
      "id": "openclaw-macos",
      "displayName": "macos",
      "version": "1.0.0",
      "platform": "macos 15.1",
      "mode": "ui",
      "instanceId": "A1B2"
    }
  }
}
```

```json
{
  "type": "res",
  "id": "c1",
  "ok": true,
  "payload": {
    "type": "hello-ok",
    "protocol": 3,
    "server": { "version": "dev", "connId": "ws-1" },
    "features": { "methods": ["health"], "events": ["tick"] },
    "snapshot": {
      "presence": [],
      "health": {},
      "stateVersion": { "presence": 0, "health": 0 },
      "uptimeMs": 0
    },
    "policy": { "maxPayload": 1048576, "maxBufferedBytes": 1048576, "tickIntervalMs": 30000 }
  }
}
```

```json
{ "type": "req", "id": "r1", "method": "health" }
```

```json
{ "type": "res", "id": "r1", "ok": true, "payload": { "ok": true } }
```

```json
{ "type": "event", "event": "tick", "payload": { "ts": 1730000000 }, "seq": 12 }
```

--------------------------------

### Profile Vitest/Vite Startup Overhead

Source: https://docs.openclaw.ai/help/testing

Writes a main-thread CPU profile for Vitest and Vite startup and transform overhead.

```bash
pnpm test:perf:profile:main
```

--------------------------------

### Configure Group Access Policy

Source: https://docs.openclaw.ai/channels/zalouser

Example configuration for restricting group access using an allowlist.

```json5
{
  channels: {
    zalouser: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["1471383327500481391"],
      groups: {
        "123456789": { allow: true },
        "Work Chat": { allow: true },
      },
    },
  },
}
```

--------------------------------

### Onboard to Moonshot API

Source: https://docs.openclaw.ai/providers/moonshot

Run the onboarding command for the Moonshot API. Use `moonshot-api-key` for the international endpoint or `moonshot-api-key-cn` for the China endpoint.

```bash
openclaw onboard --auth-choice moonshot-api-key
```

```bash
openclaw onboard --auth-choice moonshot-api-key-cn
```

--------------------------------

### Manage MiniMax Model Configuration

Source: https://docs.openclaw.ai/providers/minimax

Commands to list available models and set the active provider model reference.

```bash
openclaw models list
```

```bash
openclaw models set minimax/MiniMax-M2.7
```

```bash
openclaw models set minimax-portal/MiniMax-M2.7
```

--------------------------------

### Create Agent Workspaces

Source: https://docs.openclaw.ai/concepts/multi-agent

Initialize multiple agent workspaces for different tasks.

```bash
openclaw agents add coding
openclaw agents add social
```

--------------------------------

### Onboard with Codex Subscription

Source: https://docs.openclaw.ai/providers/openai

Initialize OpenClaw using Codex OAuth credentials.

```bash
openclaw onboard --auth-choice openai-codex
```

```bash
openclaw models auth login --provider openai-codex
```

--------------------------------

### Agent Tool: Get Status

Source: https://docs.openclaw.ai/plugins/voice-call

The `get_status` action for the `voice_call` agent tool. Requires a `callId`.

```tool_definition
get_status (callId)
```

--------------------------------

### Create GCP VM Instance

Source: https://docs.openclaw.ai/install/gcp

Create a Compute Engine VM instance named 'openclaw-gateway'. The 'e2-small' machine type is recommended for Docker builds. Ensure the boot disk is at least 20GB.

```bash
gcloud compute instances create openclaw-gateway \
  --zone=us-central1-a \
  --machine-type=e2-small \
  --boot-disk-size=20GB \
  --image-family=debian-12 \
  --image-project=debian-cloud
```

--------------------------------

### Build Sandbox Images

Source: https://docs.openclaw.ai/gateway/configuration-reference

Commands to build the primary sandbox image and the optional browser image.

```bash
scripts/sandbox-setup.sh           # main sandbox image
scripts/sandbox-browser-setup.sh   # optional browser image
```

--------------------------------

### GET /security/audit

Source: https://docs.openclaw.ai/gateway/security

Retrieves the current security and configuration audit findings for the OpenClaw AI project.

```APIDOC
## GET /security/audit

### Description
Retrieves a list of security findings, including plugin safety, skill integrity, and configuration exposure risks.

### Method
GET

### Endpoint
/security/audit

### Response
#### Success Response (200)
- **plugins.installs_version_drift** (string) - Plugin install records drift from installed packages
- **plugins.code_safety** (string) - Plugin code scan results
- **security.exposure.open_channels_with_exec** (string) - Shared/public rooms reaching exec-enabled agents
- **models.legacy** (string) - Legacy model configuration status
- **summary.attack_surface** (string) - Roll-up summary of auth, channel, tool, and exposure posture
```

--------------------------------

### Skill Management API

Source: https://docs.openclaw.ai/web/control-ui

Manage skills, including their status, enabling/disabling, installation, and API key updates.

```APIDOC
## Skill Management API

### Description
Manage the lifecycle and configuration of skills.

### Endpoints
- `skills.*`: A wildcard for all skill-related operations (e.g., `skills.status`, `skills.enable`, `skills.disable`, `skills.install`, `skills.updateApiKey`).
```

--------------------------------

### Update All Plugins using OpenClaw CLI

Source: https://docs.openclaw.ai/tools/clawhub

Update all installed plugins to their latest available versions from ClawHub.

```bash
openclaw plugins update --all
```

--------------------------------

### Run non-interactive onboarding

Source: https://docs.openclaw.ai/providers/together

Configures the Together API key in a non-interactive environment, suitable for scripts or automated deployments.

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice together-api-key \
  --together-api-key "$TOGETHER_API_KEY"
```

--------------------------------

### List Standard Models

Source: https://docs.openclaw.ai/providers/stepfun

Verify available models for the standard StepFun provider.

```bash
openclaw models list --provider stepfun
```

--------------------------------

### Reset OpenClaw via CLI

Source: https://docs.openclaw.ai/help/faq

Commands to reset the OpenClaw installation or perform a full non-interactive reset.

```bash
openclaw reset
```

```bash
openclaw reset --scope full --yes --non-interactive
```

```bash
openclaw onboard --install-daemon
```

--------------------------------

### Remove macOS OpenClaw App

Source: https://docs.openclaw.ai/install/uninstall

Deletes the OpenClaw macOS application. Use this if you installed the application directly.

```bash
rm -rf /Applications/OpenClaw.app
```

--------------------------------

### POST /run

Source: https://docs.openclaw.ai/tools/lobster

Executes a Lobster pipeline or workflow file.

```APIDOC
## POST /run

### Description
Executes a pipeline string or a path to a .lobster workflow file.

### Request Body
- **action** (string) - Required - Must be "run"
- **pipeline** (string) - Required - The pipeline command string or file path
- **cwd** (string) - Optional - Relative working directory for the pipeline
- **timeoutMs** (integer) - Optional - Abort duration in milliseconds (default: 20000)
- **maxStdoutBytes** (integer) - Optional - Max output size in bytes (default: 512000)
- **argsJson** (string) - Optional - JSON string of arguments for workflow files

### Request Example
{
  "action": "run",
  "pipeline": "/path/to/inbox-triage.lobster",
  "argsJson": "{\"tag\":\"family\"}"
}

### Response
#### Success Response (200)
- **ok** (boolean) - Execution success status
- **status** (string) - Current status (ok, needs_approval, cancelled)
- **requiresApproval** (object) - Present if workflow is paused; contains resumeToken
```

--------------------------------

### Onboard BlueBubbles via CLI

Source: https://docs.openclaw.ai/channels/bluebubbles

Use the interactive wizard or direct CLI command to add the BlueBubbles channel.

```bash
openclaw onboard
```

```bash
openclaw channels add bluebubbles --http-url http://192.168.1.100:1234 --password <password>
```

--------------------------------

### Run a node host

Source: https://docs.openclaw.ai/nodes/index

Connect a node host using a gateway token via environment variables.

```bash
export OPENCLAW_GATEWAY_TOKEN="<gateway-token>"
openclaw node run --host 127.0.0.1 --port 18790 --display-name "Build Node"
```

--------------------------------

### Load LaunchAgent via launchctl

Source: https://docs.openclaw.ai/channels/bluebubbles

Commands to unload and load the LaunchAgent configuration.

```bash
launchctl unload ~/Library/LaunchAgents/com.user.poke-messages.plist 2>/dev/null || true
launchctl load ~/Library/LaunchAgents/com.user.poke-messages.plist
```

--------------------------------

### List Available Models

Source: https://docs.openclaw.ai/help/testing

Commands to display available models and their provider IDs for testing.

```bash
openclaw models list
openclaw models list --json
```

--------------------------------

### Generate and describe images

Source: https://docs.openclaw.ai/cli/infer

Image commands support generation, editing, and description. For image describe, the --model flag must follow the <provider/model> format.

```bash
openclaw infer image generate --prompt "friendly lobster illustration" --json
openclaw infer image generate --prompt "cinematic product photo of headphones" --json
openclaw infer image describe --file ./photo.jpg --json
openclaw infer image describe --file ./ui-screenshot.png --model openai/gpt-4.1-mini --json
```

--------------------------------

### Define openclaw.channel metadata

Source: https://docs.openclaw.ai/plugins/sdk-setup

Example configuration object for a channel, including labels, aliases, and exposure settings.

```json
{
  "openclaw": {
    "channel": {
      "id": "my-channel",
      "label": "My Channel",
      "selectionLabel": "My Channel (self-hosted)",
      "detailLabel": "My Channel Bot",
      "docsPath": "/channels/my-channel",
      "docsLabel": "my-channel",
      "blurb": "Webhook-based self-hosted chat integration.",
      "order": 80,
      "aliases": ["mc"],
      "preferOver": ["my-channel-legacy"],
      "selectionDocsPrefix": "Guide:",
      "selectionExtras": ["Markdown"],
      "markdownCapable": true,
      "exposure": {
        "configured": true,
        "setup": true,
        "docs": true
      },
      "quickstartAllowFrom": true
    }
  }
}
```

--------------------------------

### Configure Video Generation Live Tests

Source: https://docs.openclaw.ai/help/testing

Environment variables to control provider selection, model targeting, and timeout settings for live tests.

```bash
OPENCLAW_LIVE_VIDEO_GENERATION_PROVIDERS="google,openai,runway"
```

```bash
OPENCLAW_LIVE_VIDEO_GENERATION_MODELS="google/veo-3.1-fast-generate-preview,openai/sora-2,runway/gen4_aleph"
```

```bash
OPENCLAW_LIVE_VIDEO_GENERATION_SKIP_PROVIDERS=""
```

```bash
OPENCLAW_LIVE_VIDEO_GENERATION_TIMEOUT_MS=60000
```

```bash
OPENCLAW_LIVE_REQUIRE_PROFILE_KEYS=1
```

--------------------------------

### Set up AWS IAM and enable discovery

Source: https://docs.openclaw.ai/providers/bedrock

Create an IAM role with Bedrock access, attach it to an EC2 instance, and configure OpenClaw to enable automatic model discovery.

```bash
# 1. Create IAM role and instance profile
aws iam create-role --role-name EC2-Bedrock-Access \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "ec2.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

aws iam attach-role-policy --role-name EC2-Bedrock-Access \
  --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess

aws iam create-instance-profile --instance-profile-name EC2-Bedrock-Access
aws iam add-role-to-instance-profile \
  --instance-profile-name EC2-Bedrock-Access \
  --role-name EC2-Bedrock-Access

# 2. Attach to your EC2 instance
aws ec2 associate-iam-instance-profile \
  --instance-id i-xxxxx \
  --iam-instance-profile Name=EC2-Bedrock-Access

# 3. On the EC2 instance, enable discovery explicitly
openclaw config set plugins.entries.amazon-bedrock.config.discovery.enabled true
openclaw config set plugins.entries.amazon-bedrock.config.discovery.region us-east-1
```

--------------------------------

### Example: Fixed Timezone Message Envelope

Source: https://docs.openclaw.ai/concepts/timezone

Shows a message envelope with a fixed timezone offset, such as GMT+1.

```text
[Signal Alice +1555 2026-01-18 06:19 GMT+1] hello
```

--------------------------------

### Onboard Arcee AI (OpenRouter)

Source: https://docs.openclaw.ai/providers/arcee

Run this command to onboard with Arcee AI via OpenRouter. Ensure you have created an API key at OpenRouter.

```bash
openclaw onboard --auth-choice arceeai-openrouter
```

--------------------------------

### Configure SSE/HTTP transport

Source: https://docs.openclaw.ai/cli/mcp

Example configuration for an MCP server using the SSE/HTTP transport with authentication headers.

```json
{
  "mcp": {
    "servers": {
      "remote-tools": {
        "url": "https://mcp.example.com",
        "headers": {
          "Authorization": "Bearer <token>"
        }
      }
    }
  }
}
```

--------------------------------

### Onboard Ollama

Source: https://docs.openclaw.ai/start/wizard-cli-automation

Use this command to onboard with Ollama, specifying a custom model ID and accepting risk.

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice ollama \
  --custom-model-id "qwen3.5:27b" \
  --accept-risk \
  --gateway-port 18789 \
  --gateway-bind loopback
```

--------------------------------

### JSON output for cleanup maintenance

Source: https://docs.openclaw.ai/cli/sessions

Example of the JSON summary returned after running a cleanup maintenance task.

```json
{
  "allAgents": true,
  "mode": "warn",
  "dryRun": true,
  "stores": [
    {
      "agentId": "main",
      "storePath": "/home/user/.openclaw/agents/main/sessions/sessions.json",
      "beforeCount": 120,
      "afterCount": 80,
      "pruned": 40,
      "capped": 0
    },
    {
      "agentId": "work",
      "storePath": "/home/user/.openclaw/agents/work/sessions/sessions.json",
      "beforeCount": 18,
      "afterCount": 18,
      "pruned": 0,
      "capped": 0
    }
  ]
}
```

--------------------------------

### Troubleshoot LM Studio Connection

Source: https://docs.openclaw.ai/providers/lmstudio

Commands to verify the server status and API accessibility.

```bash
# Start via desktop app, or headless:
lms server start --port 1234
```

```bash
curl http://localhost:1234/api/v1/models
```

--------------------------------

### Update OpenClaw via CLI

Source: https://docs.openclaw.ai/install/updating

The recommended method to update OpenClaw, which detects the installation type and restarts the gateway.

```bash
openclaw update
```

--------------------------------

### Authenticate and Configure Azure CLI

Source: https://docs.openclaw.ai/install/azure

Sign in to the Azure CLI and install the SSH extension required for Bastion tunneling.

```bash
az login
az extension add -n ssh
```

--------------------------------

### Switch OpenClaw Update Channels

Source: https://docs.openclaw.ai/install/development-channels

Persists the chosen update channel in the configuration and aligns the installation method accordingly.

```bash
openclaw update --channel stable
openclaw update --channel beta
openclaw update --channel dev
```

--------------------------------

### Run OpenClaw Plugin Doctor

Source: https://docs.openclaw.ai/cli/plugins

Run the plugin doctor to diagnose and fix potential issues with installed plugins.

```bash
openclaw plugins doctor
```

--------------------------------

### Configure diagnostics.cacheTrace in YAML

Source: https://docs.openclaw.ai/reference/prompt-caching

Use this configuration block to enable and customize cache tracing output in your OpenClaw setup.

```yaml
diagnostics:
  cacheTrace:
    enabled: true
    filePath: "~/.openclaw/logs/cache-trace.jsonl" # optional
    includeMessages: false # default true
    includePrompt: false # default true
    includeSystem: false # default true
```

--------------------------------

### OpenProse File Structure

Source: https://docs.openclaw.ai/prose

Illustrates the default directory structure for OpenProse state management within a workspace, including runs and agents.

```text
.prose/
├── .env
├── runs/
│   └── {YYYYMMDD}-{HHMMSS}-{random}/
│       ├── program.prose
│       ├── state.md
│       ├── bindings/
│       └── agents/
└── agents/
```

--------------------------------

### Create Openclaw Backup

Source: https://docs.openclaw.ai/cli/reset

Before resetting, create a backup of your local state using `openclaw backup create` to ensure you have a restorable snapshot.

```bash
openclaw backup create
```

--------------------------------

### Check Node Status via CLI

Source: https://docs.openclaw.ai/help/faq

Commands to verify the status and list of connected nodes in an OpenClaw setup.

```bash
openclaw nodes status
openclaw nodes list
```

--------------------------------

### Define Deployment Variables

Source: https://docs.openclaw.ai/install/azure

Set environment variables for resource naming and network configuration.

```bash
RG="rg-openclaw"
LOCATION="westus2"
VNET_NAME="vnet-openclaw"
VNET_PREFIX="10.40.0.0/16"
VM_SUBNET_NAME="snet-openclaw-vm"
VM_SUBNET_PREFIX="10.40.2.0/24"
BASTION_SUBNET_PREFIX="10.40.1.0/26"
NSG_NAME="nsg-openclaw-vm"
VM_NAME="vm-openclaw"
ADMIN_USERNAME="openclaw"
BASTION_NAME="bas-openclaw"
BASTION_PIP_NAME="pip-openclaw-bastion"
```

--------------------------------

### Configure Gateway Access Methods

Source: https://docs.openclaw.ai/help/faq

Commands and configurations for exposing the OpenClaw Gateway via different network setups.

```bash
openclaw gateway --tailscale serve
```

```bash
openclaw gateway --bind tailnet --token "<token>"
```

```bash
ssh -N -L 18789:127.0.0.1:18789 user@host
```

--------------------------------

### Onboard Qianfan API Key

Source: https://docs.openclaw.ai/providers/qianfan

Run this command to onboard the Qianfan provider using an API key. Ensure you have your Baidu Cloud account and API key ready.

```bash
openclaw onboard --auth-choice qianfan-api-key
```

--------------------------------

### Configure gateway token via environment reference

Source: https://docs.openclaw.ai/cli/onboard

Set a gateway token using an environment variable reference for secure non-interactive onboarding.

```bash
export OPENCLAW_GATEWAY_TOKEN="your-token"
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice skip \
  --gateway-auth token \
  --gateway-token-ref-env OPENCLAW_GATEWAY_TOKEN \
  --accept-risk
```

--------------------------------

### Outbound Media and Runtime Helpers

Source: https://docs.openclaw.ai/plugins/sdk-channel-plugins

Use `openclaw/plugin-sdk/outbound-media` and `openclaw/plugin-sdk/outbound-runtime` for media loading, outbound identity/send delegates, and payload planning.

```javascript
openclaw/plugin-sdk/outbound-media
```

```javascript
openclaw/plugin-sdk/outbound-runtime
```

--------------------------------

### Configuration: agents.defaults.systemPromptOverride

Source: https://docs.openclaw.ai/gateway/configuration-reference

Allows replacing the entire system prompt with a fixed string for controlled experiments.

```APIDOC
## Configuration: agents.defaults.systemPromptOverride

### Description
Overrides the OpenClaw-assembled system prompt with a fixed string. Can be set globally or per-agent.

### Request Body
- **systemPromptOverride** (string) - Optional - The fixed system prompt string. Empty or whitespace-only values are ignored.

### Request Example
{
  "agents": {
    "defaults": {
      "systemPromptOverride": "You are a helpful assistant."
    }
  }
}
```

--------------------------------

### Onboard Arcee AI (Direct)

Source: https://docs.openclaw.ai/providers/arcee

Run this command to onboard with Arcee AI using an API key. Ensure you have created an API key at Arcee AI.

```bash
openclaw onboard --auth-choice arceeai-api-key
```

--------------------------------

### Verify Gateway Configuration and Status

Source: https://docs.openclaw.ai/gateway/troubleshooting

Use these commands to inspect current gateway binding, authentication settings, and runtime logs.

```bash
openclaw config get gateway.bind
openclaw config get gateway.auth.mode
openclaw config get gateway.auth.token
openclaw gateway status
openclaw logs --follow
```

--------------------------------

### Configure Chutes Models

Source: https://docs.openclaw.ai/providers/chutes

Example configuration for defining default models and aliases within the OpenClaw agent settings.

```json5
{
  agents: {
    defaults: {
      model: { primary: "chutes/zai-org/GLM-4.7-TEE" },
      models: {
        "chutes/zai-org/GLM-4.7-TEE": { alias: "Chutes GLM 4.7" },
        "chutes/deepseek-ai/DeepSeek-V3.2-TEE": { alias: "Chutes DeepSeek V3.2" },
      },
    },
  },
}
```

--------------------------------

### Handle plan validation errors

Source: https://docs.openclaw.ai/gateway/secrets-plan-contract

Example of an error message returned when a target path does not match the expected schema.

```text
Invalid plan target path for models.providers.apiKey: models.providers.openai.baseUrl
```

--------------------------------

### CLI: openclaw sandbox list

Source: https://docs.openclaw.ai/cli/sandbox

List all sandbox runtimes with their status, configuration, and metadata.

```APIDOC
## CLI: openclaw sandbox list

### Description
List all sandbox runtimes with their status and configuration.

### Parameters
#### Query Parameters
- **--browser** (flag) - Optional - List only browser containers
- **--json** (flag) - Optional - JSON output
```

--------------------------------

### List Marketplace Plugins

Source: https://docs.openclaw.ai/cli/plugins

Lists plugins from a specified source, such as a local path, GitHub repository, or marketplace manifest.

```bash
openclaw plugins marketplace list <source>
openclaw plugins marketplace list <source> --json
```

--------------------------------

### Example: Local Timezone Message Envelope

Source: https://docs.openclaw.ai/concepts/timezone

Illustrates a message envelope with a local timezone timestamp, which is the default behavior.

```text
[Signal Alice +1555 2026-01-18 00:19 PST] hello
```

--------------------------------

### Session Management Commands

Source: https://docs.openclaw.ai/help/faq

Commands used within the chat interface to compact history or start a new session.

```text
/compact
```

```text
/new
/reset
```

--------------------------------

### Configure API Key Environment Variables

Source: https://docs.openclaw.ai/gateway/authentication

Set the provider API key as an environment variable and verify the connection status.

```bash
export <PROVIDER>_API_KEY="..."
openclaw models status
```

--------------------------------

### Preview Update Actions

Source: https://docs.openclaw.ai/install/development-channels

Simulates an update process to display planned actions, effective channels, and potential downgrade requirements without applying changes.

```bash
openclaw update --dry-run
openclaw update --channel beta --dry-run
openclaw update --tag 2026.4.1-beta.1 --dry-run
openclaw update --dry-run --json
```

--------------------------------

### Execute web_fetch request

Source: https://docs.openclaw.ai/tools/web-fetch

Perform a basic HTTP GET request to a specified URL using the web_fetch tool.

```javascript
await web_fetch({ url: "https://example.com/article" });
```

--------------------------------

### Apply Sandbox Configuration Changes

Source: https://docs.openclaw.ai/cli/sandbox

Recreate all containers after modifying sandbox settings in the configuration file.

```bash
# Edit config: agents.defaults.sandbox.* (or agents.list[].sandbox.*)

# Recreate to apply new config
openclaw sandbox recreate --all
```

--------------------------------

### GET /v1/models/{id}

Source: https://docs.openclaw.ai/gateway/openai-http-api

Retrieves details for a specific model. This endpoint is served when the OpenAI-compatible HTTP surface is enabled.

```APIDOC
## GET /v1/models/{id}

### Description
Retrieves detailed information about a specific model. This endpoint is available when the Gateway's OpenAI-compatible HTTP surface is enabled.

### Method
GET

### Endpoint
`http://<gateway-host>:<port>/v1/models/{id}`

### Parameters
#### Path Parameters
- **id** (string) - Required - The unique identifier of the model to retrieve.

### Response
#### Success Response (200)
- **id** (string) - The unique identifier of the model.
- **object** (string) - Type of object, e.g., `model`.
- **created** (integer) - Unix timestamp of model creation.
- **owned_by** (string) - The entity that owns the model (e.g., `openclaw`).

#### Response Example
```json
{
  "id": "openclaw",
  "object": "model",
  "created": 1677610602,
  "owned_by": "openclaw"
}
```
```

--------------------------------

### Update All Skills using OpenClaw CLI

Source: https://docs.openclaw.ai/tools/clawhub

Update all installed skills to their latest available versions from ClawHub with a single command.

```bash
openclaw skills update --all
```

--------------------------------

### Non-interactive Step Plan Onboarding

Source: https://docs.openclaw.ai/providers/stepfun

Perform onboarding for the Step Plan provider without interactive prompts.

```bash
openclaw onboard --auth-choice stepfun-plan-api-key-intl \
  --stepfun-api-key "$STEPFUN_API_KEY"
```

--------------------------------

### Find Global npm Prefix

Source: https://docs.openclaw.ai/install/node

Determine the global installation directory for npm packages. This is useful for troubleshooting PATH issues.

```bash
npm prefix -g
```

--------------------------------

### Configure Kimi Coding Provider

Source: https://docs.openclaw.ai/gateway/configuration-reference

Set up the Kimi Coding provider, which is Anthropic-compatible. Set KIMI_API_KEY. Use `openclaw onboard` for a shortcut.

```json5
{
  env: { KIMI_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "kimi/kimi-code" },
      models: { "kimi/kimi-code": { alias: "Kimi Code" } },
    },
  },
}
```

--------------------------------

### Create Local Nix Flake

Source: https://docs.openclaw.ai/install/nix

Use the agent-first template from the nix-openclaw repo to create a local flake for your OpenClaw installation.

```bash
mkdir -p ~/code/openclaw-local
# Copy templates/agent-first/flake.nix from the nix-openclaw repo
```

--------------------------------

### Enable Plugin in Configuration

Source: https://docs.openclaw.ai/concepts/context-engine

Enable the registered context engine within the project configuration file.

```json5
{
  plugins: {
    slots: {
      contextEngine: "my-engine",
    },
    entries: {
      "my-engine": {
        enabled: true,
      },
    },
  },
}
```

--------------------------------

### Verify Venice AI Setup

Source: https://docs.openclaw.ai/providers/venice

Test the configuration by sending a message to a specific model using the OpenClaw agent command.

```bash
openclaw agent --model venice/kimi-k2-5 --message "Hello, are you working?"
```

--------------------------------

### Deploy OpenClaw on Kubernetes

Source: https://docs.openclaw.ai/install/kubernetes

Commands to set the provider API key and execute the deployment script.

```bash
# Replace with your provider: ANTHROPIC, GEMINI, OPENAI, or OPENROUTER
export <PROVIDER>_API_KEY="..."
./scripts/k8s/deploy.sh

kubectl port-forward svc/openclaw 18789:18789 -n openclaw
open http://localhost:18789
```

```bash
# Replace with your provider: ANTHROPIC, GEMINI, OPENAI, or OPENROUTER
export <PROVIDER>_API_KEY="..."
./scripts/k8s/deploy.sh
```

--------------------------------

### Channel Plugin Package Metadata

Source: https://docs.openclaw.ai/plugins/sdk-setup

Configure your `package.json` for a channel plugin, specifying extensions, setup entry, and channel-specific metadata.

```json
{
  "name": "@myorg/openclaw-my-channel",
  "version": "1.0.0",
  "type": "module",
  "openclaw": {
    "extensions": ["./index.ts"],
    "setupEntry": "./setup-entry.ts",
    "channel": {
      "id": "my-channel",
      "label": "My Channel",
      "blurb": "Short description of the channel."
    }
  }
}
```

--------------------------------

### OpenClaw Honcho CLI Commands

Source: https://docs.openclaw.ai/concepts/memory-honcho

These commands are used to interact with the OpenClaw Honcho system for setup, status checks, and querying.

```bash
openclaw honcho setup                        # Configure API key and migrate files
```

```bash
openclaw honcho status                       # Check connection status
```

```bash
openclaw honcho ask <question>               # Query Honcho about the user
```

```bash
openclaw honcho search <query> [-k N] [-d D] # Semantic search over memory
```

--------------------------------

### Configure Message Handling and Queueing

Source: https://docs.openclaw.ai/gateway/configuration-reference

Set up global message handling, response prefixes, acknowledgment reactions, and queueing behavior for different channels. Defaults can be overridden per channel or account.

```json5
{
  messages: {
    responsePrefix: "🦞", // or "auto"
    ackReaction: "👀",
    ackReactionScope: "group-mentions", // group-mentions | group-all | direct | all
    removeAckAfterReply: false,
    queue: {
      mode: "collect", // steer | followup | collect | steer-backlog | steer+backlog | queue | interrupt
      debounceMs: 1000,
      cap: 20,
      drop: "summarize", // old | new | summarize
      byChannel: {
        whatsapp: "collect",
        telegram: "collect",
      },
    },
    inbound: {
      debounceMs: 2000, // 0 disables
      byChannel: {
        whatsapp: 5000,
        slack: 1500,
      },
    },
  },
}
```

--------------------------------

### Configure Browserless Remote CDP

Source: https://docs.openclaw.ai/tools/browser

Example configuration for connecting to a Browserless hosted Chromium service using a WebSocket URL.

```json5
{
  browser: {
    enabled: true,
    defaultProfile: "browserless",
    remoteCdpTimeoutMs: 2000,
    remoteCdpHandshakeTimeoutMs: 4000,
    profiles: {
      browserless: {
        cdpUrl: "wss://production-sfo.browserless.io?token=<BROWSERLESS_API_KEY>",
        color: "#00AA00",
      },
    },
  },
}
```

--------------------------------

### Bootstrap New Matrix Server-Side Key Backup

Source: https://docs.openclaw.ai/install/migrating-matrix

If no server-side key backup exists yet, execute this command to create one. This is essential for future recovery operations.

```bash
openclaw matrix verify bootstrap
```

--------------------------------

### Invoke LLM Task in Pipeline

Source: https://docs.openclaw.ai/tools/lobster

Example of calling the llm-task tool within a Lobster pipeline to process structured data.

```lobster
openclaw.invoke --tool llm-task --action json --args-json '{
  "prompt": "Given the input email, return intent and draft.",
  "thinking": "low",
  "input": { "subject": "Hello", "body": "Can you help?" },
  "schema": {
    "type": "object",
    "properties": {
      "intent": { "type": "string" },
      "draft": { "type": "string" }
    },
    "required": ["intent", "draft"],
    "additionalProperties": false
  }
}'
```

--------------------------------

### Chain CLI Commands for Lobster

Source: https://docs.openclaw.ai/tools/lobster

Example of chaining small JSON-outputting CLI commands for use within a Lobster pipeline.

```bash
inbox list --json
inbox categorize --json
inbox apply --json
```

--------------------------------

### Capture Media via CLI

Source: https://docs.openclaw.ai/nodes/camera

Use the CLI helper to snap photos or record clips, which automatically handles decoding media to temporary files.

```bash
openclaw nodes camera snap --node <id>               # default: both front + back (2 MEDIA lines)
openclaw nodes camera snap --node <id> --facing front
openclaw nodes camera clip --node <id> --duration 3000
openclaw nodes camera clip --node <id> --no-audio
```

--------------------------------

### Configure Heartbeat for Cache Warmth

Source: https://docs.openclaw.ai/reference/token-use

Example YAML configuration to maintain a 1-hour cache by setting a 55-minute heartbeat interval.

```yaml
agents:
  defaults:
    model:
      primary: "anthropic/claude-opus-4-6"
    models:
      "anthropic/claude-opus-4-6":
        params:
          cacheRetention: "long"
    heartbeat:
      every: "55m"
```

--------------------------------

### Tool Profiles and Allowlisting

Source: https://docs.openclaw.ai/tools/web-fetch

Instructions on how to include the `web_fetch` tool in tool profiles or allowlists for agents.

```APIDOC
## Tool Profiles and Allowlisting

### Description
To use the `web_fetch` tool, you need to ensure it is included in your agent's tool profiles or explicitly allowlisted.

### Allowlisting `web_fetch`
Add `"web_fetch"` to the `tools.allow` list in your configuration.

### Allowlisting `group:web`
Alternatively, you can allow the entire `web` group, which includes `web_fetch`, `web_search`, and `x_search`.

### Example Configuration
```json
{
  "tools": {
    "allow": ["web_fetch"]
    // or:
    // "allow": ["group:web"]
  }
}
```

```

--------------------------------

### Switch to a Specific OpenRouter Model

Source: https://docs.openclaw.ai/providers/openrouter

After onboarding, you can switch to a specific model by running this command. Replace `<provider>/<model>` with the desired model identifier.

```bash
openclaw models set openrouter/<provider>/<model>
```

--------------------------------

### Inspect Effective Sandbox Configuration

Source: https://docs.openclaw.ai/gateway/sandboxing

Use the 'openclaw sandbox explain' command to view the effective sandbox mode, tool policy, and configuration keys.

```bash
openclaw sandbox explain
```

--------------------------------

### Node Connection Request

Source: https://docs.openclaw.ai/gateway/protocol

A specific example of a connection request initiated by a node client, including capability and command declarations.

```json
{
  "type": "req",
  "id": "…",
  "method": "connect",
  "params": {
    "minProtocol": 3,
    "maxProtocol": 3,
    "client": {
      "id": "ios-node",
      "version": "1.2.3",
      "platform": "ios",
      "mode": "node"
    },
    "role": "node",
    "scopes": [],
    "caps": ["camera", "canvas", "screen", "location", "voice"],
    "commands": ["camera.snap", "canvas.navigate", "screen.record", "location.get"],
    "permissions": { "camera.capture": true, "screen.record": false },
    "auth": { "token": "…" },
    "locale": "en-US",
    "userAgent": "openclaw-ios/1.2.3",
    "device": {
      "id": "device_fingerprint",
      "publicKey": "…",
      "signature": "…",
      "signedAt": 1737264000000,
      "nonce": "…"
    }
  }
}
```

--------------------------------

### Run OpenClaw via direct node entrypoint

Source: https://docs.openclaw.ai/cli/acp

Use the direct CLI entrypoint for repo-local checkouts to maintain a clean ACP stream.

```bash
env OPENCLAW_HIDE_BANNER=1 OPENCLAW_SUPPRESS_NOTES=1 node openclaw.mjs acp ...
```

--------------------------------

### JSON output for session listing

Source: https://docs.openclaw.ai/cli/sessions

Example of the JSON structure returned when using the --json flag with the sessions command.

```json
{
  "path": null,
  "stores": [
    { "agentId": "main", "path": "/home/user/.openclaw/agents/main/sessions/sessions.json" },
    { "agentId": "work", "path": "/home/user/.openclaw/agents/work/sessions/sessions.json" }
  ],
  "allAgents": true,
  "count": 2,
  "activeMinutes": null,
  "sessions": [
    { "agentId": "main", "key": "agent:main:main", "model": "gpt-5" },
    { "agentId": "work", "key": "agent:work:main", "model": "claude-opus-4-6" }
  ]
}
```

--------------------------------

### Create a Service Account

Source: https://docs.openclaw.ai/install/gcp

Create a dedicated service account for automation or CI/CD pipelines. This follows the principle of least privilege.

```bash
gcloud iam service-accounts create openclaw-deploy \
  --display-name="OpenClaw Deployment"
```

--------------------------------

### Launch the Openclaw TUI

Source: https://docs.openclaw.ai/web/tui

Starts the Terminal UI for interacting with the Gateway. This command opens the interactive chat interface in your terminal.

```bash
openclaw tui
```

--------------------------------

### Inspect Context Detail

Source: https://docs.openclaw.ai/concepts/context

Use the `/context detail` command for a more in-depth breakdown of context usage, showing sizes for individual skills and tool schemas.

```bash
/context detail
```

--------------------------------

### Start Chrome with remote debugging on Windows

Source: https://docs.openclaw.ai/tools/browser-wsl2-windows-remote-cdp-troubleshooting

Launch Chrome with the remote debugging port enabled to allow external connections.

```powershell
chrome.exe --remote-debugging-port=9222
```

--------------------------------

### Run Gateway in Development Mode

Source: https://docs.openclaw.ai/pi-dev

Start the OpenClaw gateway in development mode. This is a recommended step for manual testing and debugging.

```bash
pnpm gateway:dev
```

--------------------------------

### Memory Tool Factories in OpenClaw

Source: https://docs.openclaw.ai/plugins/sdk-runtime

Create memory tool factories for getting and searching, and register memory CLI tools.

```typescript
const getTool = api.runtime.tools.createMemoryGetTool(/* ... */);
const searchTool = api.runtime.tools.createMemorySearchTool(/* ... */);
api.runtime.tools.registerMemoryCli(/* ... */);
```

--------------------------------

### Connect to Hetzner VPS

Source: https://docs.openclaw.ai/install/hetzner

Use this command to establish an SSH connection to your Hetzner VPS. Ensure you replace YOUR_VPS_IP with the actual IP address of your server.

```bash
ssh root@YOUR_VPS_IP
```

--------------------------------

### Check Xcode and Swift Versions

Source: https://docs.openclaw.ai/platforms/mac/dev-setup

Verify that your installed Xcode and Swift toolchain versions meet the requirements for building the macOS application.

```bash
xcodebuild -version
xcrun swift --version
```

--------------------------------

### Configure GPT-OSS 120B Model

Source: https://docs.openclaw.ai/providers/huggingface

This configuration sets the GPT-OSS 120B model as an alias. Ensure the model reference is correct for your setup.

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "huggingface/openai/gpt-oss-120b"
      },
      "models": {
        "huggingface/openai/gpt-oss-120b": { "alias": "GPT-OSS 120B" }
      }
    }
  }
}
```

--------------------------------

### Configure OpenClaw Environment Variables

Source: https://docs.openclaw.ai/install/gcp

Create a `.env` file in the repository root and define environment variables for OpenClaw image, gateway token, binding, port, and directory configurations.

```bash
OPENCLAW_IMAGE=openclaw:latest
OPENCLAW_GATEWAY_TOKEN=
OPENCLAW_GATEWAY_BIND=lan
OPENCLAW_GATEWAY_PORT=18789

OPENCLAW_CONFIG_DIR=/home/$USER/.openclaw
OPENCLAW_WORKSPACE_DIR=/home/$USER/.openclaw/workspace

GOG_KEYRING_PASSWORD=
```

--------------------------------

### Automate Onboarding with Non-Interactive Mode

Source: https://docs.openclaw.ai/reference/wizard

Use the `--non-interactive` flag for scripting onboarding. Add `--json` for machine-readable output. Ensure required environment variables like ANTHROPIC_API_KEY are set.

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice apiKey \
  --anthropic-api-key "$ANTHROPIC_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback \
  --install-daemon \
  --daemon-runtime node \
  --skip-skills
```

--------------------------------

### Configure Wide-area Discovery

Source: https://docs.openclaw.ai/gateway/configuration-reference

Enables DNS-SD for cross-network discovery. Requires additional setup with a DNS server and Tailscale split DNS.

```json5
{
  discovery: {
    wideArea: { enabled: true },
  },
}
```

--------------------------------

### Manage Devices and Nodes CLI

Source: https://docs.openclaw.ai/nodes

Commands for listing, approving, and rejecting device pairings, and checking node status and descriptions. Use these to manage node connections to the Gateway.

```bash
openclaw devices list
openclaw devices approve <requestId>
openclaw devices reject <requestId>
openclaw nodes status
openclaw nodes describe --node <idOrNameOrIp>
```

--------------------------------

### Perform full configuration replacement

Source: https://docs.openclaw.ai/gateway/configuration

Use config.apply to replace the entire configuration. Requires a baseHash from a previous config.get call.

```bash
openclaw gateway call config.get --params '{}'  # capture payload.hash
openclaw gateway call config.apply --params '{
  "raw": "{ agents: { defaults: { workspace: \"~/.openclaw/workspace\" } } }",
  "baseHash": "<hash>",
  "sessionKey": "agent:main:whatsapp:direct:+15555550123"
}'
```

--------------------------------

### Create WireGuard Configuration

Source: https://docs.openclaw.ai/install/fly

Generates a WireGuard configuration file for secure access to your private Fly.io deployment. This is a one-time setup step.

```bash
fly wireguard create
```

--------------------------------

### Search for Recent Results

Source: https://docs.openclaw.ai/tools/web

Retrieve recent search results within a specified timeframe. Use the 'freshness' parameter, for example, 'week'.

```javascript
await web_search({ query: "AI developments", freshness: "week" });
```

--------------------------------

### List Sandbox Runtimes

Source: https://docs.openclaw.ai/cli/sandbox

Display all active sandbox runtimes with their status and configuration details.

```bash
openclaw sandbox list
openclaw sandbox list --browser  # List only browser containers
openclaw sandbox list --json     # JSON output
```

--------------------------------

### Sync Skills in ClawHub CLI

Source: https://docs.openclaw.ai/tools/clawhub

Scan local skills and publish new or updated ones. Use `--all` to upload everything without prompts, `--dry-run` to see what would be uploaded, and `--bump` to specify the version update type.

```bash
clawhub sync
```

```bash
clawhub sync --root <dir...>
```

```bash
clawhub sync --all
```

```bash
clawhub sync --dry-run
```

```bash
clawhub sync --bump <type>
```

```bash
clawhub sync --changelog <text>
```

```bash
clawhub sync --tags <tags>
```

```bash
clawhub sync --concurrency <n>
```

--------------------------------

### Configure Plugin Allowlist

Source: https://docs.openclaw.ai/tools/browser

Example of a restrictive plugin allowlist that prevents the browser plugin from loading. Add 'browser' to the list to enable it.

```json5
{
  plugins: {
    allow: ["telegram"],
  },
}
```

--------------------------------

### Register Image Generation Provider

Source: https://docs.openclaw.ai/plugins/architecture

Used to register a plugin for generating images, with examples like 'openai', 'google', 'fal', and 'minimax'.

```javascript
api.registerImageGenerationProvider(...)
```

--------------------------------

### Configure OpenAI Speech Synthesis

Source: https://docs.openclaw.ai/providers/openai

Example configuration object for setting the TTS model and voice provider within the application settings.

```json5
{
  messages: {
    tts: {
      providers: {
        openai: { model: "gpt-4o-mini-tts", voice: "coral" },
      },
    },
  },
}
```

--------------------------------

### Configure Synthetic provider

Source: https://docs.openclaw.ai/providers/synthetic

Example configuration for the Synthetic provider within the OpenClaw environment, including base URL and model definitions.

```json5
{
  env: { SYNTHETIC_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "synthetic/hf:MiniMaxAI/MiniMax-M2.5" },
      models: { "synthetic/hf:MiniMaxAI/MiniMax-M2.5": { alias: "MiniMax M2.5" } },
    },
  },
  models: {
    mode: "merge",
    providers: {
      synthetic: {
        baseUrl: "https://api.synthetic.new/anthropic",
        apiKey: "${SYNTHETIC_API_KEY}",
        api: "anthropic-messages",
        models: [
          {
            id: "hf:MiniMaxAI/MiniMax-M2.5",
            name: "MiniMax M2.5",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 192000,
            maxTokens: 65536,
          },
        ],
      },
    },
  },
}
```

--------------------------------

### Memory Promote Explain

Source: https://docs.openclaw.ai/cli/memory

Explain a specific memory promotion candidate and its score breakdown. Requires a selector for the candidate.

```APIDOC
## `openclaw memory promote-explain`

### Description
Explains a specific promotion candidate and its score breakdown.

### Method
CLI Command

### Endpoint
N/A

### Parameters
#### Path Parameters
- `<selector>` (string) - Required - Candidate key, path fragment, or snippet fragment to look up.

#### Query Parameters
- `--agent <id>` (string) - Optional - Scope to a single agent (default: the default agent).
- `--include-promoted` (boolean) - Optional - Include already promoted candidates.
- `--json` (boolean) - Optional - Print JSON output.

### Request Example
```bash
openclaw memory promote-explain "authentication module bug"
openclaw memory promote-explain "/path/to/memory.md#line10" --json
```

### Response
#### Success Response (200)
- Detailed explanation of the promotion candidate and its score components.

#### Response Example
```json
{
  "candidate_id": "abc123xyz",
  "explanation": {
    "score": 0.85,
    "breakdown": {
      "frequency": 0.2,
      "relevance": 0.3,
      "recency": 0.15
    }
  }
}
```
```

--------------------------------

### Invoke System Command on Node

Source: https://docs.openclaw.ai/nodes/index

Invoke a system command on a specified OpenClaw node. This example checks if 'git' is available on the node.

```bash
openclaw nodes invoke --node <idOrNameOrIp> --command system.which --params '{"name":"git"}'
```

--------------------------------

### Define UI Hints for Configuration Fields

Source: https://docs.openclaw.ai/plugins/manifest

Maps configuration field names to rendering metadata like labels, help text, and sensitivity flags.

```json
{
  "uiHints": {
    "apiKey": {
      "label": "API key",
      "help": "Used for OpenRouter requests",
      "placeholder": "sk-or-v1-...",
      "sensitive": true
    }
  }
}
```

--------------------------------

### Streamable HTTP Transport Configuration

Source: https://docs.openclaw.ai/cli/mcp

Configuration example for the streamable-http transport, including URL, transport type, connection timeout, and headers.

```APIDOC
## Streamable HTTP Transport Configuration

### Description
Configuration for the `streamable-http` transport option, which enables bidirectional communication with remote MCP servers using HTTP streaming.

### Method
N/A (Configuration Example)

### Endpoint
N/A (Configuration Example)

### Parameters
#### Request Body Fields
- **url** (string) - Required - HTTP or HTTPS URL of the remote server.
- **transport** (string) - Optional - Set to `"streamable-http"` to select this transport. If omitted, OpenClaw defaults to `sse`.
- **connectionTimeoutMs** (integer) - Optional - Per-server connection timeout in milliseconds.
- **headers** (object) - Optional - Key-value map of HTTP headers (e.g., authorization tokens).

### Request Example
```json
{
  "mcp": {
    "servers": {
      "streaming-tools": {
        "url": "https://mcp.example.com/stream",
        "transport": "streamable-http",
        "connectionTimeoutMs": 10000,
        "headers": {
          "Authorization": "Bearer <token>"
        }
      }
    }
  }
}
```

### Response
N/A (Configuration Example)

### Error Handling
N/A (Configuration Example)
```

--------------------------------

### Configure Tool Allow and Deny Lists

Source: https://docs.openclaw.ai/tools/index

Use `tools.allow` and `tools.deny` in your configuration to control which tools agents can call. Deny lists take precedence over allow lists.

```json5
{
  tools: {
    allow: ["group:fs", "browser", "web_search"],
    deny: ["exec"],
  },
}
```

--------------------------------

### Configure Telegram Error Policies

Source: https://docs.openclaw.ai/channels/telegram

Example configuration for setting global error policies and applying specific overrides for a Telegram group.

```json5
{
  channels: {
    telegram: {
      errorPolicy: "reply",
      errorCooldownMs: 120000,
      groups: {
        "-1001234567890": {
          errorPolicy: "silent", // suppress errors in this group
        },
      },
    },
  },
}
```

--------------------------------

### Configure Telegram Forum Topic Settings

Source: https://docs.openclaw.ai/channels/telegram

Example structure for defining forum topic mention settings within the OpenClaw configuration.

```json5
"42": {
                  requireMention: false,
                },
              },
            },
          },
        },
      },
    }
```

--------------------------------

### Inspect Device Pairing and Identity

Source: https://docs.openclaw.ai/gateway/troubleshooting

Commands to list devices and pairing channels, monitor logs, and run diagnostic checks for identity-related issues.

```bash
openclaw devices list
openclaw pairing list --channel <channel> [--account <id>]
openclaw logs --follow
openclaw doctor
```

--------------------------------

### Onboard Step Plan Provider

Source: https://docs.openclaw.ai/providers/stepfun

Commands to initialize the Step Plan provider for international or China-based endpoints.

```bash
openclaw onboard --auth-choice stepfun-plan-api-key-intl
```

```bash
openclaw onboard --auth-choice stepfun-plan-api-key-cn
```

--------------------------------

### Verify Gateway Service

Source: https://docs.openclaw.ai/install/docker-vm-runtime

Monitor the logs of the gateway service to ensure it has started correctly and is listening on the expected network interface and port.

```bash
docker compose logs -f openclaw-gateway
```

--------------------------------

### Configure OpenShell Backend

Source: https://docs.openclaw.ai/gateway/sandboxing

Set the OpenShell backend for agent defaults. Use 'openshell' for remote sandboxing. Ensure 'enabled' is true for the 'openshell' plugin.

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "all",
        backend: "openshell",
        scope: "session",
        workspaceAccess: "rw",
      },
    },
  },
  plugins: {
    entries: {
      openshell: {
        enabled: true,
        config: {
          from: "openclaw",
          mode: "remote", // mirror | remote
          remoteWorkspaceDir: "/sandbox",
          remoteAgentWorkspaceDir: "/agent",
        },
      },
    },
  },
}
```

--------------------------------

### List Available Music Providers

Source: https://docs.openclaw.ai/tools/music-generation

Use the `action: "list"` parameter with the `music_generate` tool to inspect available shared providers and models at runtime.

```text
/tool music_generate action=list
```

--------------------------------

### Run OpenClaw Gateway

Source: https://docs.openclaw.ai/channels/irc

Start or restart the OpenClaw gateway service after configuring IRC settings. This command initiates the gateway process.

```bash
openclaw gateway run
```

--------------------------------

### Configure Non-interactive Mistral Onboarding

Source: https://docs.openclaw.ai/cli/onboard

Authenticate with Mistral using an API key in a non-interactive environment.

```bash
openclaw onboard --non-interactive \
  --auth-choice mistral-api-key \
  --mistral-api-key "$MISTRAL_API_KEY"
```

--------------------------------

### Location Get Command Parameters

Source: https://docs.openclaw.ai/nodes/location-command

Parameters for the `location.get` command. Configure timeout, maximum age of the location data, and desired accuracy.

```json
{
  "timeoutMs": 10000,
  "maxAgeMs": 15000,
  "desiredAccuracy": "coarse|balanced|precise"
}
```

--------------------------------

### Get VM IP Address

Source: https://docs.openclaw.ai/install/macos-vm

Retrieves the IP address assigned to the 'openclaw' Lume VM. This is necessary for establishing an SSH connection.

```bash
lume get openclaw
```

--------------------------------

### Verify System Architecture

Source: https://docs.openclaw.ai/install/oracle

Check the current machine architecture to ensure compatibility with ARM64 binaries.

```bash
uname -m
```

--------------------------------

### CLI Configuration Management

Source: https://docs.openclaw.ai/cli

Commands for managing the openclaw.json configuration file, including getting, setting, unsetting values, and schema validation.

```APIDOC
## CLI config

### Description
Manage non-interactive configuration settings for OpenClaw.

### Subcommands
- **config get <path>** - Print a config value.
- **config set <path> <value>** - Set a config value.
- **config unset <path>** - Remove a value.
- **config file** - Print active config file path.
- **config schema** - Print JSON schema for openclaw.json.
- **config validate** - Validate current config against schema.
```

--------------------------------

### Pair and approve devices

Source: https://docs.openclaw.ai/nodes/index

List pending requests and approve a node connection on the gateway host.

```bash
openclaw devices list
openclaw devices approve <requestId>
openclaw nodes status
```

--------------------------------

### CLI Config Management

Source: https://docs.openclaw.ai/cli/index

Commands for managing the openclaw.json configuration file, including getting, setting, unsetting values, and schema validation.

```APIDOC
## CLI config

### Description
Manage non-interactive configuration settings for OpenClaw.

### Subcommands
- **config get <path>**: Print a config value.
- **config set**: Update configuration values using value, SecretRef, provider, or batch modes.
- **config unset <path>**: Remove a configuration value.
- **config file**: Print the active config file path.
- **config schema**: Print the JSON schema for openclaw.json.
- **config validate**: Validate current config against the schema.
```

--------------------------------

### Uninstall OpenClaw Gateway (macOS launchd)

Source: https://docs.openclaw.ai/install/uninstall

Manually removes the OpenClaw gateway service on macOS using launchd. This is for cases where the CLI is not installed.

```bash
launchctl bootout gui/$UID/ai.openclaw.gateway
rm -f ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

--------------------------------

### List Marketplace Plugins

Source: https://docs.openclaw.ai/cli/plugins

List plugins available in a specific marketplace. Use the --json flag for programmatic access.

```bash
openclaw plugins marketplace list <marketplace>
```

```bash
openclaw plugins marketplace list <marketplace> --json
```

--------------------------------

### OpenClaw Channels - Add / Remove Accounts

Source: https://docs.openclaw.ai/cli/channels

Commands for adding and removing channel accounts, including various authentication methods and interactive setup.

```APIDOC
## OpenClaw Channels - Add / Remove Accounts

### Description
Manage the addition and removal of channel accounts.

### Commands

#### Add Account
- `openclaw channels add --channel telegram --token <bot-token>`: Adds a Telegram channel account using a bot token.
- `openclaw channels add --channel nostr --private-key "$NOSTR_PRIVATE_KEY"`: Adds a Nostr channel account using a private key.

#### Remove Account
- `openclaw channels remove --channel telegram --delete`: Removes a Telegram channel account.

### Authentication and Configuration Flags

Tip: `openclaw channels add --help` shows per-channel flags.

**Common non-interactive add surfaces:**

*   **Bot-token channels:** `--token`, `--bot-token`, `--app-token`, `--token-file`
*   **Signal/iMessage transport fields:** `--signal-number`, `--cli-path`, `--http-url`, `--http-host`, `--http-port`, `--db-path`, `--service`, `--region`
*   **Google Chat fields:** `--webhook-path`, `--webhook-url`, `--audience-type`, `--audience`
*   **Matrix fields:** `--homeserver`, `--user-id`, `--access-token`, `--password`, `--device-name`, `--initial-sync-limit`
*   **Nostr fields:** `--private-key`, `--relay-urls`
*   **Tlon fields:** `--ship`, `--url`, `--code`, `--group-channels`, `--dm-allowlist`, `--auto-discover-channels`
*   `--use-env`: For default-account env-backed auth where supported.

### Interactive Wizard

When `openclaw channels add` is run without flags, an interactive wizard prompts for:

*   Account IDs per selected channel.
*   Optional display names for those accounts.
*   Confirmation to bind configured channel accounts to agents.

If binding is confirmed, the wizard prompts for the agent to own each configured channel account and writes account-scoped routing bindings. These can also be managed later with `openclaw agents bindings`, `openclaw agents bind`, and `openclaw agents unbind`.

### Routing Behavior

*   Existing channel-only bindings continue to match the default account.
*   `channels add` does not auto-create or rewrite bindings in non-interactive mode.
*   Interactive setup can optionally add account-scoped bindings.
*   Run `openclaw doctor --fix` to resolve mixed config states.
```

--------------------------------

### Run Video Generation Live Tests

Source: https://docs.openclaw.ai/help/testing

Execute the shared video generation provider test suite with optional environment variable configuration.

```bash
OPENCLAW_LIVE_TEST=1 pnpm test:live -- extensions/video-generation-providers.live.test.ts
```

```bash
pnpm test:live:media video
```

```bash
pnpm test:live --video-providers fal
```

```bash
OPENCLAW_LIVE_TEST=1 OPENCLAW_LIVE_VYDRA_VIDEO=1 pnpm test:live -- extensions/vydra/vydra.live.test.ts
```

--------------------------------

### Configure Caddy Reverse Proxy

Source: https://docs.openclaw.ai/channels/googlechat

Use Caddy to proxy only the `/googlechat` path to your OpenClaw instance. This setup ignores other paths, returning a 404.

```caddy
your-domain.com {
    reverse_proxy /googlechat* localhost:18789
}
```

--------------------------------

### Minimal TTS Configuration

Source: https://docs.openclaw.ai/tools/tts

Enable TTS and set the primary provider. Ensure the provider is configured in your environment.

```json
{
  messages: {
    tts: {
      auto: "always",
      provider: "elevenlabs",
    },
  },
}
```

--------------------------------

### Search the OpenClaw documentation index

Source: https://docs.openclaw.ai/cli/docs

Use these commands to query the live documentation index. Providing no arguments opens the search entrypoint, while specific terms filter the results.

```bash
openclaw docs
openclaw docs browser existing-session
openclaw docs sandbox allowHostControl
openclaw docs gateway token secretref
```

--------------------------------

### Configure DeepSeek in JSON5

Source: https://docs.openclaw.ai/providers/deepseek

Example configuration snippet for defining the DeepSeek API key and default model within the OpenClaw configuration file.

```json5
{
  env: { DEEPSEEK_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "deepseek/deepseek-chat" },
    },
  },
}
```

--------------------------------

### Configure Recommended OpenClaw Settings

Source: https://docs.openclaw.ai/gateway/configuration-examples

Includes identity customization, model selection, and granular WhatsApp group mention requirements.

```json5
{
  identity: {
    name: "Clawd",
    theme: "helpful assistant",
    emoji: "🦞",
  },
  agent: {
    workspace: "~/.openclaw/workspace",
    model: { primary: "anthropic/claude-sonnet-4-6" },
  },
  channels: {
    whatsapp: {
      allowFrom: ["+15555550123"],
      groups: { "*": { requireMention: true } },
    },
  },
}
```

--------------------------------

### Mount Custom Control UI

Source: https://docs.openclaw.ai/start/getting-started

Configure a custom directory for static dashboard assets.

```bash
mkdir -p "$HOME/.openclaw/control-ui-custom"
# Copy your built static files into that directory.
```

```json
{
  "gateway": {
    "controlUi": {
      "enabled": true,
      "root": "$HOME/.openclaw/control-ui-custom"
    }
  }
}
```

```bash
openclaw gateway restart
openclaw dashboard
```

--------------------------------

### Bridge Instances via CLI

Source: https://docs.openclaw.ai/help/faq

Example command to send a message from one agent to another via the CLI, useful for inter-instance communication.

```bash
openclaw agent --message "Hello from local bot" --deliver --channel telegram --reply-to <chat-id>
```

--------------------------------

### Example: Elapsed Time Message Envelope

Source: https://docs.openclaw.ai/concepts/timezone

Demonstrates a message envelope that includes elapsed time in addition to the absolute timestamp in UTC format.

```text
[Signal Alice +1555 +2m 2026-01-18T05:19Z] follow-up
```

--------------------------------

### Configure Default Music Generation Models

Source: https://docs.openclaw.ai/tools/music-generation

JSON configuration for setting primary and fallback models for music generation.

```json5
{
  agents: {
    defaults: {
      musicGenerationModel: {
        primary: "google/lyria-3-clip-preview",
        fallbacks: ["minimax/music-2.5+"],
      },
    },
  },
}
```

--------------------------------

### Configure memory-core dreaming

Source: https://docs.openclaw.ai/concepts/dreaming

Enable the dreaming plugin in the memory-core configuration. Use the custom cadence example to specify a timezone and cron frequency.

```json
{
  "plugins": {
    "entries": {
      "memory-core": {
        "config": {
          "dreaming": {
            "enabled": true
          }
        }
      }
    }
  }
}
```

```json
{
  "plugins": {
    "entries": {
      "memory-core": {
        "config": {
          "dreaming": {
            "enabled": true,
            "timezone": "America/Los_Angeles",
            "frequency": "0 */6 * * *"
          }
        }
      }
    }
  }
}
```

--------------------------------

### Configure Video Generation Model

Source: https://docs.openclaw.ai/tools/video-generation

Set the default video generation model using the configuration file or the CLI.

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: {
        primary: "qwen/wan2.6-t2v",
        fallbacks: ["qwen/wan2.6-r2v-flash"],
      },
    },
  },
}
```

```bash
openclaw config set agents.defaults.videoGenerationModel.primary "qwen/wan2.6-t2v"
```

--------------------------------

### config.get

Source: https://docs.openclaw.ai/gateway/configuration

Fetches the current configuration snapshot and its hash.

```APIDOC
## GET /config/get

### Description
Fetches the current configuration snapshot and its hash.

### Method
GET

### Endpoint
/config/get

### Response
#### Success Response (200)
- **config** (object) - The current configuration.
- **hash** (string) - The hash of the current configuration.

#### Response Example
```json
{
  "config": {
    "agents": {
      "defaults": {
        "workspace": "~/.openclaw/workspace"
      }
    }
  },
  "hash": "abcdef1234567890"
}
```
```