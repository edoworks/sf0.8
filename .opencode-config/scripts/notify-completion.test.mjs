import assert from "node:assert/strict";
import test from "node:test";
import { loadTopic, notifyCompletion, publishCompletion } from "./notify-completion.mjs";

const topic = "a".repeat(32);

function topicSource({ directoryMode = 0o700, fileMode = 0o400, directoryUid = 501, fileUid = 501, fileSize = 65, value = topic, directorySymlink = false } = {}) {
  return {
    path: "/secure/ntfy_topic",
    uid: 501,
    lstat: () => ({
      isDirectory: () => true,
      isSymbolicLink: () => directorySymlink,
      mode: directoryMode,
      uid: directoryUid,
    }),
    open: () => 7,
    fstat: () => ({ isFile: () => true, mode: fileMode, uid: fileUid, size: fileSize }),
    readFile: () => `${value}\n`,
    close: () => {},
  };
}

test("retrieves the topic from a private owner-controlled file", () => {
  assert.equal(loadTopic(topicSource()), topic);
});

test("rejects permissive or foreign-owned topic files", () => {
  assert.equal(loadTopic(topicSource({ fileMode: 0o600 })), null);
  assert.equal(loadTopic(topicSource({ directoryMode: 0o755 })), null);
  assert.equal(loadTopic(topicSource({ directoryUid: 0 })), null);
  assert.equal(loadTopic(topicSource({ fileUid: 0 })), null);
  assert.equal(loadTopic(topicSource({ directorySymlink: true })), null);
  assert.equal(loadTopic(topicSource({ fileSize: 129 })), null);
  assert.equal(loadTopic(topicSource({ value: "short" })), null);
});

test("rejects a symlink at open time", () => {
  assert.equal(loadTopic({ ...topicSource(), open: () => { throw new Error("ELOOP"); } }), null);
});

test("publishes only the fixed sanitized completion message", async () => {
  let observed;
  const result = await publishCompletion({
    topic,
    fetchImpl: async (url, request) => {
      observed = { url, request };
      return { ok: true, status: 200 };
    },
  });
  assert.deepEqual(result, { status: "sent", attempts: 1 });
  assert.equal(observed.url, "https://ntfy.sh");
  assert.deepEqual(JSON.parse(observed.request.body), {
    topic,
    message: "A non-trivial OpenCode task completed.",
    title: "OpenCode task complete",
    tags: ["white_check_mark"],
  });
  assert.equal(JSON.stringify(observed).includes(topic), true);
  assert.equal(JSON.stringify(observed).includes("sf0.5"), false);
});

test("retries bounded explicit throttling", async () => {
  let attempts = 0;
  const result = await publishCompletion({
    topic,
    sleep: async () => {},
    fetchImpl: async () => ({ ok: ++attempts === 3, status: attempts === 3 ? 200 : 429 }),
  });
  assert.deepEqual(result, { status: "sent", attempts: 3 });
});

test("fails closed on endpoint substitution", async () => {
  await assert.rejects(() => publishCompletion({ topic, endpoint: "https://example.com" }), /exactly https:\/\/ntfy\.sh/);
});

test("reports missing runtime routing without throwing", async () => {
  const spawn = (command) => ({ status: command === "/usr/bin/osascript" ? 0 : 1, stdout: "" });
  assert.deepEqual(await notifyCompletion({ spawn, topicSource: topicSource({ fileMode: 0o600 }) }), { status: "not_configured", fallback: "sent" });
});
