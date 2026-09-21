#!/usr/bin/env node
import { homedir } from "node:os";
import { join } from "node:path";
import { acquireRoutingLock, classifyTitle, readJson, run, writeJsonAtomic } from "./routing-lib.mjs";

const home = homedir();
const database = join(home, ".local", "share", "opencode", "opencode.db");
const root = join(home, ".config", "opencode", "model-routing");
const releaseLock = await acquireRoutingLock(root);
try {
const rows = JSON.parse(run("sqlite3", [
  "-readonly",
  "-json",
  database,
  "SELECT id,title,agent,model,cost,tokens_input,tokens_output,tokens_reasoning,tokens_cache_read,time_created FROM session ORDER BY time_created"
]));

const sessions = rows.map((row) => {
  let model = {};
  try { model = JSON.parse(row.model || "{}"); } catch {}
  return {
    agent: row.agent,
    provider: model.providerID ?? "unknown",
    model: model.id ?? "unknown",
    variant: model.variant ?? null,
    category: classifyTitle(row.title || "", row.agent || ""),
    recorded_cost: Number(row.cost || 0),
    tokens: {
      input: Number(row.tokens_input || 0),
      output: Number(row.tokens_output || 0),
      reasoning: Number(row.tokens_reasoning || 0),
      cache_read: Number(row.tokens_cache_read || 0)
    },
    created_at: new Date(Number(row.time_created)).toISOString()
  };
});

const groups = {};
for (const session of sessions) {
  const key = `${session.provider}/${session.model}`;
  groups[key] ??= { provider: session.provider, model: session.model, sessions: 0, recorded_cost: 0, tokens: { input: 0, output: 0, reasoning: 0, cache_read: 0 }, categories: {} };
  const group = groups[key];
  group.sessions += 1;
  group.recorded_cost += session.recorded_cost;
  for (const tokenType of Object.keys(group.tokens)) group.tokens[tokenType] += session.tokens[tokenType];
  group.categories[session.category] = (group.categories[session.category] ?? 0) + 1;
}

const audit = {
  schema_version: 1,
  generated_at: new Date().toISOString(),
  limitations: [
    "OAuth, subscription, and included-quota providers may record zero cost; zero is not proof of unlimited free usage.",
    "Title classification is heuristic and does not inspect prompt content.",
    "Historical prices are not reconstructed; recorded costs and tokens are reported separately."
  ],
  totals: { sessions: sessions.length, models: Object.keys(groups).length },
  groups: Object.values(groups).sort((a, b) => b.sessions - a.sessions)
};
await writeJsonAtomic(join(root, "history-audit.json"), audit);

const policy = await readJson(join(root, "policy.json"));
const covered = new Set(audit.groups.map((group) => group.provider));
process.stdout.write(`${JSON.stringify({
  generated_at: audit.generated_at,
  sessions: audit.totals.sessions,
  historical_providers: [...covered].sort(),
  configured_providers: Object.keys(policy.providers),
  output: join(root, "history-audit.json")
}, null, 2)}\n`);
} finally {
  await releaseLock();
}
