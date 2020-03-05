#!/usr/bin/env bash

set -x

SRC="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ ! -e "${SRC}/.tmux" ];then
    echo "Not found: [${SRC}/.tmux]"
    exit 1
fi

mkdir -p ~/.config/fontconfig
find "${SRC}" -mindepth 1 -maxdepth 1  -print0 -type f -name '\.*' | xargs -0 -I {} ln -snf {} ~

if [ -d "$SRC/dot_vim" ];then
    ln -snf "$SRC/dot_vim/" ~/.vim
fi
if [ -f ~/.vim/vimrc ];then
    ln -snf ~/.vim/vimrc ~/.vimrc
fi

mkdir -p ~/local/bin
ln -snf "$SRC"/bin/* ~/local/bin

if [ ! -f ~/local/bin/adb-sync ];then
    wget --no-glob https://raw.githubusercontent.com/google/adb-sync/master/adb-sync -P ~/local/bin
fi
chmod a+x ~/local/bin/adb-sync
