#!/bin/sh

SRC="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ ! -e "${SRC}/.tmux" ];then
    echo "Not found: [${SRC}/.tmux]"
    exit 1
fi

ln -snf $SRC/.gitconfig ~/.gitconfig
ln -snf $SRC/.screenrc ~/.screenrc
ln -snf $SRC/.zsh ~/.zsh
ln -snf $SRC/.zprofile ~/.zprofile
ln -snf $SRC/.zlogout ~/.zlogout
ln -snf $SRC/.zshrc ~/.zshrc

ln -snf $SRC/fonts.conf ~/.fonts.conf
mkdir -p ~/.config/fontconfig
ln -snf $SRC/fonts.conf ~/.config/fontconfig/fonts.conf

ln -snf $SRC/.tmux.conf ~/.tmux.conf
ln -snf $SRC/.tmux ~/.tmux
ln -snf $SRC/.latexmkrc ~/.latexmkrc
ln -snf $SRC/.clang-format ~/.clang-format
ln -snf $SRC/.npmrc ~/.npmrc
ln -snf $SRC/.eslintrc.json ~/.eslintrc.json
ln -snf $SRC/.markdownlint.json ~/.markdownlint.json

if [ -d $SRC/dot_vim ];then
    ln -snf $SRC/dot_vim/ ~/.vim
fi
if [ -f ~/.vim/vimrc ];then
    ln -snf ~/.vim/vimrc ~/.vimrc
fi

