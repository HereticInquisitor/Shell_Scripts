#!/bin/bash

# System Cleanup Script

# Remove temporary files
echo "Removing temporary files..."
sudo rm -rf /tmp/*

# Clear package manager cache
echo "Clearing package manager cache..."
sudo pacman -Sc --noconfirm  # For Manjaro, adjust for your package manager

# Remove old logs
echo "Removing old log files..."
sudo find /var/log -type f -name "*.log" -delete

# Remove old versions of installed packages
echo "Removing old versions of installed packages..."
sudo paccache -r

# Clean up orphaned packages
echo "Removing orphaned packages..."
sudo pacman -Rns $(pacman -Qdtq) --noconfirm  # For Manjaro, adjust for your package manager

echo "System cleanup completed."
