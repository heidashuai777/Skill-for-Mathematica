#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "wolfram_resource_lookup.py"
MANIFEST = ROOT / "data" / "wolfram-resource-manifest.json"


def load_module():
    spec = importlib.util.spec_from_file_location("wolfram_resource_lookup", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load wolfram_resource_lookup module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WolframResourceLookupTests(unittest.TestCase):
    def test_comment_query_prefers_comment_prompt(self) -> None:
        lookup = load_module()
        manifest = lookup.load_manifest(MANIFEST)
        matches = lookup.match_resources(manifest, "add useful comments to Mathematica code", kind="prompts")
        self.assertEqual(matches[0]["name"], "CodeCommentInsert")

    def test_usage_docs_query_prefers_doc_annotator(self) -> None:
        lookup = load_module()
        manifest = lookup.load_manifest(MANIFEST)
        matches = lookup.match_resources(manifest, "generate usage messages for package functions", kind="prompts")
        self.assertEqual(matches[0]["name"], "CodeDocAnnotator")

    def test_rerank_query_can_search_examples(self) -> None:
        lookup = load_module()
        manifest = lookup.load_manifest(MANIFEST)
        matches = lookup.match_resources(manifest, "rerank semantic search snippets", kind="examples")
        self.assertEqual(matches[0]["name"], "Re-ranking Text Matches in Semantic Search Queries")

    def test_cli_outputs_json(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--manifest",
                str(MANIFEST),
                "--kind",
                "prompts",
                "--query",
                "check for hallucinated Wolfram symbols",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["matches"][0]["name"], "LLMPromptAssessment")
        self.assertEqual(payload["mode"], "offline-manifest")


if __name__ == "__main__":
    unittest.main()
