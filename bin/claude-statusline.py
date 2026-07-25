#!/usr/bin/env python3
import contextlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, cast

# ANSI color codes
C_RESET = "\033[0m"
C_MODEL = "\033[2;36m"  # dim cyan
C_DIR = "\033[2;33m"  # dim yellow
C_GIT = "\033[2;32m"  # dim green
C_CTX = "\033[2;35m"  # dim magenta
C_LIMIT = "\033[2;34m"  # dim blue
C_COST = "\033[2;32m"  # dim green

# Warning colors
C_WARN = "\033[1;33m"  # bold yellow
C_DANGER = "\033[1;31m"  # bold red

SEP = "\033[2m|\033[0m"

# Thresholds
CTX_DANGER_THRESHOLD = 10.0
CTX_WARN_THRESHOLD = 20.0
LIMIT_DANGER_THRESHOLD = 90.0
LIMIT_WARN_THRESHOLD = 80.0


def _get_dict(data: Any, key: str) -> dict[str, Any]:
    if isinstance(data, dict):
        d = cast(dict[Any, Any], data)
        val = d.get(key)
        if isinstance(val, dict):
            vd = cast(dict[Any, Any], val)
            res: dict[str, Any] = {}
            for k, v in vd.items():
                if isinstance(k, str):
                    res[k] = v
            return res
    return {}


def _get_val(data: Any, key: str) -> Any:
    if isinstance(data, dict):
        d = cast(dict[Any, Any], data)
        return d.get(key)
    return None


def get_git_info(cwd: str) -> str:
    if not cwd or not Path(cwd).is_dir():
        return ""
    try:
        # Get current branch with timeout to prevent hanging
        branch_res = subprocess.run(
            ["git", "-C", cwd, "--no-optional-locks", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=False,
            timeout=0.5,
        )
        branch = branch_res.stdout.strip()
        if not branch:
            return ""

        # Check for uncommitted changes
        status_res = subprocess.run(
            ["git", "-C", cwd, "--no-optional-locks", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=False,
            timeout=0.5,
        )
        dirty = "*" if status_res.stdout.strip() else ""

        return f"{branch}{dirty}"
    except FileNotFoundError, subprocess.TimeoutExpired:
        return ""


def get_cwd(data: dict[str, Any]) -> str:
    ws_dict = _get_dict(data, "workspace")
    ws_dir = ws_dict.get("current_dir")
    if ws_dir is not None:
        return str(ws_dir)
    cwd_val = _get_val(data, "cwd")
    return str(cwd_val) if cwd_val is not None else ""


def get_model_part(data: dict[str, Any]) -> str:
    model_dict = _get_dict(data, "model")
    display_name = model_dict.get("display_name")
    model_id = model_dict.get("id")
    model_name = str(display_name or model_id or "unknown")

    effort_dict = _get_dict(data, "effort")
    effort_val = effort_dict.get("level")
    effort = str(effort_val) if effort_val is not None else ""

    model_part = f"{model_name}({effort})" if effort else model_name
    return f"{C_MODEL}{model_part}{C_RESET}"


def get_dir_part(cwd: str) -> str:
    if not cwd:
        return ""
    home = str(Path.home())
    dir_display = cwd.replace(home, "~", 1) if cwd.startswith(home) else cwd
    return f"{C_DIR}{dir_display}{C_RESET}" if dir_display else ""


def get_context_part(data: dict[str, Any]) -> str:
    ctx_dict = _get_dict(data, "context_window")
    remaining = ctx_dict.get("remaining_percentage")
    if remaining is None or remaining == "":
        return ""

    try:
        rem_val = float(str(remaining))
        if rem_val <= CTX_DANGER_THRESHOLD:
            ctx_color = C_DANGER
        elif rem_val <= CTX_WARN_THRESHOLD:
            ctx_color = C_WARN
        else:
            ctx_color = C_CTX
        return f"{ctx_color}ctx: {rem_val:.0f}%{C_RESET}"
    except ValueError:
        return f"{C_CTX}ctx: {remaining}%{C_RESET}"


def get_rate_limit_part(data: dict[str, Any]) -> str:
    rl_dict = _get_dict(data, "rate_limits")
    five_h_dict = _get_dict(rl_dict, "five_hour")
    five_hour = five_h_dict.get("used_percentage")

    weekly_dict = _get_dict(rl_dict, "seven_day")
    weekly = weekly_dict.get("used_percentage")

    limit_parts: list[str] = []
    if five_hour is not None and five_hour != "":
        try:
            fh_val = float(str(five_hour))
            color = (
                C_DANGER
                if fh_val >= LIMIT_DANGER_THRESHOLD
                else (C_WARN if fh_val >= LIMIT_WARN_THRESHOLD else C_LIMIT)
            )
            limit_parts.append(f"{color}5h:{fh_val:.0f}%{C_RESET}")
        except ValueError:
            pass

    if weekly is not None and weekly != "":
        try:
            w_val = float(str(weekly))
            color = (
                C_DANGER if w_val >= LIMIT_DANGER_THRESHOLD else (C_WARN if w_val >= LIMIT_WARN_THRESHOLD else C_LIMIT)
            )
            limit_parts.append(f"{color}7d:{w_val:.0f}%{C_RESET}")
        except ValueError:
            pass

    return " ".join(limit_parts)


def get_cost_part(data: dict[str, Any]) -> str:
    cost_dict = _get_dict(data, "cost")
    cost = cost_dict.get("total_cost_usd")
    if cost is not None:
        with contextlib.suppress(ValueError):
            return f"{C_COST}${float(str(cost)):.2f}{C_RESET}"
    return ""


def main() -> None:
    try:
        raw_data: Any = json.load(sys.stdin)
        if not isinstance(raw_data, dict):
            return
        rd = cast(dict[Any, Any], raw_data)
        data: dict[str, Any] = {}
        for k, v in rd.items():
            if isinstance(k, str):
                data[k] = v
    except Exception:
        return

    cwd = get_cwd(data)
    git_info = get_git_info(cwd)

    parts: list[str] = [
        get_model_part(data),
        get_dir_part(cwd),
        f"{C_GIT}{git_info}{C_RESET}" if git_info else "",
        get_context_part(data),
        get_rate_limit_part(data),
        get_cost_part(data),
    ]

    filtered_parts = [p for p in parts if p]
    if filtered_parts:
        print(f" {SEP} ".join(filtered_parts))


if __name__ == "__main__":
    main()
