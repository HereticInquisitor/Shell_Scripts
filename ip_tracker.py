import socket
import subprocess
import time
import requests
from datetime import datetime

REPO_PATH = "/home/ayush/Ayush/Ip_repo"
FILE_NAME = "pie.txt" 


# Unable to fetch time 
TIME_API = "http://api.timezonedb.com/v2.1/get-time-zone"
API_KEY = "XTBJR3C5778K"  


def get_wifi_ip_address():
    """Fetch the current IP address assigned by the Wi-Fi network."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))  # Google's public DNS server so that it doesn't return the loop back address
        ip_address = sock.getsockname()[0]
        sock.close()
        return ip_address
    except Exception as e:
        print(f"Error fetching Wi-Fi IP address: {e}")
        return None

def get_current_time():
    """Fetch the current local time from an online API."""
    try:
        params = {
            "key": API_KEY,
            "format": "json",
            "by": "zone",
            "zone": "auto",
        }
        response = requests.get(TIME_API, params=params)
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "OK":
                local_time = data["formatted"]
                return local_time
            else:
                print(f"Error fetching time: {data['message']}")
                return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            print(f"Failed to fetch time from API. HTTP status code: {response.status_code}")
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"Error fetching time from API: {e}")
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


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
        # Nhi chal rha for some reason
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
        
        print(f"Committed and pushed changes to the main branch: {commit_message}")
    except subprocess.CalledProcessError as e:
        print(f"Error committing or pushing changes: {e}")

def monitor_ip_changes():
    """Continuously monitor for IP address changes."""
    last_ip = None

    while True:
        current_ip = get_wifi_ip_address()
        if current_ip and current_ip != last_ip:
            print(f"IP address changed. New IP: {current_ip}")
            write_ip_to_file(current_ip)
            commit_and_push_changes()
            last_ip = current_ip
        else:
            print("No IP address change detected.")
        time.sleep(10)

if __name__ == "__main__":
    print("Starting IP address monitoring and GitHub sync...")
    monitor_ip_changes()
