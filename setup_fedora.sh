#!/bin/bash

# install dnf packages
xargs -a ./packages.txt sudo dnf install -y

# install oh-my-posh
curl -s https://ohmyposh.dev/install.sh | bash -s

# install homebrew
curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh