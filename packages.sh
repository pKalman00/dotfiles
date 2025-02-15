#!/bin/bash

read -p "Backup current packages to list (b) or restore from list (r)? " asw

case $asw in
b)
    # get list of installed packages
    yay -Qmq >~/aur_packages.txt
    echo "yay done"
    pacman -Qqe >~/pacman_packages.txt
    echo "pacman done"
    # filter aur from pacman
    grep -v -Fxf ~/aur_packages.txt ~/pacman_packages.txt >~/pacman_packages.tmp
    rsync -arz ~/pacman_packages.tmp ~/pacman_packages.txt
    rm ~/pacman_packages.tmp
    # prompt to sync to the repo (not applicable in case the script is run separately)
    read -p "Sync lists to repo? (y/n) " asw
    case $asw in
    y)
        rsync -arz ~/aur_packages.txt packages/aur_packages.txt
        rsync -arz ~/pacman_packages.txt packages/pacman_packages.txt
        ;;
    esac
    ;;
r)
    # restore from the files (remember to use the py script to update local files)
    yay -S --needed - <~/aur_packages.txt
    echo "yay done"
    sudo pacman -S --needed - <~/pacman_packages.txt
    echo "pacman done"
    ;;
esac
