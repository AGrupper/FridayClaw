import { spawn } from "node:child_process";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";

const WORKSPACE_DIR = "C:\\Users\\Amit\\.openclaw\\workspace";
const STATE_PATH = join(
  WORKSPACE_DIR,
  "state",
  "friday-project-intelligence",
  "brainstorm-pending.json",
);
const SCRIPT_PATH = join(WORKSPACE_DIR, "scripts", "friday_project_intelligence.py");
const PENDING_TTL_MS = 30 * 60 * 1000;

type PendingState = {
  version: number;
  pending: Record<string, { createdAt: number; source: string }>;
};

function readPendingState(): PendingState {
  try {
    return JSON.parse(readFileSync(STATE_PATH, "utf8")) as PendingState;
  } catch {
    return { version: 1, pending: {} };
  }
}

function writePendingState(state: PendingState) {
  mkdirSync(dirname(STATE_PATH), { recursive: true });
  writeFileSync(STATE_PATH, `${JSON.stringify(state, null, 2)}\n`, "utf8");
}

function pendingKey(ctx: {
  channel?: string;
  channelId?: string;
  accountId?: string;
  conversationId?: string;
  senderId?: string;
  from?: string;
}) {
  return [
    ctx.channelId ?? ctx.channel ?? "unknown",
    ctx.senderId ?? "unknown",
  ].join(":");
}

function cleanExpired(state: PendingState) {
  const now = Date.now();
  for (const [key, pending] of Object.entries(state.pending)) {
    if (now - pending.createdAt > PENDING_TTL_MS) delete state.pending[key];
  }
}

function sourceRef(ctx: {
  channel?: string;
  channelId?: string;
  senderId?: string;
  sessionKey?: string;
}) {
  const channel = ctx.channelId ?? ctx.channel ?? "telegram";
  const sender = ctx.senderId ? ` sender ${ctx.senderId}` : "";
  const session = ctx.sessionKey ? ` session ${ctx.sessionKey}` : "";
  return `${channel}${sender}${session}`.trim();
}

function titleFromTranscript(text: string) {
  const first = text
    .split(/\r?\n/)
    .map((line) => line.trim())
    .find(Boolean);
  if (!first || first.length > 120 || /^(assistant|you|user):/i.test(first)) {
    return "";
  }
  return first;
}

function todayIso() {
  return new Date().toISOString().slice(0, 10);
}

function conciseReplyFromResult(raw: string) {
  const parsed = JSON.parse(raw);
  const preview = parsed.preview ?? parsed;
  return (
    preview.telegram_message ??
    preview.telegramMessage ??
    `Filed brainstorm digest${parsed.page_id ? ` ${parsed.page_id}` : ""}.`
  );
}

function runBrainstormApply(transcript: string, ctx: { senderId?: string; sessionKey?: string }) {
  return new Promise<string>((resolve) => {
    const args = [
      SCRIPT_PATH,
      "--apply-brainstorm-stdin",
      "--brainstorm-date",
      todayIso(),
      "--brainstorm-source-ref",
      sourceRef({ channelId: "telegram", senderId: ctx.senderId, sessionKey: ctx.sessionKey }),
    ];
    const title = titleFromTranscript(transcript);
    if (title) args.push("--brainstorm-title", title);

    const child = spawn("python", args, {
      cwd: WORKSPACE_DIR,
      env: { ...process.env },
      windowsHide: true,
      stdio: ["pipe", "pipe", "pipe"],
    });

    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (chunk) => {
      stdout += chunk.toString();
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString();
    });
    child.on("error", (err) => {
      resolve(`I couldn't file that brainstorm yet: ${err.message}`);
    });
    child.on("close", (code) => {
      if (code !== 0) {
        const message = stderr.trim().split(/\r?\n/).slice(-1)[0] || `exit code ${code}`;
        resolve(`I couldn't file that brainstorm yet: ${message}`);
        return;
      }
      try {
        resolve(conciseReplyFromResult(stdout));
      } catch {
        resolve("Filed the brainstorm digest, but I could not format the filing summary.");
      }
    });
    child.stdin.end(transcript, "utf8");
  });
}

const fridayBrainstormPlugin = {
  id: "friday-brainstorm",
  name: "Friday Brainstorm Intake",
  description: "Deterministic Voicepal brainstorming intake for Friday.",
  register(api: any) {
    api.registerCommand({
      name: "brainstorm",
      description: "File a Voicepal brainstorming transcript as a Notion digest.",
      acceptsArgs: true,
      requireAuth: true,
      nativeProgressMessages: {
        telegram: "Filing brainstorm digest...",
      },
      handler: async (ctx: any) => {
        const transcript = (ctx.args ?? "").trim();
        if (transcript) {
          return { text: await runBrainstormApply(transcript, ctx) };
        }

        const state = readPendingState();
        cleanExpired(state);
        state.pending[pendingKey(ctx)] = {
          createdAt: Date.now(),
          source: sourceRef(ctx),
        };
        writePendingState(state);
        return {
          text: "Ready. Send the Voicepal brainstorming transcript in your next message and I will file the digest.",
        };
      },
    });

    api.on("before_dispatch", async (event: any, ctx: any) => {
      if ((ctx.channelId ?? event.channel) !== "telegram") return;
      const content = (event.content ?? event.body ?? "").trim();
      if (!content || content.startsWith("/")) return;

      const state = readPendingState();
      cleanExpired(state);
      const key = pendingKey(ctx);
      if (!state.pending[key]) {
        writePendingState(state);
        return;
      }

      delete state.pending[key];
      writePendingState(state);

      if (content.length < 200) {
        return {
          handled: true,
          text: "That does not look like a full Voicepal transcript. Send `/brainstorm` again when you are ready to file one.",
        };
      }

      return {
        handled: true,
        text: await runBrainstormApply(content, ctx),
      };
    });
  },
};

export default fridayBrainstormPlugin;
