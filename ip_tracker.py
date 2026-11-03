import os
import socket
import subprocess
import time
import requests
from datetime import datetime

REPO_PATH = "/home/ayush/Ayush/Ip_repo"
FILE_NAME = "pie.txt" 

TIME_API = "http://worldtimeapi.org/api/ip"

def get_active_ip_address():
    """Fetch the current IP address assigned by the active network (Wi-Fi or Ethernet)."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80)) 
        ip_address = sock.getsockname()[0]
        sock.close()
        return ip_address
    except Exception as e:
        return None

def get_current_time():
    """Fetch the current local time from an online API, fallback to system time."""
    try:
        response = requests.get(TIME_API, timeout=5)
        if response.status_code == 200:
            data = response.json()
            iso_time = data.get("datetime", "")
            if iso_time:
                parsed_time = datetime.fromisoformat(iso_time)
                return parsed_time.strftime("%Y-%m-%d %H:%M:%S")
            
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
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

def sync_with_github(commit_message=None):
    """
    Checks for uncommitted changes or unpushed commits and syncs them to GitHub.
    Returns True if fully synced, False if a network/git error occurred.
    """
    try:
        # 1. Check if there are any uncommitted changes in the local repo
        status = subprocess.run(
            ["git", "-C", REPO_PATH, "status", "--porcelain"], 
            capture_output=True, text=True
        )
        
        if status.stdout.strip():
            msg = commit_message or f"Updated IP at {get_current_time()} (Recovered sync)"
            subprocess.run(["git", "-C", REPO_PATH, "add", FILE_NAME], check=True)
            subprocess.run(["git", "-C", REPO_PATH, "commit", "-m", msg], check=True)
            print(f"Committed local changes: '{msg}'")
            
        # 2. Fetch latest status from origin
        subprocess.run(["git", "-C", REPO_PATH, "fetch", "origin"], check=True)
        
        # 3. Check if we have commits locally that aren't pushed to remote yet
        rev_count = subprocess.run(
            ["git", "-C", REPO_PATH, "rev-list", "--count", "origin/main..main"],
            capture_output=True, text=True, check=True
        )
        
        if int(rev_count.stdout.strip()) > 0:
            print("Unpushed local commits found. Syncing with remote...")
            subprocess.run(["git", "-C", REPO_PATH, "pull", "--rebase", "origin", "main"], check=True)
            subprocess.run(["git", "-C", REPO_PATH, "push", "origin", "main"], check=True)
            print("Successfully pushed to GitHub.")
        
        return True # Everything is perfectly in sync
        
    except subprocess.CalledProcessError as e:
        print(f"Git sync failed (likely due to network transition): {e}")
        return False
    except Exception as e:
        print(f"Unexpected error during sync: {e}")
        return False

def monitor_ip_changes():
    """Continuously monitor for IP address changes (Ethernet or Wi-Fi)."""
    last_ip = read_ip_from_file()
    print(f"Initial IP loaded from file: {last_ip}")
    
    # We start with needs_sync = True on purpose! 
    # This ensures it fixes your current stranded commit the very first time it boots.
    needs_sync = True 

    while True:
        current_ip = get_active_ip_address()
        
        if current_ip and current_ip != last_ip:
            print(f"Network change detected! New IP: {current_ip}")
            write_ip_to_file(current_ip)
            last_ip = current_ip
            needs_sync = True # New data written, trigger a sync attempt
        
        if needs_sync:
            msg = f"Updated IP at {get_current_time()}"
            if sync_with_github(msg):
                needs_sync = False # Successfully pushed, disable the flag
            else:
                print("Will retry push in 10 seconds...")
        
        time.sleep(10)

if __name__ == "__main__":
    print("Starting IP address monitoring and GitHub sync...")
    monitor_ip_changes()
