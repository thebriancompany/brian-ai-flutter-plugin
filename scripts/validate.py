#!/usr/bin/env python3
"""외부 의존성 없이 이 저장소의 스킬·메타데이터·참조·라이선스를 검증한다."""

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def read_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise ValueError(f"frontmatter 없음: {path}")
    # 이 저장소는 단순한 name과 JSON 호환 인용 description만 사용한다.
    lines = match.group(1).splitlines()
    if len(lines) != 2 or not lines[0].startswith("name: ") or not lines[1].startswith("description: "):
        raise ValueError(f"지원하지 않는 frontmatter: {path}")
    return lines[0][6:], json.loads(lines[1][13:])


def prose_and_fences(text, path):
    prose = []
    active = False
    for line in text.splitlines():
        if line.startswith("```"):
            active = not active
        elif not active:
            prose.append(line)
    if active:
        raise ValueError(f"닫히지 않은 코드 블록: {path}")
    return "\n".join(prose)


def validate(root=ROOT):
    root = Path(root).resolve()
    manifest = json.loads((root / "plugin.json").read_text())
    overlay = json.loads((root / ".codex-plugin/plugin.json").read_text())
    marketplace = json.loads((root / ".agents/plugins/marketplace.json").read_text())
    inventory = json.loads((root / "docs/import-manifest.json").read_text())
    for key in ("name", "version", "license"):
        if manifest[key] != overlay[key]:
            raise ValueError(f"플러그인 메타데이터 불일치: {key}")
    if overlay["skills"] != "./skills/":
        raise ValueError("스킬 경로 불일치")
    entry = marketplace["plugins"][0]
    if entry["name"] != manifest["name"] or entry["source"] != {"source": "local", "path": "./"}:
        raise ValueError("마켓플레이스 경로 불일치")
    license_text = (root / "LICENSE").read_text()
    if "Copyright (c) 2026 Very Good Ventures" not in license_text or "Permission is hereby granted" not in license_text:
        raise ValueError("필수 MIT 고지 누락")
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    if len(skills) != 16:
        raise ValueError(f"스킬 수 불일치: {len(skills)}")
    for path in skills:
        name, description = read_frontmatter(path)
        if name != path.parent.name or not re.fullmatch(r"flutter-[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            raise ValueError(f"스킬 이름 오류: {path}")
        if not re.search(r"[가-힣]", description) or len(description) > 1024:
            raise ValueError(f"한국어 설명 오류: {path}")
        if (path.parent / "LICENSE").read_text() != license_text:
            raise ValueError(f"개별 스킬 MIT 고지 불일치: {path}")
        metadata = (path.parent / "agents/openai.yaml").read_text()
        if not metadata.startswith("interface:\n"):
            raise ValueError(f"UI 메타데이터 누락: {path}")
        for line in metadata.splitlines()[1:]:
            key, value = line.strip().split(": ", 1)
            value = json.loads(value)
            if not re.search(r"[가-힣]", value):
                raise ValueError(f"한국어 UI 필드 누락: {path}: {key}")
            if key == "short_description" and not 25 <= len(value) <= 64:
                raise ValueError(f"UI 설명 길이 오류: {path}")

    documents = sorted((root / "skills").rglob("*.md"))
    if len(documents) != 68:
        raise ValueError(f"문서 수 불일치: {len(documents)}")
    mapped = [row["target"] for row in inventory["files"]]
    actual = [str(path.relative_to(root)) for path in documents]
    if len(mapped) != len(set(mapped)) or set(mapped) != set(actual):
        raise ValueError("이식 목록과 실제 문서 불일치")
    for path in documents:
        text = path.read_text()
        prose = prose_and_fences(text, path)
        if not re.search(r"[가-힣]", prose):
            raise ValueError(f"한국어 본문 없음: {path}")
        if re.search(r"@@CODE:|CLAUDE_PLUGIN_ROOT|AskUserQuestion|allowed-tools:|\$ARGUMENTS|mcp__|VGV|VeryGoodOpenSource|Very Good Ventures", text):
            raise ValueError(f"변환 잔여물: {path}")
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", prose):
            if ":" in target or target.startswith("#"):
                continue
            linked = (path.parent / unquote(target.split("#")[0])).resolve()
            if root not in linked.parents or not linked.exists():
                raise ValueError(f"잘못된 상대 참조: {path} -> {target}")
    print(f"검증 완료: 스킬 {len(skills)}개, 문서 {len(documents)}개, 메타데이터·상대 링크·MIT 고지")


if __name__ == "__main__":
    try:
        validate()
    except (OSError, ValueError, KeyError) as error:
        sys.exit(f"검증 실패: {error}")
