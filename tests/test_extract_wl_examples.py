#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "extract_wl_examples.py"


def load_module():
    spec = importlib.util.spec_from_file_location("extract_wl_examples", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load extract_wl_examples module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ExtractWLExamplesTests(unittest.TestCase):
    def test_collects_markdown_fences_and_wl_files(self) -> None:
        extractor = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                textwrap.dedent(
                    """
                    # Examples

                    ```Mathematica
                    Needs["Demo`"]
                    DemoSymbol[x]
                    ```

                    ```python
                    print("ignore")
                    ```
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )
            (root / "example.wl").write_text("ClearAll[f]\nf[x_] := x^2\n", encoding="utf-8")

            examples = list(extractor.collect_examples([root]))

        self.assertEqual(len(examples), 2)
        self.assertEqual(examples[0]["source_type"], "markdown-fence")
        self.assertIn("DemoSymbol[x]", examples[0]["code"])
        self.assertEqual(examples[1]["source_type"], "wolfram-file")
        self.assertIn("f[x_] := x^2", examples[1]["code"])

    def test_cli_writes_jsonl(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / "examples.jsonl"
            (root / "notes.md").write_text(
                "```wl\nPlot[Sin[x], {x, 0, Pi}]\n```\n",
                encoding="utf-8",
            )

            subprocess.run(
                [sys.executable, str(SCRIPT), str(root), "--output", str(output)],
                check=True,
                capture_output=True,
                text=True,
            )
            rows = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["language"], "wl")
        self.assertIn("Plot[Sin[x]", rows[0]["code"])


if __name__ == "__main__":
    unittest.main()
