#!/bin/sh

SRC=$HOME/Dropbox/dotfiles/

ln -s $SRC/.gitconfig ~/.gitconfig 
ln -s $SRC/.screenrc ~/.screenrc
ln -s $SRC/.signature ~/.signature
ln -s $SRC/dot_vim/ ~/.vim
ln -s $SRC/dot_vim/vimrc ~/.vimrc
ln -s $SRC/.zsh ~/.zsh
ln -s $SRC/.zprofile ~/.zprofile
ln -s $SRC/.zlogout ~/.zlogout
ln -s $SRC/.zshrc ~/.zshrc


ln -s $SRC/.tmux.conf ~/.tmux.conf
ln -s $SRC/.tmux ~/.tmux
