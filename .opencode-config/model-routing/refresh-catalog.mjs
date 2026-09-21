#!/usr/bin/env node
import { homedir } from "node:os";
import { join } from "node:path";
import {
  acquireRoutingLock,
  applyTrustedPricing,
  applyBenchmarkStatuses,
  candidatesFor,
  normalizeCatalogModel,
  parseVerboseModels,
  readJson,
  routingPaths,
  run,
  sanitizeError,
  writeJsonAtomic
} from "./routing-lib.mjs";

const root = join(homedir(), ".config", "opencode", "model-routing");
const releaseLock = await acquireRoutingLock(root);
try {
const paths = routingPaths(root);
const policy = await readJson(paths.policy);
const benchmarks = await readJson(paths.benchmarks);
const pricing = await readJson(join(root, "provider-pricing.json"));

run("opencode", ["models", "--refresh"]);
const models = [];
const failures = [];
for (const [provider, providerPolicy] of Object.entries(policy.providers)) {
  if (!providerPolicy.enabled) continue;
  try {
    const output = run("opencode", ["models", provider, "--verbose"]);
    models.push(...parseVerboseModels(output));
  } catch (error) {
    failures.push({ provider, error: sanitizeError(error.message) });
  }
}

if (failures.length > 0) throw new Error(`catalog refresh incomplete; retaining last known-good catalog: ${JSON.stringify(failures)}`);
if (models.length === 0) throw new Error("catalog refresh returned no models; retaining last known-good catalog");
const now = new Date().toISOString();
const generation = `${Date.now()}-${process.pid}`;
const catalog = {
  schema_version: 1,
  generation,
  refreshed_at: now,
  providers: Object.keys(policy.providers),
  failures,
  models: applyTrustedPricing(models.map(normalizeCatalogModel), pricing).sort((a, b) => a.full_name.localeCompare(b.full_name))
};
const candidates = {
  schema_version: 1,
  generation,
  refreshed_at: now,
  promotion_policy: "routine and standard require passing benchmarks; other tiers also require operator approval",
  providers: applyBenchmarkStatuses(candidatesFor(catalog, policy), benchmarks)
};

await writeJsonAtomic(paths.catalog, catalog);
await writeJsonAtomic(paths.candidates, candidates);
process.stdout.write(`${JSON.stringify({ refreshed_at: now, models: models.length, failures }, null, 2)}\n`);
} finally {
  await releaseLock();
}
