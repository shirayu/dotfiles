function _tmux_sanitize_winname() {
    local name="$1"

    # For tmux 3.7
    # cf: https://www.reddit.com/r/tmux/comments/1uisgmr/comment/oui4uhi/
    name="${name//./․}"
    name="${name//:/∶}"
    echo "$name"
}

function _tmux_myprecmd() {
    if [ "$TMUX" ]; then
        local winname="${PWD##*/}"
        tmux rename-window "$(_tmux_sanitize_winname "${winname:-/}")"
    else
        echo -ne "\033]0;$(hostname)\007"
    fi
}
add-zsh-hook precmd _tmux_myprecmd

function _tmux_mypreexec() {
    if [ "$TMUX" ]; then
        tmux rename-window "$(_tmux_sanitize_winname "$1")"
    fi
}
add-zsh-hook preexec _tmux_mypreexec
