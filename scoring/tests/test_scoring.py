#!/usr/bin/env python

import unittest

# Path hackery
import os.path
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, ROOT)

from score import Scorer, InvalidScoresheetException


class ScorerTests(unittest.TestCase):
    def test(self) -> None:
        self.fail()


if __name__ == '__main__':
    unittest.main()
