"""Behavior checks: run python -m unittest -v."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest

import main


class CBRTests(unittest.TestCase):
    def test_retrieval_and_exact_match(self):
        ranked = main.retrieve(main.NEW_PROBLEM, main.SEED_CASES)
        self.assertEqual(ranked[0][1]["id"], "C01")
        self.assertAlmostEqual(ranked[0][0], 0.95)
        self.assertEqual(main.similarity(main.NEW_PROBLEM, main.NEW_PROBLEM), 1)

    def test_adaptation_preserves_original_and_changes_workload(self):
        original = deepcopy(main.SEED_CASES[0])
        plan = main.adapt(main.NEW_PROBLEM, original)
        self.assertEqual(plan["practice_count"], 4)
        self.assertIn("x = 4", plan["worked_example"])
        self.assertEqual(original, main.SEED_CASES[0])

    def test_revision_and_pending_cases(self):
        plan = main.adapt(main.NEW_PROBLEM, main.SEED_CASES[0])
        outcome = main.revise(plan, 2)
        self.assertEqual(outcome["status"], "needs_review")
        self.assertEqual(plan["practice_count"], 6)
        self.assertEqual(main.revise(plan, None)["status"], "pending")
        pending = deepcopy(main.SEED_CASES[0])
        pending["outcome"]["status"] = "pending"
        with self.assertRaises(ValueError):
            main.retrieve(main.NEW_PROBLEM, [pending])

    def test_persistence_and_duplicate_prevention(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "cases.json"
            cases = main.load_cases(path)
            plan = main.adapt(main.NEW_PROBLEM, cases[0])
            outcome = main.revise(plan, 4, simulated=True)
            saved, added = main.retain(cases, main.NEW_PROBLEM, plan, outcome, "C01", path)
            self.assertTrue(added)
            self.assertEqual(saved["id"], "C06")
            reloaded = main.load_cases(path)
            self.assertEqual(len(reloaded), 6)
            self.assertEqual(main.retrieve(main.NEW_PROBLEM, reloaded)[0][1]["id"], "C06")
            _, added = main.retain(reloaded, main.NEW_PROBLEM, plan, outcome, "C06", path)
            self.assertFalse(added)
            self.assertEqual(len(main.load_cases(path)), 6)

    def test_invalid_profile_and_malformed_saved_file(self):
        bad = deepcopy(main.NEW_PROBLEM)
        bad["frequency"] = 0
        with self.assertRaises(ValueError):
            main.validate_problem(bad)
        bad = deepcopy(main.NEW_PROBLEM)
        bad["errors"] = ["formula_misuse"]
        with self.assertRaises(ValueError):
            main.validate_problem(bad)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "broken.json"
            path.write_text("not json", encoding="utf-8")
            with self.assertRaises(ValueError):
                main.load_cases(path)
            self.assertEqual(path.read_text(encoding="utf-8"), "not json")


if __name__ == "__main__":
    unittest.main()
