#!/usr/bin/env python3
"""검증한 플러그인 배포 파일만 ZIP으로 묶는다."""

import argparse
import json
import zipfile
from pathlib import Path

try:
    from .validate import ROOT, validate
except ImportError:
    from validate import ROOT, validate


def package(output):
    validate()
    output = Path(output).resolve()
    files = [ROOT / name for name in (
        "plugin.json", ".codex-plugin/plugin.json", ".agents/plugins/marketplace.json", "LICENSE", "README.md",
        "docs/porting.md", "docs/import-manifest.json", "scripts/install_skills.py",
        "scripts/validate.py", "scripts/package_plugin.py", "tests/test_install.py", "tests/test_package.py",
    )]
    files.extend(path for path in (ROOT / "skills").rglob("*") if path.is_file())
    if output in files or ROOT / "skills" in output.parents:
        raise ValueError("출력 경로가 배포 원본과 겹칩니다.")
    for path in files:
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"배포 원본 오류: {path}")
    output.parent.mkdir(parents=True, exist_ok=True)
    # 배포물의 시간·권한을 고정해 같은 입력은 같은 ZIP을 만든다.
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(files):
            info = zipfile.ZipInfo(str(path.relative_to(ROOT)), date_time=(2026, 10, 12, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    print(f"배포 파일: {output}")
    return output


if __name__ == "__main__":
    version = json.loads((ROOT / "plugin.json").read_text())["version"]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist" / f"brian-ai-flutter-plugin-{version}.zip")
    package(parser.parse_args().output)
