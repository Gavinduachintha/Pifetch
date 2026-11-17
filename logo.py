from config import GREEN, RESET

LOGO = [
    "       .-------.",
    "      /  .---.  \\",
    "     |  /     \\  |",
    "     | |  PI5 |  |",
    "     |  \\     /  |",
    "      \\  '---'  /",
    "       '-------'",
    "          | |",
    "       ___| |___",
]

def get_logo():
    return [f"{GREEN}{line}{RESET}" for line in LOGO]