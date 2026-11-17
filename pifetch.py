#!/usr/bin/env python3

import argparse
import shutil

from config import GREEN, ORANGE, WHITE, GRAY, RESET
from system_info import collect
from logo import get_logo


def main():
    parser = argparse.ArgumentParser(
        description="Custom Raspberry Pi system fetch"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable terminal colors"
    )
    args = parser.parse_args()

    green = "" if args.no_color else GREEN
    orange = "" if args.no_color else ORANGE
    white = "" if args.no_color else WHITE
    gray = "" if args.no_color else GRAY
    reset = "" if args.no_color else RESET

    info = collect()
    logo = get_logo()

    terminal_width = shutil.get_terminal_size((100, 24)).columns

    print()

    items = list(info.items())

    for i in range(max(len(logo), len(items))):
        left = logo[i] if i < len(logo) else " " * 23

        if i < len(items):
            key, value = items[i]

            right = (
                f"{orange}{key:<12}{reset}"
                f"{gray}│{reset} "
                f"{white}{value}{reset}"
            )
        else:
            right = ""

        print(f"{left:<23}  {right}")

    print()
    print(
        f"{green}●{reset} {gray}RASPBERRY PI ENGINEERING WORKSTATION{reset}"
    )
    print()


if __name__ == "__main__":
    main()