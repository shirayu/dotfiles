#!/bin/sh
SSH_AGENT_FILE=/tmp/.ssh-agent-$(hostname)-${USERNAME}
/usr/bin/gnome-keyring-daemon --start --components=ssh > "${SSH_AGENT_FILE}"

