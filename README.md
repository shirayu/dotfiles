
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
./setup.py --test
sudo chsh $(whoami) -s $(which zsh)

mise up

~/.config/nvim/setup.sh update
```

### Setting

`./setup_config.json`

## Commands

### diary

Create or open a daily markdown diary.

```bash
diary              # today
diary +1           # tomorrow
diary +3           # 3 days later
diary -1           # yesterday
diary 2026-06-05
diary 0605
```

Diary files are created under `~/secret/diary/YYYY/MM/DD.md` by default.

## Test

```bash
./setup.py --test
```
