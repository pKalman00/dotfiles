#!/usr/bin/env bash

if [ "$ROFI_RETV" -eq 0 ]; then
    echo -en "\0use-hot-keys\x1ftrue\n"
    cliphist list | while read -r line; do
        content=$(echo "$line" | cut -f2-)
        echo -en "${content}\0info\x1f${line}\n"
    done
elif [ "$ROFI_RETV" -eq 1 ]; then
    echo "$ROFI_INFO" | cliphist decode | wl-copy
elif [ "$ROFI_RETV" -eq 10 ]; then
    echo "$ROFI_INFO" | cliphist delete
elif [ "$ROFI_RETV" -eq 11 ]; then
    cliphist wipe
fi
