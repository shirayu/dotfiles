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

if [ ! -f ~/.local/bin/adb-sync ]; then
    wget --no-glob https://raw.githubusercontent.com/google/adb-sync/master/adb-sync -P ~/.local/bin
fi
chmod a+x ~/.local/bin/adb-sync

# https://qiita.com/q1701/items/00418d17ec97cc2768f7
mkdir -p ~/.config/fontconfig && ln -s "${SRC}/dot_config/fontconfig/fonts.conf" ~/.config/fontconfig/fonts.conf

mkdir -p ~/.config/mise && ln -s "${SRC}/dot_config/mise/mise_config.toml" ~/.config/mise/config.toml
