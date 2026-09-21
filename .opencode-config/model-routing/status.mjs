#!/usr/bin/env node
import { homedir } from "node:os";
import { join } from "node:path";
import { benchmarkSuiteDigest } from "./benchmark-suite.mjs";
import { isBenchmarkCurrent, readJson, routingPaths } from "./routing-lib.mjs";

const root = join(homedir(), ".config", "opencode", "model-routing");
const paths = routingPaths(root);
const [policy, approved, catalog, candidates] = await Promise.all([
  readJson(paths.policy),
  readJson(paths.approved),
  readJson(paths.catalog),
  readJson(paths.candidates)
]);
const catalogModels = new Set(catalog.models.map((model) => model.full_name));
const benchmarks = await readJson(paths.benchmarks);
const benchmarkByRoute = new Map((benchmarks.results ?? []).map((result) => [`${result.provider}/${result.model}/${result.tier}`, result]));
const routes = Object.entries(approved.routes).map(([name, route]) => {
  const benchmark = benchmarkByRoute.get(`${route.provider}/${route.model}/${route.tier}`);
  const expectedDigest = policy.auto_promotion_tiers.includes(route.tier)
    ? benchmarkSuiteDigest(route.tier, policy.tiers[route.tier].minimum_quality, policy.benchmark_suite_version)
    : null;
  const benchmarkStatus = !benchmark
    ? "manual_or_not_evaluated"
    : expectedDigest && isBenchmarkCurrent(benchmark, policy, expectedDigest) ? "passed" : "stale_or_invalid";
  return {
  name,
  tier: route.tier,
  model: `${route.provider}/${route.model}`,
  variant: route.variant,
  available_in_catalog: catalogModels.has(`${route.provider}/${route.model}`),
  approval_required: policy.approval_required_tiers.includes(route.tier),
  benchmark_status: benchmarkStatus,
  startup_fallback: route.startup_fallback ? `${route.startup_fallback.provider}/${route.startup_fallback.model}` : null
  };
});
const unevaluated = Object.values(candidates.providers)
  .flatMap((tiers) => Object.values(tiers).flat())
  .filter((candidate) => candidate.benchmark_status === "not_evaluated" || candidate.benchmark_suite_version !== policy.benchmark_suite_version).length;
process.stdout.write(`${JSON.stringify({ catalog_refreshed_at: catalog.refreshed_at, catalog_models: catalog.models.length, unevaluated_candidates: unevaluated, routes }, null, 2)}\n`);
