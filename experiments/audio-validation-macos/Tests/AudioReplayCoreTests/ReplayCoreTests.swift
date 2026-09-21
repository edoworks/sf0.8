import XCTest
@testable import AudioReplayCore

final class ReplayCoreTests: XCTestCase {
    func testMatchingExpectedLabelPasses() {
        let observations = [Observation(label: "cat", confidence: 0.8)]
        let decision = ReplayEvaluator.decision(observations: observations, expectedLabels: ["cat"])
        XCTAssertEqual(.target, decision)
        XCTAssertEqual(.pass, ReplayEvaluator.status(decision: decision, expectedDecision: .target))
    }

    func testNonMatchingExpectedLabelFails() {
        let observations = [Observation(label: "speech", confidence: 0.8)]
        let decision = ReplayEvaluator.decision(observations: observations, expectedLabels: ["cat"])
        XCTAssertEqual(.nonTarget, decision)
        XCTAssertEqual(.pass, ReplayEvaluator.status(decision: decision, expectedDecision: .nonTarget))
    }

    func testNoObservationAbstains() {
        XCTAssertEqual(.abstain, ReplayEvaluator.decision(observations: [], expectedLabels: ["cat"]))
    }

    func testMissingExpectedLabelAbstains() {
        let observations = [Observation(label: "cat", confidence: 0.8)]
        XCTAssertEqual(.abstain, ReplayEvaluator.decision(observations: observations, expectedLabels: []))
    }

    func testLowConfidenceTargetAbstains() {
        let observations = [Observation(label: "cat", confidence: 0.49)]
        XCTAssertEqual(
            .abstain,
            ReplayEvaluator.decision(observations: observations, expectedLabels: ["cat"], minimumConfidence: 0.5)
        )
    }

    func testInvalidThresholdFailsClosed() {
        let observations = [Observation(label: "cat", confidence: 0.8)]
        XCTAssertEqual(
            .abstain,
            ReplayEvaluator.decision(observations: observations, expectedLabels: ["cat"], minimumConfidence: 1.1)
        )
    }

    func testUnexpectedDecisionFailsFixture() {
        XCTAssertEqual(.fail, ReplayEvaluator.status(decision: .abstain, expectedDecision: .target))
    }

    func testEventWindowIncludesBoundedPreAndPostRoll() {
        XCTAssertEqual(
            EventWindow(frames: 5..<16),
            EventWindow.bounded(triggerFrame: 10, preRollFrames: 5, postRollFrames: 5, availableFrames: 100)
        )
        XCTAssertEqual(
            EventWindow(frames: 0..<4),
            EventWindow.bounded(triggerFrame: 1, preRollFrames: 5, postRollFrames: 2, availableFrames: 4)
        )
    }

    func testEventWindowRejectsInvalidTrigger() {
        XCTAssertNil(EventWindow.bounded(triggerFrame: 4, preRollFrames: 1, postRollFrames: 1, availableFrames: 4))
    }
}
