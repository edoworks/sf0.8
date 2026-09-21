import test from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, readFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import costRouter from "./cost-router.mjs";
import { messageText, recordToolAttribution } from "./cost-router-lib.mjs";
import { assertTierCoherence, classifyTitle } from "../model-routing/routing-lib.mjs";

test("messageText joins text parts only", () => {
  assert.equal(messageText({ parts: [{ type: "text", text: "Crop the screenshot" }, { type: "file", text: "ignored" }, { type: "text", text: "and close the issue" }] }), "Crop the screenshot\nand close the issue");
  assert.equal(messageText(undefined), "");
  assert.equal(messageText({}), "");
});

test("configured legacy plugin exposes only its default initializer", async () => {
  const module = await import("./cost-router.mjs");
  assert.deepEqual(Object.keys(module), ["default"]);
});

test("routine-class turn text classifies as mechanical", () => {
  assert.equal(classifyTitle(messageText({ parts: [{ type: "text", text: "Crop the screenshot and resize it" }] }), "build"), "deterministic_or_mechanical");
  assert.equal(classifyTitle(messageText({ parts: [{ type: "text", text: "Run a shell command and inspect status" }] }), "build"), "deterministic_or_mechanical");
  assert.equal(classifyTitle(messageText({ parts: [{ type: "text", text: "Design the routing architecture" }] }), "build"), "construction_or_other");
});

test("coherence rule rejects routine work on complex routes and passes real construction", () => {
  assert.throws(() => assertTierCoherence(classifyTitle("Crop the screenshot", "frontier-build"), "complex", "openai/gpt-5.6-terra"), /routine-class task/);
  assert.equal(assertTierCoherence(classifyTitle("Design the routing architecture", "frontier-build"), "complex", "openai/gpt-5.6-terra"), "complex");
});

test("routine work is rejected before standard or cloud dispatch", async () => {
  const hooks = await costRouter();
  await assert.rejects(() => hooks["chat.params"]({
    agent: "build",
    model: { providerID: "openai", id: "gpt-5.6-luna" },
    provider: { id: "openai" },
    message: { parts: [{ type: "text", text: "Check status and verify the baseline" }] },
  }, {}), /must not dispatch to a standard route/);
});

test("tool attribution records model identity without command text or raw session IDs", async () => {
  const root = await mkdtemp(join(tmpdir(), "cost-router-attribution-"));
  const path = join(root, "tool-attribution.jsonl");
  await recordToolAttribution({
    sessionID: "session-secret-like-value",
    agent: "build",
    provider: "openai",
    model: "gpt-5.6-luna",
    tool: "bash",
    path,
  });
  const record = JSON.parse(await readFile(path, "utf8"));
  assert.equal(record.agent, "build");
  assert.equal(record.provider, "openai");
  assert.equal(record.model, "gpt-5.6-luna");
  assert.equal(record.tool, "bash");
  assert.notEqual(record.session, "session-secret-like-value");
  assert.equal("command" in record, false);
  await rm(root, { recursive: true, force: true });
});
