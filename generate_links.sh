#!/usr/bin/env bash

set -x

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ ! -e "${SRC}/.tmux" ]; then
    echo "Not found: [${SRC}/.tmux]"
    exit 1
fi

find "${SRC}" -mindepth 1 -maxdepth 1 -type f -name '\.*' -not -name '\.gitignore' -print0 | xargs -0 -I {} ln -snf {} ~
find "${SRC}" -mindepth 1 -maxdepth 1 -type d -name '\.*' -not -name '\.git' -not -name '.mypy_cache' -print0 | xargs -0 -I {} ln -snf {} ~

mkdir -p ~/.local/bin
ln -snf "$SRC"/bin/* ~/.local/bin

# https://qiita.com/q1701/items/00418d17ec97cc2768f7
mkdir -p ~/.config/fontconfig && ln -s "${SRC}/dot_config/fontconfig/fonts.conf" ~/.config/fontconfig/fonts.conf

ln -s "${SRC}/dot_config/mise" ~/.config/mise

ln -s "${SRC}/dot_config/pnpm" ~/.config/pnpm

mkdir -p ~/.claude/ && ln -s "${SRC}/dot_config/claude/settings.json" ~/.claude/settings.json
mkdir -p ~/.claude/ && ln -s "${SRC}/dot_config/ripgrep" ~/.config/ripgrep
