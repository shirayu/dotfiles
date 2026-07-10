import importlib.machinery
import importlib.util
import unittest
from pathlib import Path


def load_setup_module():
    setup_path = Path(__file__).resolve().parents[1] / "setup.py"
    loader = importlib.machinery.SourceFileLoader("setup_module", str(setup_path))
    spec = importlib.util.spec_from_loader("setup_module", loader)
    if spec is None:
        raise ImportError(f"Cannot load setup module from {setup_path}")
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


setup_module = load_setup_module()


class MergeTomlSectionTest(unittest.TestCase):
    TARGET = (
        '[projects."/home/foo"]\n'
        "trust_level = \"trusted\"\n"
        "\n"
        "[tui]\n"
        "status_line = [\n"
        '  "a",\n'
        '  "b",\n'
        "]\n"
        "status_line_use_colors = true\n"
        "\n"
        '[tui.model_availability_nux]\n'
        '"gpt-5.5" = 4\n'
    )

    def test_no_change_when_source_matches_target(self):
        source = "[tui]\nstatus_line = [\n" '  "a",\n' '  "b",\n' "]\n" "status_line_use_colors = true\n"
        merged = setup_module.merge_toml_section(self.TARGET, source, "tui")
        self.assertEqual(merged, self.TARGET)

    def test_overwrites_existing_key_only(self):
        source = "[tui]\nstatus_line_use_colors = false\n"
        merged = setup_module.merge_toml_section(self.TARGET, source, "tui")
        self.assertIn("status_line_use_colors = false", merged)
        self.assertIn('  "a",\n', merged)  # status_line は変更されない
        self.assertIn("[tui.model_availability_nux]", merged)  # サブテーブルは温存

    def test_adds_new_key(self):
        source = '[tui]\nnew_key = "hello"\n'
        merged = setup_module.merge_toml_section(self.TARGET, source, "tui")
        self.assertIn('new_key = "hello"', merged)
        self.assertIn("status_line_use_colors = true", merged)
        self.assertIn("[tui.model_availability_nux]", merged)

    def test_creates_missing_section(self):
        source = "[newsection]\nfoo = 1\n"
        merged = setup_module.merge_toml_section(self.TARGET, source, "newsection")
        self.assertTrue(merged.startswith(self.TARGET.rstrip("\n") + "\n\n[newsection]\nfoo = 1\n") or "[newsection]\nfoo = 1\n" in merged)
        self.assertIn(self.TARGET.strip(), merged)

    def test_creates_section_in_empty_target(self):
        merged = setup_module.merge_toml_section("", "[newsection]\nfoo = 1\n", "newsection")
        self.assertEqual(merged, "[newsection]\nfoo = 1\n")

    def test_raises_when_source_missing_section(self):
        with self.assertRaises(ValueError):
            setup_module.merge_toml_section(self.TARGET, "[other]\nfoo = 1\n", "tui")


if __name__ == "__main__":
    unittest.main()
