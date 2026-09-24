#!/usr/bin/env python3
"""Fail closed on basic public URL, placeholder, and canonical-link defects."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
import os
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin, urlparse
from urllib.request import Request, urlopen


PLACEHOLDER_RE = re.compile(
    r"\[(?:[A-Z][A-Z0-9_]*_(?:URL|LINK)|TODO|TBD)\]|"
    r"(?:https?://)?(?:example\.com|your-domain\.com)|"
    r"\blorem ipsum\b",
    re.IGNORECASE,
)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.canonicals: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")
        if tag == "link" and values.get("rel", "").lower() == "canonical" and values.get("href"):
            self.canonicals.append(values["href"] or "")


def fetch(url: str, timeout: float) -> tuple[int, str, str]:
    request = Request(url, headers={"User-Agent": "edoworks-public-surface-preflight/1"})
    with urlopen(request, timeout=timeout) as response:
        return response.status, response.geturl(), response.read().decode("utf-8", "replace")


def fetch_json(url: str, timeout: float) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "edoworks-public-surface-preflight/1",
    }
    if token := os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    request = Request(
        url,
        headers=headers,
    )
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def github_metadata(repo: str, timeout: float, expected: dict | None = None) -> dict:
    if "/" not in repo or repo.startswith("/") or repo.endswith("/"):
        raise ValueError(f"invalid GitHub repository: {repo}")
    data = fetch_json(f"https://api.github.com/repos/{repo}", timeout)
    errors = []
    if data.get("visibility") != "public":
        errors.append(f"repository is not public: {data.get('visibility', 'unknown')}")
    license_id = (data.get("license") or {}).get("spdx_id")
    if not data.get("license") and not (expected or {}).get("allow_missing_license"):
        errors.append("repository has no detected license")
    actual = {
        "description": data.get("description"),
        "homepage": data.get("homepage") or None,
        "archived": bool(data.get("archived")),
        "fork": bool(data.get("fork")),
        "visibility": data.get("visibility"),
        "license": license_id,
        "default_branch": data.get("default_branch"),
    }
    for field in (
        "description",
        "homepage",
        "archived",
        "fork",
        "visibility",
        "license",
        "default_branch",
    ):
        if expected is not None and field in expected and actual[field] != expected[field]:
            errors.append(
                f"{field} mismatch: expected {expected[field]!r}, observed {actual[field]!r}"
            )
    return {
        "repo": repo,
        "html_url": data.get("html_url"),
        **actual,
        "errors": errors,
        "status": "pass" if not errors else "blocked",
    }


def github_tag_target(repo: str, tag: str, timeout: float) -> str | None:
    encoded_tag = quote(tag, safe="")
    tag_ref = fetch_json(
        f"https://api.github.com/repos/{repo}/git/ref/tags/{encoded_tag}",
        timeout,
    ).get("object", {})
    if tag_ref.get("type") == "tag":
        tag_ref = fetch_json(
            f"https://api.github.com/repos/{repo}/git/tags/{tag_ref.get('sha', '')}",
            timeout,
        ).get("object", {})
    return tag_ref.get("sha")


def github_release(repo: str, tag: str, timeout: float, expected: dict | None = None) -> dict:
    data = fetch_json(f"https://api.github.com/repos/{repo}/releases/tags/{tag}", timeout)
    errors = []
    if data.get("draft"):
        errors.append("release is a draft")
    if data.get("prerelease") and not (
        expected is not None and expected.get("prerelease") is True
    ):
        errors.append("release is a prerelease")
    actual = {
        "draft": bool(data.get("draft")),
        "prerelease": bool(data.get("prerelease")),
        "immutable": bool(data.get("immutable")),
        "asset_names": sorted(asset.get("name") for asset in data.get("assets", [])),
        "asset_digests": {
            asset.get("name"): asset.get("digest")
            for asset in data.get("assets", [])
            if asset.get("name") and asset.get("digest")
        },
    }
    actual["asset_count"] = len(actual["asset_names"])
    for field in (
        "draft",
        "prerelease",
        "immutable",
        "asset_count",
        "asset_names",
        "asset_digests",
    ):
        if expected is not None and field in expected and actual[field] != expected[field]:
            errors.append(
                f"{field} mismatch: expected {expected[field]!r}, observed {actual[field]!r}"
            )
    if expected is not None and "tag_target_commit" in expected:
        actual["tag_target_commit"] = github_tag_target(repo, tag, timeout)
        if actual["tag_target_commit"] != expected["tag_target_commit"]:
            errors.append(
                "tag_target_commit mismatch: expected "
                f"{expected['tag_target_commit']!r}, observed {actual['tag_target_commit']!r}"
            )
    if expected is not None and expected.get("distribution_url"):
        try:
            status, final_url, _ = fetch(expected["distribution_url"], timeout)
            actual["distribution_url"] = expected["distribution_url"]
            actual["distribution_final_url"] = final_url
            if status >= 400:
                errors.append(f"distribution URL returned HTTP {status}")
        except (HTTPError, URLError, TimeoutError, ValueError) as error:
            errors.append(f"distribution URL unavailable: {error}")
    if expected is not None and expected.get("documentation_url"):
        try:
            status, _, body = fetch(expected["documentation_url"], timeout)
            actual["documentation_url"] = expected["documentation_url"]
            if status >= 400:
                errors.append(f"documentation URL returned HTTP {status}")
            for required_text in expected.get("documentation_contains", []):
                if required_text not in body:
                    errors.append(f"documentation text missing: {required_text}")
        except (HTTPError, URLError, TimeoutError, ValueError) as error:
            errors.append(f"documentation URL unavailable: {error}")
    return {
        "repo": repo,
        "tag": tag,
        "html_url": data.get("html_url"),
        **actual,
        "errors": errors,
        "status": "pass" if not errors else "blocked",
    }


def validate_github_contract(contract: dict) -> list[str]:
    errors: list[str] = []
    required = {
        "schema_version",
        "completion_status",
        "declared_repository_blockers",
        "repositories",
        "releases",
    }
    if set(contract) != required:
        errors.append("contract fields drifted")
    if contract.get("schema_version") != 1:
        errors.append("contract schema_version must be 1")
    if contract.get("completion_status") not in {"IN_PROGRESS", "COMPLETE"}:
        errors.append("contract completion_status is invalid")
    repositories = contract.get("repositories")
    releases = contract.get("releases")
    blockers = contract.get("declared_repository_blockers")
    if not isinstance(repositories, list) or not repositories:
        errors.append("contract repositories must be a non-empty list")
        repositories = []
    if not isinstance(releases, list) or not releases:
        errors.append("contract releases must be a non-empty list")
        releases = []
    if not isinstance(blockers, dict):
        errors.append("declared_repository_blockers must be an object")
        blockers = {}
    repo_ids = [item.get("repo") for item in repositories if isinstance(item, dict)]
    release_ids = [
        (item.get("repo"), item.get("tag"))
        for item in releases
        if isinstance(item, dict)
    ]
    if len(repo_ids) != len(set(repo_ids)) or any(not item for item in repo_ids):
        errors.append("contract repository ids must be non-empty and unique")
    if len(release_ids) != len(set(release_ids)) or any(not all(item) for item in release_ids):
        errors.append("contract release ids must be non-empty and unique")
    repository_required = {
        "repo",
        "description",
        "homepage",
        "archived",
        "fork",
        "visibility",
        "license",
        "default_branch",
    }
    for index, repository in enumerate(repositories):
        if not isinstance(repository, dict):
            errors.append(f"contract repositories[{index}] must be an object")
            continue
        allowed = repository_required | {"allow_missing_license", "license_policy"}
        if not repository_required.issubset(repository) or not set(repository).issubset(allowed):
            errors.append(f"contract repositories[{index}] fields drifted")
        if not isinstance(repository.get("description"), str) or not repository.get("description"):
            errors.append(f"contract repositories[{index}] description is invalid")
        if repository.get("homepage") is not None and not isinstance(repository.get("homepage"), str):
            errors.append(f"contract repositories[{index}] homepage is invalid")
        if type(repository.get("archived")) is not bool or type(repository.get("fork")) is not bool:
            errors.append(f"contract repositories[{index}] lifecycle flags are invalid")
        if repository.get("visibility") != "public":
            errors.append(f"contract repositories[{index}] visibility is invalid")
        if repository.get("license") is not None and not isinstance(repository.get("license"), str):
            errors.append(f"contract repositories[{index}] license is invalid")
        if not isinstance(repository.get("default_branch"), str) or not repository.get("default_branch"):
            errors.append(f"contract repositories[{index}] default branch is invalid")
        if repository.get("license") is None and not (
            repository.get("allow_missing_license") is True
            and isinstance(repository.get("license_policy"), str)
            and repository.get("license_policy")
        ):
            errors.append(f"contract repositories[{index}] lacks missing-license policy")
    release_required = {
        "repo",
        "tag",
        "draft",
        "prerelease",
        "immutable",
        "asset_count",
        "asset_names",
        "tag_target_commit",
    }
    release_optional = {
        "asset_digests",
        "distribution_url",
        "documentation_url",
        "documentation_contains",
    }
    for index, release in enumerate(releases):
        if not isinstance(release, dict):
            errors.append(f"contract releases[{index}] must be an object")
            continue
        if not release_required.issubset(release) or not set(release).issubset(
            release_required | release_optional
        ):
            errors.append(f"contract releases[{index}] fields drifted")
        if any(type(release.get(field)) is not bool for field in ("draft", "prerelease", "immutable")):
            errors.append(f"contract releases[{index}] release flags are invalid")
        asset_count = release.get("asset_count")
        asset_names = release.get("asset_names")
        asset_digests = release.get("asset_digests")
        if type(asset_count) is not int or not isinstance(asset_names, list) or not all(
            isinstance(name, str) and name for name in asset_names
        ):
            errors.append(f"contract releases[{index}] asset inventory is invalid")
        elif asset_count != len(asset_names):
            errors.append(f"contract releases[{index}] asset count disagrees with names")
        if asset_count and (
            not isinstance(asset_digests, dict)
            or set(asset_digests) != set(asset_names)
            or not all(
                re.fullmatch(r"sha256:[0-9a-f]{64}", str(value))
                for value in asset_digests.values()
            )
        ):
            errors.append(f"contract releases[{index}] asset digests are incomplete")
        if not re.fullmatch(r"[0-9a-f]{40}", str(release.get("tag_target_commit", ""))):
            errors.append(f"contract releases[{index}] tag target is invalid")
        if "distribution_url" in release and not isinstance(release["distribution_url"], str):
            errors.append(f"contract releases[{index}] distribution URL is invalid")
        if "documentation_url" in release and not isinstance(release["documentation_url"], str):
            errors.append(f"contract releases[{index}] documentation URL is invalid")
        if "documentation_contains" in release and (
            not isinstance(release["documentation_contains"], list)
            or not release["documentation_contains"]
            or not all(isinstance(item, str) and item for item in release["documentation_contains"])
        ):
            errors.append(f"contract releases[{index}] documentation assertions are invalid")
    if not set(blockers).issubset(set(repo_ids)) or not all(
        isinstance(value, list) and value and all(isinstance(item, str) for item in value)
        for value in blockers.values()
    ):
        errors.append("declared blockers must map contract repositories to exact errors")
    if contract.get("completion_status") == "COMPLETE" and blockers:
        errors.append("complete contract cannot declare blockers")
    return errors


def pypi_metadata(package: str, timeout: float) -> dict:
    data = fetch_json(f"https://pypi.org/pypi/{package}/json", timeout)
    info = data.get("info", {})
    errors = []
    if not info.get("version"):
        errors.append("package has no current version")
    has_license = bool(
        info.get("license")
        or info.get("license_expression")
        or info.get("license_files")
        or any("License ::" in item for item in info.get("classifiers", []))
    )
    if not has_license:
        errors.append("package has no declared license")
    return {
        "package": package,
        "version": info.get("version"),
        "license": info.get("license"),
        "home_page": info.get("home_page"),
        "errors": errors,
        "status": "pass" if not errors else "blocked",
    }


def check_link(base: str, href: str, timeout: float) -> str | None:
    if href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return None
    target = urljoin(base, href)
    try:
        status, _, _ = fetch(target, timeout)
    except (HTTPError, URLError, TimeoutError, ValueError) as error:
        return f"broken link {target}: {error}"
    if status >= 400:
        return f"broken link {target}: HTTP {status}"
    return None


def audit(
    url: str,
    expected_canonical: str | None,
    required_text: list[str],
    forbidden_text: list[str],
    timeout: float,
    check_links: bool,
) -> dict:
    result: dict = {"url": url, "errors": [], "warnings": [], "status": "blocked"}
    try:
        status, final_url, body = fetch(url, timeout)
    except (HTTPError, URLError, TimeoutError, ValueError) as error:
        result["errors"].append(f"unreachable: {error}")
        return result

    result["http_status"] = status
    result["final_url"] = final_url
    if status >= 400:
        result["errors"].append(f"HTTP {status}")

    placeholders = sorted(set(PLACEHOLDER_RE.findall(body)))
    if placeholders:
        result["errors"].append(f"placeholder content: {placeholders}")
    for text in required_text:
        if text not in body:
            result["errors"].append(f"required lifecycle/status text missing: {text}")
    for text in forbidden_text:
        if text in body:
            result["errors"].append(f"forbidden lifecycle/status text present: {text}")

    parser = PageParser()
    parser.feed(body)
    canonicals = [urljoin(final_url, item) for item in parser.canonicals]
    result["canonical_urls"] = canonicals
    if expected_canonical and expected_canonical not in canonicals:
        result["errors"].append(
            f"expected canonical missing: {expected_canonical} (found {canonicals or 'none'})"
        )

    if check_links:
        for href in sorted(set(parser.links)):
            error = check_link(final_url, href, timeout)
            if error:
                result["errors"].append(error)

    result["status"] = "pass" if not result["errors"] else "blocked"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("urls", nargs="*", help="public URLs to audit")
    parser.add_argument("--expected-canonical", help="canonical URL required on every page")
    parser.add_argument("--require-text", action="append", default=[], help="visible text required on every page")
    parser.add_argument("--forbid-text", action="append", default=[], help="visible text forbidden on every page")
    parser.add_argument("--github-repo", action="append", default=[], help="public OWNER/REPO metadata to validate")
    parser.add_argument(
        "--github-release",
        action="append",
        nargs=2,
        metavar=("OWNER/REPO", "TAG"),
        default=[],
        help="stable GitHub release metadata to validate",
    )
    parser.add_argument("--pypi-package", action="append", default=[], help="PyPI package metadata to validate")
    parser.add_argument(
        "--github-contract",
        help="JSON contract with exact repository and release metadata expectations",
    )
    parser.add_argument(
        "--allow-declared-blockers",
        action="store_true",
        help="pass only when live blockers exactly match an IN_PROGRESS contract",
    )
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--skip-links", action="store_true", help="skip outbound link requests")
    parser.add_argument("--json", action="store_true", help="emit machine-readable output")
    args = parser.parse_args()
    if not any(
        (
            args.urls,
            args.github_repo,
            args.github_release,
            args.pypi_package,
            args.github_contract,
        )
    ):
        parser.error("provide at least one URL, metadata target, release, package, or contract")
    results = [
        audit(
            url,
            args.expected_canonical,
            args.require_text,
            args.forbid_text,
            args.timeout,
            not args.skip_links,
        )
        for url in args.urls
    ]
    metadata = []
    for repo in args.github_repo:
        try:
            metadata.append(github_metadata(repo, args.timeout))
        except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as error:
            metadata.append({"repo": repo, "errors": [f"metadata unavailable: {error}"], "status": "blocked"})
    contract = {"repositories": [], "releases": []}
    contract_errors = []
    if args.github_contract:
        try:
            with open(args.github_contract, encoding="utf-8") as contract_file:
                contract = json.load(contract_file)
            contract_errors = validate_github_contract(contract)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            metadata.append(
                {
                    "repo": "github-contract",
                    "errors": [f"contract unavailable: {error}"],
                    "status": "blocked",
                }
            )
        if contract_errors:
            metadata.append(
                {
                    "repo": "github-contract",
                    "errors": contract_errors,
                    "status": "blocked",
                }
            )
        for expectation in contract.get("repositories", []) if not contract_errors else []:
            repo = expectation.get("repo", "")
            try:
                metadata.append(github_metadata(repo, args.timeout, expectation))
            except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as error:
                metadata.append(
                    {"repo": repo, "errors": [f"metadata unavailable: {error}"], "status": "blocked"}
                )
    releases = []
    for repo, tag in args.github_release:
        try:
            releases.append(github_release(repo, tag, args.timeout))
        except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as error:
            releases.append({"repo": repo, "tag": tag, "errors": [f"release unavailable: {error}"], "status": "blocked"})
    for expectation in contract.get("releases", []) if not contract_errors else []:
        repo = expectation.get("repo", "")
        tag = expectation.get("tag", "")
        try:
            releases.append(github_release(repo, tag, args.timeout, expectation))
        except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as error:
            releases.append(
                {
                    "repo": repo,
                    "tag": tag,
                    "errors": [f"release unavailable: {error}"],
                    "status": "blocked",
                }
            )
    packages = []
    for package in args.pypi_package:
        try:
            packages.append(pypi_metadata(package, args.timeout))
        except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as error:
            packages.append({"package": package, "errors": [f"package unavailable: {error}"], "status": "blocked"})
    if args.json:
        print(json.dumps({"pages": results, "github_repositories": metadata, "github_releases": releases, "pypi_packages": packages}, indent=2, sort_keys=True))
    else:
        for result in results:
            print(f"{result['status']}: {result['url']}")
            for error in result["errors"]:
                print(f"  ERROR: {error}")
        for item in metadata:
            print(f"{item['status']}: github.com/{item['repo']}")
            for error in item["errors"]:
                print(f"  ERROR: {error}")
        for item in releases:
            print(f"{item['status']}: github.com/{item['repo']}/releases/tag/{item['tag']}")
            for error in item["errors"]:
                print(f"  ERROR: {error}")
        for item in packages:
            print(f"{item['status']}: pypi.org/project/{item['package']}")
            for error in item["errors"]:
                print(f"  ERROR: {error}")
    checks = results + metadata + releases + packages
    if args.allow_declared_blockers and args.github_contract and not contract_errors:
        actual_blockers = {
            item["repo"]: item.get("errors", [])
            for item in metadata
            if item.get("status") == "blocked" and item.get("repo") != "github-contract"
        }
        declared_blockers = contract["declared_repository_blockers"]
        non_repository_failures = results + releases + packages
        blockers_match_status = (
            contract["completion_status"] == "IN_PROGRESS"
            and actual_blockers == declared_blockers
        ) or (
            contract["completion_status"] == "COMPLETE"
            and not actual_blockers
            and not declared_blockers
        )
        return 0 if (
            blockers_match_status
            and all(item["status"] == "pass" for item in non_repository_failures)
        ) else 1
    return 0 if all(item["status"] == "pass" for item in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
