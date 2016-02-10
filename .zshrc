
HISTFILE=~/.zsh_history
HISTSIZE=100000
SAVEHIST=100000

#FPATH
MYFPATH=/usr/share/zsh/4.3.11/functions
if [ -e $MYFPATH ];then
    export FPATH=$FPATH:$MYFPATH
fi
MYFPATH=$HOME/local/share/zsh/5.0.7/functions
if [ -e $MYFPATH ];then
    export FPATH=$MYFPATH:$FPATH
fi

# Loading complement setting, and set it.
autoload -Uz compinit && compinit -u -C
# highlighting complement canditates
autoload colors
zstyle ':completion:*' list-colors "${LS_COLORS}"
zstyle ':completion:*:default' list-colors ${(s.:.)LS_COLORS}

autoload -U add-zsh-hook

if [[ $ZSH_SETTING_PATH == '' ]]; then
    export ZSH_SETTING_PATH=$HOME/.zsh/
    source $ZSH_SETTING_PATH/zshrc.envvar
fi

if [ -e $GOROOT/misc/zsh/go ]; then
    source $GOROOT/misc/zsh/go

    __customized_go_tool_complete() {
        if [[ "${words[2]}" = "run" ]] ;then
            _files ; #suggest all file names
            if [[ $CURRENT -lt 4 ]]; then
                __go_tool_complete ;
            fi
        else
            __go_tool_complete ;
        fi
    }
    compdef __customized_go_tool_complete go
fi

OLD_ZSH_HOSTS=(orchid reed lotus)
if (( ! ${OLD_ZSH_HOSTS[(I)`hostname -s`]} )); then
    source $ZSH_SETTING_PATH/zshrc.authsock
    source $ZSH_SETTING_PATH/zshrc.prompt
fi

source $ZSH_SETTING_PATH/zshrc.gxp
source $ZSH_SETTING_PATH/zshrc.keybind
source $ZSH_SETTING_PATH/zshrc.options
source $ZSH_SETTING_PATH/zshrc.alias
source $ZSH_SETTING_PATH/zshrc.change_title_bar
source $ZSH_SETTING_PATH/zshrc.peco

# cd #go home-dir

NO_SCREEN_HOSTS=(orchid reed lotus)
if (( ! ${NO_SCREEN_HOSTS[(I)`hostname -s`]} )); then

    #CDD    http://blog.m4i.jp/entry/2012/01/26/064329
#     source $ZSH_SETTING_PATH/zshrc.cdd
#     add-zsh-hook chpwd _cdd_chpwd


    #screen
#     source $ZSH_SETTING_PATH/zshrc.screen
#     screen -xR -U

    #tmux
    source $ZSH_SETTING_PATH/zshrc.tmux
    if [ $SHLVL = 1 ]; then
      tmux attach || tmux
    fi

fi
