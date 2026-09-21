#!/usr/bin/env python3
"""Render a bounded contribution card from a verified local evidence record."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


def build_card(opportunity: dict, constraints: dict, today: date | None = None) -> dict:
    """Return a card or an explicit abstention; this function never retrieves or writes."""
    today = today or date.today()
    required = (
        "stable_id", "title", "responsible_project", "canonical_source", "supporting_passage",
        "retrieval_date", "verification_date", "status", "contribution_requested",
        "acceptance_route", "prerequisites", "relevant_skills", "estimated_effort",
        "deliverable", "smallest_reversible_step", "risk_pathway", "benefit_mechanism",
        "mechanism_assumptions", "counterevidence", "uncertainties", "downsides",
        "recipient_burden", "expiry_rule", "wanted_evidence", "source_verified", "expiry_date",
        "competing_work",
    )
    missing = [field for field in required if field not in opportunity]
    if missing:
        return {"decision": "ABSTAIN", "reasons": [f"missing evidence fields: {', '.join(missing)}"]}
    if not opportunity["source_verified"]:
        return {"decision": "ABSTAIN", "reasons": ["canonical source is not directly verified"]}
    if opportunity["status"] != "open":
        return {"decision": "ABSTAIN", "reasons": [f"opportunity status is {opportunity['status']}"]}
    if not opportunity["wanted_evidence"]:
        return {"decision": "ABSTAIN", "reasons": ["current maintainer-want evidence is absent"]}
    if opportunity["competing_work"]:
        return {"decision": "ABSTAIN", "reasons": ["competing work is already open for this opportunity"]}
    if opportunity["expiry_date"] < today.isoformat():
        return {"decision": "ABSTAIN", "reasons": ["opportunity verification has expired"]}

    required_skills = set(opportunity["relevant_skills"])
    supplied_skills = set(constraints.get("skills", []))
    missing_skills = sorted(required_skills - supplied_skills)
    available_hours = constraints.get("available_hours")
    effort_hours = opportunity["estimated_effort"]["hours"]
    reasons = []
    if missing_skills:
        reasons.append(f"missing stated skills: {', '.join(missing_skills)}")
    if available_hours is not None and available_hours < effort_hours:
        reasons.append(f"available time ({available_hours}h) is below estimate ({effort_hours}h)")
    if reasons:
        return {"decision": "ABSTAIN", "reasons": reasons}

    return {
        "decision": "CARD",
        "stable_id": opportunity["stable_id"],
        "what_could_i_do": opportunity["contribution_requested"],
        "why_it_fits": {"skills": sorted(supplied_skills & required_skills), "estimated_effort": opportunity["estimated_effort"]},
        "why_it_might_help": opportunity["benefit_mechanism"],
        "evidence": {
            "source": opportunity["canonical_source"],
            "passage": opportunity["supporting_passage"],
            "retrieved": opportunity["retrieval_date"],
            "verified": opportunity["verification_date"],
        },
        "epistemic_status": {
            "observed": opportunity["observed"],
            "organization_claim": opportunity["organization_claim"],
            "our_inference": opportunity["our_inference"],
            "unknown": opportunity["uncertainties"],
        },
        "wanted_now": opportunity["wanted_evidence"],
        "counterfactual": "UNKNOWN: whether this contribution would happen without this user.",
        "recipient_burden": opportunity["recipient_burden"],
        "smallest_reversible_step": opportunity["smallest_reversible_step"],
        "useful_completed_result": opportunity["deliverable"],
        "expiry": opportunity["expiry_rule"],
        "sources": [opportunity["canonical_source"]],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("opportunity", type=Path)
    parser.add_argument("--skills", nargs="*", default=[])
    parser.add_argument("--hours", type=float)
    args = parser.parse_args()
    result = build_card(json.loads(args.opportunity.read_text(encoding="utf-8")), {"skills": args.skills, "available_hours": args.hours})
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
