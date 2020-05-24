HISTFILE=~/.zsh_history
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_IGNORE_SPACE
setopt HIST_FIND_NO_DUPS
setopt HIST_REDUCE_BLANKS
setopt HIST_NO_STORE
export HISTSIZE=100000
export SAVEHIST=100000

# Loading complement setting, and set it.
if [ -e "$HOME/local/opt/tmsu/misc/zsh" ]; then
    FPATH="$HOME/local/opt/tmsu/misc/zsh:$FPATH"
fi
autoload -Uz compinit && compinit -u -C

autoload -U add-zsh-hook

if [[ "${ZSH_SETTING_PATH}" == '' ]]; then
    export ZSH_SETTING_PATH=$HOME/.zsh/
    source "${ZSH_SETTING_PATH}/zshrc.envvar"
fi

# highlighting complement candidates
autoload colors
export LS_COLORS='rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:'
zstyle ':completion:*' list-colors "${LS_COLORS}"
zstyle ':completion:*:default' list-colors "${(s.:.)LS_COLORS}"

if [ -e "$GOROOT/misc/zsh/go" ]; then
    source "$GOROOT/misc/zsh/go"

    __customized_go_tool_complete() {
        if [[ ${words[2]} == "run" ]]; then
            _files #suggest all file names
            if [[ $CURRENT -lt 4 ]]; then
                __go_tool_complete
            fi
        else
            __go_tool_complete
        fi
    }
    compdef __customized_go_tool_complete go
fi

source "$ZSH_SETTING_PATH/zshrc.authsock"
source "$ZSH_SETTING_PATH/zshrc.prompt"
source "$ZSH_SETTING_PATH/zshrc.keybind"
source "$ZSH_SETTING_PATH/zshrc.options"
source "$ZSH_SETTING_PATH/zshrc.alias"
source "$ZSH_SETTING_PATH/zshrc.change_title_bar"
source "$ZSH_SETTING_PATH/zshrc.peco"
source "$ZSH_SETTING_PATH/zshrc.gcp"

#tmux
source "$ZSH_SETTING_PATH/zshrc.tmux"
if [[ $SHLVL == 1 ]]; then
    tmux attach || tmux
fi
