import test from "node:test";
import assert from "node:assert/strict";
import { assertClosed, parseIssueNumbers } from "./issue-closeout.mjs";

test("parseIssueNumbers accepts unique positive issue numbers", () => {
  assert.deepEqual(parseIssueNumbers("29, 33,36"), ["29", "33", "36"]);
});

test("parseIssueNumbers rejects duplicates and invalid numbers", () => {
  assert.throws(() => parseIssueNumbers("29,29"), /duplicates/);
  assert.throws(() => parseIssueNumbers("open"), /positive numeric/);
});

test("assertClosed passes only when every issue is closed", () => {
  assert.equal(assertClosed([{ number: 29, state: "CLOSED" }]), true);
  assert.throws(
    () => assertClosed([{ number: 29, state: "OPEN" }, { number: 33, state: "CLOSED" }]),
    /29:OPEN/
  );
});
