#!/usr/bin/env node

import { createHash } from "node:crypto";
import { readFileSync, realpathSync } from "node:fs";
import { dirname, isAbsolute, relative, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

export const REQUIRED_SECTIONS = [
  "Outcome",
  "Scope",
  "Out of scope",
  "Acceptance criteria",
  "Verification",
  "Dependencies",
  "Authority and privacy",
  "Source provenance",
  "Classification",
  "Priority",
  "Triage review"
];

export const ALLOWED_CLASSIFICATIONS = new Set([
  "bug",
  "documentation",
  "enhancement",
  "good first issue",
  "help wanted",
  "question",
  "duplicate",
  "invalid",
  "wontfix"
]);

function fail(message) {
  throw new Error(message);
}

function requireString(value, field) {
  if (typeof value !== "string" || value.trim() === "") fail(`${field} must be a non-empty string`);
}

function requireStringArray(value, field) {
  if (!Array.isArray(value) || value.length === 0) fail(`${field} must be a non-empty array`);
  for (const entry of value) requireString(entry, `${field} entry`);
}

function requireLabelArray(value) {
  requireStringArray(value, "labels");
  for (const label of value) {
    if (label.includes(",")) fail("labels must contain one GitHub label per entry");
  }
}

function bodySections(body) {
  const matches = [...body.matchAll(/^# (.+?)\s*$/gm)];
  const sections = new Map();
  for (let index = 0; index < matches.length; index += 1) {
    const start = matches[index].index + matches[index][0].length;
    const end = matches[index + 1]?.index ?? body.length;
    sections.set(matches[index][1].trim().toLowerCase(), body.slice(start, end).trim());
  }
  return sections;
}

export function sha256(text) {
  return createHash("sha256").update(text).digest("hex");
}

export function validateIssueIntent(intentPath) {
  const absoluteIntentPath = realpathSync(intentPath);
  const intent = JSON.parse(readFileSync(absoluteIntentPath, "utf8"));
  if (intent.schema_version !== 1) fail("schema_version must be 1");
  requireString(intent.repo, "repo");
  if (!/^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(intent.repo)) fail("repo must be owner/name");
  requireString(intent.title, "title");
  requireString(intent.body_file, "body_file");
  requireString(intent.body_sha256, "body_sha256");
  requireLabelArray(intent.labels);
  requireString(intent.classification, "classification");
  if (!ALLOWED_CLASSIFICATIONS.has(intent.classification)) fail("classification is not an allowed GitHub label");
  if (!intent.labels.includes(intent.classification)) fail("labels must include classification");
  requireString(intent.priority, "priority");
  if (!/^P[0-3]$/.test(intent.priority)) fail("priority must be P0, P1, P2, or P3");
  requireStringArray(intent.dependencies, "dependencies");
  requireStringArray(intent.authority_constraints, "authority_constraints");
  requireStringArray(intent.source_provenance, "source_provenance");
  requireStringArray(intent.duplicate_review, "duplicate_review");
  requireStringArray(intent.reprioritization_review, "reprioritization_review");

  if (isAbsolute(intent.body_file)) fail("body_file must be relative to the intent file");
  const intentDirectory = dirname(absoluteIntentPath);
  const bodyPath = realpathSync(resolve(intentDirectory, intent.body_file));
  const bodyRelative = relative(intentDirectory, bodyPath);
  if (bodyRelative.startsWith("..") || isAbsolute(bodyRelative)) fail("body_file must stay within the intent directory");

  const body = readFileSync(bodyPath, "utf8");
  if (sha256(body) !== intent.body_sha256) fail("body_sha256 does not match body_file");
  const sections = bodySections(body);
  for (const section of REQUIRED_SECTIONS) {
    if (!sections.get(section.toLowerCase())) fail(`body is missing non-empty '# ${section}' section`);
  }

  return { intent, intentPath: absoluteIntentPath, bodyPath, body };
}

export function verifyReadback(validated, remote) {
  if (remote.title !== validated.intent.title) fail("remote title differs from frozen intent");
  if (remote.body !== validated.body) fail("remote body differs from frozen body_file");
  return true;
}

function verifyRemote(validated, issueNumber) {
  if (!/^\d+$/.test(issueNumber)) fail("issue number must be numeric");
  const result = spawnSync(
    "gh",
    ["issue", "view", "--repo", validated.intent.repo, issueNumber, "--json", "title,body,labels"],
    { encoding: "utf8" }
  );
  if (result.status !== 0) fail(result.stderr.trim() || "gh issue view failed");
  const remote = JSON.parse(result.stdout);
  verifyReadback(validated, remote);
  const remoteLabels = new Set((remote.labels ?? []).map((label) => typeof label === "string" ? label : label.name));
  for (const label of validated.intent.labels) {
    if (!remoteLabels.has(label)) fail(`remote issue is missing label: ${label}`);
  }
}

function usage() {
  return "usage: issue-intent.mjs validate INTENT.json | verify-remote INTENT.json ISSUE_NUMBER";
}

function main(argv) {
  const [command, intentPath, issueNumber, ...extra] = argv;
  if (extra.length > 0 || !intentPath || !["validate", "verify-remote"].includes(command)) fail(usage());
  const validated = validateIssueIntent(intentPath);
  if (command === "verify-remote") {
    if (!issueNumber) fail(usage());
    verifyRemote(validated, issueNumber);
  } else if (issueNumber) {
    fail(usage());
  }
  process.stdout.write(`${command === "validate" ? "VALID" : "MATCH"}\n`);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === realpathSync(process.argv[1])) {
  try {
    main(process.argv.slice(2));
  } catch (error) {
    process.stderr.write(`ERROR: ${error.message}\n`);
    process.exitCode = 1;
  }
}
