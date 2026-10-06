import unittest

try:
    import pandas as pd

    from tsresearch.models import spec_name
    from tsresearch.selection import CANDIDATE_SPECS, choose_models
    HAVE_RESEARCH = True
except ImportError:
    HAVE_RESEARCH = False


@unittest.skipUnless(HAVE_RESEARCH, "research extras not installed")
class SelectionTests(unittest.TestCase):
    def table(self, scores):
        return pd.DataFrame([{"model": spec_name(s), "horizon": h, "rel_rmse": scores[spec_name(s)]}
                             for s in CANDIDATE_SPECS for h in (1, 5)])

    def test_choice_uses_only_the_supplied_validation_scores(self):
        scores = {spec_name(s): 1.05 for s in CANDIDATE_SPECS}
        scores["naive"] = 1.0
        scores["ridge(alpha=100.0)"] = 1.02
        scores["extra_trees(min_leaf=60)"] = 0.99
        scores["gradient_boosting(max_depth=2)"] = 1.01
        chosen = choose_models(self.table(scores))
        self.assertEqual(spec_name(chosen["center"]), "extra_trees(min_leaf=60)")
        self.assertEqual(spec_name(chosen["best_learned"]), "extra_trees(min_leaf=60)")
        names = {spec_name(s) for s in chosen["frozen"]}
        self.assertEqual(names, {"naive", "drift", "ridge(alpha=100.0)",
                                 "extra_trees(min_leaf=60)", "gradient_boosting(max_depth=2)"})

    def test_persistence_can_be_the_centre_when_nothing_beats_it(self):
        scores = {spec_name(s): 1.03 for s in CANDIDATE_SPECS}
        scores["naive"] = 1.0
        chosen = choose_models(self.table(scores))
        self.assertEqual(spec_name(chosen["center"]), "naive")
        self.assertNotEqual(chosen["best_learned"]["family"], "naive")


if __name__ == "__main__":
    unittest.main()
