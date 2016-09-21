#!/bin/sh

SRC=~/Dropbox/dotfiles/
if [ ! -e $SRC ];then
    SRC=~/.dotfiles/
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
ln -s $SRC/fonts.conf ~/.config/fontconfig/fonts.conf

ln -s $SRC/.tmux.conf ~/.tmux.conf
ln -s $SRC/.tmux ~/.tmux
ln -s $SRC/.latexmkrc ~/.latexmkrc
ln -s $SRC/.clang-format ~/.clang-format
