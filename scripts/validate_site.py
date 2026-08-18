#!/usr/bin/env python3
"""Validate the static report without changing repository files."""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


class ReportParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.hrefs: list[str] = []
        self.mermaid_nodes = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        if tag == "a" and values.get("href"):
            self.hrefs.append(values["href"] or "")
        classes = (values.get("class") or "").split()
        if "mermaid" in classes:
            self.mermaid_nodes += 1


def local_target(href: str) -> Path | None:
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc or href.startswith(("mailto:", "javascript:", "/")):
        return None
    path = unquote(parsed.path)
    if not path:
        return INDEX
    target = (ROOT / path).resolve()
    try:
        target.relative_to(ROOT)
    except ValueError:
        raise ValueError(f"Link escapes repository root: {href}") from None
    if target.is_dir():
        target = target / "index.html"
    return target


def main() -> int:
    failures: list[str] = []
    if not INDEX.is_file():
        print("Missing index.html", file=sys.stderr)
        return 1

    parser = ReportParser()
    try:
        parser.feed(INDEX.read_text(encoding="utf-8"))
        parser.close()
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Unable to parse index.html: {error}", file=sys.stderr)
        return 1

    for href in parser.hrefs:
        parsed = urlsplit(href)
        try:
            target = local_target(href)
        except ValueError as error:
            failures.append(str(error))
            continue
        if target is not None and not target.is_file():
            failures.append(f"Missing local target: {href}")
        if parsed.fragment and target == INDEX and unquote(parsed.fragment) not in parser.ids:
            failures.append(f"Missing index anchor: #{parsed.fragment}")

    if parser.mermaid_nodes == 0:
        failures.append("No Mermaid source blocks found")
    if not (ROOT / ".nojekyll").is_file():
        failures.append("Missing .nojekyll")

    if failures:
        print("Static report validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    local_links = sum(local_target(href) is not None for href in parser.hrefs)
    print(
        f"Validated index.html: {len(parser.ids)} anchors, "
        f"{local_links} local links, {parser.mermaid_nodes} Mermaid blocks."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
