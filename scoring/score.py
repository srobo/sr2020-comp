import collections

EXPECTED_TOKENS = {'S': 8, 'G': 8}
VALID_TOKENS = set(EXPECTED_TOKENS.keys())


class InvalidScoresheetException(Exception):
    pass


class Scorer(object):
    def __init__(self, teams_data, arena_data):
        self._teams_data = teams_data
        self._zone_contents = {
            k: collections.Counter(zone['tokens'].replace(' ', ''))
            for k, zone in arena_data.items()
        }

    def calculate_scores(self):
        def zone_score(zone_data):
            if not zone_data:
                return 0
            return  3 * sum(zone_data.values()) / len(zone_data)

        scores = {
            tla: zone_score(self._zone_contents[team_data['zone']])
            for tla, team_data in self._teams_data.items()
        }
        return scores

    def validate(self, extra_data):
        merged = collections.Counter()
        for zone, zone_data in self._zone_contents.items():
            merged.update(zone_data)

            extra = set(zone_data.keys()) - VALID_TOKENS
            if extra:
                raise InvalidScoresheetException(
                    "Invalid token type {} in zone {}".format(
                        ", ".join(repr(x) for x in extra),
                        zone,
                    ),
                )

        if merged != EXPECTED_TOKENS:
            raise InvalidScoresheetException(
                "Invalid number of tokens: expecting {} but was {}".format(
                    EXPECTED_TOKENS,
                    dict(merged),
                ),
            )


if __name__ == '__main__':
    import libproton
    libproton.main(Scorer)
