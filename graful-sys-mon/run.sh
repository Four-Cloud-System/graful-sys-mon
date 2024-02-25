#!/bin/bash

# Function to update system packages
update_system_packages() {
    sudo apt update
}

# Function to install Python 3 and pip
install_python_packages() {
    sudo apt install -y python3 python3-pip
}

# Function to install Python libraries
install_python_libraries() {
    pip install psutil docker python-dotenv

}

# Function to read existing environment variables from .env file
read_env_variables() {
    source "$SCRIPT_DIR/.env" || exit 1
}

# Function to prompt for thresholds and server name
prompt_user_input() {
    read -p "Enter CPU threshold (default $CPU_THRESHOLD%): " new_cpu_threshold
    cpu_threshold=${new_cpu_threshold:-$CPU_THRESHOLD}
    read -p "Enter Memory threshold (default $MEMORY_THRESHOLD%): " new_memory_threshold
    memory_threshold=${new_memory_threshold:-$MEMORY_THRESHOLD}
    read -p "Enter Disk threshold (default $DISK_THRESHOLD%): " new_disk_threshold
    disk_threshold=${new_disk_threshold:-$DISK_THRESHOLD}
    read -p "Enter Server name (default $SERVER_NAME): " new_server_name
    server_name=${new_server_name:-$SERVER_NAME}
}

# Function to update .env file with new values
update_env_file() {
    sed -i "s/CPU_THRESHOLD=.*/CPU_THRESHOLD=$cpu_threshold/" "$SCRIPT_DIR/.env"
    sed -i "s/MEMORY_THRESHOLD=.*/MEMORY_THRESHOLD=$memory_threshold/" "$SCRIPT_DIR/.env"
    sed -i "s/DISK_THRESHOLD=.*/DISK_THRESHOLD=$disk_threshold/" "$SCRIPT_DIR/.env"
    sed -i "s/SERVER_NAME=.*/SERVER_NAME='$server_name'/" "$SCRIPT_DIR/.env"
}

Function to run the Python script
run_python_script() {
    python3 "$SCRIPT_DIR/system_alert_service.py"
}

# Main function
main() {
    update_system_packages
    install_python_packages
    install_python_libraries
    read_env_variables
    prompt_user_input
    update_env_file
    run_python_script
}

# Get the directory of the script
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

# Execute main function
main
