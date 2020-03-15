#!/usr/bin/env python

import unittest

import yaml

# Path hackery
import pathlib
import sys
ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from score import Scorer, InvalidScoresheetException, EXPECTED_TOKENS
NUM_TOKENS = sum(EXPECTED_TOKENS.values())

TEAMS_DATA =  {
    'ABC': {'zone': 0},
    'DEF': {'zone': 1},
    'GHI': {'zone': 2},
}


class ScorerTests(unittest.TestCase):
    longMessage = True

    def construct_scorer(self, zone_contents):
        return Scorer(TEAMS_DATA, zone_contents)

    def assertScores(self, expected_scores, zone_contents):
        scorer = self.construct_scorer(zone_contents)
        actual_scores = scorer.calculate_scores()

        self.assertEqual(expected_scores, actual_scores, "Wrong scores")

    def setUp(self):
        self.other_contents = {'tokens': 'SSSS SSSS GGGG GGGG'}
        self.zone_contents = {
            zone: {'tokens': ''}
            for zone in range(4)
        }
        self.zone_contents['other'] = self.other_contents

    def test_template(self):
        template_path = ROOT / 'template.yaml'
        with template_path.open() as f:
            data = yaml.load(f)

        teams_data = data['teams']
        arena_data = data.get('arena_zones')
        extra_data = data.get('other')

        scorer = Scorer(teams_data, arena_data)
        scores = scorer.calculate_scores()

        scorer.validate(extra_data)

        self.assertEqual(
            teams_data.keys(),
            scores.keys(),
            "Should return score values for every team",
        )

    def test_too_many_tokens_overall(self):
        # There are a total of 8 tokens of each colour
        self.zone_contents[0]['tokens'] = 'S' * 4
        self.zone_contents[1]['tokens'] = 'G' * 4

        scorer = self.construct_scorer(self.zone_contents)

        with self.assertRaises(InvalidScoresheetException):
            scorer.validate(None)

    def test_too_many_tokens_of_one_colour(self):
        # There are a total of 8 tokens of each colour
        self.zone_contents[0]['tokens'] = 'S' * 3
        self.zone_contents[1]['tokens'] = 'G' * 5
        self.other_contents['tokens'] = 'SG' * 4

        self.assertEqual(
            NUM_TOKENS,
            len(''.join(x['tokens'] for x in self.zone_contents.values())),
            "Test should maintain expected total tokens",
        )

        scorer = self.construct_scorer(self.zone_contents)

        with self.assertRaises(InvalidScoresheetException):
            scorer.validate(None)

    def test_invalid_token_colour(self):
        self.other_contents['tokens'] = 'Q' + self.other_contents['tokens'][:-1]

        scorer = self.construct_scorer(self.zone_contents)

        with self.assertRaises(InvalidScoresheetException):
            scorer.validate(None)

    def test_no_tokens_move(self):
        self.assertScores({
            'ABC': 0,
            'DEF': 0,
            'GHI': 0,
        }, self.zone_contents)

    def test_single_silver_token_in_zone(self):
        self.zone_contents[0]['tokens'] = 'S'

        self.assertScores({
            'ABC': 3,
            'DEF': 0,
            'GHI': 0,
        }, self.zone_contents)

    def test_single_gold_token_in_zone(self):
        self.zone_contents[1]['tokens'] = 'G'

        self.assertScores({
            'ABC': 0,
            'DEF': 3,
            'GHI': 0,
        }, self.zone_contents)

    def test_two_silver_tokens_in_zone(self):
        self.zone_contents[2]['tokens'] = 'SS'

        self.assertScores({
            'ABC': 0,
            'DEF': 0,
            'GHI': 6,
        }, self.zone_contents)

    def test_two_gold_tokens_in_zone(self):
        self.zone_contents[0]['tokens'] = 'GG'

        self.assertScores({
            'ABC': 6,
            'DEF': 0,
            'GHI': 0,
        }, self.zone_contents)

    def test_mixed_tokens_in_zone(self):
        self.zone_contents[0]['tokens'] = 'SG'

        self.assertScores({
            'ABC': 2,
            'DEF': 0,
            'GHI': 0,
        }, self.zone_contents)

    def test_two_of_each_types_in_zone(self):
        self.zone_contents[0]['tokens'] = 'SS GG'

        self.assertScores({
            'ABC': 4,
            'DEF': 0,
            'GHI': 0,
        }, self.zone_contents)

    def test_imbalanced_mixed_tokens_in_zone(self):
        self.zone_contents[0]['tokens'] = 'SSS SSS G'

        self.assertScores({
            'ABC': 7,
            'DEF': 0,
            'GHI': 0,
        }, self.zone_contents)

    def test_lots_of_scores(self):
        self.zone_contents[0]['tokens'] = 'SSS'
        self.zone_contents[1]['tokens'] = 'SS GG'
        self.zone_contents[2]['tokens'] = 'GGG GG S'

        self.assertScores({
            'ABC': 9,
            'DEF': 4,
            'GHI': 6,
        }, self.zone_contents)


if __name__ == '__main__':
    unittest.main()
