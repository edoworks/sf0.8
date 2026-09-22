#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { realpathSync } from "node:fs";
import { fileURLToPath } from "node:url";

export function parseIssueNumbers(value) {
  if (typeof value !== "string" || value.trim() === "") {
    throw new Error("--issues must contain one or more numeric issue numbers");
  }

  const numbers = value.split(",").map((entry) => entry.trim());
  if (numbers.some((number) => !/^\d+$/.test(number) || Number(number) < 1)) {
    throw new Error("--issues must contain positive numeric issue numbers");
  }

  const unique = [...new Set(numbers)];
  if (unique.length !== numbers.length) {
    throw new Error("--issues must not contain duplicates");
  }
  return unique;
}

export function assertClosed(issues) {
  const notClosed = issues.filter((issue) => issue.state !== "CLOSED");
  if (notClosed.length > 0) {
    const details = notClosed.map((issue) => `${issue.number}:${issue.state ?? "UNKNOWN"}`).join(", ");
    throw new Error(`tracking issues are not closed: ${details}`);
  }
  return true;
}

function readIssue(repo, number) {
  const result = spawnSync(
    "gh",
    ["issue", "view", "--repo", repo, number, "--json", "number,title,state"],
    { encoding: "utf8" }
  );
  if (result.status !== 0) {
    throw new Error(result.stderr.trim() || `could not read ${repo}#${number}`);
  }
  try {
    return JSON.parse(result.stdout);
  } catch {
    throw new Error(`invalid issue response for ${repo}#${number}`);
  }
}

function usage() {
  return "usage: issue-closeout.mjs verify --repo OWNER/REPO --issues NUMBER[,NUMBER...]";
}

function main(argv) {
  if (argv[0] !== "verify") throw new Error(usage());

  let repo;
  let issues;
  for (let index = 1; index < argv.length; index += 1) {
    const flag = argv[index];
    const value = argv[index + 1];
    if (flag === "--repo") repo = value;
    else if (flag === "--issues") issues = value;
    else throw new Error(usage());
    index += 1;
  }

  if (!repo || !/^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(repo) || !issues) {
    throw new Error(usage());
  }

  const issueNumbers = parseIssueNumbers(issues);
  const states = issueNumbers.map((number) => readIssue(repo, number));
  assertClosed(states);
  process.stdout.write("CLOSED\n");
}

if (process.argv[1] && fileURLToPath(import.meta.url) === realpathSync(process.argv[1])) {
  try {
    main(process.argv.slice(2));
  } catch (error) {
    process.stderr.write(`ERROR: ${error.message}\n`);
    process.exitCode = 1;
  }
}
