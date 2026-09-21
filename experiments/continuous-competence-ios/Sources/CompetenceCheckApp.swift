import SwiftUI
#if canImport(FoundationModels)
import FoundationModels
#endif

@main
struct CompetenceCheckApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

enum SessionMode: String, CaseIterable, Codable, Identifiable {
    case control = "CONTROL"
    case intervention = "INTERVENTION"

    var id: String { rawValue }
}

enum SessionStep: String {
    case start
    case retrieve
    case inspect
    case finish
}

struct ExperimentTask: Codable, Equatable {
    let id: String
    let title: String
    let prompt: String
    let code: String
    let examples: String
    let defect: String
    let repair: String
    let complexity: String
    let concept: String
    let reference: String
    let referenceURL: String
    let hints: [String]
    let explanation: String

    static let all: [ExperimentTask] = [longestRun, binarySearch, transactionBoundary] + financeData

    static let longestRun = ExperimentTask(
        id: "longest-run",
        title: "Off-by-one inspection",
        prompt: "A function should return the length of the longest consecutive run in a list. Identify the smallest repair and explain its time complexity.",
        code: """
        def longest_run(values):
            if not values:
                return 0

            best = 1
            current = 1

            for i in range(1, len(values) - 1):
                if values[i] == values[i - 1]:
                    current += 1
                else:
                    current = 1
                best = max(best, current)

            return best
        """,
        examples: "[1, 1, 2, 2, 2] -> 3; [7, 7] -> 2; [3, 4, 5] -> 1",
        defect: "The range stops before the final item, so a run ending at the final item is not fully inspected.",
        repair: "Change range(1, len(values) - 1) to range(1, len(values)).",
        complexity: "O(n) time and O(1) auxiliary space.",
        concept: "Loop bounds and invariant: after each iteration, current describes the run ending at the item just inspected, while best is the largest run seen so far.",
        reference: "Python documentation: range()",
        referenceURL: "https://docs.python.org/3/library/functions.html#func-range",
        hints: [
            "Trace the final example by hand and ask whether the last index is ever inspected.",
            "Compare the exclusive stop value with the last valid index.",
            "The loop should stop at len(values), not one position earlier."
        ],
        explanation: "The stop value of range is exclusive. Using len(values) - 1 means the final position is omitted. Extending the stop value to len(values) preserves the linear scan and constant extra space."
    )

    static let binarySearch = ExperimentTask(
        id: "binary-search",
        title: "Invariant inspection",
        prompt: "A binary search returns an index for a sorted list or -1. Identify the invariant that must hold after each iteration and give its complexity.",
        code: """
        def search(values, target):
            low, high = 0, len(values)
            while low < high:
                mid = (low + high) // 2
                if values[mid] < target:
                    low = mid + 1
                else:
                    high = mid
            return low if values[low] == target else -1
        """,
        examples: "[1, 3, 5], 3 -> 1; [1, 3, 5], 4 -> -1; [] -> -1",
        defect: "The empty-list case reads values[0] after the loop, and any absent target may leave low == len(values).",
        repair: "Return -1 when low == len(values) before indexing, or use a loop condition that proves the index is valid.",
        complexity: "O(log n) time and O(1) auxiliary space.",
        concept: "Binary search works by preserving a shrinking candidate interval. Boundary proofs matter as much as the midpoint calculation.",
        reference: "MIT OpenCourseWare: Binary Search Trees and Algorithms",
        referenceURL: "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/",
        hints: [
            "Test the smallest valid input before reasoning about the general case.",
            "Ask whether low can equal len(values) when target is absent.",
            "Every array access needs a proof that its index is in bounds."
        ],
        explanation: "The interval logic is a lower-bound search, but the final indexing assumes a match position exists. Empty input and a target larger than every element violate that assumption. Guarding low before indexing makes the boundary proof explicit without changing logarithmic complexity."
    )

    static let transactionBoundary = ExperimentTask(
        id: "transaction-boundary",
        title: "Failure-atomicity inspection",
        prompt: "A service updates a balance and then writes an audit record. Explain the failure mode if the audit write fails, and name a safer boundary.",
        code: """
        balance.debit(amount)
        audit.write(.debit(amount))
        """,
        examples: "Debit succeeds + audit fails -> state changed without an audit record",
        defect: "The two side effects can commit independently, so a failure between them leaves an inconsistent observable state.",
        repair: "Put both writes behind one transactional boundary, or use an outbox/idempotent retry design with an explicit reconciliation policy.",
        complexity: "O(1) application steps; durability and retry semantics are the important correctness properties.",
        concept: "Atomicity is a systems invariant: observers should not see a partially applied business operation unless the design explicitly models it.",
        reference: "Martin Kleppmann, Designing Data-Intensive Applications: Transactions",
        referenceURL: "https://dataintensive.net/",
        hints: [
            "Insert a failure immediately after the first line.",
            "List what an external observer sees after that failure.",
            "Choose one boundary that makes the business operation recoverable and idempotent."
        ],
        explanation: "The defect is not syntax; it is a broken failure invariant. If the process stops after the debit, the audit trail lies by omission. A database transaction is appropriate when both writes share a durable store. Across systems, an outbox plus idempotent consumer makes the partial state visible and repairable."
    )

    static let financeData: [ExperimentTask] = [
        ExperimentTask(
            id: "spark-late-events", title: "Spark: late financial events",
            prompt: "A Spark job aggregates card transactions by five-minute window. Events can arrive 20 minutes late, and the output must not count a transaction twice. What design choices make the result correct?",
            code: """
            transactions
              .withWatermark("eventTime", "20 minutes")
              .groupBy(window($"eventTime", "5 minutes"), $"accountId")
              .agg(sum($"amount"))
            """,
            examples: "late event -> watermark policy; retry -> event ID deduplication",
            defect: "A watermark bounds state but does not deduplicate business events or define behavior after the watermark.",
            repair: "Deduplicate by event ID, use durable checkpointing, define late-data handling, and reconcile events outside the watermark.",
            complexity: "State and shuffle cost depend on key cardinality and watermark horizon; correctness depends on replay semantics.",
            concept: "Event time, processing time, watermarks, and business idempotency are separate concerns in streaming systems.",
            reference: "Apache Spark Structured Streaming programming guide",
            referenceURL: "https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html",
            hints: ["Separate event time from processing time.", "Ask what uniquely identifies a transaction across retries.", "A checkpoint is not business-level deduplication."],
            explanation: "Watermarks bound state; they do not make delivery exactly once. Use an event ID, durable checkpointing, and an explicit policy for events outside the watermark."
        ),
        ExperimentTask(
            id: "synapse-distribution-skew", title: "Synapse: distribution and skew",
            prompt: "A fact table joins transactions to accounts, but one enterprise account owns 40% of the rows and the query is slow. What should you inspect before changing the schema?",
            code: """
            SELECT a.segment, SUM(t.amount)
            FROM fact_transactions t
            JOIN dim_account a ON t.account_id = a.account_id
            GROUP BY a.segment;
            """,
            examples: "hot account -> possible skew; stale statistics -> possible bad plan",
            defect: "Treating a slow MPP join as a generic indexing problem can miss skew, data movement, or stale statistics.",
            repair: "Measure distribution balance, inspect the actual plan and statistics, then choose distribution based on workload evidence.",
            complexity: "Distributed performance is dominated by movement and balance, not only logical join complexity.",
            concept: "MPP query design requires reasoning about where rows live and how much data moves between distributions.",
            reference: "Microsoft Learn: Azure Synapse dedicated SQL pool best practices",
            referenceURL: "https://learn.microsoft.com/azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-best-practices",
            hints: ["Measure per-distribution balance.", "Compare estimated and actual rows.", "Choose distribution after inspecting the physical plan."],
            explanation: "Measure skew, statistics, and data movement before changing the schema. Hash, round-robin, and replicated distribution each fit different workload evidence."
        ),
        ExperimentTask(
            id: "event-hubs-ordering", title: "Event Hubs: ordering and replay",
            prompt: "A payments consumer must preserve order for events belonging to one account while scaling across many accounts. What keying and checkpoint decisions matter?",
            code: """
            producer.send(EventData(payload), partitionKey = accountId)
            consumer.checkpoint after durable processing
            """,
            examples: "same account -> same partition key; crash after write -> idempotent replay",
            defect: "A checkpoint does not create a global order or exactly-once business effect when a consumer crashes between writing and checkpointing.",
            repair: "Partition by the ordered entity, checkpoint after durable processing, and make downstream writes idempotent with event IDs.",
            complexity: "Throughput scales by partition and consumer parallelism; ordering is scoped to a partition.",
            concept: "Transport ordering and business-level exactly-once effects are different guarantees.",
            reference: "Microsoft Learn: Azure Event Hubs features and terminology",
            referenceURL: "https://learn.microsoft.com/azure/event-hubs/event-hubs-features",
            hints: ["State which entity needs ordering.", "Ask what happens between the write and checkpoint.", "Transport ordering is not exactly-once business effect."],
            explanation: "Event Hubs provides ordering within a partition, not a global transaction. Stable partition keys, checkpoint placement, and idempotent writes make replay safe."
        ),
        ExperimentTask(
            id: "adls-small-files", title: "ADLS Gen2: file layout",
            prompt: "A transaction lake has millions of tiny JSON files and Spark spends most of its time listing and opening files. What is the safer remediation?",
            code: """
            abfss://raw@account.dfs.core.windows.net/transactions/
              year=2026/month=09/day=20/hour=10/
            """,
            examples: "tiny files -> compaction; concurrent readers -> committed publish boundary",
            defect: "Increasing executor count does not solve metadata and file-open overhead, and in-place compaction can expose partial results.",
            repair: "Compact into appropriately sized columnar files, publish through a safe boundary, and make reruns idempotent.",
            complexity: "File and metadata overhead can dominate scan cost; layout determines recovery and read efficiency.",
            concept: "A lake layout is part of the algorithm: partitioning, file size, format, and publication semantics affect correctness and cost.",
            reference: "Microsoft Learn: Azure Data Lake Storage Gen2 best practices",
            referenceURL: "https://learn.microsoft.com/azure/storage/blobs/data-lake-storage-best-practices",
            hints: ["Measure files per partition and bytes per file.", "Separate raw ingestion from curated layout.", "Readers need a consistent committed view."],
            explanation: "Tiny files amplify listing and open costs. Compact into columnar files, publish a consistent view, and make reruns safe rather than simply adding compute."
        ),
        ExperimentTask(
            id: "financial-reconciliation", title: "Financial transactions: reconciliation",
            prompt: "The ledger, payment processor, and event stream disagree after a retry storm. Design a reconciliation check without silently changing the ledger.",
            code: """
            SELECT event_id, COUNT(*)
            FROM settlement_events
            GROUP BY event_id
            HAVING COUNT(*) <> 1;
            """,
            examples: "duplicate ID -> exception; amount mismatch -> auditable review",
            defect: "A cleanup job that mutates the ledger to make totals match can destroy evidence and hide the original delivery defect.",
            repair: "Reconcile immutable IDs, counts, amounts, ordering metadata, and time windows; emit auditable exceptions and approved compensating entries.",
            complexity: "Reconciliation is a bounded join and aggregation; operational correctness depends on auditability and idempotency.",
            concept: "Financial correctness includes evidence, provenance, and controlled correction, not only a matching final total.",
            reference: "Federal Reserve: operational resilience and auditability",
            referenceURL: "https://www.federalreserve.gov/supervisionreg/srletters/sr2119.htm",
            hints: ["Define identity and source of truth.", "Compare counts and sums, not only totals.", "An exception queue preserves evidence."],
            explanation: "Reconciliation should detect missing, duplicate, mismatched, and late records with immutable evidence. Corrections belong in an auditable ledger workflow, not an opaque cleanup query."
        ),
        ExperimentTask(
            id: "testing-boundaries", title: "Testing: protect the behavior",
            prompt: "A parser passes happy-path tests but fails in production at empty input, malformed records, and schema changes. What test strategy should you add?",
            code: """
            parse(input) -> result
            parse(empty) -> ?
            parse(malformed) -> ?
            """,
            examples: "empty input -> explicit contract; malformed record -> safe failure",
            defect: "Happy-path tests do not protect boundary behavior, failure contracts, or integration assumptions.",
            repair: "Define behavior first, add boundary and failure cases, reproduce regressions, and test observable contracts.",
            complexity: "Test value is about risk and contract coverage, not raw test count.",
            concept: "Effective tests make normal cases, boundaries, failures, and integration seams executable.",
            reference: "Google Engineering Practices: testing",
            referenceURL: "https://google.github.io/eng-practices/review/developer/testing/",
            hints: ["List empty, maximal, malformed, and repeated inputs.", "Write failure behavior before assertions.", "A regression test must fail for the old defect."],
            explanation: "Good tests protect behavior that could regress without coupling every assertion to implementation details."
        ),
        ExperimentTask(
            id: "observability-contract", title: "Observability: make failure diagnosable",
            prompt: "A transaction pipeline reports only 'job failed'. What telemetry distinguishes bad input, dependency failure, lag, and code regression without logging sensitive data?",
            code: """
            request -> validate -> enrich -> write
                      ?         ?          ?
            """,
            examples: "dependency timeout -> bounded retry; sensitive data -> redacted context",
            defect: "A generic failure message prevents diagnosis, while unbounded payload logging can create a privacy incident.",
            repair: "Instrument stage latency, errors, lag, and correlation IDs with bounded, redacted context and actionable alerts.",
            complexity: "Telemetry should reduce diagnosis time without becoming an unbounded data pipeline.",
            concept: "Observability is a diagnostic contract connecting stages while excluding secrets and sensitive payloads.",
            reference: "OpenTelemetry documentation: signals and semantic conventions",
            referenceURL: "https://opentelemetry.io/docs/concepts/signals/",
            hints: ["Name the failure hypotheses on-call must distinguish.", "Prefer stable IDs over payloads.", "Metrics, logs, and traces answer different questions."],
            explanation: "Capture structured context that distinguishes failure classes, but deliberately exclude secrets and sensitive payloads."
        ),
        ExperimentTask(
            id: "secret-handling", title: "Security: keep secrets out of code",
            prompt: "A developer proposes committing a cloud connection string to simplify local testing. What safer workflow preserves speed without making the secret part of the artifact?",
            code: "const connectionString = \"...secret...\"\nclient.connect(connectionString)",
            examples: "local development -> injected credential; leak -> revoke and rotate",
            defect: "A secret in source control persists in history and expands the blast radius of every clone and artifact.",
            repair: "Inject short-lived, least-privilege credentials through an approved secret store and scan before merge.",
            complexity: "Security controls reduce expected incident cost; convenience is not a reason to widen credential scope.",
            concept: "Secure development makes runtime injection, narrow scope, short lifetime, scanning, and rotation routine.",
            reference: "OWASP Secrets Management Cheat Sheet",
            referenceURL: "https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html",
            hints: ["Assume repository history is copied.", "Separate configuration from credentials.", "A leaked credential requires rotation, not only deletion."],
            explanation: "Inject credentials at runtime, minimize scope and lifetime, scan before merge, and rotate immediately if exposure occurs."
        ),
        ExperimentTask(
            id: "api-compatibility", title: "API design: change without surprise",
            prompt: "You need to add a required field to an API consumed by multiple teams. How do you evolve the contract without breaking clients that have not deployed yet?",
            code: "v1 response: { id, amount }\nproposed:   { id, amount, currency! }",
            examples: "old client + new server -> additive change; new requirement -> migration",
            defect: "Making a new field mandatory for every existing client couples independent deployments and creates an avoidable breaking change.",
            repair: "Use an additive change, default or negotiation, contract tests, adoption telemetry, and a documented deprecation path.",
            complexity: "Compatibility cost is an organizational dependency problem, not only a type-system problem.",
            concept: "API evolution respects independently deployed consumers through compatibility and measured migration.",
            reference: "Microsoft REST API Guidelines",
            referenceURL: "https://github.com/microsoft/api-guidelines",
            hints: ["Consider both deployment orders.", "Define migration and rollback first.", "Measure who still depends on old behavior."],
            explanation: "Additive changes, explicit versioning or negotiation, contract tests, and measured deprecation reduce surprise."
        )
    ]
}

struct SessionResult: Codable, Identifiable, Equatable {
    let id: UUID
    let mode: SessionMode
    let taskID: String
    let startedAt: Date
    let finishedAt: Date
    let answer: String
    let confidenceBefore: Int?
    let assistedWork: String?
    let defect: String?
    let repair: String?
    let confidenceAfter: Int?
    let hintsRevealed: Int
    let explanationRevealed: Bool
    let appleIntelligenceUsed: Bool

    var durationSeconds: Int {
        Int(finishedAt.timeIntervalSince(startedAt).rounded())
    }
}

@MainActor
final class SessionStore: ObservableObject {
    @Published private(set) var results: [SessionResult] = []

    private let key = "continuous-competence-ios-results"

    init(defaults: UserDefaults = .standard) {
        if let data = defaults.data(forKey: key),
           let decoded = try? JSONDecoder().decode([SessionResult].self, from: data) {
            results = decoded
        }
    }

    func append(_ result: SessionResult, defaults: UserDefaults = .standard) {
        results.append(result)
        if let data = try? JSONEncoder().encode(results) {
            defaults.set(data, forKey: key)
        }
    }

    func exportJSON() -> String {
        let encoder = JSONEncoder()
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
        guard let data = try? encoder.encode(results),
              let string = String(data: data, encoding: .utf8) else {
            return "[]"
        }
        return string
    }
}

struct ContentView: View {
    @StateObject private var store = SessionStore()
    @State private var mode: SessionMode = .intervention
    @State private var step: SessionStep = .start
    @State private var startedAt = Date()
    @State private var answer = ""
    @State private var confidenceBefore = ""
    @State private var assistedWork = ""
    @State private var defect = ""
    @State private var repair = ""
    @State private var confidenceAfter = ""
    @State private var selectedTaskIndex = 0
    @State private var hintsRevealed = 0
    @State private var explanationRevealed = false
    @State private var appleIntelligenceResponse = ""
    @State private var appleIntelligenceUsed = false
    @State private var isGenerating = false
    @State private var showLibrary = false

    private var task: ExperimentTask { ExperimentTask.all[selectedTaskIndex] }

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    header
                    modePicker
                    content
                }
                .frame(maxWidth: 720, alignment: .leading)
                .padding(.horizontal, 20)
                .padding(.vertical, 24)
                .frame(maxWidth: .infinity, alignment: .center)
            }
            .background(Color(red: 0.96, green: 0.95, blue: 0.91))
            .navigationBarHidden(true)
            .preferredColorScheme(.light)
            .sheet(isPresented: $showLibrary) {
                LearningLibraryView(tasks: ExperimentTask.all)
            }
        }
    }

    private var header: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text("LOCAL EXPERIMENT")
                .font(.caption.weight(.bold))
                .tracking(2)
                .foregroundStyle(.orange)
            Text("Competence Check")
                .font(.largeTitle.weight(.bold))
                .foregroundStyle(Color(red: 0.09, green: 0.13, blue: 0.12))
        }
    }

    private var modePicker: some View {
        Picker("Session mode", selection: $mode) {
            ForEach(SessionMode.allCases) { option in
                Text(option.rawValue).tag(option)
            }
        }
        .pickerStyle(.segmented)
        .disabled(step != .start)
        .accessibilityHint("Control uses your ordinary method. Intervention adds controlled error inspection.")
    }

    @ViewBuilder
    private var content: some View {
        switch step {
        case .start:
            card {
                Text("10 MINUTES / LOCAL ONLY")
                    .font(.caption.weight(.bold))
                    .tracking(1.5)
                    .foregroundStyle(.orange)
                Text("One small competence check")
                    .font(.title2.weight(.bold))
                Text("A local learning instrument for a busy engineer: retrieve a concept, inspect a worked problem, and review the reference when you need a refresher.")
                    .foregroundStyle(.secondary)
                Picker("Question", selection: $selectedTaskIndex) {
                    ForEach(Array(ExperimentTask.all.enumerated()), id: \.offset) { index, task in
                        Text(task.title).tag(index)
                    }
                }
                .pickerStyle(.menu)
                Button("Open concept library") { showLibrary = true }
                    .buttonStyle(.bordered)
                notice("Do not use confidential code or record personal data.")
                primaryButton("Start session") { begin() }
            }
        case .retrieve:
            card {
                stepLabel("01 / RETRIEVE")
                Text("Think before assistance")
                    .font(.title2.weight(.bold))
                Text(task.prompt)
                    .font(.headline)
                Text("Examples: \(task.examples)")
                    .foregroundStyle(.secondary)
                Text("Concept refresher: \(task.concept)")
                    .font(.subheadline)
                input("Your answer", text: $answer, prompt: "State the repair and complexity in your own words.")
                numberInput("Confidence before checking", text: $confidenceBefore)
                primaryButton("Commit and continue") { step = .inspect }
            }
        case .inspect:
            card {
                stepLabel(mode == .control ? "02 / CONTROL" : "02 / INSPECT")
                Text(mode == .control ? "Use your ordinary method" : "Challenge a plausible answer")
                    .font(.title2.weight(.bold))
                if mode == .control {
                    Text("You may now use your normal AI, documentation, notes, or practice method. Record what changed and whether you independently checked it.")
                        .foregroundStyle(.secondary)
                    input("What did you do?", text: $assistedWork, prompt: "Briefly describe the method and result.")
                } else {
                    Text("An AI assistant returned this answer. Find the smallest defect, repair it, and explain why it matters.")
                    ScrollView(.horizontal, showsIndicators: true) {
                        Text(task.code)
                            .font(.system(.footnote, design: .monospaced))
                            .foregroundStyle(.white)
                            .padding(14)
                    }
                    .background(Color(red: 0.12, green: 0.17, blue: 0.16))
                    .clipShape(RoundedRectangle(cornerRadius: 12))
                    input("Defect", text: $defect, prompt: "What is wrong, if anything?")
                    input("Repair and explanation", text: $repair, prompt: "Give the smallest repair and complexity.")
                    hintLadder
                    explanationPanel
                    appleIntelligencePanel
                    numberInput("Confidence after verification", text: $confidenceAfter)
                }
                primaryButton("Finish session") { finish() }
            }
        case .finish:
            card {
                stepLabel("SESSION SAVED LOCALLY")
                Text("Keep the result separate from performance")
                    .font(.title2.weight(.bold))
                LabeledContent("Condition", value: mode.rawValue)
                LabeledContent("Storage", value: "This device only")
                notice("This records an experiment session, not mastery, effectiveness, or a product result.")
                ShareLink(item: store.exportJSON()) {
                    Label("Export JSON", systemImage: "square.and.arrow.up")
                }
                .buttonStyle(.borderedProminent)
                primaryButton("Run again") { reset() }
            }
        }
    }

    private func card<Content: View>(@ViewBuilder content: () -> Content) -> some View {
        VStack(alignment: .leading, spacing: 16, content: content)
            .padding(20)
            .background(.white.opacity(0.82))
            .clipShape(RoundedRectangle(cornerRadius: 20))
            .overlay(RoundedRectangle(cornerRadius: 20).stroke(.black.opacity(0.08)))
    }

    private func stepLabel(_ text: String) -> some View {
        Text(text)
            .font(.caption.weight(.bold))
            .tracking(1.2)
            .foregroundStyle(.orange)
    }

    private func notice(_ text: String) -> some View {
        Text(text)
            .font(.subheadline)
            .padding(12)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(.orange.opacity(0.12))
            .clipShape(RoundedRectangle(cornerRadius: 10))
    }

    private func input(_ title: String, text: Binding<String>, prompt: String) -> some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(title).font(.subheadline.weight(.semibold))
            TextField(prompt, text: text, axis: .vertical)
                .lineLimit(3...8)
                .textFieldStyle(.roundedBorder)
        }
    }

    private func numberInput(_ title: String, text: Binding<String>) -> some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(title).font(.subheadline.weight(.semibold))
            TextField("0–100", text: text)
                .keyboardType(.numberPad)
                .textFieldStyle(.roundedBorder)
                .frame(maxWidth: 130)
        }
    }

    private var hintLadder: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Progressive hints").font(.subheadline.weight(.semibold))
            ForEach(Array(task.hints.prefix(hintsRevealed).enumerated()), id: \.offset) { index, hint in
                Label("Hint \(index + 1): \(hint)", systemImage: "lightbulb")
                    .font(.subheadline)
            }
            if hintsRevealed < task.hints.count {
                Button("Reveal hint \(hintsRevealed + 1)") {
                    hintsRevealed += 1
                }
                .buttonStyle(.bordered)
            }
        }
        .padding(12)
        .background(.yellow.opacity(0.14))
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }

    private var explanationPanel: some View {
        VStack(alignment: .leading, spacing: 8) {
            Button(explanationRevealed ? "Explanation shown" : "Show plain-language explanation") {
                explanationRevealed = true
            }
            .buttonStyle(.bordered)
            if explanationRevealed {
                Text(task.explanation)
                    .font(.subheadline)
                Link("Review: \(task.reference)", destination: URL(string: task.referenceURL)!)
                    .font(.subheadline.weight(.semibold))
            }
        }
    }

    private var appleIntelligencePanel: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Apple Intelligence").font(.subheadline.weight(.semibold))
            Text("When available, ask the on-device model to re-explain this concept. Your answer is not sent to a server by this experiment.")
                .font(.subheadline)
                .foregroundStyle(.secondary)
            Button(isGenerating ? "Generating..." : "Ask Apple Intelligence for a hint") {
                Task { await generateAppleIntelligenceHelp() }
            }
            .buttonStyle(.bordered)
            .disabled(isGenerating)
            if !appleIntelligenceResponse.isEmpty {
                Text(appleIntelligenceResponse)
                    .font(.subheadline)
                    .padding(10)
                    .background(.blue.opacity(0.08))
                    .clipShape(RoundedRectangle(cornerRadius: 10))
            }
        }
        .padding(12)
        .background(.blue.opacity(0.06))
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }

    private func generateAppleIntelligenceHelp() async {
        isGenerating = true
        defer { isGenerating = false }
        #if canImport(FoundationModels)
        if #available(iOS 26.0, *) {
            let session = LanguageModelSession()
            do {
                let response = try await session.respond(to: "Explain this software-engineering concept in plain language, give one analogy, and ask one checking question. Concept: \(task.concept)")
                appleIntelligenceResponse = response.content
                appleIntelligenceUsed = true
                return
            } catch {
                appleIntelligenceResponse = "Apple Intelligence is unavailable right now. Use the local explanation and reference instead."
                return
            }
        }
        #endif
        appleIntelligenceResponse = "Apple Intelligence requires a supported device with Apple Intelligence enabled. Use the local explanation and reference instead."
    }

    private func primaryButton(_ title: String, action: @escaping () -> Void) -> some View {
        Button(title, action: action)
            .buttonStyle(.borderedProminent)
            .tint(Color(red: 0.09, green: 0.13, blue: 0.12))
            .accessibilityHint("Advances the local experiment without sending data anywhere.")
    }

    private func begin() {
        startedAt = Date()
        hintsRevealed = 0
        explanationRevealed = false
        appleIntelligenceResponse = ""
        appleIntelligenceUsed = false
        step = .retrieve
    }

    private func finish() {
        let result = SessionResult(
            id: UUID(),
            mode: mode,
            taskID: task.id,
            startedAt: startedAt,
            finishedAt: Date(),
            answer: answer,
            confidenceBefore: Int(confidenceBefore),
            assistedWork: mode == .control ? assistedWork : nil,
            defect: mode == .intervention ? defect : nil,
            repair: mode == .intervention ? repair : nil,
            confidenceAfter: mode == .intervention ? Int(confidenceAfter) : nil,
            hintsRevealed: hintsRevealed,
            explanationRevealed: explanationRevealed,
            appleIntelligenceUsed: appleIntelligenceUsed
        )
        store.append(result)
        step = .finish
    }

    private func reset() {
        answer = ""
        confidenceBefore = ""
        assistedWork = ""
        defect = ""
        repair = ""
        confidenceAfter = ""
        hintsRevealed = 0
        explanationRevealed = false
        appleIntelligenceResponse = ""
        appleIntelligenceUsed = false
        step = .start
    }
}

struct LearningLibraryView: View {
    let tasks: [ExperimentTask]
    @Environment(\.dismiss) private var dismiss

    private let commonQuestions = [
        ("What does O(n) actually mean?", "As input grows, the work grows roughly in proportion to the number of items. It describes a growth trend, not a stopwatch promise."),
        ("When should I use a transaction?", "Use one when several state changes must appear as one durable business operation, or explicitly model retries and reconciliation when they cross system boundaries."),
        ("What makes a test valuable?", "A valuable test protects a behavior or invariant that could regress. Prefer boundary cases, failure paths, and a name that explains the contract."),
        ("How do I debug an unfamiliar system?", "Build a narrow mental model: reproduce, observe inputs and outputs, form one hypothesis, change one variable, and record what falsified it.")
    ]

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 18) {
                    Text("ENGINEERING REFRESHER")
                        .font(.caption.weight(.bold))
                        .tracking(1.5)
                        .foregroundStyle(.orange)
                    Text("Learn by retrieval, then verify")
                        .font(.largeTitle.weight(.bold))
                    Text("Short explanations are paired with a reference and a checking question. The goal is to rebuild a usable mental model, not collect trivia.")
                        .foregroundStyle(.secondary)

                    sectionTitle("Concept cards")
                    ForEach(tasks, id: \.id) { task in
                        VStack(alignment: .leading, spacing: 8) {
                            Text(task.title).font(.headline)
                            Text(task.concept).font(.subheadline)
                            Link(task.reference, destination: URL(string: task.referenceURL)!)
                                .font(.subheadline.weight(.semibold))
                        }
                        .padding(14)
                        .background(.white.opacity(0.85))
                        .clipShape(RoundedRectangle(cornerRadius: 14))
                    }

                    sectionTitle("Common questions")
                    ForEach(commonQuestions, id: \.0) { question, answer in
                        DisclosureGroup(question) {
                            Text(answer)
                                .font(.subheadline)
                                .padding(.top, 6)
                        }
                        .padding(12)
                        .background(.white.opacity(0.85))
                        .clipShape(RoundedRectangle(cornerRadius: 12))
                    }

                    sectionTitle("Visual walkthroughs")
                    walkthrough(
                        title: "Binary search: shrink the interval",
                        diagram: "[ low ........ high ]\n          mid\n[ low .. mid )  or  ( mid .. high ]",
                        steps: [
                            "Start with a candidate interval containing every possible answer.",
                            "Inspect the midpoint and discard the half that cannot contain the target.",
                            "Repeat until the interval is empty or one candidate remains."
                        ]
                    )
                    walkthrough(
                        title: "Failure-safe write: make the boundary explicit",
                        diagram: "request\n   |\n   v\n[transaction: debit + audit]\n   |\n   v\n committed or rolled back",
                        steps: [
                            "Name the business operation, not just the individual writes.",
                            "Choose one durable boundary for the operation when possible.",
                            "If systems cross a boundary, use an outbox, idempotency, and reconciliation."
                        ]
                    )
                }
                .padding(20)
            }
            .background(Color(red: 0.96, green: 0.95, blue: 0.91))
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Close") { dismiss() }
                }
            }
        }
    }

    private func sectionTitle(_ title: String) -> some View {
        Text(title)
            .font(.title3.weight(.bold))
            .padding(.top, 8)
    }

    private func walkthrough(title: String, diagram: String, steps: [String]) -> some View {
        VStack(alignment: .leading, spacing: 10) {
            Text(title).font(.headline)
            Text(diagram)
                .font(.system(.footnote, design: .monospaced))
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding(14)
                .foregroundStyle(.white)
                .background(Color(red: 0.12, green: 0.17, blue: 0.16))
                .clipShape(RoundedRectangle(cornerRadius: 10))
            ForEach(Array(steps.enumerated()), id: \.offset) { index, step in
                Label(step, systemImage: "\(index + 1).circle")
                    .font(.subheadline)
            }
        }
        .padding(14)
        .background(.white.opacity(0.85))
        .clipShape(RoundedRectangle(cornerRadius: 14))
    }
}

#Preview {
    ContentView()
}
