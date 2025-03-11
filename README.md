
# dotfiles

This is my dotfiles. (Except for [~/.config/nvim](https://github.com/shirayu/config_nvim))

## Setup

```bash
sudo apt update
sudo apt install -y git htop jq make rsync shellcheck task-japanese zsh zsh-syntax-highlighting locales tmux wget unar unzip
sudo /usr/sbin/dpkg-reconfigure locales
sudo timedatectl set-timezone Asia/Tokyo

git clone https://github.com/shirayu/config_nvim ~/.config/nvim
gsettings set org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:$(gsettings get org.gnome.Terminal.ProfilesList default | tr -d \')/ font "Moralerspace Argon HWNF 14"

git clone https://github.com/shirayu/dotfiles.git ~/.dotfiles
curl https://mise.run | sh
bash ~/.dotfiles/generate_links.sh
sudo chsh $(whoami) -s $(which zsh)

mise up

~/.config/nvim/setup.sh update
```

### Instruction for the client desktop and laptop PCs (debian+gnome3)

- Register ``mysshagent.sh`` in ``.zsh`` folder to ``gnome-session-properties``
    - The file generated by ``gnome-keyring-daemon`` has the environment variable ``SSH_AUTH_SOCK``
    - ``zshrc.envvar`` uses this variable to user the socket in shells in the ``screen``
