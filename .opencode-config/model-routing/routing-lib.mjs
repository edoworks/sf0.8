import { spawnSync } from "node:child_process";
import { randomUUID } from "node:crypto";
import { mkdir, readFile, rename, rm, stat, writeFile } from "node:fs/promises";
import { join } from "node:path";

export async function readJson(path) {
  return JSON.parse(await readFile(path, "utf8"));
}

export async function writeJsonAtomic(path, value) {
  const temporary = `${path}.${process.pid}.tmp`;
  await writeFile(temporary, `${JSON.stringify(value, null, 2)}\n`, { encoding: "utf8", mode: 0o600 });
  await rename(temporary, path);
}

export async function acquireRoutingLock(root) {
  const lock = join(root, ".update.lock");
  const owner = join(lock, "owner.json");
  const inheritedToken = process.env.MODEL_ROUTING_LOCK_TOKEN;
  if (inheritedToken) {
    const current = JSON.parse(await readFile(owner, "utf8"));
    if (current.token !== inheritedToken) throw new Error("invalid inherited model-routing lock token");
    return async () => {};
  }
  const token = randomUUID();
  const processIdentity = (pid) => spawnSync("ps", ["-o", "lstart=", "-p", String(pid)], { encoding: "utf8" }).stdout?.trim() || null;
  const create = async () => {
    await mkdir(lock);
    await writeFile(owner, `${JSON.stringify({ pid: process.pid, pid_started_at: processIdentity(process.pid), token, created_at: new Date().toISOString() })}\n`, { encoding: "utf8", mode: 0o600 });
  };
  while (true) {
    try {
      await create();
      break;
    } catch (error) {
      if (error.code !== "EEXIST") throw error;
      let current;
      try { current = JSON.parse(await readFile(owner, "utf8")); } catch {}
      let alive = false;
      if (Number.isInteger(current?.pid)) {
        try { process.kill(current.pid, 0); alive = true; } catch (pidError) { alive = pidError.code === "EPERM"; }
        if (alive && current.pid_started_at && processIdentity(current.pid) !== current.pid_started_at) alive = false;
      }
      let createdAt = Date.parse(current?.created_at);
      if (!Number.isFinite(createdAt)) {
        try { createdAt = (await stat(lock)).mtimeMs; } catch {}
      }
      const old = Number.isFinite(createdAt) && Date.now() - createdAt > 2 * 60 * 60 * 1000;
      if (!old || alive) throw new Error(`model routing update already in progress (${lock})`);
      const quarantine = `${lock}.stale-${randomUUID()}`;
      try { await rename(lock, quarantine); } catch (renameError) {
        if (renameError.code === "ENOENT") continue;
        throw renameError;
      }
      await rm(quarantine, { recursive: true, force: true });
    }
  }
  const release = async () => {
    let current;
    try { current = JSON.parse(await readFile(owner, "utf8")); } catch { return; }
    if (current.token === token) await rm(lock, { recursive: true, force: true });
  };
  release.token = token;
  return release;
}

export function parseVerboseModels(text) {
  const models = [];
  const lines = text.split("\n");
  for (let index = 0; index < lines.length; index += 1) {
    const fullName = lines[index].trim();
    if (!/^[a-z0-9-]+\/.+$/i.test(fullName) || lines[index + 1]?.trim() !== "{") continue;
    let depth = 0;
    let json = "";
    for (index += 1; index < lines.length; index += 1) {
      const line = lines[index];
      json += `${line}\n`;
      for (const character of line) {
        if (character === "{") depth += 1;
        if (character === "}") depth -= 1;
      }
      if (depth === 0) break;
    }
    const metadata = JSON.parse(json);
    const slash = fullName.indexOf("/");
    models.push({
      full_name: fullName,
      provider: fullName.slice(0, slash),
      model: fullName.slice(slash + 1),
      ...metadata
    });
  }
  return models;
}

export function run(command, args, options = {}) {
  const result = spawnSync(command, args, {
    encoding: "utf8",
    maxBuffer: 100 * 1024 * 1024,
    ...options
  });
  if (result.status !== 0) {
    throw new Error(`${command} ${args.join(" ")} failed: ${result.stderr || result.stdout}`);
  }
  return result.stdout;
}

export function modelCost(model) {
  const input = Number(model.cost?.input ?? 0);
  const output = Number(model.cost?.output ?? 0);
  const cacheRead = Number(model.cost?.cache?.read ?? model.cost?.cache_read ?? 0);
  return input + (3 * output) + (10 * cacheRead);
}

export function hasComparableCost(model) {
  const values = [model.cost?.input, model.cost?.output, model.cost?.cache?.read ?? model.cost?.cache_read];
  return values.every((value) => typeof value === "number" && Number.isFinite(value) && value >= 0);
}

export function normalizeCatalogModel(model) {
  const capability = (name) => Boolean(model.capabilities?.[name]);
  const modalities = (direction) => Object.fromEntries(
    ["text", "audio", "image", "video", "pdf"].map((name) => [name, Boolean(model.capabilities?.[direction]?.[name])])
  );
  return {
    full_name: model.full_name,
    provider: model.provider,
    model: model.model,
    id: model.id,
    providerID: model.providerID,
    name: model.name,
    family: model.family || null,
    status: model.status || null,
    release_date: model.release_date || null,
    cost: model.cost ? {
      input: model.cost.input ?? null,
      output: model.cost.output ?? null,
      cache: {
        read: model.cost.cache?.read ?? model.cost.cache_read ?? null,
        write: model.cost.cache?.write ?? model.cost.cache_write ?? null
      }
    } : null,
    limit: model.limit ? {
      context: model.limit.context ?? null,
      input: model.limit.input ?? null,
      output: model.limit.output ?? null
    } : null,
    capabilities: {
      temperature: capability("temperature"),
      reasoning: capability("reasoning"),
      attachment: capability("attachment"),
      toolcall: capability("toolcall"),
      input: modalities("input"),
      output: modalities("output"),
      interleaved: capability("interleaved")
    },
    variants: Object.keys(model.variants ?? {})
  };
}

export function applyTrustedPricing(models, pricing) {
  return models.map((model) => {
    const provider = pricing.providers?.[model.provider];
    if (!provider) return model;
    const rates = provider.models?.[model.model];
    if (!rates) return { ...model, cost: null, price_source: pricing.sources?.[model.provider] ?? null, price_updated_at: pricing.updated_at };
    return {
      ...model,
      cost: {
        input: rates.input,
        output: rates.output,
        cache: {
          read: rates.cached_input,
          write: null,
        },
      },
      price_source: pricing.sources?.[model.provider] ?? null,
      price_updated_at: pricing.updated_at,
    };
  });
}

export function sanitizeError(value) {
  return String(value)
    .replace(/https?:\/\/[^\s/@:]+:[^\s/@]+@/gi, "https://[redacted]@")
    .replace(/([?&](?:token|key|secret|password)=)[^&\s]+/gi, "$1[redacted]")
    .replace(/(bearer\s+)[a-z0-9._~+\/-]+/gi, "$1[redacted]")
    .slice(0, 1000);
}

export function isCatalogFresh(catalog, maxAgeHours, now = Date.now()) {
  const refreshedAt = Date.parse(catalog?.refreshed_at);
  const age = now - refreshedAt;
  return Number.isFinite(refreshedAt) && age >= -5 * 60 * 1000 && age <= maxAgeHours * 60 * 60 * 1000;
}

export function isBenchmarkCurrent(result, policy, expectedDigest, now = Date.now()) {
  const measuredAt = Date.parse(result?.measured_at);
  const age = now - measuredAt;
  return result?.status === "passed"
    && result.suite_version === policy.benchmark_suite_version
    && result.fixture_set_sha256 === expectedDigest
    && Number.isFinite(measuredAt)
    && age >= -5 * 60 * 1000
    && age <= policy.benchmark_max_age_days * 86400000;
}

export function supportsTier(model, tier) {
  if (model.status !== "active") return false;
  const capabilities = model.capabilities ?? {};
  if (!capabilities.toolcall || !capabilities.input?.text || !capabilities.output?.text) return false;
  if (tier === "vision") return Boolean(capabilities.input?.image && capabilities.attachment);
  if (["standard", "complex", "trust_boundary"].includes(tier)) return Boolean(capabilities.reasoning);
  return true;
}

export function needsBenchmark(model, policy, expectedDigest, now = Date.now()) {
  if (!model.pricing_comparable) return false;
  if (model.benchmark_status === "not_evaluated") return true;
  const benchmarkedAt = Date.parse(model.benchmarked_at);
  if (model.benchmark_status === "error") {
    return !Number.isFinite(benchmarkedAt)
      || now - benchmarkedAt > policy.benchmark_error_retry_hours * 3600000;
  }
  if (model.benchmark_suite_version !== policy.benchmark_suite_version) return true;
  if (model.benchmark_fixture_set_sha256 !== expectedDigest) return true;
  const age = now - benchmarkedAt;
  return !Number.isFinite(benchmarkedAt)
    || age < -5 * 60 * 1000
    || age > policy.benchmark_max_age_days * 86400000;
}

export function supportsRoute(model, route) {
  return Boolean(model)
    && supportsTier(model, route.tier)
    && (!route.variant || model.variants?.includes(route.variant));
}

export function candidatesFor(catalog, policy) {
  const output = {};
  for (const [provider, providerPolicy] of Object.entries(policy.providers)) {
    if (!providerPolicy.enabled) continue;
    output[provider] = {};
    for (const tier of Object.keys(policy.tiers)) {
      output[provider][tier] = catalog.models
        .filter((model) => model.provider === provider && supportsTier(model, tier))
        .sort((a, b) => {
          const costDifference = modelCost(a) - modelCost(b);
          if (costDifference !== 0) return costDifference;
          return String(b.release_date ?? "").localeCompare(String(a.release_date ?? ""));
        })
        .map((model) => ({
          model: model.model,
          release_date: model.release_date || null,
          effective_catalog_cost: modelCost(model),
          pricing_comparable: hasComparableCost(model),
          cost: model.cost,
          context: model.limit?.context ?? null,
          benchmark_status: "not_evaluated"
        }));
    }
  }
  return output;
}

export function applyBenchmarkStatuses(candidates, benchmarks) {
  const byKey = new Map();
  for (const result of benchmarks.results ?? []) {
    byKey.set(`${result.provider}/${result.model}/${result.tier}`, result);
  }
  for (const [provider, tiers] of Object.entries(candidates)) {
    for (const [tier, models] of Object.entries(tiers)) {
      for (const model of models) {
        const result = byKey.get(`${provider}/${model.model}/${tier}`);
        if (result) {
          model.benchmark_status = result.status;
          model.quality_score = result.quality_score;
          model.benchmarked_at = result.measured_at;
          model.benchmark_suite_version = result.suite_version ?? null;
          model.benchmark_fixture_set_sha256 = result.fixture_set_sha256 ?? null;
        }
      }
    }
  }
  return candidates;
}

export function classifyTitle(title, agent) {
  const normalized = title.toLowerCase();
  if (agent === "explore" || /\b(explore|map|locate|search)\b/.test(normalized)) return "routine_exploration";
  if (/\b(commit|bookkeeping|format|state edit|screenshot|crop|resize|ocr|rename|notify|notification|status check|status|doctor|verify|ledger|baseline|restart|cleanup|run command|run shell|shell command|bash|terminal|execute|log tail|issue (close|comment|update)|close issue)s?\b/.test(normalized)) return "deterministic_or_mechanical";
  if (/\b(review|rubberduck|recheck|audit|confirm|clearance)\b/.test(normalized)) return "review";
  return "construction_or_other";
}

export const ROUTINE_CLASSIFICATIONS = Object.freeze(["routine_exploration", "deterministic_or_mechanical"]);

export function assertTierCoherence(classification, tier, routeLabel) {
  if (ROUTINE_CLASSIFICATIONS.includes(classification) && ["standard", "complex"].includes(tier)) {
    throw new Error(`routine-class task (${classification}) must not dispatch to a ${tier} route ${routeLabel}; use small, explore, or an approved routine route`);
  }
  return tier;
}

export function routingPaths(root) {
  return {
    policy: join(root, "policy.json"),
    approved: join(root, "approved.json"),
    benchmarks: join(root, "benchmarks.json"),
    catalog: join(root, "catalog.json"),
    candidates: join(root, "candidates.json")
  };
}
