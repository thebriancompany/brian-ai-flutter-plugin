#!/usr/bin/env python3
"""한국어 스킬 전체를 Codex 검색 경로에 설치한다. 외부 패키지는 필요 없다."""

import argparse
import hashlib
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fingerprint(directory):
    """상대 경로와 파일 내용으로 설치본이 동일한지 확인한다."""
    return {
        str(path.relative_to(directory)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in directory.rglob("*")
        if path.is_file()
    }


def install(source, destination, replace=False, dry_run=False):
    source = Path(source).resolve()
    destination = Path(destination).expanduser().resolve()
    if source == destination or source in destination.parents or destination in source.parents:
        raise ValueError("설치 원본과 대상 디렉터리가 겹칩니다.")
    skills = sorted(path for path in source.iterdir() if path.is_dir() and (path / "SKILL.md").is_file())
    if not skills:
        raise ValueError("설치할 SKILL.md가 없습니다.")

    plan = []
    for skill in skills:
        if not (skill / "LICENSE").is_file():
            raise ValueError(f"라이선스가 없습니다: {skill.name}")
        if any(path.is_symlink() for path in skill.rglob("*")) or skill.is_symlink():
            raise ValueError(f"원본에 심볼릭 링크가 있습니다: {skill.name}")
        target = destination / skill.name
        if target.is_symlink() or (target.exists() and not target.is_dir()):
            raise ValueError(f"설치 대상이 일반 디렉터리가 아닙니다: {target}")
        if target.exists() and any(path.is_symlink() for path in target.rglob("*")):
            raise ValueError(f"설치 대상 내부에 심볼릭 링크가 있습니다: {target}")
        if target.exists() and fingerprint(skill) == fingerprint(target):
            action = "유지"
        elif target.exists():
            if not replace:
                raise ValueError(f"기존 스킬과 충돌합니다: {target}\n백업 후 교체하려면 --replace를 사용하세요.")
            action = "백업 후 갱신"
        else:
            action = "설치"
        plan.append((skill, target, action))

    # 모든 충돌을 먼저 확인하므로 거절된 설치는 파일을 일부만 남기지 않는다.
    for _, target, action in plan:
        print(f"{action}: {target}")
    changes = [item for item in plan if item[2] != "유지"]
    if dry_run or not changes:
        return None

    destination.mkdir(parents=True, exist_ok=True)
    backup_root = None
    applied = []
    with tempfile.TemporaryDirectory(prefix=".flutter-skills-stage-", dir=destination) as staging:
        staging = Path(staging)
        for skill, _, _ in changes:
            shutil.copytree(skill, staging / skill.name)
        try:
            for skill, target, _ in changes:
                backup = None
                if target.exists():
                    if backup_root is None:
                        backups = destination.parent / ".skill-backups"
                        backups.mkdir(exist_ok=True)
                        backup_root = Path(tempfile.mkdtemp(prefix="flutter-", dir=backups))
                    backup = backup_root / target.name
                    target.rename(backup)
                applied.append((target, backup))
                (staging / skill.name).rename(target)
        except BaseException:
            for target, backup in reversed(applied):
                if target.exists():
                    shutil.rmtree(target)
                if backup is not None and backup.exists():
                    backup.rename(target)
            raise
    if backup_root:
        print(f"기존 스킬 백업: {backup_root}")
    return backup_root


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", type=Path, default=Path.home() / ".agents" / "skills", help="기본값: ~/.agents/skills")
    parser.add_argument("--replace", action="store_true", help="충돌하는 스킬을 백업한 뒤 갱신")
    parser.add_argument("--dry-run", action="store_true", help="파일을 쓰지 않고 설치 계획만 확인")
    args = parser.parse_args()
    try:
        install(ROOT / "skills", args.dest, args.replace, args.dry_run)
    except (ValueError, OSError) as error:
        parser.exit(1, f"설치 실패: {error}\n")


if __name__ == "__main__":
    main()
