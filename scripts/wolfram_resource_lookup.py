#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "data" / "wolfram-resource-manifest.json"

ALIASES = {
    "WolframSampleCode": {"sample", "example", "canonical", "usage", "resourcefunction"},
    "CodeReformat": {"format", "reformat", "cleanup", "clean", "readable", "indent"},
    "CodeCommentInsert": {"comment", "comments", "annotate", "explain"},
    "CodeDocAnnotator": {"documentation", "docs", "usage", "message", "messages", "paclet"},
    "FunctionNameSuggest": {"function", "rename", "api", "name", "naming"},
    "VariableNameSuggest": {"variable", "variables", "rename", "name", "naming"},
    "LLMPromptAssessment": {"assess", "assessment", "hallucinated", "hallucination", "symbols", "verify"},
    "Generate Email Replies with a Semantic Search Memory": {"memory", "cache", "retrieval", "semantic"},
    "Provide Socioeconomic Data with an LLM Tool to Avoid Hallucinations": {
        "tool",
        "lookup",
        "exact",
        "hallucination",
        "hallucinated",
        "evidence",
    },
    "Re-ranking Text Matches in Semantic Search Queries": {"rerank", "reranking", "semantic", "search", "snippets"},
}


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def tokenize(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9]+", text.lower()) if len(token) > 1}


def iter_resources(manifest: dict[str, Any], kind: str = "all") -> list[dict[str, Any]]:
    if kind == "all":
        resources = list(manifest.get("prompts", [])) + list(manifest.get("examples", []))
    elif kind in {"prompts", "examples"}:
        resources = list(manifest.get(kind, []))
    else:
        raise ValueError(f"unsupported kind: {kind}")
    return resources


def score_resource(resource: dict[str, Any], query_tokens: set[str]) -> tuple[int, int, str]:
    name = resource["name"]
    searchable_text = " ".join(
        str(resource.get(field, "")) for field in ["name", "repository", "role", "use_when"]
    )
    resource_tokens = tokenize(searchable_text)
    alias_tokens = ALIASES.get(name, set())
    overlap = query_tokens & resource_tokens
    alias_overlap = query_tokens & alias_tokens
    score = len(overlap) + (2 * len(alias_overlap))
    return score, len(alias_overlap), name


def match_resources(
    manifest: dict[str, Any],
    query: str,
    kind: str = "all",
    limit: int = 5,
) -> list[dict[str, Any]]:
    query_tokens = tokenize(query)
    scored = []
    for resource in iter_resources(manifest, kind):
        score, alias_score, name = score_resource(resource, query_tokens)
        if score > 0:
            item = dict(resource)
            item["score"] = score
            item["alias_score"] = alias_score
            scored.append(item)

    scored.sort(key=lambda item: (-item["score"], -item["alias_score"], item["name"]))
    return scored[:limit]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Offline lookup for candidate Wolfram prompt/example resources in the local manifest."
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--kind", choices=["all", "prompts", "examples"], default="all")
    parser.add_argument("--query", help="Natural-language task to match against manifest entries.")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--list", action="store_true", help="List resources without query ranking.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    manifest = load_manifest(args.manifest)

    if args.list:
        matches = iter_resources(manifest, args.kind)
    elif args.query:
        matches = match_resources(manifest, args.query, kind=args.kind, limit=args.limit)
    else:
        parser.error("provide --query or --list")

    payload = {
        "mode": "offline-manifest",
        "manifest": str(args.manifest),
        "kind": args.kind,
        "query": args.query,
        "matches": matches,
        "note": "These are candidate resources from the local manifest. Verify live Wolfram availability before citing them as evidence.",
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
