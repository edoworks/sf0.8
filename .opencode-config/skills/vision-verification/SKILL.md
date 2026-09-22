---
name: vision-verification
description: Verify rendered UI screenshots using a local vision-capable LLM via the Ollama API. Use when you need to visually confirm app screenshots, check layout/color/hierarchy from captured images, or unblock visual review gates without manual human inspection. Covers the mechanical API call pattern, thinking-mode disable, checklist prompts, and evidence recording.
---

# Vision Verification

Verify rendered UI screenshots using a local vision-capable LLM (Ollama
`qwen3.5:4b`) via the Ollama generate API. This unblocks visual review gates
without manual human inspection for deterministic and subjective-aesthetic
checks.

## When To Use

- After capturing an app screenshot (simulator or physical device) that needs
  visual verification against PRD criteria or a design checklist.
- When a visual review gate is blocking progress and the active session model
  lacks image input capability.
- For rendered UI verification, visual regression checks, and
  accessibility-relevant layout inspection from captured images.

## When NOT To Use

- Release, upload, submission, or external-write decisions — vision
  verification does not authorize these; they remain human-gated.
- Trust-boundary analysis (authentication, authorization, isolation, signing)
  — use the `trust-review` route instead.
- Deterministic layout assertions that can be expressed as XCUITest frame
  checks — prefer automated UI tests; use vision as a complement, not a
  replacement.

## Procedure

### 1. Confirm the vision model is available

```bash
ollama list
```

Ensure `qwen3.5:4b` (or a larger vision-capable model) is installed locally.
Fallback: `ollama-cloud/gemma4:31b` via the cloud API if the local model is
unavailable or insufficient quality.

### 2. Capture the screenshot

Use `xcrun simctl io <simulator-uuid> screenshot <path>` for simulator
screenshots, or the `macos-screenshot` skill for macOS app captures.

### 3. Run the vision model via the Ollama API

The Ollama CLI does not support image input directly. Use the HTTP API with
a base64-encoded image. Write a Python script:

```python
import base64
import json
import urllib.request

with open("<screenshot-path>", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode("utf-8")

prompt = """<your verification checklist here>"""

payload = {
    "model": "qwen3.5:4b",
    "prompt": prompt,
    "images": [image_b64],
    "stream": False,
    "think": False,
    "options": {"temperature": 0.1, "num_predict": 600}
}

req = urllib.request.Request(
    "http://localhost:11434/api/generate",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)

with urllib.request.urlopen(req, timeout=300) as resp:
    result = json.loads(resp.read().decode("utf-8"))
    print(result.get("response", ""))
```

### 4. Critical parameters

- **`think: false`** — Disable thinking mode. With thinking enabled, the model
  may spend all tokens on internal reasoning and return an empty `response`
  field. The thinking output appears in `result["thinking"]` but is not the
  verified answer.
- **`num_predict: 600`** — Set a generous token limit (500-800) so the model
  has room to complete its answer after any thinking.
- **`temperature: 0.1`** — Low temperature for deterministic, repeatable
  observations.
- **`stream: false`** — Wait for the full response rather than streaming.

### 5. Checklist prompt structure

Frame the prompt as a numbered checklist with explicit PASS/FAIL/UNCERTAIN
labels required for each item. Example:

```
For each question answer PASS, FAIL, or UNCERTAIN with a one-sentence observation.

1. CONTENT: Are all expected labels and values visible?
2. LAYOUT: Is the content in the expected top-to-bottom order?
3. COLOR: Does the background/card/button match the expected palette?
4. CLIPPING: Is any text cut off or requiring horizontal scroll?
5. HIERARCHY: Is the primary action the most prominent element?
6. IMPRESSION: Does it look calm/restrained (not cluttered)?
```

### 6. Interpret results

- **PASS** — the criterion is met.
- **FAIL** — the criterion is not met; investigate and fix.
- **UNCERTAIN** — the model cannot determine; may need human review or a
  stronger vision model. Check whether UNCERTAIN is expected by design (e.g.,
  a label being smaller than its value is by design, not a defect).
- **Model labeling errors** — the vision model may label a check "FAIL" but
  the observation text actually confirms the criterion (e.g., "FAIL — no
  clipping observed"). Reclassify based on the observation text, not the
  label.

### 7. Record evidence

Store vision verification results in the chunk evidence JSON under
`visual_verification.vision_model_verification` with:
- `model`: the vision model used (e.g., `ollama/qwen3.5:4b`)
- `screenshot`: path to the verified screenshot
- `date`: verification date
- `results`: per-check PASS/FAIL/UNCERTAIN with observations
- `note`: any reclassifications or design-expected UNCERTAIN items

## Escalation

If `qwen3.5:4b` quality is insufficient:
1. Try `qwen3.5:9b` or `qwen3.5:27b` (larger, slower, better quality).
2. Try the cloud fallback `ollama-cloud/gemma4:31b` via the cloud API.
3. If still insufficient, request owner approval for a stronger vision model
   via the `model-routing` skill.

## Constraints

- Vision auto-invocation is limited to screenshot-only assertion inputs per
  owner approval 2026-09-21.
- Vision verification does not authorize release, upload, submission, or any
  external write.
- The vision model can be wrong — always cross-check with deterministic UI
  tests where possible.
- Never fabricate a PASS; if the model returns UNCERTAIN or empty, record it
  honestly and escalate.
- The Ollama API runs on `http://localhost:11434`; ensure the daemon is
  running before attempting the API call.
- Base64-encoding large screenshots increases payload size; for very large
  images, consider downscaling before encoding.