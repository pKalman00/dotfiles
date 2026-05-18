#!/usr/bin/env bash

# Path to the battery charge threshold file
THRESHOLD_FILE="/sys/class/power_supply/BAT0/charge_control_end_threshold"

# Get the current threshold
CURRENT_VAL=$(cat "$THRESHOLD_FILE")

# Define some common presets, but Rofi will also allow custom typing
PRESETS="80\n100"

# Show Rofi dmenu
# -p: The prompt text
# -mesg: A message box showing the current status
# -theme-str: We override your global width for this specific small window
# CHOICE=$(echo -e "$PRESETS" | rofi -dmenu \
#     -p "Charge Limit" \
#     -mesg "Current: <b>$CURRENT_VAL%</b>" \
#     -theme-str 'window { width: 15%; } listview { lines: 3; } entry { placeholder: "Set % (1-100)"; }')
CHOICE=$(echo -e "$PRESETS" | rofi -dmenu \
    -p "󱐋" \
    -mesg "Current: <b>$CURRENT_VAL%</b>" \
    -theme-str 'window { width: 20%; } listview { lines: 3; } entry { placeholder: "Set % (1-100)"; }' )

# Exit if the user hits Escape/cancels
if [ -z "$CHOICE" ]; then
    exit 0
fi

# Validate that the input is a number between 1 and 100
if [[ "$CHOICE" =~ ^[0-9]+$ ]] && [ "$CHOICE" -le 100 ] && [ "$CHOICE" -ge 1 ]; then
    # Write the value using run0
    # We use 'tee' because simple redirection (>) happens before run0 elevates permissions
    if echo "$CHOICE" | run0 --background="" tee "$THRESHOLD_FILE" > /dev/null; then
        notify-send "Battery Limit" "Threshold set to $CHOICE%" -i battery
    else
        notify-send "Battery Limit" "Failed to set threshold. Check permissions." -u critical
    fi
else
    notify-send "Battery Limit" "Invalid input: $CHOICE (Must be 1-100)" -u critical
fi
