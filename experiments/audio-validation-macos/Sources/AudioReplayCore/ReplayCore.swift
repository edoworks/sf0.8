import AVFoundation
import CryptoKit
import Foundation
import SoundAnalysis

public struct ReplayManifest: Codable, Sendable {
    public let schemaVersion: Int
    public let fixtures: [FixtureInput]

    public init(schemaVersion: Int = 1, fixtures: [FixtureInput]) {
        self.schemaVersion = schemaVersion
        self.fixtures = fixtures
    }

    enum CodingKeys: String, CodingKey {
        case schemaVersion = "schema_version"
        case fixtures
    }
}

public struct FixtureInput: Codable, Sendable {
    public let id: String
    public let path: String
    public let expectedLabels: [String]
    public let minimumConfidence: Double
    public let expectedDecision: ReplayDecision

    public init(
        id: String,
        path: String,
        expectedLabels: [String] = [],
        minimumConfidence: Double = 0.5,
        expectedDecision: ReplayDecision
    ) {
        self.id = id
        self.path = path
        self.expectedLabels = expectedLabels
        self.minimumConfidence = minimumConfidence
        self.expectedDecision = expectedDecision
    }

    enum CodingKeys: String, CodingKey {
        case id
        case path
        case expectedLabels = "expected_labels"
        case minimumConfidence = "minimum_confidence"
        case expectedDecision = "expected_decision"
    }
}

public struct Observation: Codable, Sendable, Equatable {
    public let label: String
    public let confidence: Double

    public init(label: String, confidence: Double) {
        self.label = label
        self.confidence = confidence
    }
}

public enum ReplayStatus: String, Codable, Sendable {
    case pass = "PASS"
    case fail = "FAIL"
}

public enum ReplayDecision: String, Codable, Sendable {
    case target = "TARGET"
    case nonTarget = "NON_TARGET"
    case abstain = "ABSTAIN"
}

public struct FixtureResult: Codable, Sendable, Equatable {
    public let id: String
    public let path: String
    public let sha256: String
    public let observations: [Observation]
    public let decision: ReplayDecision
    public let status: ReplayStatus
    public let sampleRate: Double
    public let frameCount: Int

    enum CodingKeys: String, CodingKey {
        case id, path, sha256, observations, decision, status
        case sampleRate = "sample_rate"
        case frameCount = "frame_count"
    }
}

public struct ReplayReport: Codable, Sendable {
    public let schemaVersion: Int
    public let runner: [String: String]
    public let environment: [String: String]
    public let deviceClaim: String
    public let fixtures: [FixtureResult]

    enum CodingKeys: String, CodingKey {
        case schemaVersion = "schema_version"
        case runner, environment
        case deviceClaim = "device_claim"
        case fixtures
    }
}

public enum ReplayError: Error, CustomStringConvertible {
    case invalidManifest
    case fixtureOutsideRoot(String)
    case fixtureMissing(String)
    case noExpectedLabel(String)
    case analysisFailed(String)
    case invalidFixture(String)

    public var description: String {
        switch self {
        case .invalidManifest: return "manifest must use schema version 1 and contain fixtures"
        case .fixtureOutsideRoot(let path): return "fixture escapes the manifest root: \(path)"
        case .fixtureMissing(let path): return "fixture does not exist: \(path)"
        case .noExpectedLabel(let id): return "fixture has no expected label: \(id)"
        case .analysisFailed(let path): return "Sound Analysis failed for fixture: \(path)"
        case .invalidFixture(let id): return "fixture contract is invalid: \(id)"
        }
    }
}

public struct EventWindow: Equatable, Sendable {
    public let frames: Range<Int>

    public init(frames: Range<Int>) {
        self.frames = frames
    }

    public static func bounded(
        triggerFrame: Int,
        preRollFrames: Int,
        postRollFrames: Int,
        availableFrames: Int
    ) -> EventWindow? {
        guard triggerFrame >= 0, preRollFrames >= 0, postRollFrames >= 0,
              availableFrames > 0, triggerFrame < availableFrames else { return nil }
        let lower = max(0, triggerFrame - preRollFrames)
        let upper = min(availableFrames, triggerFrame + postRollFrames + 1)
        return EventWindow(frames: lower..<upper)
    }
}

public enum ReplayEvaluator {
    public static func decision(
        observations: [Observation],
        expectedLabels: [String],
        minimumConfidence: Double = 0.5
    ) -> ReplayDecision {
        guard (0...1).contains(minimumConfidence), !expectedLabels.isEmpty else { return .abstain }
        let candidates = observations.filter { $0.confidence >= minimumConfidence }
        guard !candidates.isEmpty else { return .abstain }
        return candidates.contains { expectedLabels.contains($0.label) } ? .target : .nonTarget
    }

    public static func status(decision: ReplayDecision, expectedDecision: ReplayDecision) -> ReplayStatus {
        decision == expectedDecision ? .pass : .fail
    }

    public static func sha256(of url: URL) throws -> String {
        let data = try Data(contentsOf: url, options: [.mappedIfSafe])
        return SHA256.hash(data: data).map { String(format: "%02x", $0) }.joined()
    }
}

private final class ClassificationObserver: NSObject, SNResultsObserving, @unchecked Sendable {
    private(set) var observations: [Observation] = []
    private(set) var error: Error?

    func request(_ request: SNRequest, didProduce result: SNResult) {
        guard let result = result as? SNClassificationResult else { return }
        observations.append(contentsOf: result.classifications.map {
            Observation(label: $0.identifier, confidence: Double($0.confidence))
        })
    }

    func request(_ request: SNRequest, didFailWithError error: Error) {
        self.error = error
    }

    func setCompletionError(_ error: Error) {
        self.error = error
    }

    func requestDidComplete(_ request: SNRequest) {}
}

public enum AudioReplayRunner {
    public static func run(manifest: ReplayManifest, root: URL) throws -> ReplayReport {
        guard manifest.schemaVersion == 1, !manifest.fixtures.isEmpty else {
            throw ReplayError.invalidManifest
        }

        let root = root.standardizedFileURL
        var results: [FixtureResult] = []
        var fixtureIDs: Set<String> = []
        for fixture in manifest.fixtures {
            guard !fixture.id.isEmpty, !fixture.path.isEmpty,
                  (0...1).contains(fixture.minimumConfidence),
                  fixtureIDs.insert(fixture.id).inserted else {
                throw ReplayError.invalidFixture(fixture.id)
            }
            let url = root.appendingPathComponent(fixture.path).standardizedFileURL
            guard url.path.hasPrefix(root.path + "/") else {
                throw ReplayError.fixtureOutsideRoot(fixture.path)
            }
            guard FileManager.default.fileExists(atPath: url.path) else {
                throw ReplayError.fixtureMissing(fixture.path)
            }

            let audioFile = try AVAudioFile(forReading: url)
            let observer = ClassificationObserver()
            let analyzer = try SNAudioFileAnalyzer(url: url)
            let request = try SNClassifySoundRequest(classifierIdentifier: .version1)
            try analyzer.add(request, withObserver: observer)
            let completed = DispatchSemaphore(value: 0)
            analyzer.analyze { success in
                if !success { observer.setCompletionError(ReplayError.analysisFailed(fixture.path)) }
                completed.signal()
            }
            completed.wait()
            if let error = observer.error { throw error }
            let decision = ReplayEvaluator.decision(
                observations: observer.observations,
                expectedLabels: fixture.expectedLabels,
                minimumConfidence: fixture.minimumConfidence
            )
            results.append(FixtureResult(
                id: fixture.id,
                path: fixture.path,
                sha256: try ReplayEvaluator.sha256(of: url),
                observations: observer.observations,
                decision: decision,
                status: ReplayEvaluator.status(decision: decision, expectedDecision: fixture.expectedDecision),
                sampleRate: audioFile.fileFormat.sampleRate,
                frameCount: Int(audioFile.length)
            ))
        }

        return ReplayReport(
            schemaVersion: 1,
            runner: ["name": "audio-replay", "version": "0.1"],
            environment: ["platform": "macOS", "os": ProcessInfo.processInfo.operatingSystemVersionString],
            deviceClaim: "HOST_REPLAY_ONLY",
            fixtures: results
        )
    }
}
