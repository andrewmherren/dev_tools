#!/usr/bin/env python3
"""Copier post-copy task: merge VS Code config and copy instruction assets."""

from __future__ import annotations

import json
import shutil
import stat
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def deep_merge_project_wins(
    base: dict[str, Any], overlay: dict[str, Any]
) -> dict[str, Any]:
    """Merge overlay into base, keeping existing base values on conflicts."""
    result = base.copy()
    for key, overlay_value in overlay.items():
        if key not in result:
            result[key] = overlay_value
        elif isinstance(result[key], dict) and isinstance(overlay_value, dict):
            result[key] = deep_merge_project_wins(result[key], overlay_value)
    return result


def deep_merge_overlay_wins(
    base: dict[str, Any], overlay: dict[str, Any]
) -> dict[str, Any]:
    """Merge overlay into base, replacing base values on conflicts."""
    result = base.copy()
    for key, overlay_value in overlay.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(overlay_value, dict)
        ):
            result[key] = deep_merge_overlay_wins(result[key], overlay_value)
        else:
            result[key] = overlay_value
    return result


def dedupe_extensions(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in values:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def merge_vscode_settings(dst_file: Path, overlays: list[Path]) -> None:
    project_settings = load_json(dst_file, {})
    template_settings: dict[str, Any] = {}

    for overlay in overlays:
        if overlay.exists():
            overlay_data = load_json(overlay, {})
            if isinstance(overlay_data, dict):
                template_settings = deep_merge_overlay_wins(
                    template_settings, overlay_data
                )

    merged = deep_merge_project_wins(project_settings, template_settings)
    write_json(dst_file, merged)


def merge_vscode_extensions(dst_file: Path, overlays: list[Path]) -> None:
    project_data = load_json(dst_file, {"recommendations": []})
    if not isinstance(project_data, dict):
        project_data = {"recommendations": []}

    project_recommendations = project_data.get("recommendations", [])
    if not isinstance(project_recommendations, list):
        project_recommendations = []

    template_recommendations: list[str] = []
    for overlay in overlays:
        if not overlay.exists():
            continue
        overlay_data = load_json(overlay, {"recommendations": []})
        if isinstance(overlay_data, dict):
            recs = overlay_data.get("recommendations", [])
            if isinstance(recs, list):
                template_recommendations.extend([str(item) for item in recs])

    recommendations = [str(item) for item in project_recommendations]
    project_data["recommendations"] = dedupe_extensions(
        recommendations + template_recommendations
    )
    write_json(dst_file, project_data)


def merge_keybindings(dst_file: Path, overlays: list[Path]) -> None:
    project_bindings = load_json(dst_file, [])
    if not isinstance(project_bindings, list):
        project_bindings = []

    overlay_bindings: list[dict[str, Any]] = []
    for overlay in overlays:
        if not overlay.exists():
            continue
        data = load_json(overlay, [])
        if isinstance(data, list):
            overlay_bindings.extend([item for item in data if isinstance(item, dict)])

    merged_map: dict[str, dict[str, Any]] = {}
    for binding in overlay_bindings:
        command = binding.get("command")
        if isinstance(command, str):
            merged_map[command] = binding

    for binding in project_bindings:
        if not isinstance(binding, dict):
            continue
        command = binding.get("command")
        if isinstance(command, str):
            merged_map[command] = binding

    write_json(dst_file, list(merged_map.values()))


def copy_if_missing(src: Path, dst: Path) -> bool:
    if dst.exists() or not src.exists():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def copy_md_files_if_missing(src_dir: Path, dst_dir: Path) -> None:
    if not src_dir.exists():
        return
    for file in sorted(src_dir.glob("*.md")):
        copy_if_missing(file, dst_dir / file.name)


def copy_tree_files_if_missing(src_dir: Path, dst_dir: Path) -> None:
    """Copy files recursively, preserving existing destination files."""
    if not src_dir.exists():
        return

    file_iter = (path for path in src_dir.rglob("*") if path.is_file())
    for src_file in sorted(file_iter):
        relative = src_file.relative_to(src_dir)
        copy_if_missing(src_file, dst_dir / relative)


def maybe_make_executable(path: Path) -> None:
    if not path.exists():
        return
    try:
        current = path.stat().st_mode
        path.chmod(current | stat.S_IXUSR)
    except OSError:
        return


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: merge_and_setup.py <language> <execution_mode>")
        return 1

    dst_path = Path.cwd().resolve()
    language = sys.argv[1]
    execution_mode = sys.argv[2]
    src_root = Path(__file__).resolve().parent.parent

    vscode_dir = dst_path / ".vscode"
    github_dir = dst_path / ".github"
    vscode_dir.mkdir(parents=True, exist_ok=True)
    (github_dir / "instructions").mkdir(parents=True, exist_ok=True)
    (github_dir / "agents").mkdir(parents=True, exist_ok=True)
    (github_dir / "skills").mkdir(parents=True, exist_ok=True)
    (github_dir / "prompts").mkdir(parents=True, exist_ok=True)
    (github_dir / "hooks").mkdir(parents=True, exist_ok=True)

    shared_dir = src_root / "fragments" / "shared"
    language_dir = src_root / "fragments" / "languages"
    execution_dir = src_root / "fragments" / "execution"

    settings_overlays = [
        shared_dir / "settings.json",
        execution_dir / f"{execution_mode}-settings.json",
        language_dir / f"{language}-settings.json",
    ]
    extensions_overlays = [
        shared_dir / "extensions.json",
        execution_dir / f"{execution_mode}-extensions.json",
        language_dir / f"{language}-extensions.json",
    ]
    keybindings_overlays = [
        shared_dir / "keybindings.json",
        execution_dir / f"{execution_mode}-keybindings.json",
        language_dir / f"{language}-keybindings.json",
    ]

    merge_vscode_settings(vscode_dir / "settings.json", settings_overlays)
    merge_vscode_extensions(vscode_dir / "extensions.json", extensions_overlays)
    merge_keybindings(vscode_dir / "keybindings.json", keybindings_overlays)

    copy_if_missing(shared_dir / "mcp.json", vscode_dir / "mcp.json")

    copy_md_files_if_missing(
        src_root / "instructions" / "common", github_dir / "instructions"
    )
    copy_if_missing(
        src_root / "instructions" / "languages" / f"{language}-conventions.md",
        github_dir / "instructions" / f"{language}-conventions.md",
    )
    copy_md_files_if_missing(
        src_root / "instructions" / "agents", github_dir / "agents"
    )
    copy_tree_files_if_missing(
        src_root / "instructions" / "skills", github_dir / "skills"
    )
    copy_md_files_if_missing(
        src_root / "instructions" / "prompts", github_dir / "prompts"
    )
    copy_tree_files_if_missing(
        src_root / "instructions" / "hooks", github_dir / "hooks"
    )

    pre_commit_src = shared_dir / "pre-commit-secret-scan.sh"
    pre_commit_dst = dst_path / ".githooks" / "pre-commit"
    if copy_if_missing(pre_commit_src, pre_commit_dst):
        maybe_make_executable(pre_commit_dst)

    if execution_mode == "host":
        shutil.rmtree(dst_path / ".devcontainer", ignore_errors=True)

    print("[OK] Copier merge/setup completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
