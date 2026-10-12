"""설치의 충돌 방지, 백업, 참조 보존을 실제 임시 파일로 검증한다."""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.install_skills import ROOT, fingerprint, install


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.destination = Path(self.temp.name) / "skills"
        self.output = contextlib.redirect_stdout(io.StringIO())
        self.output.__enter__()
        self.addCleanup(self.output.__exit__, None, None, None)

    def test_dry_run_does_not_create_destination(self):
        install(ROOT / "skills", self.destination, dry_run=True)
        self.assertFalse(self.destination.exists())

    def test_install_preserves_complete_tree_and_is_idempotent(self):
        install(ROOT / "skills", self.destination)
        self.assertEqual(fingerprint(ROOT / "skills"), fingerprint(self.destination))
        before = (self.destination / "flutter-bloc/SKILL.md").stat().st_mtime_ns
        install(ROOT / "skills", self.destination)
        self.assertEqual(before, (self.destination / "flutter-bloc/SKILL.md").stat().st_mtime_ns)

    def test_conflict_aborts_before_any_other_skill_is_written(self):
        conflict = self.destination / "flutter-testing"
        conflict.mkdir(parents=True)
        (conflict / "personal.txt").write_text("개인 수정")
        with self.assertRaises(ValueError):
            install(ROOT / "skills", self.destination)
        self.assertEqual(["flutter-testing"], [path.name for path in self.destination.iterdir()])
        self.assertEqual("개인 수정", (conflict / "personal.txt").read_text())

    def test_replace_backs_up_old_files_and_keeps_unrelated_skills(self):
        install(ROOT / "skills", self.destination)
        changed = self.destination / "flutter-bloc/SKILL.md"
        changed.write_text("사용자 변경")
        unrelated = self.destination / "personal"
        unrelated.mkdir()
        backup = install(ROOT / "skills", self.destination, replace=True)
        self.assertEqual("사용자 변경", (backup / "flutter-bloc/SKILL.md").read_text())
        self.assertTrue(unrelated.is_dir())
        self.assertEqual((ROOT / "skills/flutter-bloc/SKILL.md").read_text(), changed.read_text())

    def test_symlink_is_not_followed_even_when_replacing(self):
        self.destination.mkdir()
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        (self.destination / "flutter-bloc").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            install(ROOT / "skills", self.destination, replace=True)
        self.assertEqual([], list(outside.iterdir()))

    def test_copy_failure_leaves_existing_install_unchanged(self):
        install(ROOT / "skills", self.destination)
        changed = self.destination / "flutter-bloc/SKILL.md"
        changed.write_text("사용자 변경")
        with patch("scripts.install_skills.shutil.copytree", side_effect=OSError("디스크 오류")):
            with self.assertRaises(OSError):
                install(ROOT / "skills", self.destination, replace=True)
        self.assertEqual("사용자 변경", changed.read_text())

    def test_overlapping_paths_are_rejected(self):
        with self.assertRaises(ValueError):
            install(ROOT / "skills", ROOT / "skills/nested")


if __name__ == "__main__":
    unittest.main()
