#!/bin/bash

# System Monitoring Script

# Function to display CPU usage
function cpu_usage() {
    echo "CPU Usage:"
    top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1"%"}'
}

# Function to display memory usage
function memory_usage() {
    echo "Memory Usage:"
    free -m | awk 'NR==2{printf "%.2f%%\n", $3*100/$2 }'
}

# Function to display disk usage
function disk_usage() {
    echo "Disk Usage:"
    df -h | awk '$NF=="/"{printf "%s\n", $5}'
}

# Function to display system uptime
function system_uptime() {
    echo "System Uptime:"
    uptime -p
}

# Function to display network information
function network_info() {
    echo "Network Information:"
    ip addr show
}

function main() {
    cpu_usage
    memory_usage
    disk_usage
    system_uptime
    network_info
}

main
