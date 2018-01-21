#!/bin/sh

SRC="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ ! -e "${SRC}/.tmux" ];then
    echo "Not found: [${SRC}/.tmux]"
    exit 1
fi

ln -s $SRC/.gitconfig ~/.gitconfig 
ln -s $SRC/.screenrc ~/.screenrc
ln -s $SRC/.signature ~/.signature
ln -s $SRC/dot_vim/ ~/.vim
ln -s $SRC/dot_vim/vimrc ~/.vimrc
ln -s $SRC/.zsh ~/.zsh
ln -s $SRC/.zprofile ~/.zprofile
ln -s $SRC/.zlogout ~/.zlogout
ln -s $SRC/.zshrc ~/.zshrc

ln -s $SRC/fonts.conf ~/.fonts.conf
mkdir -p ~/.config/fontconfig
ln -s $SRC/fonts.conf ~/.config/fontconfig/fonts.conf

ln -s $SRC/.tmux.conf ~/.tmux.conf
ln -s $SRC/.tmux ~/.tmux
ln -s $SRC/.latexmkrc ~/.latexmkrc
ln -s $SRC/.clang-format ~/.clang-format
ln -s $SRC/.npmrc ~/.npmrc
ln -s $SRC/.eslintrc.json ~/.eslintrc.json
