#!/usr/bin/env python3
"""
Run all ha-scripts generators in process.

Usage:
    ./generate_all.py /path/to/ha-config
"""

import sys
from pathlib import Path

from generate_input_booleans import run as generate_input_booleans
from generate_climates import run as generate_climates
from generate_templates import run as generate_templates


GENERATORS = [
    ("Input Booleans", generate_input_booleans),
    ("Climates", generate_climates),
    ("Templates", generate_templates),
]


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: generate_all.py /path/to/ha-config", file=sys.stderr)
        raise SystemExit(1)

    config_root = Path(sys.argv[1]).expanduser().resolve()

    for label, func in GENERATORS:
        print(f"→ {label}")
        func(config_root)

    print("\n✔ All generators completed successfully")
    print("💡 Restart Home Assistant to apply changes.")


if __name__ == "__main__":
    main()
