# Pifetch

<p align="center">
  <strong>A small, dependency-free system fetch utility for Raspberry Pi and Linux.</strong>
  <br>
  Collect useful hardware and operating-system details and display them in a compact terminal dashboard.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8 or newer">
  <img src="https://img.shields.io/badge/Platform-Raspberry%20Pi%20%7C%20Linux-C51A4A?style=for-the-badge&logo=raspberrypi&logoColor=white" alt="Raspberry Pi and Linux">
  <img src="https://img.shields.io/badge/Dependencies-None-2E8B57?style=for-the-badge" alt="No external dependencies">
</p>

## Overview

Pifetch is a lightweight terminal information tool inspired by the familiar `fetch` family of utilities. It is designed for Raspberry Pi workstations, servers, and lab machines where a quick view of the current system is useful.

The output combines:

- A Raspberry Pi-themed ASCII logo
- Hardware and kernel information
- CPU frequency, temperature, and load
- Memory and disk usage
- Network interfaces and IPv4 addresses
- A color-coded, readable terminal layout

Pifetch uses Python's standard library only, so there is no package installation step and no virtual environment required.

## Preview

```text
       .-------.  USER        │ pi
      /  .---.  \  HOST        │ raspberrypi
     |  /     \  |  MODEL       │ Raspberry Pi 5 Model B Rev 1.0
     | |  PI5 |  |  OS          │ Debian GNU/Linux 12 (bookworm)
     |  \     /  |  KERNEL      │ 6.6.31+rpt-rpi-2712
      \  '---'  /  ARCH        │ aarch64
       '-------'  SHELL       │ /bin/bash
          | |     UPTIME      │ 2d 4h 18m
       ___| |___  CPU         │ ARM ...
                    CPU FREQ    │ 2400 MHz
                    CPU TEMP    │ 43.2 °C
                    LOAD        │ 0.18
                    MEMORY      │ 812 MiB / 4096 MiB
                    DISK        │ 8.1 GB / 59.6 GB
                    INTERFACES  │ eth0, wlan0
                    IP ADDRESS  │ eth0: 192.168.1.20/24

● RASPBERRY PI ENGINEERING WORKSTATION
```

## Requirements

- Linux, especially Raspberry Pi OS
- Python 3.8 or newer
- A terminal with ANSI color support for the default colored output
- The `ip` command for IPv4 address discovery

Pifetch reads standard Linux interfaces such as `/proc`, `/sys`, and `/etc/os-release`. Some values are reported as `Unknown` or `Unavailable` when the underlying interface is missing, such as when the program is run on a non-Raspberry Pi machine.

## Installation

Clone the repository:

```bash
git clone https://github.com/Gavinduachintha/Pifetch.git
cd Pifetch
```

No third-party dependencies are required.

For a convenient command available from anywhere, create a symlink:

```bash
mkdir -p "$HOME/.local/bin"
ln -s "$(pwd)/pifetch.py" "$HOME/.local/bin/pifetch"
chmod +x pifetch.py
```

Make sure `"$HOME/.local/bin"` is in your `PATH`, then run:

```bash
pifetch
```

## Usage

Run the script directly from the repository:

```bash
python3 pifetch.py
```

Disable ANSI colors when redirecting output, using a minimal terminal, or collecting plain text:

```bash
python3 pifetch.py --no-color
```

Save a plain-text report:

```bash
python3 pifetch.py --no-color > system-report.txt
```

Display command-line help:

```bash
python3 pifetch.py --help
```

## Information displayed

| Field | Source or meaning |
| --- | --- |
| `USER` | Current `USER` environment variable |
| `HOST` | System hostname |
| `MODEL` | Raspberry Pi model from `/proc/device-tree/model` |
| `OS` | Pretty Linux distribution name from `/etc/os-release` |
| `KERNEL` | Running kernel release |
| `ARCH` | Machine architecture |
| `SHELL` | Current `SHELL` environment variable |
| `UPTIME` | Elapsed time from `/proc/uptime` |
| `CPU` | Processor description from `/proc/cpuinfo` |
| `CPU FREQ` | Current frequency of CPU 0, when available |
| `CPU TEMP` | Thermal zone 0 temperature, when available |
| `LOAD` | One-minute load average |
| `MEMORY` | Used and total memory from `/proc/meminfo` |
| `DISK` | Used and total space for the root filesystem |
| `INTERFACES` | Network interfaces other than loopback |
| `IP ADDRESS` | IPv4 addresses reported by `ip -o -4 addr show` |

## Project structure

```text
Pifetch/
├── pifetch.py       # CLI entry point and terminal layout
├── system_info.py   # Linux system information collectors
├── logo.py          # Raspberry Pi ASCII logo
├── config.py        # ANSI color definitions
└── README.md        # Project documentation
```

The code is intentionally split into presentation and collection layers: `system_info.py` gathers values, while `pifetch.py` formats them for the terminal. This keeps the collectors easy to extend without changing the display loop.

## Design notes

- **No external dependencies:** only Python's standard library is used.
- **Safe fallbacks:** unavailable hardware-specific values are displayed as `Unknown` or `Unavailable` instead of stopping the report.
- **Readable output:** labels, separators, and values use distinct colors, with `--no-color` available for automation.

## Troubleshooting

### The model or temperature is unavailable

This is expected on many non-Raspberry Pi systems and in containers. Pifetch depends on Raspberry Pi/Linux kernel interfaces that may not be mounted or exposed in those environments.

### IP addresses are unavailable

Install the package that provides the `ip` command for your distribution. On Debian-based systems:

```bash
sudo apt update
sudo apt install iproute2
```

### Colors look incorrect

Use the plain-output mode:

```bash
python3 pifetch.py --no-color
```

## Contributing

Contributions are welcome. A good contribution should:

1. Keep the standard-library-only approach unless there is a strong reason to change it.
2. Preserve the existing output style and `--no-color` behavior.
3. Handle missing Linux files or commands with a clear fallback.
4. Keep collectors in `system_info.py` and presentation logic in `pifetch.py`.
5. Run a syntax check before opening a pull request:

   ```bash
   python3 -m py_compile pifetch.py config.py logo.py system_info.py
   ```

## License

No license is currently declared in this repository. Add a license file before distributing or reusing the project outside its intended context.

## Acknowledgements

Pifetch is part of the classic terminal “fetch” tradition: small utilities that turn system metadata into a useful and recognizable startup display.
