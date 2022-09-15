# Introduction

This is the pi-monitor project, which will reports many stats from your Raspberry Pi to stat.createlab.org.

# Installation

Make sure you have a recent version of python3 (>=3.6)

    /usr/bin/python3 --version

(If you want to use python3 from a different directory, for now you'll need to hand-edit install.py after cloning and before running install.py below)

Clone into your homedir, and install.  Okay to do this either as a standard user, or as root.  This will handle dependencies and plug into the current user's crontab

    cd ~
    git clone --recursive https://github.com/CMU-CREATE-Lab/pi-monitor.git
    cd pi-monitor
    # if needed, hand edit install.py to change path to python3 if /usr/bin/python3 isn't what you want to use
    ./install.py

# Update to new version remotely via ssh

    ssh <hostname> "cd pi-monitor && git pull && git submodule update && ./install.py"

# Reported data

Here's an example of reported data:

    {
        "ImageBacklogCnt": 1,
        "CpuTempC": 51.12,
        "GpuTempC": 51.1,
        "UptimeHrs": 27.78,
        "SDcard": {
            "PctUsed": 4,
            "TotalGB": 120
        },
        "RAM": {
            "PctUsed": 21.1,
            "TotalGB": 3.93
        },
        "LoadAvg": {
            "1min": 0.26,
            "5min": 0.19,
            "15min": 0.31
        },
        "CpuUtil": {
            "cpu": "all",
            "usr": 3.08,
            "nice": 0,
            "sys": 2.44,
            "iowait": 0.04,
            "irq": 0,
            "soft": 0.14,
            "steal": 0,
            "guest": 0,
            "gnice": 0,
            "idle": 94.31
        },
        "CpuFreqGhz": 1.8,
        "Throttling": {
            "Undervolt": false,
            "ARMFreqCapped": false,
            "Throttled": false,
            "SoftTempLimit": false,
            "UndervoltSinceBoot": false,
            "ThrottledSinceBoot": false,
            "ARMFreqCappedSinceBoot": false,
            "SoftTempLimitSinceBoot": false
        },
        "ClockInfo": {
            "Timezone": "America/New_York",
            "LocalRTC": "no",
            "CanNTP": "yes",
            "NTP": "yes",
            "NTPSynchronized": "yes",
            "TimeUSec": "Thu 2022-09-15 09:47:14 EDT",
            "FallbackNTPServers": "0.debian.pool.ntp.org 1.debian.pool.ntp.org 2.debian.pool.ntp.org 3.debian.pool.ntp.org",
            "ServerName": "0.debian.pool.ntp.org",
            "ServerAddress": "204.2.134.163",
            "RootDistanceMaxUSec": "5s",
            "PollIntervalMinUSec": "32s",
            "PollIntervalMaxUSec": "34min 8s",
            "PollIntervalUSec": "34min 8s",
            "NTPMessage": "{ Leap=0, Version=4, Mode=4, Stratum=3, Precision=-23, RootDelay=7.858ms, RootDispersion=44.891ms, Reference=2C18C722, OriginateTimestamp=Thu 2022-09-15 09:31:21 EDT, ReceiveTimestamp=Thu 2022-09-15 09:31:21 EDT, TransmitTimestamp=Thu 2022-09-15 09:31:21 EDT, DestinationTimestamp=Thu 2022-09-15 09:31:21 EDT, Ignored=no PacketCount=13, Jitter=35.229ms }",
            "Frequency": "-921736"
        }
    }
