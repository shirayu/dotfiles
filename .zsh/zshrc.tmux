

function _tmux_myprecmd () {
    if [ "$TMUX" ]; then
        tmux rename-window "${PWD##*/}"
    else
        echo -ne "\033]0;`hostname`\007"
    fi
}
add-zsh-hook precmd _tmux_myprecmd


function _tmux_mypreexec () {
    if [ "$TMUX" ]; then
        tmux rename-window "$1"
    fi
}
add-zsh-hook preexec _tmux_mypreexec

