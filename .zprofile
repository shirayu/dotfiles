
#ssh-agent
export SSH_AGENT_FILE=/tmp/.ssh-agent-`hostname`-${USERNAME}
export SSH_SOCK_LIST=/tmp/.ssh-sock-`hostname`-${USERNAME}

#TODO check the file owner is *me*

#save my sock
echo ${SSH_AUTH_SOCK} >> ${SSH_SOCK_LIST}

# Read current ssh-agent setting
# [!]  $SSH_AUTH_SOCK will be overwrite
if [ -e ${SSH_AGENT_FILE} ]; then
    source ${SSH_AGENT_FILE}
    export SSH_AUTH_SOCK=${SSH_AUTH_SOCK}
fi

