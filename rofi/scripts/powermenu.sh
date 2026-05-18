#!/usr/bin/env bash

# Options
shutdown='  Power off'
reboot='󰑐  Reboot'
lock='  Lock'
suspend='󰤄  Suspend'
logout='󰍃  Log out'

# Output options for Rofi
# if [ "$#" -eq 0 ]; then
#     echo -e "$shutdown\n$reboot\n$lock\n$suspend\n$logout\x00urgent\x1f0"
# else
if [ "$#" -eq 0 ]; then
    # This line tells Rofi to mark the 0th index (Power off) as urgent
    echo -en "\0urgent\x1f0\n"
    
    # Now print the options as usual
    echo -e "$shutdown"
    echo -e "$reboot"
    echo -e "$lock"
    echo -e "$suspend"
    echo -e "$logout"
else
    # Actions based on selection
    case $1 in
        $shutdown)
            systemctl poweroff ;;
            # hyprshutdown -t 'Shutting down...' --post-cmd 'shutdown -P 0' ;;
        $reboot)
            systemctl reboot ;;
            # hyprshutdown -t 'Restarting...' --post-cmd 'reboot' ;;
        $lock)
            # Change this to your locker (e.g., swaylock, hyprlock)
            hyprlock ;; 
        $suspend)
            systemctl suspend ;;
        $logout)
            # Assuming Hyprland based on your previous config path
            # hyprctl dispatch "hl.dsp.exit()" ;;
            hyprshutdown >/dev/null 2>&1 && hyprshutdown || hyprctl dispatch 'hl.dsp.exit()' ;;
    esac
fi
