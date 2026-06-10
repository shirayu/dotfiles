import argparse
import importlib.machinery
import importlib.util
import unittest
from datetime import datetime
from pathlib import Path


def load_diary_module():
    diary_path = Path(__file__).resolve().parents[1] / "bin" / "diary"
    loader = importlib.machinery.SourceFileLoader("diary", str(diary_path))
    spec = importlib.util.spec_from_loader("diary", loader)
    if spec is None:
        raise ImportError(f"Cannot load diary module from {diary_path}")
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


diary = load_diary_module()


class DiaryTest(unittest.TestCase):
    def test_parse_date(self):
        today = datetime(2026, 6, 5, 12, 34, 56)
        cases = [
            ("today", "2026-06-05"),
            ("tod", "2026-06-05"),
            ("yesterday", "2026-06-04"),
            ("yes", "2026-06-04"),
            ("y", "2026-06-04"),
            ("yy", "2026-06-03"),
            ("yyy", "2026-06-02"),
            ("tomorrow", "2026-06-06"),
            ("tom", "2026-06-06"),
            ("t", "2026-06-06"),
            ("tt", "2026-06-07"),
            ("ttt", "2026-06-08"),
            ("+1", "2026-06-06"),
            ("+3", "2026-06-08"),
            ("-1", "2026-06-04"),
            ("2026-07-08", "2026-07-08"),
            ("20260708", "2026-07-08"),
            ("07-08", "2026-07-08"),
            ("0708", "2026-07-08"),
            ("08", "2026-06-08"),
        ]

        for date_str, expected in cases:
            with self.subTest(date_str=date_str):
                self.assertEqual(
                    diary.parse_date(date_str, today).strftime("%Y-%m-%d"),
                    expected,
                )

    def test_parse_date_rejects_invalid_date(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            diary.parse_date("not-a-date", datetime(2026, 6, 5))

    def test_diary_file_path(self):
        root = Path("/diary")
        target_date = datetime(2026, 7, 8)

        self.assertEqual(
            diary.diary_file_path(root, target_date),
            Path("/diary/2026/07/08.md"),
        )

    def test_ensure_diary_file_creates_file(self):
        import tempfile

        target_date = datetime(2026, 7, 8)

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            file_path = diary.ensure_diary_file(root, target_date)

            self.assertEqual(file_path, root / "2026" / "07" / "08.md")
            self.assertEqual(
                file_path.read_text(encoding="utf-8"),
                "# 2026-07-08\n\n",
            )


if __name__ == "__main__":
    unittest.main()
