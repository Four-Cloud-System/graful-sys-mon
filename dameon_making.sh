#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

# Define the path to the alert service file
ALERT_SERVICE_FILE="$SCRIPT_DIR/alert.service"

# Create the alert service file
echo "
[Unit]
Description=Alert Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $SCRIPT_DIR/system_alert_service.py
WorkingDirectory=$SCRIPT_DIR
Restart=always

[Install]
WantedBy=multi-user.target
" > "$ALERT_SERVICE_FILE"

# Display the content of the alert service file
cat "$ALERT_SERVICE_FILE"
