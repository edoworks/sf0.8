import test from "node:test";
import assert from "node:assert/strict";
import { readdir, readFile } from "node:fs/promises";
import { join } from "node:path";

const commandRoot = join(process.env.HOME, ".config", "opencode", "commands");

test("sf0.8 has one canonical continuation command", async () => {
  const commands = (await readdir(commandRoot)).filter((name) => name.startsWith("continue") && name.endsWith(".md"));
  assert.deepEqual(commands, ["continue-sf08.md"]);
  const content = await readFile(join(commandRoot, commands[0]), "utf8");
  assert.match(content, /^agent: explore$/m);
  assert.doesNotMatch(content, /continue-(?:original|sf08-build)/);
});
