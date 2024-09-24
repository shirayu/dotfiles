
# dotfiles

This is my dotfiles. (Except for [.vim](https://github.com/shirayu/dot_vim))

## Setup

```bash
sudo apt update
sudo apt install -y git htop jq make rsync shellcheck task-japanese zsh locales tmux
sudo /usr/sbin/dpkg-reconfigure locales
sudo timedatectl set-timezone Asia/Tokyo

git clone https://github.com/shirayu/dot_vim.git ~/.vim
git clone https://github.com/shirayu/dotfiles.git ~/.dotfiles
curl https://mise.run | sh # https://mise.jdx.dev/getting-started.html
bash ~/.dotfiles/generate_links.sh
sudo chsh $(whoami) -s $(which zsh)

mise up

mkdir -p ~/.vim/dein/repos/github.com/Shougo/dein.vim
git clone https://github.com/Shougo/dein.vim.git ~/.vim/dein/repos/github.com/Shougo/dein.vim
vi +':call dein#install()' +q
~/.vim/setup.sh update
```

### Instruction for the client desktop and laptop PCs (debian+gnome3)

- Register ``mysshagent.sh`` in ``.zsh`` folder to ``gnome-session-properties``
    - The file generated by ``gnome-keyring-daemon`` has the environment variable ``SSH_AUTH_SOCK``
    - ``zshrc.envvar`` uses this variable to user the socket in shells in the ``screen``
