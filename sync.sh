#!/bin/bash

# Make sure you have a host with this name in your ~/.ssh/config
SERVER_ALIAS="tv"
LOCAL_REPO_PATH=$(pwd)
REMOTE_BASE_PATH="/tmp"

rsync -avz -e ssh --chown=root:root --exclude '.git' $LOCAL_REPO_PATH/ $SERVER_ALIAS:$REMOTE_BASE_PATH