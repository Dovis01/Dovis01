#!/usr/bin/env python3
"""Make generated contribution snakes lighter and remove the level bars."""

from __future__ import annotations

import re
import sys
from pathlib import Path


BAR_PATTERN = re.compile(r'<rect class="u u[0-3]"[^>]*/>')
CELL_ANIMATION_PATTERN = re.compile(r"animation-name:c[0-9a-z]+")
SOURCE_VIEWBOX = 'viewBox="-16 -32 880 192"'
TARGET_VIEWBOX = 'viewBox="-16 -32 880 144"'
SOURCE_HEIGHT = 'height="192"'
TARGET_HEIGHT = 'height="144"'


def optimize(path: Path) -> None:
    svg = path.read_text(encoding="utf-8")

    svg, removed_bars = BAR_PATTERN.subn("", svg)
    if removed_bars != 4:
        raise ValueError(f"{path}: expected 4 level bars, found {removed_bars}")

    svg, disabled_cells = CELL_ANIMATION_PATTERN.subn("animation-name:none", svg)
    if disabled_cells == 0:
        raise ValueError(f"{path}: no contribution-cell animations found")

    if SOURCE_VIEWBOX not in svg or SOURCE_HEIGHT not in svg:
        raise ValueError(f"{path}: unexpected SVG dimensions")

    svg = svg.replace(SOURCE_VIEWBOX, TARGET_VIEWBOX, 1)
    svg = svg.replace(SOURCE_HEIGHT, TARGET_HEIGHT, 1)
    path.write_text(svg, encoding="utf-8")

    print(
        f"optimized {path}: removed {removed_bars} bars, "
        f"disabled {disabled_cells} cell animations"
    )


def main(arguments: list[str]) -> int:
    if not arguments:
        print("usage: optimize_snake.py <svg> [<svg> ...]", file=sys.stderr)
        return 2

    for argument in arguments:
        optimize(Path(argument))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
