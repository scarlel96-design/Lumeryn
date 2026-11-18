"""Validate proposed JSON contracts without running AI services."""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.validate_contracts import validate


def handoff() -> dict:
    return {
        "wo_id": "WO-AGENT-00",
        "agent": "grok",
        "status": "BLOCKED",
        "master_sha256": hashlib.sha256((ROOT / "docs/MASTER_PLAN.md").read_bytes()).hexdigest(),
        "commands_executed": [],
        "files_changed": [],
        "tests": [],
        "blockers": ["No login"],
        "ready_for_review": False,
    }


class ContractValidationTests(unittest.TestCase):
    def validate_data(self, kind: str, data: dict) -> list[str]:
        with tempfile.TemporaryDirectory() as temp:
            file = Path(temp) / "candidate.json"
            file.write_text(json.dumps(data), encoding="utf-8")
            return validate(ROOT, kind, file)

    def test_example_module_manifest(self):
        file = ROOT / "plugins/examples/math-tool/manifest.json"
        self.assertEqual(validate(ROOT, "module", file), [])

    def test_module_requires_capability(self):
        obj = json.loads((ROOT / "plugins/examples/math-tool/manifest.json").read_text())
        obj["capabilities"] = []
        self.assertTrue(self.validate_data("module", obj))

    def test_blocked_handoff_is_not_a_success_claim(self):
        self.assertEqual(self.validate_data("handoff", handoff()), [])

    def test_handoff_rejects_stale_master_hash(self):
        bad = handoff()
        bad["master_sha256"] = "0" * 64
        self.assertTrue(any("master_sha256 differs" in issue for issue in self.validate_data("handoff", bad)))

    def test_handoff_rejects_unverified_completion(self):
        bad = handoff()
        bad["status"] = "COMPLETED"
        bad["blockers"] = []
        bad["ready_for_review"] = True
        self.assertTrue(any("PASS test" in issue for issue in self.validate_data("handoff", bad)))

    def test_handoff_rejects_uncommitted_changes(self):
        bad = handoff()
        bad["status"] = "COMPLETED"
        bad["blockers"] = []
        bad["ready_for_review"] = True
        bad["files_changed"] = ["example.py"]
        bad["tests"] = [{"name": "unit", "status": "PASS"}]
        self.assertTrue(any("result_commit" in issue for issue in self.validate_data("handoff", bad)))


if __name__ == "__main__":
    unittest.main()
