import XCTest
@testable import CompetenceCheck

final class CompetenceCheckTests: XCTestCase {
    func testFixtureContainsControlledDefectAndRepair() {
        let task = ExperimentTask.longestRun
        XCTAssertTrue(task.code.contains("len(values) - 1"))
        XCTAssertTrue(task.repair.contains("len(values))"))
        XCTAssertEqual(task.complexity, "O(n) time and O(1) auxiliary space.")
    }

    func testQuestionBankHasReferenceBackedLearningSupport() {
        XCTAssertGreaterThanOrEqual(ExperimentTask.all.count, 3)
        XCTAssertTrue(ExperimentTask.all.allSatisfy { $0.hints.count >= 3 })
        XCTAssertTrue(ExperimentTask.all.allSatisfy { !$0.referenceURL.isEmpty && !$0.explanation.isEmpty })
    }

    func testQuestionBankCoversFinancialDataPlatforms() {
        let text = ExperimentTask.financeData.map { "\($0.title) \($0.concept)" }.joined(separator: " ")
        XCTAssertTrue(text.contains("Spark"))
        XCTAssertTrue(text.contains("Synapse"))
        XCTAssertTrue(text.contains("Event Hubs"))
        XCTAssertTrue(text.contains("ADLS Gen2"))
        XCTAssertTrue(text.contains("Financial transactions"))
    }

    func testQuestionBankCoversSoftwareEngineeringPractices() {
        let practiceIDs = Set(["testing-boundaries", "observability-contract", "secret-handling", "api-compatibility"])
        XCTAssertTrue(practiceIDs.isSubset(of: Set(ExperimentTask.all.map(\.id))))
        XCTAssertTrue(ExperimentTask.all.filter { practiceIDs.contains($0.id) }.allSatisfy { !$0.reference.isEmpty })
    }

    @MainActor
    func testSessionStoreRoundTripsLocally() {
        let suite = "competence-check-tests"
        let defaults = UserDefaults(suiteName: suite)!
        defaults.removePersistentDomain(forName: suite)
        let store = SessionStore(defaults: defaults)
        let now = Date()
        let result = SessionResult(
            id: UUID(), mode: .intervention, taskID: "longest-run", startedAt: now, finishedAt: now,
            answer: "repair", confidenceBefore: 60, assistedWork: nil,
            defect: "off by one", repair: "extend range", confidenceAfter: 90,
            hintsRevealed: 1, explanationRevealed: true, appleIntelligenceUsed: false
        )

        store.append(result, defaults: defaults)
        let reloaded = SessionStore(defaults: defaults)
        XCTAssertEqual(reloaded.results, [result])
        XCTAssertTrue(reloaded.exportJSON().contains("INTERVENTION"))
    }
}
