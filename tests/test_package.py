"""실제 ZIP의 설치 가능성과 라이선스 포함 여부를 검증한다."""

import contextlib
import io
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.package_plugin import package
from scripts.validate import ROOT, validate


class PackageTests(unittest.TestCase):
    def test_archive_is_complete_and_can_be_validated_after_extraction(self):
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stdout(io.StringIO()):
            folder = Path(folder)
            archive_path = package(folder / "plugin.zip")
            with zipfile.ZipFile(archive_path) as archive:
                names = archive.namelist()
                self.assertEqual(16, sum(name.endswith("/SKILL.md") for name in names))
                self.assertEqual(17, sum(name == "LICENSE" or name.endswith("/LICENSE") for name in names))
                self.assertFalse(any(".git/" in name or "__pycache__" in name for name in names))
                archive.extractall(folder / "extracted")
            validate(folder / "extracted")
            second = package(folder / "second.zip")
            self.assertEqual(archive_path.read_bytes(), second.read_bytes())

    def test_cannot_overwrite_a_skill_with_archive(self):
        with contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(ValueError):
                package(ROOT / "skills/flutter-bloc/SKILL.md")


if __name__ == "__main__":
    unittest.main()
