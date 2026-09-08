#!/usr/bin/env python3

import tempfile
import unittest
from pathlib import Path

from optimize_snake import optimize


class OptimizeSnakeTest(unittest.TestCase):
    def test_removes_all_available_bars_when_a_tier_is_missing(self) -> None:
        source = (
            '<svg viewBox="-16 -32 880 192" width="880" height="192">'
            '<style>.c.c0{animation-name:c0}.s.s0{animation-name:s0}</style>'
            '<rect class="u u0" height="12" width="300" x="0" y="144"/>'
            '<rect class="u u1" height="12" width="200" x="300" y="144"/>'
            '<rect class="u u2" height="12" width="100" x="500" y="144"/>'
            '<rect class="c c0" x="2" y="2"/>'
            '<rect class="s s0" x="1" y="1"/>'
            '</svg>'
        )

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "snake.svg"
            path.write_text(source, encoding="utf-8")

            optimize(path)

            optimized = path.read_text(encoding="utf-8")
            self.assertNotIn('<rect class="u ', optimized)
            self.assertIn('viewBox="-16 -32 880 144"', optimized)
            self.assertIn('height="144"', optimized)
            self.assertIn("animation-name:c0", optimized)
            self.assertIn("animation-name:s0", optimized)


if __name__ == "__main__":
    unittest.main()
