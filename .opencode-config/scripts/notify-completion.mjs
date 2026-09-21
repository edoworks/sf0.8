#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { closeSync, constants, fstatSync, lstatSync, openSync, readFileSync } from "node:fs";
import { dirname } from "node:path";
import { pathToFileURL } from "node:url";

export const EXACT_ENDPOINT = "https://ntfy.sh";
export const TOPIC_FILE = "/Users/hello/factory-secrets/ntfy_topic";
export const TOPIC_PATTERN = /^[-_a-zA-Z0-9]{32,64}$/;

export function loadTopic({
  path = TOPIC_FILE,
  lstat = lstatSync,
  open = openSync,
  fstat = fstatSync,
  readFile = readFileSync,
  close = closeSync,
  uid = process.getuid(),
} = {}) {
  let descriptor;
  try {
    const directory = lstat(dirname(path));
    if (!directory.isDirectory() || directory.isSymbolicLink() || (directory.mode & 0o777) !== 0o700 || directory.uid !== uid) return null;
    descriptor = open(path, constants.O_RDONLY | constants.O_NOFOLLOW);
    const file = fstat(descriptor);
    if (!file.isFile() || (file.mode & 0o777) !== 0o400 || file.uid !== uid || file.size > 128) return null;
    const topic = readFile(descriptor, "utf8").trim();
    return TOPIC_PATTERN.test(topic) ? topic : null;
  } catch {
    return null;
  } finally {
    if (descriptor !== undefined) close(descriptor);
  }
}

export async function publishCompletion({
  result = "completed",
  topic,
  endpoint = EXACT_ENDPOINT,
  retries = 3,
  fetchImpl = fetch,
  sleep = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds)),
  timeoutMs = 10_000,
} = {}) {
  if (!new Set(["completed", "blocked"]).has(result)) throw new Error("result must be completed or blocked");
  if (!TOPIC_PATTERN.test(topic ?? "")) return { status: "not_configured" };
  if (endpoint !== EXACT_ENDPOINT) throw new Error("endpoint must be exactly https://ntfy.sh");
  if (!Number.isInteger(retries) || retries < 1 || retries > 5) throw new Error("retries must be between 1 and 5");
  if (!Number.isInteger(timeoutMs) || timeoutMs < 1_000 || timeoutMs > 30_000) throw new Error("timeout must be between 1000 and 30000ms");

  const title = result === "completed" ? "OpenCode task complete" : "OpenCode task blocked";
  const message = result === "completed" ? "A non-trivial OpenCode task completed." : "A non-trivial OpenCode task needs attention.";
  for (let attempt = 1; attempt <= retries; attempt += 1) {
    try {
      const response = await fetchImpl(EXACT_ENDPOINT, {
        method: "POST",
        redirect: "error",
        signal: AbortSignal.timeout(timeoutMs),
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          topic,
          message,
          title,
          tags: [result === "completed" ? "white_check_mark" : "warning"],
        }),
      });
      if (response.ok) return { status: "sent", attempts: attempt };
      if (response.status !== 429) return { status: "failed", attempts: attempt };
    } catch {
      // The server may have accepted a timed-out request. Do not risk a duplicate.
      return { status: "delivery_uncertain", attempts: attempt };
    }
    if (attempt < retries) await sleep(100 * 2 ** (attempt - 1));
  }
  return { status: "failed", attempts: retries };
}

export function sendLocalFallback(result, spawn = spawnSync) {
  const message = result === "completed" ? "OpenCode task complete" : "OpenCode task blocked";
  const notification = spawn("/usr/bin/osascript", ["-e", `display notification "${message}" with title "OpenCode"`], {
    encoding: "utf8",
    stdio: "ignore",
    timeout: 5_000,
  });
  return notification.status === 0 ? "sent" : "failed";
}

export async function notifyCompletion({ result = "completed", spawn = spawnSync, topicSource, ...options } = {}) {
  try {
    const topic = loadTopic(topicSource);
    const delivery = await publishCompletion({ ...options, result, topic });
    return delivery.status === "sent" ? delivery : { ...delivery, fallback: sendLocalFallback(result, spawn) };
  } catch {
    return { status: "failed_before_delivery", fallback: sendLocalFallback(result, spawn) };
  }
}

async function main() {
  const resultIndex = process.argv.indexOf("--result");
  const result = resultIndex === -1 ? "completed" : process.argv[resultIndex + 1];
  if (!new Set(["completed", "blocked"]).has(result)) {
    process.exitCode = 2;
    process.stdout.write(`${JSON.stringify({ status: "invalid_arguments" })}\n`);
    return;
  }
  process.stdout.write(`${JSON.stringify(await notifyCompletion({ result }))}\n`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) await main();
