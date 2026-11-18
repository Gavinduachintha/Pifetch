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

Pifetch is a lightweight terminal information tool inspired by the familiar `fetch` family of utilities. It is designed for Raspberry Pi workstations, servers, and Linux lab machines where a quick overview of the current system is useful.

The output combines:

- A custom Raspberry Pi-themed ASCII logo
- Hardware and kernel information
- CPU frequency, temperature, and load
- Memory and disk usage
- Network interfaces and IPv4 addresses
- A color-coded, readable terminal layout

Pifetch uses Python's standard library only. No third-party packages, installation dependencies, or virtual environments are required.

## Preview

Pifetch displays the ASCII logo and system information side by side in a compact terminal dashboard.

```text
██████╗ ██╗███████╗███████╗████████╗     USER        │ pi
██╔══██╗██║██╔════╝██╔════╝╚══██╔══╝     HOST        │ raspberrypi
██████╔╝██║█████╗  █████╗     ██║        MODEL       │ Raspberry Pi 5 Model B Rev 1.0
██╔═══╝ ██║██╔══╝  ██╔══╝     ██║        OS          │ Debian GNU/Linux 12 (bookworm)
██║     ██║██║     ███████╗   ██║        KERNEL      │ 6.6.31+rpt-rpi-2712
╚═╝     ╚═╝╚═╝     ╚══════╝   ╚═╝        ARCH        │ aarch64
                                         SHELL       │ /bin/bash
┌───────────────────────┐                UPTIME      │ 2d 4h 18m
│  PI 5 // SYSTEM READY │                CPU         │ ARM ...
│  [██████████] 100%    │                CPU FREQ    │ 2400 MHz
└───────────────────────┘                CPU TEMP    │ 43.2 °C
                                         LOAD        │ 0.18
> initializing pifetch...                MEMORY      │ 812 MiB / 4096 MiB
> access granted_                        DISK        │ 8.1 GB / 59.6 GB
                                         INTERFACES  │ eth0, wlan0
                                         IP ADDRESS  │ eth0: 192.168.1.20/24
```

*Example output from a Raspberry Pi 5. Hardware values and system details vary depending on the machine.*

## Requirements

- Linux, especially Raspberry Pi OS
- Python 3.8 or newer
- A terminal with ANSI color support for the default colored output
- The `ip` command for IPv4 address discovery

Pifetch reads standard Linux interfaces such as `/proc`, `/sys`, and `/etc/os-release`.

Some hardware-specific values may be reported as `Unknown` or `Unavailable` when the underlying interface is missing, such as when running on a non-Raspberry Pi machine.

## Installation

Clone the repository:

```bash
git clone https://github.com/Gavinduachintha/Pifetch.git
cd Pifetch
```

No third-party dependencies are required.

### Optional: Run Pifetch from anywhere

Create a local binary directory if it does not already exist:

```bash
mkdir -p "$HOME/.local/bin"
```

Create a symbolic link:

```bash
ln -s "$(pwd)/pifetch.py" "$HOME/.local/bin/pifetch"
```

Make the script executable:

```bash
chmod +x pifetch.py
```

Ensure `"$HOME/.local/bin"` is included in your `PATH`.

Run Pifetch:

```bash
pifetch
```

## Usage

### Run directly

```bash
python3 pifetch.py
```

### Disable ANSI colors

Useful when redirecting output, using a minimal terminal, or collecting plain-text information.

```bash
python3 pifetch.py --no-color
```

### Save a system report

```bash
python3 pifetch.py --no-color > system-report.txt
```

### Display command-line help

```bash
python3 pifetch.py --help
```

## Information displayed

| Field | Description |
| --- | --- |
| `USER` | Current `USER` environment variable |
| `HOST` | System hostname |
| `MODEL` | Raspberry Pi model from `/proc/device-tree/model` |
| `OS` | Distribution name from `/etc/os-release` |
| `KERNEL` | Running kernel release |
| `ARCH` | Machine architecture |
| `SHELL` | Current `SHELL` environment variable |
| `UPTIME` | Elapsed time from `/proc/uptime` |
| `CPU` | Processor description from `/proc/cpuinfo` |
| `CPU FREQ` | Current frequency of CPU 0, when available |
| `CPU TEMP` | Thermal zone 0 temperature, when available |
| `LOAD` | One-minute system load average |
| `MEMORY` | Used and total memory from `/proc/meminfo` |
| `DISK` | Used and total space for the root filesystem |
| `INTERFACES` | Network interfaces excluding loopback |
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

The code is intentionally separated into collection and presentation layers.

- `system_info.py` gathers system information.
- `logo.py` contains the ASCII artwork.
- `config.py` defines terminal colors.
- `pifetch.py` handles command-line arguments and formats the output.

This separation makes it easier to extend system information collectors without modifying the terminal display logic.

## Design notes

- **Dependency-free:** Uses Python's standard library only.
- **Lightweight:** Reads information directly from Linux system interfaces.
- **Safe fallbacks:** Missing hardware-specific information is displayed as `Unknown` or `Unavailable`.
- **Readable output:** Uses distinct colors for labels, separators, and values.
- **Plain-text support:** Provides a `--no-color` option for automation and redirected output.
- **Modular structure:** Separates system information collection from terminal presentation.

## Troubleshooting

### The model or temperature is unavailable

This can happen on non-Raspberry Pi systems or inside containers.

Pifetch depends on Linux kernel interfaces that may not be mounted or exposed in those environments.

### IP addresses are unavailable

Make sure the package providing the `ip` command is installed.

On Debian-based systems:

```bash
sudo apt update
sudo apt install iproute2
```

### Colors look incorrect

Try running Pifetch without ANSI colors:

```bash
python3 pifetch.py --no-color
```

### The `pifetch` command is not found

Ensure that `$HOME/.local/bin` is included in your `PATH`.

For Bash, add the following line to `~/.bashrc`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Reload the configuration:

```bash
source ~/.bashrc
```

## Contributing

Contributions are welcome.

A good contribution should:

1. Preserve the standard-library-only approach unless there is a strong reason to change it.
2. Maintain the existing terminal output style and `--no-color` behavior.
3. Handle missing Linux files or commands with appropriate fallbacks.
4. Keep system information collectors in `system_info.py`.
5. Keep presentation logic in `pifetch.py`.
6. Include clear descriptions of any new functionality.

Before submitting a pull request, run a syntax check:

```bash
python3 -m py_compile pifetch.py config.py logo.py system_info.py
```

## License

No license is currently declared in this repository.

A license file should be added before distributing or reusing the project outside its intended context.

## Acknowledgements

Pifetch is part of the classic terminal `fetch` tradition: small utilities that turn system metadata into a useful and recognizable startup display.

Built for Raspberry Pi and Linux enthusiasts who appreciate a little more personality in their terminal.
