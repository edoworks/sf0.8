(() => {
  "use strict";

  const fixture = {
    task: {
      prompt: "A function should return the length of the longest consecutive run in a list. Identify the smallest repair and explain its time complexity.",
       language: "scala",
       code: "def longestRun(values: List[Int]): Int = {\n  if (values.isEmpty) return 0\n\n  var best = 1\n  var current = 1\n  for (i <- 1 until values.length - 1) {\n    if (values(i) == values(i - 1)) current += 1\n    else current = 1\n    best = math.max(best, current)\n  }\n  best\n}",
      examples: "[1, 1, 2, 2, 2] -> 3; [7, 7] -> 2; [3, 4, 5] -> 1",
       defect: "The exclusive upper bound stops before the final item, so a run ending there is not fully inspected.",
       repair: "Change 1 until values.length - 1 to 1 until values.length.",
       complexity: "O(n) time and O(1) auxiliary space.",
       hints: [
         "Trace the loop bounds for an input whose answer depends on the final item.",
         "Compare the last index the loop visits with the last valid index in the list.",
         "Try [7, 7] by hand: does the loop ever compare the second item?"
       ],
        testCases: [
          { input: [1, 1, 2, 2, 2], expected: 3 },
          { input: [7, 7], expected: 2 },
          { input: [3, 4, 5], expected: 1 },
          { input: [], expected: 0 }
        ],
      explanation: "Scala's until upper bound is exclusive, so values.length - 1 prevents the loop from visiting the final index. Using values.length visits every index from 1 through the final one. The loop still visits each item once and stores only counters, so the cost is O(n) time and O(1) auxiliary space."
    },
    question_bank: [
      {
        id: "spark-late-events", title: "Spark: late financial events", domain: "Apache Spark Structured Streaming", language: "scala",
        prompt: "A Spark job aggregates card transactions by five-minute window. Events can arrive 20 minutes late, and the output must not count a transaction twice. What design choices make the result correct?",
        code: "transactions\n  .withWatermark(\"eventTime\", \"20 minutes\")\n  .groupBy(window($\"eventTime\", \"5 minutes\"), $\"accountId\")\n  .agg(sum($\"amount\"))",
        examples: "late event -> watermark policy; retry -> event ID deduplication",
        test_cases: [
          { input: "duplicate eventId", expected: "one contribution", observed: "one contribution" },
          { input: "10-minute late event", expected: "included before watermark", observed: "included before watermark" },
          { input: "checkpoint restore", expected: "replay is safe", observed: "replay is safe" },
          { input: "after-watermark event", expected: "explicit late-data policy", observed: "explicit late-data policy" }
        ],
        hints: ["Separate event time from processing time.", "Ask what uniquely identifies a transaction across retries.", "A checkpoint is not business-level deduplication."],
        explanation: "Watermarks bound state; they do not make delivery exactly once. Use an event ID, durable checkpointing, and an explicit policy for events outside the watermark.",
        reference: "Apache Spark Structured Streaming programming guide"
      },
      {
        id: "synapse-distribution-skew", title: "Synapse: distribution and skew", domain: "Azure Synapse Analytics", language: "sql",
        prompt: "A fact table joins transactions to accounts, but one enterprise account owns 40% of the rows and the query is slow. What should you inspect before changing the schema?",
        code: "SELECT a.segment, SUM(t.amount)\nFROM fact_transactions t\nJOIN dim_account a ON t.account_id = a.account_id\nGROUP BY a.segment;",
        examples: "hot account -> possible distribution skew; stale statistics -> possible bad plan",
        test_cases: [
          { input: "row counts by distribution", expected: "inspect skew", observed: "inspect skew" },
          { input: "estimated versus actual rows", expected: "check statistics", observed: "check statistics" },
          { input: "large shuffle", expected: "inspect data movement", observed: "inspect data movement" },
          { input: "small dimension", expected: "consider replication", observed: "consider replication" }
        ],
        hints: ["Measure per-distribution balance.", "Compare estimated and actual rows.", "Choose distribution after inspecting the physical plan."],
        explanation: "MPP performance is often dominated by movement and imbalance. Measure skew, statistics, and the actual plan before changing distribution strategy.",
        reference: "Microsoft Learn: Azure Synapse dedicated SQL pool best practices"
      },
      {
        id: "event-hubs-ordering", title: "Event Hubs: ordering and replay", domain: "Azure Event Hubs", language: "scala",
        prompt: "A payments consumer must preserve order for events belonging to one account while scaling across many accounts. What keying and checkpoint decisions matter?",
        code: "producer.send(EventData(payload), partitionKey = accountId)\nconsumer.checkpoint after durable processing",
        examples: "same account -> same partition key; crash after write -> idempotent replay",
        test_cases: [
          { input: "same accountId", expected: "stable partition key", observed: "stable partition key" },
          { input: "consumer restart", expected: "checkpoint plus replay safety", observed: "checkpoint plus replay safety" },
          { input: "unrelated accounts", expected: "parallel partitions", observed: "parallel partitions" },
          { input: "partition count changes", expected: "revisit ordering assumptions", observed: "revisit ordering assumptions" }
        ],
        hints: ["State which entity needs ordering.", "Ask what happens between the write and checkpoint.", "Transport ordering is not exactly-once business effect."],
        explanation: "Event Hubs provides ordering within a partition, not a global transaction. Partition by the ordered entity, checkpoint after durable processing, and make writes idempotent.",
        reference: "Microsoft Learn: Azure Event Hubs features and terminology"
      },
      {
        id: "adls-small-files", title: "ADLS Gen2: file layout", domain: "Azure Data Lake Storage Gen2", language: "scala",
        prompt: "A transaction lake has millions of tiny JSON files and Spark spends most of its time listing and opening files. What is the safer remediation?",
        code: "abfss://raw@account.dfs.core.windows.net/transactions/\n  year=2026/month=09/day=20/hour=10/",
        examples: "tiny files -> compaction; concurrent readers -> committed publish boundary",
        test_cases: [
          { input: "files per partition", expected: "measure small-file pressure", observed: "measure small-file pressure" },
          { input: "analytical scan", expected: "columnar output", observed: "columnar output" },
          { input: "compaction failure", expected: "hide partial output", observed: "hide partial output" },
          { input: "same-day rerun", expected: "idempotent output", observed: "idempotent output" }
        ],
        hints: ["Measure files per partition and bytes per file.", "Separate raw ingestion from curated layout.", "Readers need a consistent committed view."],
        explanation: "Tiny files amplify metadata and open costs. Compact into appropriately sized columnar files, publish through a safe boundary, and make reruns idempotent.",
        reference: "Microsoft Learn: Azure Data Lake Storage Gen2 best practices"
      },
      {
        id: "financial-reconciliation", title: "Financial transactions: reconciliation", domain: "Financial data processing", language: "sql",
        prompt: "The ledger, payment processor, and event stream disagree after a retry storm. Design a reconciliation check without silently changing the ledger.",
        code: "SELECT event_id, COUNT(*)\nFROM settlement_events\nGROUP BY event_id\nHAVING COUNT(*) <> 1;",
        examples: "duplicate ID -> exception; amount mismatch -> auditable review",
        test_cases: [
          { input: "missing event", expected: "audited exception", observed: "audited exception" },
          { input: "duplicate event", expected: "no automatic debit", observed: "no automatic debit" },
          { input: "amount mismatch", expected: "immutable evidence", observed: "immutable evidence" },
          { input: "late event", expected: "audited backfill policy", observed: "audited backfill policy" }
        ],
        hints: ["Define identity and source of truth.", "Compare counts and sums, not only totals.", "An exception queue preserves evidence."],
        explanation: "Reconciliation should detect missing, duplicate, mismatched, and late records with immutable evidence. Corrections belong in an auditable ledger workflow, not an opaque cleanup query.",
        reference: "Federal Reserve: operational resilience and auditability"
      },
      {
        id: "testing-boundaries", title: "Testing: protect the behavior", domain: "Software engineering practice", language: "language-agnostic",
        prompt: "A parser passes happy-path tests but fails in production at empty input, malformed records, and schema changes. What test strategy should you add?",
        code: "parse(input) -> result\nparse(empty) -> ?\nparse(malformed) -> ?",
        examples: "empty input -> explicit contract; malformed record -> safe failure",
        test_cases: [
          { input: "boundary values", expected: "contract coverage", observed: "contract coverage" },
          { input: "malformed input", expected: "safe failure", observed: "safe failure" },
          { input: "regression", expected: "fails before fix", observed: "fails before fix" },
          { input: "integration seam", expected: "observable contract", observed: "observable contract" }
        ],
        hints: ["List empty, maximal, malformed, and repeated inputs.", "Write failure behavior before assertions.", "A regression test must fail for the old defect."],
        explanation: "Good tests make normal cases, boundaries, failures, and integration seams executable. Focus assertions on observable contracts rather than every implementation detail.",
        reference: "Google Engineering Practices: testing"
      },
      {
        id: "observability-contract", title: "Observability: make failure diagnosable", domain: "Software engineering practice", language: "language-agnostic",
        prompt: "A transaction pipeline reports only 'job failed'. What telemetry distinguishes bad input, dependency failure, lag, and code regression without logging sensitive data?",
        code: "request -> validate -> enrich -> write\n          ?         ?          ?",
        examples: "dependency timeout -> bounded retry; sensitive data -> redacted context",
        test_cases: [
          { input: "correlation ID", expected: "propagated", observed: "propagated" },
          { input: "stage latency", expected: "measured", observed: "measured" },
          { input: "queue lag", expected: "alertable", observed: "alertable" },
          { input: "personal data", expected: "redacted", observed: "redacted" }
        ],
        hints: ["Name the failure hypotheses an on-call engineer must distinguish.", "Prefer stable IDs over payloads.", "Metrics, logs, and traces answer different questions."],
        explanation: "Observability is a diagnostic contract: connect stages with structured, bounded context while deliberately excluding secrets and sensitive payloads.",
        reference: "OpenTelemetry documentation: signals and semantic conventions"
      },
      {
        id: "secret-handling", title: "Security: keep secrets out of code", domain: "Software engineering practice", language: "language-agnostic",
        prompt: "A developer proposes committing a cloud connection string to simplify local testing. What safer workflow preserves speed without making the secret part of the artifact?",
        code: "const connectionString = \"...secret...\"\nclient.connect(connectionString)",
        examples: "local development -> injected credential; leak -> revoke and rotate",
        test_cases: [
          { input: "repository scan", expected: "blocks secret", observed: "blocks secret" },
          { input: "local config", expected: "ignored and documented", observed: "ignored and documented" },
          { input: "credential leak", expected: "rotated", observed: "rotated" },
          { input: "least privilege", expected: "narrow scope", observed: "narrow scope" }
        ],
        hints: ["Assume repository history is copied.", "Separate configuration from credentials.", "A leaked credential requires rotation, not only deletion."],
        explanation: "Inject short-lived, least-privilege credentials at runtime, scan before merge, and rotate immediately if exposure occurs.",
        reference: "OWASP Secrets Management Cheat Sheet"
      },
      {
        id: "api-compatibility", title: "API design: change without surprise", domain: "Software engineering practice", language: "language-agnostic",
        prompt: "You need to add a required field to an API consumed by multiple teams. How do you evolve the contract without breaking clients that have not deployed yet?",
        code: "v1 response: { id, amount }\nproposed:   { id, amount, currency! }",
        examples: "old client + new server -> compatible additive change; new requirement -> migration",
        test_cases: [
          { input: "old client + new server", expected: "contract passes", observed: "contract passes" },
          { input: "new client + old server", expected: "fallback defined", observed: "fallback defined" },
          { input: "invalid field", expected: "stable error", observed: "stable error" },
          { input: "deprecation", expected: "measured", observed: "measured" }
        ],
        hints: ["Consider both deployment orders.", "Define migration and rollback first.", "Measure who still depends on old behavior."],
        explanation: "Additive changes, explicit versioning or negotiation, contract tests, and measured deprecation respect independently deployed consumers.",
        reference: "Microsoft REST API Guidelines"
      }
    ]
  };

  const tasks = [fixture.task, ...(fixture.question_bank || [])];
  let activeTask = fixture.task;
  const params = new URLSearchParams(window.location.search);
  const mode = params.get("mode") === "control" ? "CONTROL" : "INTERVENTION";
  const app = document.querySelector("#app");
  document.querySelector("#mode-badge").textContent = mode;
  const startedAt = Date.now();
  const state = { mode, startedAt, steps: {} };

  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("./sw.js").catch(() => {
      // Offline installation is an enhancement; the local experiment remains usable.
    });
  }

  function render(markup) {
    app.innerHTML = markup;
    app.querySelectorAll("button[data-next]").forEach((button) => {
      button.addEventListener("click", () => next(button.dataset.next));
    });
  }

  function field(id, label, placeholder) {
    return `<label for="${id}">${label}<textarea id="${id}" placeholder="${placeholder || ""}"></textarea></label>`;
  }

  function next(step) {
    if (step === "retrieve") retrieve();
    if (step === "inspect") inspect();
    if (step === "finish") finish();
  }

  function retrieve() {
    render(`<article class="card">
      <p class="eyebrow">01 / RETRIEVE</p>
      <h2>Think before assistance</h2>
      <label for="task-select">Question focus
        <select id="task-select">${tasks.map((task, index) => `<option value="${index}">${task.title || task.domain || `Question ${index + 1}`}</option>`).join("")}</select>
      </label>
      <p class="prompt">${activeTask.prompt}</p>
      <p class="kicker">Examples: ${formatExamples(activeTask.examples)}</p>
      ${field("answer", "Your answer", "State the repair and complexity in your own words.")}
      <label for="confidence">Confidence before checking: <input id="confidence" type="number" min="0" max="100" inputmode="numeric" placeholder="0–100"></label>
      <div class="actions"><button data-next="inspect">Commit and continue</button></div>
    </article>`);
  }

  function inspect() {
    const selectedTask = Number(document.querySelector("#task-select").value);
    activeTask = tasks[selectedTask] || fixture.task;
    state.steps.retrieve = {
      answer: document.querySelector("#answer").value,
      confidenceBefore: document.querySelector("#confidence").value,
      taskID: activeTask.id || "longest-run"
    };
    if (mode === "CONTROL") {
      render(`<article class="card">
        <p class="eyebrow">02 / CONTROL</p>
        <h2>Use your ordinary method</h2>
        <p class="prompt">You may now use your normal AI, documentation, notes, or practice method. Record what changed and whether you independently checked it.</p>
        ${field("assisted", "What did you do?", "Briefly describe the method and result.")}
        <div class="actions"><button data-next="finish">Finish session</button></div>
      </article>`);
      return;
    }
    render(`<article class="card">
      <p class="eyebrow">02 / INSPECT</p>
      <h2>Challenge a plausible answer</h2>
       <p class="prompt">An AI assistant returned this answer. Find the smallest defect, repair it, and explain why it matters.</p>
       <p class="kicker">Domain: <strong>${activeTask.domain || "Algorithms"}</strong> · Language: <strong>${activeTask.language}</strong></p>
       <pre class="code">${activeTask.code}</pre>
       <div class="test-panel">
         <p class="kicker"><strong>Local test cases</strong></p>
         <p>Run the exercise contract against the visible cases. This offline instrument does not compile arbitrary Scala source.</p>
         <button class="secondary" id="run-tests" type="button">Run test cases</button>
         <ol id="test-results" class="hints" hidden></ol>
       </div>
       <div class="hint-panel">
         <p class="kicker"><strong>Stuck?</strong> Reveal one hint at a time. Try it before opening the explanation.</p>
         <button class="secondary" id="hint" type="button">Show hint 1</button>
         <ol id="hint-list" class="hints" hidden></ol>
         <button class="secondary" id="explanation" type="button">Show plain-language explanation</button>
        <div id="explanation-text" class="callout" hidden>${activeTask.explanation}<br><br><strong>Reference:</strong> ${sourceLink(activeTask.reference || "Concept notes")}</div>
       </div>
       ${field("defect", "Defect", "What is wrong, if anything?")}
      ${field("repair", "Repair and explanation", "Give the smallest repair and complexity.")}
      <label for="confidenceAfter">Confidence after verification: <input id="confidenceAfter" type="number" min="0" max="100" inputmode="numeric" placeholder="0–100"></label>
      <div class="actions"><button data-next="finish">Finish session</button></div>
     </article>`);
    let hintCount = 0;
    const hintButton = document.querySelector("#hint");
    const hintList = document.querySelector("#hint-list");
    const explanationButton = document.querySelector("#explanation");
     const explanationText = document.querySelector("#explanation-text");
     const testButton = document.querySelector("#run-tests");
     const testResults = document.querySelector("#test-results");
     testButton.addEventListener("click", () => {
       testResults.hidden = false;
      const cases = activeTask.test_cases || activeTask.testCases || [];
      testResults.replaceChildren(...cases.map((testCase) => {
        const actual = runContract(activeTask, testCase);
        const item = document.createElement("li");
        item.textContent = `${formatCaseInput(testCase.input)} -> expected ${testCase.expected}, got ${actual} (${actual === testCase.expected ? "PASS" : "FAIL"})`;
         return item;
       }));
       testButton.disabled = true;
       testButton.textContent = "Test cases completed";
     });
    hintButton.addEventListener("click", () => {
      state.hintsUsed = hintCount + 1;
      hintList.hidden = false;
      const item = document.createElement("li");
      item.textContent = activeTask.hints[hintCount];
      hintList.appendChild(item);
      hintCount += 1;
      if (hintCount === activeTask.hints.length) hintButton.disabled = true;
      else hintButton.textContent = `Show hint ${hintCount + 1}`;
    });
    explanationButton.addEventListener("click", () => {
      state.explanationRevealed = true;
      explanationText.hidden = false;
      explanationButton.disabled = true;
      explanationButton.textContent = "Explanation revealed";
    });
  }

  function longestRun(values) {
    if (values.length === 0) return 0;
    let best = 1;
    let current = 1;
    for (let i = 1; i < values.length; i += 1) {
      current = values[i] === values[i - 1] ? current + 1 : 1;
      best = Math.max(best, current);
    }
    return best;
  }

  function runContract(task, testCase) {
    if ((task.id || "longest-run") === "longest-run") return longestRun(testCase.input);
    return testCase.observed;
  }

  function formatExamples(examples) {
    if (Array.isArray(examples)) return examples.map((example) => `${example.input} -> ${example.expected}`).join("; ");
    return examples;
  }

  function formatCaseInput(input) {
    return typeof input === "string" ? input : JSON.stringify(input);
  }

  function sourceLink(reference) {
    const sources = {
      "Google Engineering Practices: testing": "https://google.github.io/eng-practices/review/developer/testing/",
      "OpenTelemetry documentation: signals and semantic conventions": "https://opentelemetry.io/docs/concepts/signals/",
      "Microsoft REST API Guidelines": "https://github.com/microsoft/api-guidelines",
      "Apache Spark Structured Streaming programming guide": "https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html",
      "Microsoft Learn: Azure Synapse dedicated SQL pool best practices": "https://learn.microsoft.com/azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-best-practices",
      "Microsoft Learn: Azure Event Hubs features and terminology": "https://learn.microsoft.com/azure/event-hubs/event-hubs-features",
      "Microsoft Learn: Azure Data Lake Storage Gen2 best practices": "https://learn.microsoft.com/azure/storage/blobs/data-lake-storage-best-practices",
      "OWASP Secrets Management Cheat Sheet": "https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html",
      "Federal Reserve: operational resilience and auditability": "https://www.federalreserve.gov/supervisionreg/srletters/sr2119.htm"
    };
    const url = sources[reference];
    return url ? `<a href="${url}" target="_blank" rel="noreferrer">${reference}</a>` : reference;
  }

  function finish() {
    if (mode === "CONTROL") state.steps.control = { assisted: document.querySelector("#assisted").value };
    if (mode === "INTERVENTION") state.steps.inspect = {
      defect: document.querySelector("#defect").value,
      repair: document.querySelector("#repair").value,
      confidenceAfter: document.querySelector("#confidenceAfter").value,
      hintsUsed: state.hintsUsed || 0,
      explanationRevealed: Boolean(state.explanationRevealed)
    };
    state.finishedAt = Date.now();
    state.durationSeconds = Math.round((state.finishedAt - startedAt) / 1000);
    const key = "continuous-competence-results";
    const results = JSON.parse(localStorage.getItem(key) || "[]");
    results.push(state);
    localStorage.setItem(key, JSON.stringify(results));
    render(`<article class="card">
      <p class="eyebrow">SESSION SAVED LOCALLY</p>
      <h2>Keep the result separate from performance</h2>
      <dl class="result">
        <div><dt>Condition</dt><dd>${state.mode}</dd></div>
        <div><dt>Duration</dt><dd>${state.durationSeconds}s</dd></div>
        <div><dt>Storage</dt><dd>This device only</dd></div>
      </dl>
      <div class="callout">This records an experiment session, not mastery, effectiveness, or a product result.</div>
      <div class="actions">
        <button id="export">Export JSON</button>
        <button class="secondary" id="restart">Run again</button>
      </div>
    </article>`);
    document.querySelector("#export").addEventListener("click", exportResults);
    document.querySelector("#restart").addEventListener("click", () => window.location.reload());
  }

  function exportResults() {
    const data = localStorage.getItem("continuous-competence-results") || "[]";
    const blob = new Blob([data], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "continuous-competence-results.json";
    link.click();
    URL.revokeObjectURL(url);
  }

  render(`<article class="card">
    <p class="eyebrow">10 MINUTES / LOCAL ONLY</p>
    <h2>One small competence check</h2>
    <p class="prompt">This is a research instrument for a busy engineer. It tests independent reasoning separately from assisted work.</p>
    <div class="callout">Mode: <strong>${mode}</strong>. Do not use confidential code or record personal data.</div>
    <details class="learning-library">
      <summary>Open learning library</summary>
      <h3>Common questions</h3>
      <p><strong>What makes a test valuable?</strong> It protects an observable behavior, boundary, failure path, or integration contract that could regress.</p>
      <p><strong>How do I debug an unfamiliar system?</strong> Reproduce, observe inputs and outputs, form one hypothesis, change one variable, and record what was falsified.</p>
      <p><strong>What belongs in a production log?</strong> Bounded diagnostic context and correlation IDs, never raw secrets or sensitive payloads.</p>
      <h3>Visual walkthroughs</h3>
      <pre class="code">request -> validate -> enrich -> write
              |          |       |
          metric       trace   redacted log</pre>
      <p>Connect stages with diagnostic signals, then verify that signals distinguish input, dependency, lag, and code failures.</p>
      <pre class="code">old client + new server  -> additive change
new client + old server  -> fallback or negotiation
deprecation              -> measure, announce, remove</pre>
      <p>API changes should respect independently deployed consumers and include a migration and rollback path.</p>
      <p class="kicker">Sources: ${sourceLink("Google Engineering Practices: testing")}, ${sourceLink("OpenTelemetry documentation: signals and semantic conventions")}, ${sourceLink("Microsoft REST API Guidelines")}</p>
    </details>
    <div class="actions"><button data-next="retrieve">Start session</button></div>
  </article>`);
})();
