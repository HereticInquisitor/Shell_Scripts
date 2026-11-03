import os
import socket
import subprocess
import time
import requests
from datetime import datetime

REPO_PATH = "/home/ayush/Ayush/Ip_repo"
FILE_NAME = "pie.txt" 

# Swapped to a free, keyless API that auto-detects timezone via IP
TIME_API = "http://worldtimeapi.org/api/ip"

def get_active_ip_address():
    """Fetch the current IP address assigned by the active network (Wi-Fi or Ethernet)."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connects to Google's DNS to determine the default network interface
        sock.connect(("8.8.8.8", 80)) 
        ip_address = sock.getsockname()[0]
        sock.close()
        return ip_address
    except Exception as e:
        print(f"Error fetching IP address: {e}")
        return None

def get_current_time():
    """Fetch the current local time from an online API, fallback to system time."""
    try:
        response = requests.get(TIME_API, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # WorldTimeAPI returns ISO 8601 format, e.g., "2026-11-03T19:31:00.123456+05:30"
            iso_time = data.get("datetime", "")
            if iso_time:
                # Parse and format it cleanly
                parsed_time = datetime.fromisoformat(iso_time)
                return parsed_time.strftime("%Y-%m-%d %H:%M:%S")
            
        print(f"API request failed with status {response.status_code}. Using system time.")
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"Error fetching time from API: {e}. Using system time.")
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def read_ip_from_file():
    """Read the currently saved IP address from the file."""
    file_path = f"{REPO_PATH}/{FILE_NAME}"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                return f.read().strip()
        except Exception as e:
            print(f"Error reading IP from file: {e}")
    return None

def write_ip_to_file(ip_address):
    """Write the current IP address to the file."""
    try:
        file_path = f"{REPO_PATH}/{FILE_NAME}"
        with open(file_path, "w") as f:
            f.write(ip_address)
        print(f"Updated {FILE_NAME} with IP: {ip_address}")
    except Exception as e:
        print(f"Error writing IP to file: {e}")

def commit_and_push_changes():
    """Commit and push changes to the GitHub repository."""
    try:
        current_time = get_current_time()
        commit_message = f"Updated IP at {current_time}"

        subprocess.run(["git", "-C", REPO_PATH, "add", FILE_NAME], check=True)
        
        subprocess.run(
            ["git", "-C", REPO_PATH, "commit", "-m", commit_message],
            check=True,
        )
        
        subprocess.run(
            ["git", "-C", REPO_PATH, "push", "origin", "main"], check=True
        )
        
        print(f"Committed and pushed changes to the main branch: '{commit_message}'")
    except subprocess.CalledProcessError as e:
        print(f"Error committing or pushing changes: {e}")

def monitor_ip_changes():
    """Continuously monitor for IP address changes (Ethernet or Wi-Fi)."""
    # Read the IP from the file first to prevent redundant commits on script restart
    last_ip = read_ip_from_file()
    print(f"Initial IP loaded from file: {last_ip}")

    while True:
        current_ip = get_active_ip_address()
        
        if current_ip and current_ip != last_ip:
            print(f"Network change detected! New IP: {current_ip}")
            write_ip_to_file(current_ip)
            commit_and_push_changes()
            last_ip = current_ip
        else:
            print("No IP address change detected.")
        
        time.sleep(10)

if __name__ == "__main__":
    print("Starting IP address monitoring and GitHub sync...")
    monitor_ip_changes()
