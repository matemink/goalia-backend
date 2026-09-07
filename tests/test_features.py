import unittest

from app.features import UNKNOWN_FEATURE_ID, build_features
from app.team_matcher import match_team


class TeamMatcherTest(unittest.TestCase):
    def test_missing_team_name_is_not_matched(self):
        self.assertIsNone(match_team(None))


class FeatureBuilderTest(unittest.TestCase):
    def test_missing_team_name_uses_unknown_feature(self):
        match = {
            "homeTeam": {"name": None},
            "awayTeam": {"name": "Arsenal"},
            "competition": {"name": "Premier League"},
        }

        features = build_features(match)

        self.assertEqual(float(UNKNOWN_FEATURE_ID), features[0])


if __name__ == "__main__":
    unittest.main()
