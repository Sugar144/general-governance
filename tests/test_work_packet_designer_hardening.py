from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROLE = ROOT / "framework/capabilities/work-packet-design/agent/work-packet-designer/role.md"
SKILL = ROOT / "framework/capabilities/work-packet-design/agent/work-packet-designer/SKILL.md"
CASES = ROOT / "tests/fixtures/work-packet/designer-hardening-regressions.json"


class WorkPacketDesignerHardeningTests(unittest.TestCase):
    def setUp(self) -> None:
        self.role = ROLE.read_text(encoding="utf-8")
        self.skill = SKILL.read_text(encoding="utf-8")
        self.cases = json.loads(CASES.read_text(encoding="utf-8"))["cases"]

    def test_all_incident_regression_controls_are_mandatory_in_role(self):
        for case in self.cases:
            with self.subTest(case_id=case["case_id"]):
                self.assertIn(case["required_role_marker"], self.role)

    def test_operational_skill_restates_hardening_cross_checks(self):
        for marker in (
            "Local/external seam split",
            "Surface-to-node closure",
            "Integration-edge closure",
            "Validation-reachability closure",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.skill)

    def test_stage8_is_bounded_self_challenge_not_completeness_warrant(self):
        self.assertIn("bounded self-challenge evidence", self.role)
        self.assertIn("must never be worded as proof", self.role)
        self.assertNotIn("STAGE8_PASS_NO_MATERIAL_MISSING_DEPENDENCY", self.role)
        self.assertNotIn("STAGE8_PASS_NO_MATERIAL_MISSING_DEPENDENCY", self.skill)

    def test_stage8_findings_require_return_to_discovery_and_revalidation(self):
        self.assertIn("return to Stages 2–6", self.role)
        self.assertIn("repeat Stage 7", self.role)


if __name__ == "__main__":
    unittest.main()
