#!/usr/bin/python3

import getpass, os, re, subprocess

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

username = getpass.getuser()
debian_release_version = float(subprocess.check_output("lsb_release -rs", shell=True, encoding="utf-8").strip())

def is_raspberry_pi():
    try:
        with open("/sys/firmware/devicetree/base/model") as f:
            if "Raspberry Pi" in f.read():
                return True
    except:
        pass
    try:
        cpuinfo = open("/proc/cpuinfo").read()
        if re.search(r"Hardware\s*:\s*BCM", cpuinfo):
            return True
    except:
        pass
    return False

IS_PI = is_raspberry_pi()

def shell_cmd(cmd):
    print(cmd)
    print(subprocess.check_output(cmd, shell=True, encoding="utf-8"))

def update_crontab(name, line):
    # Read current
    completed = subprocess.run(f"crontab -u {username} -l", shell=True, capture_output=True, encoding="utf-8")
    assert(completed.returncode == 0 or "no crontab for" in completed.stderr)
    prev_crontab = completed.stdout.splitlines(keepends=True)
    token = f"AUTOINSTALLED:{name}"
    installme = f"{line} # {token}"
    old_lines = [line for line in prev_crontab if token in line]
    other_lines = [line for line in prev_crontab if token not in line]
    if len(old_lines) == 1 and old_lines[0].strip() == installme:
        print(f"{name}: already up-to-date in {username} crontab: {installme}")
        return
    elif old_lines:
        print(f"{name}: replacing entry in {username} crontab: {installme}")
    else:
        print(f"{name}: adding entry in {username} crontab: {installme}")
    new_crontab_content = ''.join(other_lines) + installme + "\n"
    subprocess.check_output(f"crontab -u {username} -", shell=True, input=new_crontab_content, encoding="utf-8")

# On amd64, use --no-upgrade to avoid pulling in unrelated upgrades (e.g., kernel)
apt_flags = "-y" if IS_PI else "-y --no-upgrade"

print("Install apt package dependencies")
shell_cmd(f"mpstat >/dev/null || sudo apt install {apt_flags} sysstat")
shell_cmd(f"ifconfig >/dev/null 2>&1 || sudo apt install {apt_flags} net-tools")
if IS_PI:
    shell_cmd(f"ntpstat >/dev/null 2>&1 || sudo apt install {apt_flags} ntpstat")

python = "/usr/bin/python3"

print("Install python dependencies")
# Note that starting in Debian Bookworm (12) / Ubuntu 24.04+, a venv is needed, otherwise
# the system refuses to let you install python packages into the system python.
# For now, we just make use of python packages found via apt.
if debian_release_version >= 12:
    shell_cmd(f"{python} -c 'import dateutil' 2>/dev/null || sudo apt install {apt_flags} python3-dateutil")
else:
    shell_cmd(f"{python} -c 'import dateutil' 2>/dev/null || sudo {python} -m pip install python-dateutil")

print(f"Run {python} monitor.py to test.")
#shell_cmd(f"{python} monitor.py")

def remove_crontab_entry(name):
    completed = subprocess.run(f"crontab -u {username} -l", shell=True, capture_output=True, encoding="utf-8")
    if completed.returncode != 0:
        return
    prev_crontab = completed.stdout.splitlines(keepends=True)
    token = f"AUTOINSTALLED:{name}"
    old_lines = [line for line in prev_crontab if token in line]
    if not old_lines:
        return
    other_lines = [line for line in prev_crontab if token not in line]
    print(f"{name}: removing old entry from {username} crontab")
    new_crontab_content = ''.join(other_lines)
    subprocess.check_output(f"crontab -u {username} -", shell=True, input=new_crontab_content, encoding="utf-8")

# Clean up old crontab entries from before rename
remove_crontab_entry("pi-monitor-periodic")
remove_crontab_entry("pi-monitor-reboot")

update_crontab("server-monitor-periodic", f"*/1 * * * * {python} {script_dir}/monitor.py")
update_crontab("server-monitor-reboot", f"@reboot {python} {script_dir}/monitor.py --reboot")
