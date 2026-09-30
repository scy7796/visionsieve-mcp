"""Contract tests for the operator-side pre-release validation pack."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


class PreReleaseValidationTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[1]
        self.validation = self.root / "pre_release_validation"

    def test_required_validation_files_exist(self):
        for name in (
            "README.md",
            "CODEX_TASK.md",
            "REAL_WORLD_TEST_REPORT.template.md",
            "claims-matrix.md",
            "run_validation.py",
        ):
            self.assertTrue((self.validation / name).is_file(), name)

    def test_readme_keeps_public_claims_bounded(self):
        text = (self.root / "README.md").read_text(encoding="utf-8")
        self.assertIn("## The comparison", text)
        self.assertIn("about 90% less visual text", text)
        self.assertIn("This is a small same-machine comparison", text)
        self.assertIn("not a general accuracy or speed leaderboard", text)
        self.assertIn("It does not silently switch models or move onto an API-billed route", text)
        self.assertIn("comparison.md", text)
        self.assertNotIn("most accurate vision MCP", text.casefold())
        self.assertNotIn("90% fewer tokens", text.casefold())

    def test_validation_runner_generates_credential_free_config_and_fixtures(self):
        script = self.validation / "run_validation.py"
        spec = importlib.util.spec_from_file_location("visual_evidence_release_validation", script)
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory(prefix="vb-release-validation-") as directory:
            root = Path(directory)
            fixtures = root / "fixtures"
            specs = module.generate_fixtures(fixtures)
            self.assertEqual(set(specs), {"text", "ui", "chart", "compare", "long", "injection"})
            config = root / "config.yaml"
            module.write_config(config, fixtures, root)
            text = config.read_text(encoding="utf-8")
            self.assertIn('model: "gpt-5.6-luna"', text)
            self.assertIn("auth_mode: chatgpt", text)
            self.assertNotIn("OPENAI_API_KEY", text)
            self.assertNotIn("CODEX_API_KEY", text)
            self.assertTrue(all((fixtures / rel).is_file() for case in specs.values() for rel in case["paths"]))

    def test_release_runner_requires_three_live_probes(self):
        text = (self.validation / "run_validation.py").read_text(encoding="utf-8")
        self.assertIn("len(live_probes) >= 3", text)
        self.assertNotIn("len(live_probes) >= min(3, args.runs)", text)

    def test_long_benchmark_is_opt_in_not_a_p0_default(self):
        text = (self.validation / "run_validation.py").read_text(encoding="utf-8")
        self.assertIn('parser.add_argument("--benchmark"', text)
        self.assertIn("if args.benchmark:", text)

    def test_codex_task_requires_execution_and_forbids_api_key(self):
        text = (self.validation / "CODEX_TASK.md").read_text(encoding="utf-8")
        self.assertIn("請在目前的電腦上實際完成安裝、執行驗證", text)
        self.assertIn("## 必須執行", text)
        self.assertIn("不得建立或使用 API Key", text)
        self.assertIn("不得讀取、輸出、複製或提交 `~/.codex/auth.json` 的內容", text)
        self.assertIn("python pre_release_validation/run_validation.py --runs 5 --host-mcp", text)
        self.assertIn("PASS", text)
        self.assertIn("CONDITIONAL PASS", text)
        self.assertIn("FAIL", text)

    def test_taiwan_chinese_docs_do_not_mix_scripts_or_legacy_terms(self):
        for relative in (
            "docs/README.zh-TW.md",
            "pre_release_validation/CODEX_TASK.md",
            "pre_release_validation/README.md",
            "pre_release_validation/claims-matrix.md",
        ):
            with self.subTest(document=relative):
                text = (self.root / relative).read_text(encoding="utf-8")
                self.assertNotRegex(
                    text,
                    r"[\u8c03\u8fd0\u4ed3\u53d1\u8d26\u5e10\u7801\u7f13\u6267\u56fe"
                    r"\u7f51\u8fd9\u5f53\u7ea7\u4f1a\u9879\u73b0\u7b7e\u636e\u8bf7"
                    r"\u9884\u6237\u8bf4\u8bed]|調用|代碼|本地|文本",
                )


if __name__ == "__main__":
    unittest.main()
