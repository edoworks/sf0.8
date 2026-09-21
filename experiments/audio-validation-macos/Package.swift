// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "AudioValidationMacOS",
    platforms: [.macOS(.v14), .iOS(.v17)],
    products: [
        .library(name: "AudioReplayCore", targets: ["AudioReplayCore"]),
        .executable(name: "audio-replay", targets: ["AudioReplay"]),
    ],
    targets: [
        .target(name: "AudioReplayCore"),
        .executableTarget(name: "AudioReplay", dependencies: ["AudioReplayCore"]),
        .testTarget(name: "AudioReplayCoreTests", dependencies: ["AudioReplayCore"]),
    ]
)
