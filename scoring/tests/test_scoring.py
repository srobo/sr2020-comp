#!/usr/bin/env python

import unittest

# Path hackery
import pathlib
import sys
ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from score import Scorer, InvalidScoresheetException


class ScorerTests(unittest.TestCase):
    def test(self) -> None:
        self.fail()


if __name__ == '__main__':
    unittest.main()
