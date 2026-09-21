import AudioReplayCore
import Foundation

struct Arguments {
    let manifest: URL
    let root: URL
    let output: URL?

    init() throws {
        var values = Array(CommandLine.arguments.dropFirst())
        if values.contains("--help") || values.contains("-h") {
            print("Usage: audio-replay --manifest MANIFEST.json [--root ROOT] [--output REPORT.json]")
            exit(0)
        }
        func value(for flag: String) throws -> String {
            guard let index = values.firstIndex(of: flag), index + 1 < values.count else {
                throw NSError(domain: "audio-replay", code: 2, userInfo: [NSLocalizedDescriptionKey: "missing \(flag)"])
            }
            let value = values[index + 1]
            values.removeSubrange(index...(index + 1))
            return value
        }

        let manifest = URL(fileURLWithPath: try value(for: "--manifest"))
        let rootPath: String
        if values.contains("--root") {
            rootPath = try value(for: "--root")
        } else {
            rootPath = manifest.deletingLastPathComponent().path
        }
        var output: URL?
        if values.contains("--output") {
            output = URL(fileURLWithPath: try value(for: "--output"))
        }
        self.manifest = manifest.standardizedFileURL
        self.root = URL(fileURLWithPath: rootPath).standardizedFileURL
        self.output = output?.standardizedFileURL
    }
}

do {
    let arguments = try Arguments()
    let decoder = JSONDecoder()
    let manifest = try decoder.decode(ReplayManifest.self, from: Data(contentsOf: arguments.manifest))
    let report = try AudioReplayRunner.run(manifest: manifest, root: arguments.root)
    let encoder = JSONEncoder()
    encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
    let data = try encoder.encode(report)
    if let output = arguments.output {
        try data.write(to: output, options: .atomic)
    } else {
        FileHandle.standardOutput.write(data)
        FileHandle.standardOutput.write(Data("\n".utf8))
    }
} catch {
    FileHandle.standardError.write(Data("ERROR: \(error)\n".utf8))
    exit(1)
}
