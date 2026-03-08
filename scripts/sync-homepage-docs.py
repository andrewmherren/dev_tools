#!/usr/bin/env python3
"""Publish selected canonical docs into homepage/guides for nginx serving."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import TypedDict

COPIER_GUIDE = "copier-guide.md"
SYNC_COMMAND = "python scripts/sync-homepage-docs.py"


class DocumentSpec(TypedDict):
    source: str
    destination: str
    rewrite: dict[str, str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync canonical docs into homepage/guides"
    )
    parser.add_argument(
        "--quiet", action="store_true", help="Suppress per-file status output"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    public_docs_dir = repo_root / "homepage" / "guides"

    documents: list[DocumentSpec] = [
        {
            "source": "README.md",
            "destination": "server-guide.md",
            "rewrite": {
                "template/README.md": f"guides/{COPIER_GUIDE}",
                "homepage/PROJECT_SETUP.md": "guides/project-integration.md",
                "docs/git-safety.md": "guides/git-safety.md",
                "docs/mcp-policy.md": "guides/mcp-policy.md",
                "homepage/README.md": "guides/server-guide.md",
            },
        },
        {
            "source": "template/README.md",
            "destination": COPIER_GUIDE,
            "rewrite": {
                "../template/README.md": f"guides/{COPIER_GUIDE}",
            },
        },
        {
            "source": "homepage/PROJECT_SETUP.md",
            "destination": "project-integration.md",
            "rewrite": {
                "../template/README.md": f"guides/{COPIER_GUIDE}",
            },
        },
        {
            "source": "docs/git-safety.md",
            "destination": "git-safety.md",
            "rewrite": {},
        },
        {
            "source": "docs/mcp-policy.md",
            "destination": "mcp-policy.md",
            "rewrite": {},
        },
    ]

    public_docs_dir.mkdir(parents=True, exist_ok=True)

    for doc in documents:
        source_path = repo_root / doc["source"]
        destination_path = public_docs_dir / doc["destination"]

        if not source_path.exists():
            message = f"Source document not found: {source_path}"
            raise FileNotFoundError(message)

        content = source_path.read_text(encoding="utf-8")
        for old_text, new_text in doc["rewrite"].items():
            content = content.replace(old_text, new_text)

        # Guard against accidental double-prefixing.
        content = content.replace("guides/guides/", "guides/")

        header = "\n".join(
            [
                "<!--",
                f"Generated file. Source: {doc['source']}",
                f"Update source docs, then run: {SYNC_COMMAND}",
                "-->",
                "",
            ]
        )

        destination_path.write_text(header + content, encoding="utf-8")

        if not args.quiet:
            status = "Synced {} -> homepage/guides/{}".format(
                doc["source"],
                doc["destination"],
            )
            print(status)

    if not args.quiet:
        print("Homepage docs are up to date.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
