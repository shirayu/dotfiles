
HISTFILE=~/.zsh_history
HISTSIZE=100000
SAVEHIST=100000


ZSH_SETTING_PATH=$HOME/.zsh/
autoload -U add-zsh-hook

source $ZSH_SETTING_PATH/zshrc.keybind
source $ZSH_SETTING_PATH/zshrc.authsock
source $ZSH_SETTING_PATH/zshrc.envvar
source $ZSH_SETTING_PATH/zshrc.prompt
source $ZSH_SETTING_PATH/zshrc.options
source $ZSH_SETTING_PATH/zshrc.alias
source $ZSH_SETTING_PATH/zshrc.change_title_bar
source $ZSH_SETTING_PATH/zshrc.peco

# cd #go home-dir

NO_SCREEN_HOSTS=(orchid reed)
if (( ! ${NO_SCREEN_HOSTS[(I)`hostname`]} )); then

    #CDD    http://blog.m4i.jp/entry/2012/01/26/064329
    autoload -Uz compinit
    compinit
    source $ZSH_SETTING_PATH/zshrc.cdd
    add-zsh-hook chpwd _cdd_chpwd


    #screen
#     source $ZSH_SETTING_PATH/zshrc.screen
#     screen -xR -U

    #tmux
    source $ZSH_SETTING_PATH/zshrc.tmux
    if [ $SHLVL = 1 ]; then
      tmux attach || tmux
    fi

fi
