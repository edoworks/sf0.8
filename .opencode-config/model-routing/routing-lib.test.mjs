import test from "node:test";
import assert from "node:assert/strict";
import { mkdir, mkdtemp, rm, utimes, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { benchmarkFixtures, benchmarkSuiteDigest, evaluateBenchmarkFixture } from "./benchmark-suite.mjs";
import { acquireRoutingLock, applyBenchmarkStatuses, applyTrustedPricing, assertTierCoherence, candidatesFor, classifyTitle, hasComparableCost, isBenchmarkCurrent, isCatalogFresh, modelCost, needsBenchmark, normalizeCatalogModel, parseVerboseModels, sanitizeError, supportsRoute, supportsTier } from "./routing-lib.mjs";

const model = {
  full_name: "demo/cheap",
  provider: "demo",
  model: "cheap",
  status: "active",
  release_date: "2026-01-01",
  cost: { input: 1, output: 2, cache: { read: 0.1 } },
  capabilities: { toolcall: true, reasoning: true, attachment: true, input: { text: true, image: true }, output: { text: true } }
};

test("parseVerboseModels parses sequential model records", () => {
  const parsed = parseVerboseModels(`demo/cheap\n${JSON.stringify(model, null, 2)}\n`);
  assert.equal(parsed.length, 1);
  assert.equal(parsed[0].full_name, "demo/cheap");
});

test("modelCost weights output and cache reads", () => {
  assert.equal(modelCost(model), 8);
});

test("missing prices are not comparable", () => {
  assert.equal(hasComparableCost(model), true);
  assert.equal(hasComparableCost({ ...model, cost: { input: 0, output: 0 } }), false);
});

test("catalog normalization drops provider internals", () => {
  const normalized = normalizeCatalogModel({ ...model, api: { url: "https://user:secret@example.test" }, headers: { authorization: "secret" }, variants: { low: { apiKey: "secret" } } });
  assert.equal("api" in normalized, false);
  assert.equal("headers" in normalized, false);
  assert.deepEqual(normalized.variants, ["low"]);
});

test("trusted subscription pricing replaces misleading catalog zeroes", () => {
  const freeClaim = { ...model, provider: "ollama-cloud", model: "cheap", cost: { input: 0, output: 0, cache: { read: 0 } } };
  const pricing = { updated_at: "2026-09-04T00:00:00Z", sources: { "ollama-cloud": "https://example.test/pricing" }, providers: { "ollama-cloud": { models: { cheap: { input: 0.2, cached_input: 0.01, output: 0.6 } } } } };
  const [priced] = applyTrustedPricing([freeClaim], pricing);
  assert.deepEqual(priced.cost, { input: 0.2, output: 0.6, cache: { read: 0.01, write: null } });
  assert.equal(priced.price_source, "https://example.test/pricing");
  const [unknown] = applyTrustedPricing([{ ...freeClaim, model: "unknown" }], pricing);
  assert.equal(unknown.cost, null);
  assert.equal(hasComparableCost(unknown), false);
});

test("error sanitization removes credentials and query secrets", () => {
  const sanitized = sanitizeError("https://user:pass@example.test/x?token=abc Bearer secret-token");
  assert.doesNotMatch(sanitized, /pass|token=abc|secret-token/);
});

test("catalog freshness rejects missing and old timestamps", () => {
  const now = Date.parse("2026-08-21T12:00:00Z");
  assert.equal(isCatalogFresh({}, 48, now), false);
  assert.equal(isCatalogFresh({ refreshed_at: "2026-08-20T12:00:00Z" }, 48, now), true);
  assert.equal(isCatalogFresh({ refreshed_at: "2026-08-18T12:00:00Z" }, 48, now), false);
  assert.equal(isCatalogFresh({ refreshed_at: "2026-08-22T12:00:00Z" }, 48, now), false);
});

test("benchmark currency binds digest and rejects future evidence", () => {
  const policy = { benchmark_suite_version: 2, benchmark_max_age_days: 30 };
  const now = Date.parse("2026-08-21T12:00:00Z");
  const result = { status: "passed", suite_version: 2, fixture_set_sha256: "abc", measured_at: "2026-08-21T11:00:00Z" };
  assert.equal(isBenchmarkCurrent(result, policy, "abc", now), true);
  assert.equal(isBenchmarkCurrent(result, policy, "def", now), false);
  assert.equal(isBenchmarkCurrent({ ...result, measured_at: "2026-08-22T12:00:00Z" }, policy, "abc", now), false);
});

test("benchmark suite digest and checks are declarative", () => {
  const digest = benchmarkSuiteDigest("routine", 0.8, 2);
  assert.match(digest, /^[a-f0-9]{64}$/);
  assert.equal(evaluateBenchmarkFixture(benchmarkFixtures.routine[0], '{"policy":"AGENTS.md","test":"npm test"}'), true);
  assert.equal(evaluateBenchmarkFixture(benchmarkFixtures.standard[2], '{"allowed":false,"reason":"Docker socket policy"}'), true);
  assert.equal(evaluateBenchmarkFixture(benchmarkFixtures.standard[2], '{"allowed":true,"reason":"allowed"}'), false);
});

test("routing lock rejects a concurrent writer", async () => {
  const root = await mkdtemp(join(tmpdir(), "model-routing-test-"));
  const release = await acquireRoutingLock(root);
  await assert.rejects(() => acquireRoutingLock(root), /already in progress/);
  await release();
  await rm(root, { recursive: true, force: true });
});

test("routing lock recovers an old ownerless lock", async () => {
  const root = await mkdtemp(join(tmpdir(), "model-routing-test-"));
  const lock = join(root, ".update.lock");
  await mkdir(lock);
  await writeFile(join(lock, "owner.json"), "corrupt");
  const old = new Date(Date.now() - 3 * 60 * 60 * 1000);
  await utimes(lock, old, old);
  const release = await acquireRoutingLock(root);
  await release();
  await rm(root, { recursive: true, force: true });
});

test("supportsTier enforces reasoning and vision", () => {
  assert.equal(supportsTier(model, "standard"), true);
  assert.equal(supportsTier(model, "vision"), true);
  assert.equal(supportsTier({ ...model, capabilities: { ...model.capabilities, reasoning: false } }, "standard"), false);
});

test("supportsRoute enforces active capabilities and variants", () => {
  const normalized = { ...model, variants: ["low"] };
  assert.equal(supportsRoute(normalized, { tier: "standard", variant: "low" }), true);
  assert.equal(supportsRoute({ ...normalized, status: "inactive" }, { tier: "standard", variant: "low" }), false);
  assert.equal(supportsRoute({ ...normalized, status: null }, { tier: "standard", variant: "low" }), false);
  assert.equal(supportsRoute(normalized, { tier: "standard", variant: "missing" }), false);
});

test("benchmark errors back off so later candidates can run", () => {
  const policy = { benchmark_suite_version: 2, benchmark_max_age_days: 30, benchmark_error_retry_hours: 24 };
  const now = Date.parse("2026-08-21T12:00:00Z");
  const failed = { pricing_comparable: true, benchmark_status: "error", benchmarked_at: "2026-08-21T11:00:00Z" };
  assert.equal(needsBenchmark(failed, policy, "abc", now), false);
  assert.equal(needsBenchmark({ ...failed, benchmarked_at: "2026-08-20T11:00:00Z" }, policy, "abc", now), true);
  assert.equal(needsBenchmark({ pricing_comparable: true, benchmark_status: "not_evaluated" }, policy, "abc", now), true);
});

test("invalid and future benchmark timestamps are rescheduled", () => {
  const policy = { benchmark_suite_version: 2, benchmark_max_age_days: 30, benchmark_error_retry_hours: 24 };
  const now = Date.parse("2026-08-21T12:00:00Z");
  const current = { pricing_comparable: true, benchmark_status: "passed", benchmark_suite_version: 2, benchmark_fixture_set_sha256: "abc" };
  assert.equal(needsBenchmark({ ...current, benchmarked_at: "invalid" }, policy, "abc", now), true);
  assert.equal(needsBenchmark({ ...current, benchmarked_at: "2026-08-22T12:00:00Z" }, policy, "abc", now), true);
  assert.equal(needsBenchmark({ ...current, benchmarked_at: "2026-08-21T11:00:00Z" }, policy, "abc", now), false);
});

test("benchmark status propagation includes fixture digest", () => {
  const candidates = { demo: { routine: [{ model: "cheap", benchmark_status: "not_evaluated" }] } };
  const result = applyBenchmarkStatuses(candidates, { results: [{ provider: "demo", model: "cheap", tier: "routine", status: "passed", fixture_set_sha256: "abc" }] });
  assert.equal(result.demo.routine[0].benchmark_fixture_set_sha256, "abc");
});

test("candidates sort by cost before recency", () => {
  const expensive = { ...model, full_name: "demo/new", model: "new", release_date: "2026-08-01", cost: { input: 10, output: 10 } };
  const result = candidatesFor({ models: [expensive, model] }, { providers: { demo: { enabled: true } }, tiers: { routine: {} } });
  assert.equal(result.demo.routine[0].model, "cheap");
});

test("classifyTitle identifies mechanical and exploration work", () => {
  assert.equal(classifyTitle("Create commit", "general"), "deterministic_or_mechanical");
  assert.equal(classifyTitle("Map API", "explore"), "routine_exploration");
  assert.equal(classifyTitle("Crop screenshot and resize it", "general"), "deterministic_or_mechanical");
  assert.equal(classifyTitle("Rename router module", "build"), "deterministic_or_mechanical");
  assert.equal(classifyTitle("Close issue 13", "general"), "deterministic_or_mechanical");
  assert.equal(classifyTitle("Design cross-module routing", "build"), "construction_or_other");
});

test("assertTierCoherence blocks routine-class work on complex routes", () => {
  assert.throws(() => assertTierCoherence("deterministic_or_mechanical", "complex", "openai/gpt-5.6-terra"), /routine-class task/);
  assert.throws(() => assertTierCoherence("routine_exploration", "complex", "openai/gpt-5.6-terra"), /routine-class task/);
  assert.throws(() => assertTierCoherence("deterministic_or_mechanical", "standard", "openai/gpt-5.6-luna"), /routine-class task/);
  assert.equal(assertTierCoherence("construction_or_other", "complex", "openai/gpt-5.6-terra"), "complex");
});
