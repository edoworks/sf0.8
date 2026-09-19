#!/usr/bin/env python3
"""Generate and validate the smallest evidence-driven executive council review."""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".factory" / "artifacts" / "executive-council"
BOARD = ROOT / ".factory" / "artifacts" / "reports" / "apple-distribution" / "release-board-2026-09-19.json"
CUSTOMER_ZERO = ROOT / ".factory" / "customer-zero.json"
EDUCATION = ROOT / ".factory" / "artifacts" / "evidence" / "education-opportunity-discovery.json"
GOVERNANCE = ROOT / ".factory" / "governance.yaml"
EVIDENCE_BUNDLE = ROOT / ".factory" / "automation" / "evidence-bundle.json"
PORTFOLIO = ROOT / ".factory" / "portfolio.yaml"
TELEMETRY = ROOT / ".factory" / "factory.sqlite"
ALLOWED_CLASSES = {"FACT", "EVIDENCE", "INFERENCE", "ASSUMPTION", "UNKNOWN", "RECOMMENDATION"}
LENSES = ("CEO", "CFO", "CPO", "CTO", "COO")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def source(path: Path, claim: str, value: Any, kind: str) -> dict[str, Any]:
    return {"kind": kind, "source": str(path.relative_to(ROOT)), "claim": claim, "value": value}


def telemetry() -> dict[str, Any]:
    with sqlite3.connect(TELEMETRY) as connection:
        runs = connection.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
        successes = connection.execute("SELECT COUNT(*) FROM runs WHERE outcome = 'success'").fetchone()[0]
        cost = connection.execute("SELECT COALESCE(SUM(usd), 0) FROM costs").fetchone()[0]
    return {"runs": runs, "successful_runs": successes, "recorded_factory_cost_usd": cost}


def evidence() -> dict[str, Any]:
    board = load(BOARD)
    education = load(EDUCATION)
    zero = load(CUSTOMER_ZERO)
    bundle = load(EVIDENCE_BUNDLE)
    counts = board["summary"]
    conflicts = [
        {
            "topic": "Product A lifecycle",
            "claims": [
                {"source": str(PORTFOLIO.relative_to(ROOT)), "value": "shelved"},
                {"source": str(CUSTOMER_ZERO.relative_to(ROOT)), "value": "active product direction"},
                {"source": str(BOARD.relative_to(ROOT)), "value": "SHELVED"},
            ],
            "status": "BLOCKED_UNRESOLVED_SOURCE_CONFLICT",
        }
    ]
    return {
        "snapshot_date": board["generated_at"],
        "sources": [str(BOARD.relative_to(ROOT)), str(CUSTOMER_ZERO.relative_to(ROOT)), str(EDUCATION.relative_to(ROOT)), str(EVIDENCE_BUNDLE.relative_to(ROOT)), str(PORTFOLIO.relative_to(ROOT))],
        "portfolio": {
            "apple_products": source(BOARD, "Apple products discovered", counts["apple_products"], "FACT"),
            "candidates": source(BOARD, "independent candidates", counts["candidates"], "FACT"),
            "ready_for_review": source(BOARD, "products ready for review", counts["ready_for_review"], "FACT"),
            "blocked": source(BOARD, "blocked products", counts["blocked"], "FACT"),
            "shelved": source(BOARD, "shelved products", counts["shelved"], "FACT"),
            "working": source(BOARD, "working products", counts["working"], "FACT"),
        },
        "customer": {
            "customer_zero_records": source(CUSTOMER_ZERO, "Customer Zero records", len(zero["products"]), "EVIDENCE"),
            "external_validation": {"kind": "UNKNOWN", "source": "not recorded in canonical evidence", "claim": "External customer behavior, payment, retention", "value": "UNKNOWN"},
            "education_external_validation": source(EDUCATION, "direct customer evidence", education["evidence_discipline"]["direct_customer_evidence"], "FACT"),
            "education_payment": source(EDUCATION, "external payment evidence", education["evidence_discipline"]["external_payment_evidence"], "FACT"),
        },
        "economics": {
            "revenue": {"kind": "UNKNOWN", "source": "not recorded in canonical evidence", "claim": "Company revenue", "value": "UNKNOWN"},
            "contribution_margin": {"kind": "UNKNOWN", "source": "not recorded in canonical evidence", "claim": "Contribution margin", "value": "UNKNOWN"},
            "operating_cost": {"kind": "UNKNOWN", "source": "not recorded in canonical evidence", "claim": "Company operating cost", "value": "UNKNOWN"},
            "factory_telemetry": source(TELEMETRY, "recorded factory telemetry cost", telemetry(), "FACT"),
        },
        "factory": {
            "verification": source(BOARD, "factory verification", board["factory"]["verification"], "EVIDENCE"),
            "customer_zero_bundle": source(EVIDENCE_BUNDLE, "Customer Zero category", bundle["categories"]["CUSTOMER-ZERO"], "EVIDENCE"),
        },
        "conflicts": conflicts,
    }


def claim(kind: str, text: str, evidence_ids: list[str], action: str | None = None) -> dict[str, Any]:
    item = {"kind": kind, "text": text, "evidence": evidence_ids}
    if action:
        item["action"] = action
    return item


def lenses(e: dict[str, Any]) -> dict[str, dict[str, Any]]:
    p = e["portfolio"]
    return {
        "CEO": {"question": "Are we solving important problems and moving toward a durable business?", "scorecard": {"Customer-Zero validated products": "UNKNOWN", "Externally validated products": 0, "Paying products": "UNKNOWN", "Founder decisions pending": 3}, "claims": [claim("FACT", "The portfolio snapshot is historical inventory-heavy: 12 Apple products but 0 working products.", ["portfolio.apple_products", "portfolio.working"]), claim("INFERENCE", "Strategy is not currently expressed as a coherent active product portfolio.", ["portfolio.working", "portfolio.shelved"]), claim("UNKNOWN", "Which commercial direction deserves sustained founder attention.", ["customer.external_validation"]), claim("RECOMMENDATION", "Choose one founder-approved customer/economic validation lane before more product expansion.", ["portfolio.working", "customer.external_validation"], "Founder decision required.")]},
        "CFO": {"question": "Are we getting closer to sustainable profitability?", "scorecard": {"Revenue": "UNKNOWN", "Operating cost": "UNKNOWN", "AI/API cost": "UNKNOWN", "Recorded factory telemetry": "$0.42", "Known unit economics": "UNKNOWN"}, "claims": [claim("FACT", "The available ledger records $0.42 of factory telemetry cost, not company operating cost.", ["economics.factory_telemetry"]), claim("UNKNOWN", "Revenue, contribution margin, and product-level economics are not recorded.", ["economics.revenue", "economics.contribution_margin"]), claim("RECOMMENDATION", "Do not authorize material product investment without a cheap experiment with a cost ceiling and a measurable payment or repeat-use outcome.", ["economics.revenue", "customer.education_payment"], "Set the ceiling before execution.")]},
        "CPO": {"question": "Are we building the right things for real customer problems?", "scorecard": {"Customer-Zero tested": 2, "Repeated voluntary usage": "UNKNOWN", "External problem validation": 0, "Paying users": "UNKNOWN", "Largest product uncertainty": "observed repeat value and payment"}, "claims": [claim("FACT", "Customer Zero direction records exist for Product A, Vorynce, and an unverified modeled intent compiler.", ["customer.customer_zero_records"]), claim("FACT", "Education hypotheses explicitly have absent direct customer and payment evidence.", ["customer.education_external_validation", "customer.education_payment"]), claim("INFERENCE", "The highest-value next product learning is behavioral validation, not another feature.", ["customer.external_validation", "portfolio.ready_for_review"]), claim("RECOMMENDATION", "Run the cheapest founder-approved real-user experiment and record repeat or payment behavior.", ["customer.education_external_validation"], "Founder approval and human participants required.")]},
        "CTO": {"question": "Are we building and operating these things well without over-engineering?", "scorecard": {"Build health": "VERIFIED for factory snapshot", "Release failures": "UNKNOWN", "Security findings": "PARTIALLY VERIFIED", "Reuse opportunities": "EVIDENCE EXISTS", "Maintenance burden": "UNKNOWN"}, "claims": [claim("EVIDENCE", "The release board records factory verification passing and a blocked Apple release lane.", ["factory.verification", "portfolio.blocked"]), claim("FACT", "Passing tests and archives do not establish customer value or release readiness.", ["factory.verification", "portfolio.ready_for_review"]), claim("INFERENCE", "Additional architecture or council infrastructure is not justified before customer evidence.", ["portfolio.ready_for_review", "customer.external_validation"]), claim("RECOMMENDATION", "Keep the council as a generated artifact and validator; defer services, schedulers, extra agents, and extraction.", ["factory.verification"], "Reassess only after repeated founder use.")]},
        "COO": {"question": "Is the factory turning decisions into verified outcomes efficiently?", "scorecard": {"Cycle time": "UNKNOWN", "Useful contributions completed": "UNKNOWN", "Release frequency": "UNKNOWN", "Blocked work": 1, "Avoidable human escalations": "UNKNOWN", "Repeated factory failures": "UNKNOWN"}, "claims": [claim("FACT", "The current release board has 0 Ready for Review, 1 blocked, and 11 shelved Apple products.", ["portfolio.ready_for_review", "portfolio.blocked", "portfolio.shelved"]), claim("INFERENCE", "The visible bottleneck is decision-to-validated-outcome flow, not lack of portfolio inventory.", ["portfolio.ready_for_review", "portfolio.candidates"]), claim("UNKNOWN", "The causal operational bottleneck cannot be proven from the current snapshot alone.", ["factory.verification"]), claim("RECOMMENDATION", "Stop broad portfolio expansion and measure one bounded validation lane from decision to observed outcome.", ["portfolio.ready_for_review", "customer.external_validation"], "Define one cycle-time observation.")]},
    }


def review() -> dict[str, Any]:
    e = evidence()
    l = lenses(e)
    return {
        "schema_version": 1,
        "review_id": f"executive-council-{date.today().isoformat()}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority": {"founder_is_final_authority": True, "operational_authority": "OBSERVE_ANALYZE_CHALLENGE_RECOMMEND_LEARN", "external_release": "HUMAN_ONLY"},
        "evidence": e,
        "lenses": l,
        "disagreements": [
            {"topic": "next investment", "positions": {"CEO": "select one coherent customer/economic lane", "CFO": "only below a cost ceiling with measurable economic learning", "CPO": "run behavioral validation before features", "CTO": "defer extraction and new infrastructure", "COO": "measure one decision-to-outcome lane"}, "material": True, "synthesis": "Run one bounded validation experiment; do not expand the portfolio or council platform."}
        ],
        "synthesis": {"kind": "RECOMMENDATION", "text": "Preserve the current portfolio as evidence, reconcile lifecycle conflicts, and run one cheap founder-approved customer/economic validation experiment before new product or council infrastructure work.", "rationale": ["0 Ready for Review", "no recorded external payment or retention evidence", "unknown company economics", "unresolved lifecycle conflict"], "founder_authority_required": True},
        "today": [
            {"id": "today-1", "action": "Founder selects one validation lane and a reversible cost/time ceiling.", "authority": "FOUNDER", "status": "PENDING"},
            {"id": "today-2", "action": "Reconcile Product A and Vorynce lifecycle/authorization records before any release or revival work.", "authority": "FOUNDER", "status": "PENDING"},
            {"id": "today-3", "action": "Use this generated review once and record whether it changed a decision or reduced cognitive load.", "authority": "FOUNDER", "status": "PENDING"},
        ],
        "stop_defer": ["Do not reactivate shelved Apple products.", "Defer extra council agents, services, schedulers, news feeds, and composite scores.", "Defer product features without observed customer behavior or an approved experiment."],
        "human_decisions": ["Select and authorize one validation lane.", "Resolve lifecycle and release authority conflicts.", "Approve any spending, external contact, release, publication, or product mutation."],
        "recommendation_tracking": [{"id": "rec-2026-09-19-01", "recommendation": "Run one bounded customer/economic validation experiment.", "evidence_at_time": ["portfolio.ready_for_review", "customer.education_payment", "economics.revenue"], "expected_outcome": "Reduce customer and economic uncertainty at low reversible cost.", "founder_decision": "UNKNOWN", "action_taken": "NOT_RECORDED", "actual_outcome": "UNKNOWN"}],
        "customer_zero": {"opened": "UNKNOWN", "affected_decision": "UNKNOWN", "caught_missed_fact": "UNKNOWN", "prevented_work": "UNKNOWN", "saved_founder_time": "UNKNOWN", "reduced_cognitive_load": "UNKNOWN", "created_cognitive_load": "UNKNOWN", "redundant_sections": "UNKNOWN", "continuation_test": "Founder voluntarily uses the review repeatedly and records decision value."},
        "practice_changes": [],
    }


def validate(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if tuple(payload.get("lenses", {})) != LENSES:
        errors.append("review must contain exactly the five lenses in CEO,CFO,CPO,CTO,COO order")
    if len(payload.get("today", [])) > 5:
        errors.append("today must contain no more than five actions")
    if re.search(r"(?:company|business|overall)\s+health\s*(?:score)?\s*(?:[:=]|is)\s*\d+", json.dumps(payload), re.IGNORECASE):
        errors.append("composite health scores are not allowed")
    for lens, data in payload.get("lenses", {}).items():
        if not data.get("question") or not data.get("scorecard"):
            errors.append(f"{lens}: question and scorecard are required")
        for item in data.get("claims", []):
            if item.get("kind") not in ALLOWED_CLASSES:
                errors.append(f"{lens}: invalid claim class")
            if not item.get("evidence"):
                errors.append(f"{lens}: claim missing evidence references")
    for conflict in payload.get("evidence", {}).get("conflicts", []):
        if conflict.get("status") not in {"BLOCKED_UNRESOLVED_SOURCE_CONFLICT", "RESOLVED"}:
            errors.append("conflicts require explicit unresolved or resolved status")
    for rec in payload.get("recommendation_tracking", []):
        for field in ("recommendation", "evidence_at_time", "expected_outcome", "founder_decision", "action_taken", "actual_outcome"):
            if field not in rec:
                errors.append(f"recommendation missing {field}")
    return errors


def render(payload: dict[str, Any]) -> str:
    e = payload["evidence"]
    p = e["portfolio"]
    def val(section: str, key: str) -> Any:
        return e[section][key]["value"]
    lines = ["# FOCULOOM - DAILY EXECUTIVE REVIEW", "", f"Date: {payload['review_id'][-10:]}", "", "## CUSTOMER", f"- Portfolio evidence: {val('portfolio', 'apple_products')} Apple inventory entries; {val('portfolio', 'working')} working in the release snapshot.", f"- Customer Zero records: {val('customer', 'customer_zero_records')}; external behavior: UNKNOWN.", "- Education customer and payment evidence: ABSENT.", "", "## ECONOMICS", "- Revenue: UNKNOWN.", "- Contribution margin: UNKNOWN.", "- Company operating cost: UNKNOWN.", f"- Recorded factory telemetry: ${val('economics', 'factory_telemetry')['recorded_factory_cost_usd']:.2f}; this is not company operating cost.", "", "## PRODUCT", "- 0 Ready for Review; do not treat tests, archives, or features as customer value.", "- Next product learning should be observed behavior, repeat use, or payment.", "", "## FACTORY", f"- {val('portfolio', 'blocked')} blocked and {val('portfolio', 'shelved')} shelved Apple entries; useful outcome throughput is UNKNOWN.", "- Factory verification is evidenced; causal operational bottleneck remains UNKNOWN.", "", "## OPPORTUNITIES", "- One cheap, reversible founder-approved customer/economic validation experiment.", "", "## EXECUTIVE DISAGREEMENTS", "- All five lenses converge on bounded validation, but differ on emphasis: strategy, cost ceiling, behavior, architecture restraint, and cycle-time measurement.", "", "## CEO SYNTHESIS", f"- {payload['synthesis']['text']}", "", "## TODAY", *[f"- {item['action']}" for item in payload["today"]], "", "## STOP / DEFER", *[f"- {item}" for item in payload["stop_defer"]], "", "## HUMAN DECISIONS", *[f"- {item}" for item in payload["human_decisions"]], "", "## COUNCIL SELF-EVALUATION", "- Continue only if repeated founder use shows a decision improved, unnecessary work stopped, an opportunity surfaced, cost reduced, or cognitive load reduced.", "- Remove sections the founder repeatedly ignores or finds redundant.", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("generate", "validate", "render"))
    parser.add_argument("--input", type=Path)
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    path = args.input or OUT / f"{date.today().isoformat()}.json"
    if args.command == "generate":
        path.write_text(json.dumps(review(), indent=2) + "\n", encoding="utf-8")
        print(path)
        return 0
    payload = load(path)
    errors = validate(payload)
    if args.command == "validate":
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        print("executive council review validation passed")
        return 0
    output = path.with_suffix(".md")
    output.write_text(render(payload), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
