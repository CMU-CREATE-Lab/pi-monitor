# Introduction

This is the pi-monitor project, which will reports many stats from your Raspberry Pi to stat.createlab.org.

# Installation

Install a recent version of python3 (>=3.6)

    sudo apt update
    sudo apt install sysstat
    /usr/bin/pip3 install python-dateutil

    cd ~
    git clone --recursive https://github.com/CMU-CREATE-Lab/pi-monitor.git
    cd pi-monitor

    # Test
    /usr/bin/python3 monitor.py 

    # Look for results here:
    https://stat.createlab.org/?serviceFilter=RPi+status

    # Add to your crontab to run on reboot and every 5 minutes
    crontab -e
    # Add these lines at the end of your user crontab, replacing <username> with your username:

    # Run monitor.py every 5 minutes
    */5 * * * * /usr/bin/python3 /home/<username>/pi-monitor/monitor.py
    # Run monitor.py upon reboot
    @reboot /usr/bin/python3 /home/<username>/pi-monitor/monitor.py --reboot
