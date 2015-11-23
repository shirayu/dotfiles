

# remove my sock name
if [ "${SSH_AUTH_SOCK}" != "" ];then
    grep -v ${SSH_AUTH_SOCK}  ${SSH_SOCK_LIST} >  ${SSH_SOCK_LIST}.bk
    mv -f ${SSH_SOCK_LIST}.bk ${SSH_SOCK_LIST}
fi
