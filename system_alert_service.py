import os
import csv
import psutil
import docker
from datetime import datetime
import time
from dotenv import load_dotenv
import socket
import requests

# Load environment variables from .env file
load_dotenv()

# Function to send Telegram message
def send_telegram_message(message):
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, params=params)
    if response.status_code != 200:
        print(f"Failed to send Telegram message: {response.text}")

# Function to write log message to file with timestamp
def log_message(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_file = os.getenv('LOG_FILE')
    with open(log_file, 'a') as f:
        f.write(f"{timestamp}: {message}\n")

# Function to get system metrics
def get_system_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    return cpu_usage, memory_usage, disk_usage

# Function to check Docker container status
def check_container_status():
    client = docker.from_env()
    containers = client.containers.list()
    running_containers = [container.name for container in containers if container.status == 'running']
    return running_containers

# Function to write system metrics to CSV file
def write_to_csv(cpu_usage, memory_usage, disk_usage):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    header = ['Timestamp', 'CPU Usage (%)', 'Memory Usage (%)', 'Disk Usage (%)']
    data = [timestamp, cpu_usage, memory_usage, disk_usage]
    
    # Check if the file exists and is empty
    file_exists = os.path.isfile(os.getenv('CSV_FILE'))
    file_empty = os.stat(os.getenv('CSV_FILE')).st_size == 0

    with open(os.getenv('CSV_FILE'), 'a') as csvfile:
        writer = csv.writer(csvfile)

        # Write header if the file is empty
        if not file_exists or file_empty:
            writer.writerow(header)

        writer.writerow(data)

# Main loop
previous_running_containers = []
server_name = os.getenv('SERVER_NAME')  # Get server name from .env file
server_ip = socket.gethostbyname(socket.gethostname())  # Get server IP dynamically
while True:
    try:
        # Get system metrics
        cpu_usage, memory_usage, disk_usage = get_system_metrics()

        # Write system metrics to CSV file
        write_to_csv(cpu_usage, memory_usage, disk_usage)

        # Check if any metrics exceed thresholds
        if cpu_usage > int(os.getenv('CPU_THRESHOLD')):
            message = f'High CPU Usage Alert: CPU usage exceeded threshold: {cpu_usage}% on server {server_name} ({server_ip})'
            log_message(message)
            send_telegram_message(message)
        if memory_usage > int(os.getenv('MEMORY_THRESHOLD')):
            message = f'High Memory Usage Alert: Memory usage exceeded threshold: {memory_usage}% on server {server_name} ({server_ip})'
            log_message(message)
            send_telegram_message(message)
        if disk_usage > int(os.getenv('DISK_THRESHOLD')):
            message = f'High Disk Usage Alert: Disk usage exceeded threshold: {disk_usage}% on server {server_name} ({server_ip})'
            log_message(message)
            send_telegram_message(message)

        # Check Docker container status
        running_containers = check_container_status()
        if set(previous_running_containers) - set(running_containers):
            stopped_containers = set(previous_running_containers) - set(running_containers)
            message = f'Container Stopped Alert: The following Docker containers have stopped: {", ".join(stopped_containers)} on server {server_name} ({server_ip})'
            log_message(message)
            send_telegram_message(message)
        previous_running_containers = running_containers

        # Wait for 20 seconds before checking again (for testing)
        time.sleep(20)
    except Exception as e:
        # Log any exceptions and continue running
        log_message(f'Error: {e}')
