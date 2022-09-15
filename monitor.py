from cgi import print_environ
import statistics
import subprocess



def gpuTempC():
    return float(subprocess.check_output(['/usr/bin/vcgencmd', 'measure_temp'])[5:-3])

def cpuTempC():
    return round(float(open("/sys/class/thermal/thermal_zone0/temp").read()) / 1000, 2)

def load_average():
    output = subprocess.check_output(['uptime'], encoding='utf8')
    tokens = output.split()
    return {
        "1min": float(tokens[-3].replace(",","")), 
        "5min": float(tokens[-2].replace(",","")), 
        "15min": float(tokens[-1].replace(",",""))
    }

# To use this, install mpstat:
# sudo apt-get install sysstat
import json
def processor_utilization():
    output = subprocess.check_output(['mpstat', '-o', 'JSON'], encoding='utf8')
    j= json.loads(output)
    return j['sysstat']['hosts'][0]['statistics'][0]['cpu-load'][0]

def cpuFreqGhz():
    text_file = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq", "r")
    data = text_file.read()
    text_file.close()
    return float(data)/1e6

import os
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            tokens = line.split()
            used = float(tokens[2])
            total = float(tokens[1])

            return {
                "PctUsed": round(used / total * 100, 1),
                "TotalGB": round(total / 1e6, 2)
            }

# 
def SDcard():
    # -m means output in megabytes (MB)
    output = subprocess.check_output(['df', '-m', '/'], encoding='utf8')
    lines = output.splitlines()
    line = lines[1]
    tokens = line.split()
    return {
        "PctUsed": float(tokens[4].replace("%","")),
        "TotalGB": round(float(tokens[1].replace(",","")) / 1000, 1)
    }

def throttled():
    GET_THROTTLED_CMD = 'vcgencmd get_throttled'
    MESSAGES = {
        0: 'Undervolt',
        1: 'ARMFreqCapped',
        2: 'Throttled',
        3: 'SoftTempLimit',
        16: 'UndervoltSinceBoot',
        17: 'ThrottledSinceBoot',
        18: 'ARMFreqCappedSinceBoot',
        19: 'SoftTempLimitSinceBoot'
    }

    throttled_output = subprocess.check_output(GET_THROTTLED_CMD, shell=True, encoding='utf8')
    throttled_binary = bin(int(throttled_output.split('=')[1], 0))

    warnings = 0
    all = {}
    for position, message in MESSAGES.items():
        # Check for the binary digits to be "on" for each warning message
        if len(throttled_binary) > position and throttled_binary[0 - position - 1] == '1':
            all[message] = True
        else:
            all[message] = False

    return all

def CPU_clock_rate():
    text_file = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")
    data = text_file.read()
    text_file.close()
    return float(data)

def uptimeHrs():
    output = subprocess.check_output(['cat', '/proc/uptime'], encoding='utf8')
    tokens = output.split()
    return round(float(tokens[0])/3600, 2)

def Timedatectl():
    output = subprocess.check_output(['timedatectl', 'show'], encoding='utf8')
    output += subprocess.check_output(['timedatectl', 'show-timesync'], encoding='utf8')
    lines = output.split('\n')
    # Build a dictionary from a=b from lines
    ret = {}
    for line in lines:
        if line:
            [key, value] = line.split('=', 1)
            ret[key] = value
    return ret

import glob

def backlog_image_count():
    backlog_image_filenames = glob.glob("/home/breathecam/breathecam/Code/pi_cam/images/*.jpg")
    backlog_image_count = len(backlog_image_filenames)
    return backlog_image_count

def allStats():
    return {
        "ImageBacklogCnt": backlog_image_count(), 
        "CpuTempC": cpuTempC(),
        "GpuTempC": gpuTempC(),
        "UptimeHrs": uptimeHrs(), 
        "SDcard": SDcard(),
        "RAM": getRAMinfo(), 
        "LoadAvg": load_average(),
        "CpuUtil": processor_utilization(), 
        "CpuFreqGhz": cpuFreqGhz(), 
        "Throttling": throttled(), 
        "ClockInfo": Timedatectl()
    }

stats = allStats()
details = json.dumps(stats)

from utils.utils import *

Stat.set_service('RPi status')

errors = []

pct_used = stats["SDcard"]["PctUsed"]
if pct_used >= 95:
    errors.append(f'SD card almost full ({pct_used}%)')

backlog_image_count_threshold = 50
backlog_image_count = stats["ImageBacklogCnt"]
if backlog_image_count > backlog_image_count_threshold:
    errors.append(f'{backlog_image_count} images in upload backlog (>{backlog_image_count_threshold})')

if errors:
    Stat.down(", ".join(errors), valid_for_secs= 600, details=details, payload=stats)
else:
    Stat.up("System is working", valid_for_secs = 600, details=details, payload=stats)


def wait_for_timesync():
    # Wait until the system clock is synchronized, and return how long it took
    waited_secs = 0
    while not os.path.exists("/run/systemd/timesync/synchronized"):
        print("waiting for time sync")
        time.sleep(1.0)
        waited_secs += 1
    return waited_secs

import sys
if "--reboot" in sys.argv:
    waited_secs = wait_for_timesync()
    Stat.warning(f"System booted.  Took {waited_secs} seconds for NTP to synchronize")

def timedatectl():
    output = subprocess.check_output(['timedatectl', 'timesync-status'], encoding='utf8')
    tokens = output()
    return tokens

