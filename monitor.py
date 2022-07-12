from cgi import print_environ
import statistics
import subprocess


def measure_temperature():
    output = subprocess.check_output(['/usr/bin/vcgencmd', 'measure_temp'])
    return float(output[5:-3])


def uptime():
    output = subprocess.check_output(['uptime'], encoding='utf8')
    tokens = output.split()
    return {
        "load average 1min": float(tokens[-3].replace(",","")), 
        "load average 5min": float(tokens[-2].replace(",","")), 
        "load average 15min": float(tokens[-1].replace(",",""))
    }

# To use this, install mpstat:
# sudo apt-get install sysstat
import json
def processor_utilization():
    output = subprocess.check_output(['mpstat', '-o', 'JSON'], encoding='utf8')
    j= json.loads(output)
    return j['sysstat']['hosts'][0]['statistics'][0]['cpu-load'][0]

def processor_frequencey():
    text_file = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq", "r")
    data = text_file.read()
    text_file.close()
    return float(data)

import os
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            tokens = line.split()
            return {
                "Total KB": float(tokens[1]),
                "used KB": float(tokens[2]),
                "Free KB": float(tokens[3])
            }

# 
def SDcard():
    # -m means output in megabytes (MB)
    output = subprocess.check_output(['df', '-m', '/'], encoding='utf8')
    print('The value of output is >>>', output, '<<<')
    lines = output.splitlines()
    print('The value of lines is >>>', lines, '<<<')
    line = lines[1]
    print('The value of line is >>>', line, '<<<')
    tokens = line.split()
    print(tokens)
    return {
    "Total MB": float(tokens[1].replace(",","")),
    "Used MB":  float(tokens[2].replace(",","")), 
    "Available MB": float(tokens[3].replace(",","")), 
    "Percent used": float(tokens[4].replace("%",""))
    }

def allStats():
    return {
        "SDcard": SDcard(),
        "ramInfo": getRAMinfo(), 
        "processor_frequencey": processor_frequencey(), 
        "processor_utilization": processor_utilization(), 
        "uptime": uptime(), 
        "measure_temperature": measure_temperature()
    }
stats = allStats()
details = json.dumps(stats)

from utils.utils import *

Stat.set_service('RPi status')

if stats["SDcard"]["Percent used"] < 95:
    Stat.up("System is working", valid_for_secs = 600, details=details, payload=stats)
else:
    Stat.down("SD card almost full", valid_for_secs= 600, details=details, payload=stats)

    #cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
def CPU_clock_rate():
     text_file = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")
     data = text_file.read()
     text_file.close()
     return float(data)

GET_THROTTLED_CMD = 'vcgencmd get_throttled'
MESSAGES = {
    0: 'Under-voltage!',
    1: 'ARM frequency capped!',
    2: 'Currently throttled!',
    3: 'Soft temperature limit active',
    16: 'Under-voltage has occurred since last reboot.',
    17: 'Throttling has occurred since last reboot.',
    18: 'ARM frequency capped has occurred since last reboot.',
    19: 'Soft temperature limit has occurred'
}

print("Checking for throttling issues since last reboot...")

throttled_output = subprocess.check_output(GET_THROTTLED_CMD, shell=True, encoding='utf8')
throttled_binary = bin(int(throttled_output.split('=')[1], 0))

warnings = 0
for position, message in MESSAGES.items():
    # Check for the binary digits to be "on" for each warning message
    if len(throttled_binary) > position and throttled_binary[0 - position - 1] == '1':
        print(message)
        warnings += 1

if warnings == 0:
    print("Looking good!")
else:
    print("Houston, we may have a problem!")

# print(measure_temperature())
# print(uptime())
# print(processor_utilization())
# print(processor_frequencey())
# print(getRAMinfo())
