
HISTFILE=~/.zsh_history
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_IGNORE_SPACE
setopt HIST_FIND_NO_DUPS
setopt HIST_REDUCE_BLANKS
setopt HIST_NO_STORE
HISTSIZE=100000
SAVEHIST=100000

# Loading complement setting, and set it.
autoload -Uz compinit && compinit -u -C
# highlighting complement candidates
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

source $ZSH_SETTING_PATH/zshrc.authsock
source $ZSH_SETTING_PATH/zshrc.prompt
source $ZSH_SETTING_PATH/zshrc.keybind
source $ZSH_SETTING_PATH/zshrc.options
source $ZSH_SETTING_PATH/zshrc.alias
source $ZSH_SETTING_PATH/zshrc.change_title_bar
source $ZSH_SETTING_PATH/zshrc.peco

#tmux
source $ZSH_SETTING_PATH/zshrc.tmux
if [[ $SHLVL = 1 ]]; then
  tmux attach || tmux
fi

