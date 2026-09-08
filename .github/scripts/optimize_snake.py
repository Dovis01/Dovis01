#!/usr/bin/env python3
"""Remove level bars and unused vertical space from generated snakes."""

from __future__ import annotations

import re
import sys
from pathlib import Path


BAR_PATTERN = re.compile(r'<rect class="u u[0-9]+"[^>]*/>')
REMAINING_BAR_PATTERN = re.compile(r'<rect class="u ')
SOURCE_VIEWBOX = 'viewBox="-16 -32 880 192"'
TARGET_VIEWBOX = 'viewBox="-16 -32 880 144"'
SOURCE_HEIGHT = 'height="192"'
TARGET_HEIGHT = 'height="144"'


def optimize(path: Path) -> None:
    svg = path.read_text(encoding="utf-8")

    svg, removed_bars = BAR_PATTERN.subn("", svg)
    if REMAINING_BAR_PATTERN.search(svg):
        raise ValueError(f"{path}: unsupported level-bar markup remains")

    if SOURCE_VIEWBOX not in svg or SOURCE_HEIGHT not in svg:
        raise ValueError(f"{path}: unexpected SVG dimensions")

    svg = svg.replace(SOURCE_VIEWBOX, TARGET_VIEWBOX, 1)
    svg = svg.replace(SOURCE_HEIGHT, TARGET_HEIGHT, 1)
    path.write_text(svg, encoding="utf-8")

    print(f"optimized {path}: removed {removed_bars} level bars")


def main(arguments: list[str]) -> int:
    if not arguments:
        print("usage: optimize_snake.py <svg> [<svg> ...]", file=sys.stderr)
        return 2

    for argument in arguments:
        optimize(Path(argument))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
