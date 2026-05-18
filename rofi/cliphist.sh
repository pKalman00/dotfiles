#!/usr/bin/env bash

if [ "$#" -eq 0 ]; then
    # Stage 1: Feed the list to Rofi
    cliphist list
else
    # Stage 2: Handle the selection
    # Use 'echo -n' and 'cliphist decode' to get the original content back to the clipboard
    echo "$1" | cliphist decode | wl-copy
fi
