#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

C_RESET = "\033[0m"
C_MODEL = "\033[2;36m"  # dim cyan
C_DIR = "\033[2;33m"  # dim yellow
C_GIT = "\033[2;32m"  # dim green
C_CTX = "\033[2;35m"  # dim magenta
C_LIMIT = "\033[2;34m"  # dim blue
SEP = "\033[2m|\033[0m"


def get_branch(cwd: str) -> str:
    if not cwd or not Path(cwd).is_dir():
        return ""
    try:
        result = subprocess.run(
            ["git", "-C", cwd, "--no-optional-locks", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout.strip()
    except FileNotFoundError:
        return ""


def main() -> None:
    data = json.load(sys.stdin)

    model = data.get("model", {})
    model_name = model.get("display_name") or model.get("id") or "unknown"
    effort = (data.get("effort") or {}).get("level") or ""

    cwd = (data.get("workspace") or {}).get("current_dir") or data.get("cwd") or ""
    home = str(Path.home())
    dir_display = cwd.replace(home, "~", 1) if cwd.startswith(home) else cwd

    branch = get_branch(cwd)

    remaining = (data.get("context_window") or {}).get("remaining_percentage")

    rate_limits = data.get("rate_limits") or {}
    five_hour = (rate_limits.get("five_hour") or {}).get("used_percentage")
    weekly = (rate_limits.get("seven_day") or {}).get("used_percentage")

    parts = []

    model_part = model_name
    if effort:
        model_part = f"{model_part}({effort})"
    parts.append(f"{C_MODEL}{model_part}{C_RESET}")

    if dir_display:
        parts.append(f"{C_DIR}{dir_display}{C_RESET}")

    if branch:
        parts.append(f"{C_GIT}{branch}{C_RESET}")

    if remaining is not None and remaining != "":
        parts.append(f"{C_CTX}ctx: {remaining}%{C_RESET}")

    limit_parts = []
    if five_hour is not None and five_hour != "":
        limit_parts.append(f"5h :{five_hour:.0f}%")
    if weekly is not None and weekly != "":
        limit_parts.append(f"7d: {weekly:.0f}%")
    if limit_parts:
        parts.append(f"{C_LIMIT}{' | '.join(limit_parts)}{C_RESET}")

    print(f" {SEP} ".join(parts))


if __name__ == "__main__":
    main()
