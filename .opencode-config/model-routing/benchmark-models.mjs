#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { homedir } from "node:os";
import { join } from "node:path";
import { benchmarkFixtures as fixtures, benchmarkSuiteDigest, evaluateBenchmarkFixture } from "./benchmark-suite.mjs";
import { acquireRoutingLock, applyBenchmarkStatuses, candidatesFor, needsBenchmark, readJson, routingPaths, writeJsonAtomic } from "./routing-lib.mjs";

const root = join(homedir(), ".config", "opencode", "model-routing");
const releaseLock = await acquireRoutingLock(root);
try {
const paths = routingPaths(root);
const policy = await readJson(paths.policy);
const catalog = await readJson(paths.catalog);
const benchmarks = await readJson(paths.benchmarks);
const requestedModel = process.argv.find((argument) => argument.startsWith("--model="))?.slice(8);
const requestedTier = process.argv.find((argument) => argument.startsWith("--tier="))?.slice(7);
const maxModels = Number(process.env.MODEL_ROUTING_MAX_BENCHMARKS ?? "4");

function responseText(stdout) {
  const chunks = [];
  for (const line of stdout.split("\n")) {
    if (!line.trim()) continue;
    try {
      const event = JSON.parse(line);
      if (event.type === "text" && typeof event.part?.text === "string") chunks.push(event.part.text);
    } catch {}
  }
  return chunks.join("").trim();
}

function runFixture(fullName, fixture) {
  const started = Date.now();
  const result = spawnSync("opencode", ["run", "--pure", "--model", fullName, "--format", "json", fixture.prompt], {
    encoding: "utf8",
    timeout: Number(process.env.MODEL_ROUTING_BENCHMARK_TIMEOUT_MS ?? "180000"),
    maxBuffer: 20 * 1024 * 1024
  });
  const text = responseText(result.stdout || "");
  return {
    passed: result.status === 0 && evaluateBenchmarkFixture(fixture, text),
    duration_ms: Date.now() - started,
    exit_status: result.status,
    response_sha256: createHash("sha256").update(text).digest("hex"),
    error: result.status === 0 ? null : "benchmark process failed"
  };
}

const candidates = applyBenchmarkStatuses(candidatesFor(catalog, policy), benchmarks);
const targets = [];
if (requestedModel && requestedTier) {
  const slash = requestedModel.indexOf("/");
  if (slash < 1 || !fixtures[requestedTier]) throw new Error("use --model=provider/model with --tier=routine|standard");
  targets.push({ provider: requestedModel.slice(0, slash), model: requestedModel.slice(slash + 1), tier: requestedTier });
} else {
  for (const [provider, tiers] of Object.entries(candidates)) {
    for (const tier of policy.auto_promotion_tiers) {
      const candidate = tiers[tier]?.find((model) => {
        const expectedDigest = benchmarkSuiteDigest(tier, policy.tiers[tier].minimum_quality, policy.benchmark_suite_version);
        return needsBenchmark(model, policy, expectedDigest);
      });
      if (candidate) targets.push({ provider, model: candidate.model, tier });
    }
  }
}

const selected = targets.slice(0, maxModels);
const results = [];
for (const target of selected) {
  const fullName = `${target.provider}/${target.model}`;
  const fixtureResults = [];
  for (const fixture of fixtures[target.tier]) {
    fixtureResults.push(runFixture(fullName, fixture));
  }
  const qualityScore = fixtureResults.filter((result) => result.passed).length / fixtureResults.length;
  const executionFailed = fixtureResults.some((result) => result.exit_status !== 0);
  const result = {
    provider: target.provider,
    model: target.model,
    tier: target.tier,
    status: executionFailed ? "error" : qualityScore >= policy.tiers[target.tier].minimum_quality ? "passed" : "failed",
    suite_version: policy.benchmark_suite_version,
    quality_score: qualityScore,
    measured_at: new Date().toISOString(),
    fixture_set_sha256: benchmarkSuiteDigest(target.tier, policy.tiers[target.tier].minimum_quality, policy.benchmark_suite_version),
    fixtures: fixtureResults
  };
  const prior = benchmarks.results.findIndex((entry) => entry.provider === target.provider && entry.model === target.model && entry.tier === target.tier);
  if (prior >= 0) benchmarks.results[prior] = result;
  else benchmarks.results.push(result);
  results.push(result);
}
benchmarks.updated_at = new Date().toISOString();
await writeJsonAtomic(paths.benchmarks, benchmarks);
process.stdout.write(`${JSON.stringify({ evaluated: results, remaining_targets: Math.max(0, targets.length - selected.length) }, null, 2)}\n`);
} finally {
  await releaseLock();
}
