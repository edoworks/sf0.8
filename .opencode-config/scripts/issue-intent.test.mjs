import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import { REQUIRED_SECTIONS, sha256, validateIssueIntent, verifyReadback } from "./issue-intent.mjs";

function fixture() {
  const directory = mkdtempSync(join(tmpdir(), "issue-intent-"));
  const body = `${REQUIRED_SECTIONS.map((section) => `# ${section}\n\n${section} detail.`).join("\n\n")}\n`;
  const intent = {
    schema_version: 1,
    repo: "edoworks/sf0.8",
    title: "Complete issue",
    body_file: "body.md",
    body_sha256: sha256(body),
    labels: ["enhancement"],
    classification: "enhancement",
    priority: "P2",
    dependencies: ["None"],
    authority_constraints: ["Owner-approved interactive write"],
    source_provenance: ["Planner record"],
    duplicate_review: ["Reviewed existing issues; no duplicate."],
    reprioritization_review: ["Reviewed related issues; no change."]
  };
  writeFileSync(join(directory, "body.md"), body);
  writeFileSync(join(directory, "intent.json"), `${JSON.stringify(intent, null, 2)}\n`);
  return { directory, body, intent, intentPath: join(directory, "intent.json") };
}

test("accepts a complete frozen issue intent", () => {
  const value = fixture();
  const validated = validateIssueIntent(value.intentPath);
  assert.equal(validated.body, value.body);
  assert.equal(validated.intent.title, value.intent.title);
});

test("rejects a missing required body section", () => {
  const value = fixture();
  const incomplete = value.body.replace("# Verification\n\nVerification detail.\n\n", "");
  value.intent.body_sha256 = sha256(incomplete);
  writeFileSync(join(value.directory, "body.md"), incomplete);
  writeFileSync(value.intentPath, JSON.stringify(value.intent));
  assert.throws(() => validateIssueIntent(value.intentPath), /Verification/);
});

test("rejects body changes after the planner freezes the digest", () => {
  const value = fixture();
  writeFileSync(join(value.directory, "body.md"), `${value.body}\nWriter summary\n`);
  assert.throws(() => validateIssueIntent(value.intentPath), /body_sha256/);
});

test("rejects body files outside the intent directory", () => {
  const value = fixture();
  const outside = mkdtempSync(join(tmpdir(), "issue-body-"));
  writeFileSync(join(outside, "body.md"), value.body);
  value.intent.body_file = `../${outside.split("/").at(-1)}/body.md`;
  writeFileSync(value.intentPath, JSON.stringify(value.intent));
  assert.throws(() => validateIssueIntent(value.intentPath), /stay within/);
});

test("readback rejects title or body drift", () => {
  const validated = validateIssueIntent(fixture().intentPath);
  assert.equal(verifyReadback(validated, { title: validated.intent.title, body: validated.body }), true);
  assert.throws(() => verifyReadback(validated, { title: "Shortened", body: validated.body }), /title/);
  assert.throws(() => verifyReadback(validated, { title: validated.intent.title, body: "summary" }), /body/);
});

test("rejects missing triage and classification metadata", () => {
  const value = fixture();
  delete value.intent.duplicate_review;
  writeFileSync(value.intentPath, JSON.stringify(value.intent));
  assert.throws(() => validateIssueIntent(value.intentPath), /duplicate_review/);
});

test("rejects a label that does not match classification", () => {
  const value = fixture();
  value.intent.classification = "bug";
  writeFileSync(value.intentPath, JSON.stringify(value.intent));
  assert.throws(() => validateIssueIntent(value.intentPath), /include classification/);
});
