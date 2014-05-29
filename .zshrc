
HISTFILE=~/.zsh_history
HISTSIZE=100000
SAVEHIST=100000


ZSH_SETTING_PATH=$HOME/.zsh/
autoload -U add-zsh-hook

source $ZSH_SETTING_PATH/zshrc.keybind
source $ZSH_SETTING_PATH/zshrc.envvar
source $ZSH_SETTING_PATH/zshrc.prompt
source $ZSH_SETTING_PATH/zshrc.options
source $ZSH_SETTING_PATH/zshrc.alias
source $ZSH_SETTING_PATH/zshrc.change_title_bar

cd #go home-dir

NO_SCREEN_HOSTS=(orchid reed)
if (( ! ${NO_SCREEN_HOSTS[(I)`hostname`]} )); then
    source $ZSH_SETTING_PATH/zshrc.screen
    autoload -U compinit
    compinit
    source $ZSH_SETTING_PATH/zshrc.cdd
    add-zsh-hook chpwd _reg_pwd_screennum


    #screen
    # -x Attach to a not detached screen session
    # -R attempts  to  resume  the youngest (in terms of creation time) detached screen session it finds
    # Gnu Screen starts automatically.
    # If you don't use screen, please detach or eixt(kill screen).
    screen -xR -U
fi
