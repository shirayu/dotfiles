
# dotfiles

This is my dotfiles. (Except for [.vim](https://github.com/shirayu/dot_vim))

## Make the default shell (the latest) zsh

- ``.bash_profile.sample`` is for the environment where users can't use ``chsh`` and the login shell is bash.
- ``.zshenv.sample`` is for the environment where users need to set proxy variables

## Instruction for the client desktop and laptop PCs (debian+gnome3)

- Register ``mysshagent.sh`` in ``.zsh`` folder to ``gnome-session-properties``
    - The file generated by ``gnome-keyring-daemon`` has the environment variable ``SSH_AUTH_SOCK``
    - ``zshrc.envvar`` uses this variable to user the socket in shells in the ``screen``

## Other tools

Run ``./command_check/check.py`` to list up uninstalled softwares.

### Perl (cpanminus)

```sh
wget https://raw.githubusercontent.com/miyagawa/cpanminus/master/cpanm -O /tmp/cpanm
export PERL_CPANM_OPT="--local-lib=$HOME/local/lib/perl"
cat /tmp/cpanm | perl - App::cpanminus
```

## obsoleted files

- screen
