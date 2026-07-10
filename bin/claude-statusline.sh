#!/usr/bin/env bash
set -euo pipefail

input="$(cat)"

model_name="$(echo "$input" | jq -r '.model.display_name // .model.id // "unknown"')"
effort="$(echo "$input" | jq -r '.effort.level // empty')"
cwd="$(echo "$input" | jq -r '.workspace.current_dir // .cwd // empty')"
dir_display="${cwd/#$HOME/\~}"

branch=""
if command -v git >/dev/null 2>&1 && [ -n "$cwd" ] && [ -d "$cwd" ]; then
    branch="$(git -C "$cwd" --no-optional-locks branch --show-current 2>/dev/null || true)"
fi

remaining="$(echo "$input" | jq -r '.context_window.remaining_percentage // empty')"

five_hour="$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')"
weekly="$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')"

# Colors (dimmed, suitable for terminals expecting dim status lines)
C_RESET=$'\033[0m'
C_MODEL=$'\033[2;36m' # dim cyan
C_DIR=$'\033[2;33m'   # dim yellow
C_GIT=$'\033[2;32m'   # dim green
C_CTX=$'\033[2;35m'   # dim magenta
C_LIMIT=$'\033[2;34m' # dim blue

parts=()

model_part="${model_name}"
if [ -n "$effort" ]; then
    model_part="${model_part}(${effort})"
fi
parts+=("${C_MODEL}${model_part}${C_RESET}")

if [ -n "$dir_display" ]; then
    parts+=("${C_DIR}${dir_display}${C_RESET}")
fi

if [ -n "$branch" ]; then
    parts+=("${C_GIT}${branch}${C_RESET}")
fi

if [ -n "$remaining" ]; then
    parts+=("${C_CTX}ctx: ${remaining}%${C_RESET}")
fi

limit_str=""
if [ -n "$five_hour" ]; then
    limit_str="5h :$(printf '%.0f' "$five_hour")%"
fi
if [ -n "$weekly" ]; then
    if [ -n "$limit_str" ]; then
        limit_str="${limit_str} | 7d:$(printf '%.0f' "$weekly")%"
    else
        limit_str="7d: $(printf '%.0f' "$weekly")%"
    fi
fi
if [ -n "$limit_str" ]; then
    parts+=("${C_LIMIT}${limit_str}${C_RESET}")
fi

sep=$'\033[2m|\033[0m'
output=""
for part in "${parts[@]}"; do
    if [ -z "$output" ]; then
        output="$part"
    else
        output="${output} ${sep} ${part}"
    fi
done

printf '%s\n' "$output"
