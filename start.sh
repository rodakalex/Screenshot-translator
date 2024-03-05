#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "This script must be run with sudo"
    exit 1
fi

git pull
sudo systemctl start docker
