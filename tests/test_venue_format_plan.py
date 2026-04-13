import importlib.util
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_module(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {module_name} from {path}")
    spec.loader.exec_module(module)
    return module


class VenueFormatPlanTest(unittest.TestCase):
    def test_iclr_requires_brief_global_summary(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_venue_format_plan.py"
        self.assertTrue(module_path.exists(), "Expected build_venue_format_plan.py to exist.")
        module = load_module("build_venue_format_plan", module_path)
        plan = module.build_venue_format_plan("ICLR")
        self.assertTrue(plan["global_summary"])
        self.assertEqual(plan["weakness_prefix"], "W")

    def test_icml_defaults_to_per_reviewer_5000(self) -> None:
        module = load_module(
            "build_venue_format_plan",
            ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_venue_format_plan.py",
        )
        plan = module.build_venue_format_plan("ICML")
        self.assertFalse(plan["global_summary"])
        self.assertEqual(plan["default_per_reviewer_limit"], 5000)

    def test_neurips_defaults_to_per_reviewer_10000(self) -> None:
        module = load_module(
            "build_venue_format_plan",
            ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_venue_format_plan.py",
        )
        plan = module.build_venue_format_plan("NeurIPS")
        self.assertFalse(plan["global_summary"])
        self.assertEqual(plan["default_per_reviewer_limit"], 10000)

    def test_aaai_defaults_to_per_reviewer_2500(self) -> None:
        module = load_module(
            "build_venue_format_plan",
            ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_venue_format_plan.py",
        )
        plan = module.build_venue_format_plan("AAAI")
        self.assertFalse(plan["global_summary"])
        self.assertEqual(plan["default_per_reviewer_limit"], 2500)

    def test_ieee_defaults_to_per_reviewer_without_limit(self) -> None:
        module = load_module(
            "build_venue_format_plan",
            ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_venue_format_plan.py",
        )
        plan = module.build_venue_format_plan("IEEE")
        self.assertFalse(plan["global_summary"])
        self.assertEqual(plan["budget_mode"], "per-reviewer")
        self.assertIsNone(plan["default_per_reviewer_limit"])

    def test_cv_family_uses_summary_and_one_page_equivalent(self) -> None:
        module = load_module(
            "build_venue_format_plan",
            ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_venue_format_plan.py",
        )
        for venue in ("CVPR", "ICCV", "ECCV"):
            with self.subTest(venue=venue):
                plan = module.build_venue_format_plan(venue)
                self.assertTrue(plan["global_summary"])
                self.assertEqual(plan["budget_mode"], "cv-one-page")
                self.assertEqual(plan["weakness_prefix"], "W")

    def test_user_per_reviewer_limit_overrides_venue_default(self) -> None:
        module = load_module(
            "build_venue_format_plan",
            ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_venue_format_plan.py",
        )
        plan = module.build_venue_format_plan("AAAI", per_reviewer_limit=5000)
        self.assertEqual(plan["default_per_reviewer_limit"], 5000)
        self.assertEqual(plan["budget_mode"], "per-reviewer")
        self.assertEqual(plan["source"], "user-override")

    def test_user_can_disable_global_summary_even_for_iclr(self) -> None:
        module = load_module(
            "build_venue_format_plan",
            ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_venue_format_plan.py",
        )
        plan = module.build_venue_format_plan("ICLR", global_summary=False)
        self.assertFalse(plan["global_summary"])
        self.assertEqual(plan["source"], "user-override")

    def test_unknown_venue_can_be_forced_into_per_reviewer_mode(self) -> None:
        module = load_module(
            "build_venue_format_plan",
            ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_venue_format_plan.py",
        )
        plan = module.build_venue_format_plan("UnknownConf", per_reviewer_limit=4000)
        self.assertEqual(plan["budget_mode"], "per-reviewer")
        self.assertEqual(plan["default_per_reviewer_limit"], 4000)
        self.assertEqual(plan["source"], "user-override")


if __name__ == "__main__":
    unittest.main()
