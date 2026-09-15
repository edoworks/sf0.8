#!/usr/bin/env python3
"""Fail closed on basic public URL, placeholder, and canonical-link defects."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
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


def audit(url: str, expected_canonical: str | None, timeout: float, check_links: bool) -> dict:
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
    parser.add_argument("urls", nargs="+", help="public URLs to audit")
    parser.add_argument("--expected-canonical", help="canonical URL required on every page")
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--skip-links", action="store_true", help="skip outbound link requests")
    parser.add_argument("--json", action="store_true", help="emit machine-readable output")
    args = parser.parse_args()
    results = [audit(url, args.expected_canonical, args.timeout, not args.skip_links) for url in args.urls]
    if args.json:
        print(json.dumps(results, indent=2, sort_keys=True))
    else:
        for result in results:
            print(f"{result['status']}: {result['url']}")
            for error in result["errors"]:
                print(f"  ERROR: {error}")
    return 0 if all(result["status"] == "pass" for result in results) else 1


if __name__ == "__main__":
    sys.exit(main())
