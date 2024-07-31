#!/bin/bash

connected_monitors=$(xrandr | grep -w "connected" | grep -v "eDP" | awk '{print $1}')
gpumode=$(envycontrol -q)
status=$(acpi -b | awk '{print $3}')

if [ -n "$connected_monitors" ]; then

    if [ "$gpumode" = "integrated" ]; then
    
        echo -e "External monitor(s) connected\nCurrently the system is in $gpumode mode"
        if [[ "$status" == *Charging* || "$status" == *Not* ]]; then
            echo "Laptop is plugged in. Enter sudo password to change GPU mode:"
            sudo envycontrol -s hybrid
            echo "GPU mode changed to hybrid. Initiating system reboot."
            sudo reboot
            
        elif [[ "$status" == *Discharging* ]]; then
            echo "Laptop is not plugged in. Press 1 to enter sudo password, 2 to skip:"
            read -p "Enter your choice: " num
            
            if [ "$num" = 1 ]; then
                sudo envycontrol -s hybrid
                echo "GPU mode changed to hybrid. Initiating system reboot."
                sudo reboot

            elif [ "$num" = 2 ]; then
                echo "GPU mode is in Integrated."
            fi
        fi
        
    elif [ "$gpumode" = "hybrid" ]; then
        echo -e "External monitor(s) connected.\nCurrently the system is in $gpumode mode"
        
        if [[ "$status" == *Discharging* ]]; then
            echo "Laptop is not plugged in. Press 1 to enter sudo password, 2 to skip:"
            read -p "Enter your choice: " num
            
            if [ "$num" = 1 ]; then
                sudo envycontrol -s integrated
                echo "GPU mode changed to integrated. Initiating system reboot."
                sudo reboot
                
            elif [ "$num" = 2 ]; then
                echo "GPU mode is in hybrid."
            fi
        fi
    fi
    
    
else

    if [ "$gpumode" = "hybrid" ]; then
        echo "No external monitor(s) connected."
        
        if [[ "$status" == *Discharging* ]]; then
            echo "Laptop is not plugged in. Enter sudo password to change GPU mode:"
            sudo envycontrol -s integrated
            echo "GPU mode changed to integrated. Initiating system reboot."
            sudo reboot
            
        elif [[ "$status" == *Charging* || "$status" == *Not* ]]; then
            echo "Laptop is plugged in. Press 1 to enter sudo password, 2 to skip:"
            read -p "Enter your choice: " nums
            
            if [ "$nums" = 1 ]; then
                sudo envycontrol -s integrated
                echo "GPU mode changed to integrated. Initiating system reboot."
                sudo reboot
                
            elif [ "$nums" = 2 ]; then
                echo "GPU mode is in hybrid."
            fi
        fi
    fi
fi

