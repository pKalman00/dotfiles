#!/bin/bash

read -p "Backup current packages to list (b) or restore from list (r)? " asw

case $asw in
    b)
        pacman -Qqe > ~/pacman_packages.txt
        echo "pacman done"
        yay -Qmq > ~/aur_packages.txt
        echo "yay done"
        read -p "Sync lists to repo? (y/n) " asw
        case $asw in
            y)
                cp -f ~/pacman_packages.txt packages/pacman_packages.txt
                cp -f ~/aur_packages.txt packages/aur_packages.txt
                ;;
        esac
        ;;
    r)
        sudo pacman -S --needed - < ~/pacman_packages.txt
        echo "pacman done"
        yay -S --needed - < ~/aur_packages.txt
        echo "yay done"
        ;;
esac