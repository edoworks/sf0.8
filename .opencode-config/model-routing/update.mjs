#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import { homedir } from "node:os";
import { join } from "node:path";
import { acquireRoutingLock } from "./routing-lib.mjs";

const root = join(homedir(), ".config", "opencode", "model-routing");
const releaseLock = await acquireRoutingLock(root);
try {
const commands = [
  ["refresh-catalog.mjs"],
  ["audit-history.mjs"],
  ["benchmark-models.mjs"],
  ["refresh-catalog.mjs"],
  ["promote-routes.mjs"]
];
const outcomes = [];
for (const [script] of commands) {
  const result = spawnSync(process.execPath, [join(root, script)], {
    encoding: "utf8",
    timeout: 20 * 60 * 1000,
    maxBuffer: 100 * 1024 * 1024,
    env: { ...process.env, MODEL_ROUTING_LOCK_TOKEN: releaseLock.token, MODEL_ROUTING_MAX_BENCHMARKS: process.env.MODEL_ROUTING_MAX_BENCHMARKS ?? "4" }
  });
  outcomes.push({ script, status: result.status, output: (result.stdout || result.stderr).trim().slice(0, 2000) });
  if (result.status !== 0) break;
}
process.stdout.write(`${JSON.stringify({ updated_at: new Date().toISOString(), outcomes }, null, 2)}\n`);
if (outcomes.some((outcome) => outcome.status !== 0)) process.exit(1);
} finally {
  await releaseLock();
}
