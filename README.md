
# dotfiles

This is my dotfiles. (Except for [~/.config/nvim](https://github.com/shirayu/config_nvim))

## Setup

```bash
sudo apt update
sudo apt install -y git htop jq make rsync shellcheck task-japanese zsh zsh-syntax-highlighting locales tmux wget unar unzip
sudo /usr/sbin/dpkg-reconfigure locales
sudo timedatectl set-timezone Asia/Tokyo

git clone https://github.com/shirayu/config_nvim ~/.config/nvim

git clone https://github.com/shirayu/dotfiles.git ~/.dotfiles
curl https://mise.run | sh
./setup.py
sudo chsh $(whoami) -s $(which zsh)

mise up

~/.config/nvim/setup.sh update
```

### Setting

`./setup_config.json`
