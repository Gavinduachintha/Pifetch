import os
import platform
import shutil
import subprocess
from pathlib import Path


def read_file(path, default="Unknown"):
    try:
        return Path(path).read_text().strip().replace("\x00", "")
    except (OSError, ValueError):
        return default


def get_os():
    data = {}
    for line in Path("/etc/os-release").read_text().splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            data[key] = value.strip('"')
    return data.get("PRETTY_NAME", "Linux")


def get_model():
    return read_file("/proc/device-tree/model")


def get_cpu():
    cpuinfo = read_file("/proc/cpuinfo", "")
    for line in cpuinfo.splitlines():
        if line.startswith(("Model", "model name", "Hardware")):
            return line.split(":", 1)[-1].strip()
    return platform.machine()


def get_temperature():
    raw = read_file(
        "/sys/class/thermal/thermal_zone0/temp", ""
    )
    try:
        return f"{int(raw) / 1000:.1f} °C"
    except ValueError:
        return "Unavailable"


def get_memory():
    info = {}

    for line in read_file("/proc/meminfo", "").splitlines():
        parts = line.split()
        if len(parts) >= 2:
            info[parts[0].rstrip(":")] = int(parts[1])

    total = info.get("MemTotal", 0)
    available = info.get("MemAvailable", 0)
    used = total - available

    return (
        f"{used / 1024:.0f} MiB / "
        f"{total / 1024:.0f} MiB"
    )


def get_disk():
    usage = shutil.disk_usage("/")
    return (
        f"{usage.used / 1024**3:.1f} GB / "
        f"{usage.total / 1024**3:.1f} GB"
    )


def get_uptime():
    seconds = float(read_file("/proc/uptime", "0").split()[0])

    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)

    result = []

    if days:
        result.append(f"{days}d")
    if hours:
        result.append(f"{hours}h")

    result.append(f"{minutes}m")

    return " ".join(result)


def get_frequency():
    raw = read_file(
        "/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq",
        ""
    )

    try:
        return f"{int(raw) / 1000:.0f} MHz"
    except ValueError:
        return "Unavailable"


def get_load():
    return read_file("/proc/loadavg").split()[0]


def get_interfaces():
    try:
        return ", ".join(
            name for name in os.listdir("/sys/class/net")
            if name != "lo"
        ) or "None"
    except OSError:
        return "Unavailable"


def get_ip():
    try:
        result = subprocess.run(
            ["ip", "-o", "-4", "addr", "show"],
            capture_output=True,
            text=True,
            timeout=2,
            check=True
        )

        addresses = []

        for line in result.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 4:
                addresses.append(f"{parts[1]}: {parts[3]}")

        return ", ".join(addresses) if addresses else "No IPv4"

    except (OSError, subprocess.SubprocessError):
        return "Unavailable"


def collect():
    return {
        "USER": os.environ.get("USER", "Unknown"),
        "HOST": platform.node(),
        "MODEL": get_model(),
        "OS": get_os(),
        "KERNEL": platform.release(),
        "ARCH": platform.machine(),
        "SHELL": os.environ.get("SHELL", "Unknown"),
        "UPTIME": get_uptime(),
        "CPU": get_cpu(),
        "CPU FREQ": get_frequency(),
        "CPU TEMP": get_temperature(),
        "LOAD": get_load(),
        "MEMORY": get_memory(),
        "DISK": get_disk(),
        "INTERFACES": get_interfaces(),
        "IP ADDRESS": get_ip(),
    }