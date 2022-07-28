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

# Reported data

Here's an example of reported data:

    {
    "SDcard": {
        "Total MB": 119494,
        "Used MB": 7174,
        "Available MB": 106205,
        "Percent used": 7
    },
    "ramInfo": {
        "Total KB": 3931056,
        "used KB": 877428,
        "Free KB": 2535608
    },
    "processor_frequencey": 1800000,
    "processor_utilization": {
        "cpu": "all",
        "usr": 4.85,
        "nice": 0,
        "sys": 0.47,
        "iowait": 0.06,
        "irq": 0,
        "soft": 0.07,
        "steal": 0,
        "guest": 0,
        "gnice": 0,
        "idle": 94.56
    },
    "uptime": {
        "hours": 3.767275
    },
    "measure_temperature": 56.4,
    "throttled": {
        "Under-voltage": false,
        "ARM frequency capped": false,
        "Currently throttled": false,
        "Soft temperature limit active": false,
        "Under-voltage has occurred since last reboot": false,
        "Throttling has occurred since last reboot": false,
        "ARM frequency capped has occurred since last reboot": false,
        "Soft temperature limit has occurred": false
    },
    "load_average": {
        "load average 1min": 0.17,
        "load average 5min": 0.3,
        "load average 15min": 0.29
    },
    "Timedatectl": {
        "Timezone": "America/New_York",
        "LocalRTC": "no",
        "CanNTP": "yes",
        "NTP": "yes",
        "NTPSynchronized": "yes",
        "TimeUSec": "Thu 2022-07-28 13:30:01 EDT",
        "FallbackNTPServers": "0.debian.pool.ntp.org 1.debian.pool.ntp.org 2.debian.pool.ntp.org 3.debian.pool.ntp.org",
        "ServerName": "0.debian.pool.ntp.org",
        "ServerAddress": "204.93.207.12",
        "RootDistanceMaxUSec": "5s",
        "PollIntervalMinUSec": "32s",
        "PollIntervalMaxUSec": "34min 8s",
        "PollIntervalUSec": "34min 8s",
        "NTPMessage": "{ Leap=0, Version=4, Mode=4, Stratum=3, Precision=-20, RootDelay=32.180ms, RootDispersion=49.880ms, Reference=CE37404D, OriginateTimestamp=Thu 2022-07-28 13:08:45 EDT, ReceiveTimestamp=Thu 2022-07-28 13:08:45 EDT, TransmitTimestamp=Thu 2022-07-28 13:08:45 EDT, DestinationTimestamp=Thu 2022-07-28 13:08:45 EDT, Ignored=no PacketCount=12, Jitter=2.954ms }",
        "Frequency": "-927975"
    },
    "backlog_image_count": 3
    }