#!/usr/bin/env node
import { homedir } from "node:os";
import { join } from "node:path";
import { benchmarkSuiteDigest } from "./benchmark-suite.mjs";
import { acquireRoutingLock, hasComparableCost, isBenchmarkCurrent, isCatalogFresh, modelCost, readJson, routingPaths, writeJsonAtomic } from "./routing-lib.mjs";

const root = join(homedir(), ".config", "opencode", "model-routing");
const releaseLock = await acquireRoutingLock(root);
try {
const paths = routingPaths(root);
const policy = await readJson(paths.policy);
const approved = await readJson(paths.approved);
const catalog = await readJson(paths.catalog);
const candidates = await readJson(paths.candidates);
const benchmarks = await readJson(paths.benchmarks);
if (catalog.generation !== candidates.generation) throw new Error("catalog and candidates generations do not match");
if (!isCatalogFresh(catalog, policy.catalog_max_age_hours)) throw new Error("catalog is stale; refusing automatic promotion");
const modelByName = new Map(catalog.models.map((model) => [model.full_name, model]));
const benchmarksByCandidate = new Map((benchmarks.results ?? []).map((result) => [`${result.provider}/${result.model}/${result.tier}`, result]));
const promotions = [];

for (const [routeName, route] of Object.entries(approved.routes)) {
  if (policy.manual_global_routes.includes(routeName)) continue;
  if (!policy.auto_promotion_tiers.includes(route.tier)) continue;
  const current = modelByName.get(`${route.provider}/${route.model}`);
  if (!current || !hasComparableCost(current)) continue;
  const providerCandidates = candidates.providers[route.provider]?.[route.tier] ?? [];
  const passing = providerCandidates.filter((candidate) => {
    const result = benchmarksByCandidate.get(`${route.provider}/${candidate.model}/${route.tier}`);
    const digest = benchmarkSuiteDigest(route.tier, policy.tiers[route.tier].minimum_quality, policy.benchmark_suite_version);
    if (!isBenchmarkCurrent(result, policy, digest)) return false;
    if (!candidate.pricing_comparable) return false;
    if (Number(candidate.quality_score) < policy.tiers[route.tier].minimum_quality) return false;
    return candidate.effective_catalog_cost <= modelCost(current);
  });
  if (passing.length === 0) continue;
  const winner = passing[0];
  if (winner.model === route.model) continue;
  promotions.push({ route: routeName, from: route.model, to: winner.model, tier: route.tier });
  approved.routes[routeName] = {
    ...route,
    model: winner.model,
    variant: null,
    basis: `automatic promotion after passing ${route.tier} benchmark at lower or equal catalog cost`,
    promoted_at: new Date().toISOString()
  };
}

if (promotions.length > 0) {
  approved.updated_at = new Date().toISOString();
  await writeJsonAtomic(paths.approved, approved);
}
process.stdout.write(`${JSON.stringify({ promotions, restart_required: promotions.length > 0 }, null, 2)}\n`);
} finally {
  await releaseLock();
}
