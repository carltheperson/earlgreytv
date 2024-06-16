#!/bin/bash

# Make sure you have a host with this name in your ~/.ssh/config
SERVER_ALIAS="tv"

# User
rsync -avz -e ssh --chown=root:root --exclude '.git' "$(pwd)/config_files/" $SERVER_ALIAS:/

# Root
# A crazy solution because I want to be promted for the root password and won't create ssh keys for user root
# ROOT_SCRIPT_CONTENT=$(cat "$(pwd)/config_files/usr/lib/systemd/system-sleep/custom-suspend.sh")
# ROOT_SCRIPT_DEST="/usr/lib/systemd/system-sleep/custom-suspend.sh"
# ssh $SERVER_ALIAS -t "echo '$ROOT_SCRIPT_CONTENT' | sudo tee $ROOT_SCRIPT_DEST > /dev/null; sudo chmod +x $ROOT_SCRIPT_DEST"