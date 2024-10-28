#!/bin/bash

read -p "Backup current packages to list (b) or restore from list (r)? " asw

case $asw in
    b)
        pacman -Qqe > ~/pacman_packages.txt
        echo "pacman done"
        yay -Qmq > ~/aur_packages.txt
        echo "yay done"
        ;;
    r)
        sudo pacman -S --needed - < ~/pacman_packages.txt
        echo "pacman done"
        yay -S --needed - < ~/aur_packages.txt
        echo "yay done"
        ;;
esac