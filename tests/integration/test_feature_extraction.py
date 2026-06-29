import unittest
from datetime import date

from extract_candidate_features import extract_features


class FeatureExtractionTests(unittest.TestCase):
    def test_description_evidence_outweighs_skills_only(self):
        base = {
            "candidate_id": "CAND_0000001",
            "profile": {"years_of_experience": 2},
            "education": [],
            "redrob_signals": {},
        }
        evidenced = {
            **base,
            "career_history": [
                {
                    "company": "Acme",
                    "title": "Data Engineer",
                    "start_date": "2024-06-24",
                    "end_date": None,
                    "duration_months": 24,
                    "is_current": True,
                    "description": (
                        "Built and operated real-time Kafka streaming pipelines; "
                        "reduced latency to 100ms at 50M events daily."
                    ),
                }
            ],
            "skills": [{"name": "Kafka"}],
        }
        skills_only = {
            **base,
            "career_history": [
                {
                    "company": "Acme",
                    "title": "Data Engineer",
                    "start_date": "2024-06-24",
                    "end_date": None,
                    "duration_months": 24,
                    "is_current": True,
                    "description": "Worked with the engineering team.",
                }
            ],
            "skills": [{"name": "Kafka"}],
        }
        rich = extract_features(evidenced, date(2026, 6, 24))
        weak = extract_features(skills_only, date(2026, 6, 24))
        self.assertGreater(rich["production_score"], weak["production_score"])
        self.assertGreater(rich["specificity_score"], weak["specificity_score"])

    def test_skill_claim_support(self):
        record = {
            "candidate_id": "CAND_0000002",
            "profile": {"years_of_experience": 1},
            "career_history": [
                {
                    "company": "Acme",
                    "title": "Engineer",
                    "start_date": "2025-06-24",
                    "end_date": None,
                    "duration_months": 12,
                    "is_current": True,
                    "description": "Built a search ranking service.",
                }
            ],
            "education": [],
            "skills": [{"name": "Search"}, {"name": "Machine Learning"}],
            "redrob_signals": {},
        }
        features = extract_features(record, date(2026, 6, 24))
        self.assertEqual(features["evidence_support_score"], 50.0)

    def test_consulting_and_contradictions(self):
        record = {
            "candidate_id": "CAND_0000003",
            "profile": {"years_of_experience": 10},
            "career_history": [
                {
                    "company": "TCS",
                    "title": "Associate",
                    "start_date": "2025-06-24",
                    "end_date": None,
                    "duration_months": 12,
                    "is_current": True,
                    "description": "",
                }
            ],
            "education": [{"start_year": 2020, "end_year": 2019}],
            "skills": [],
            "redrob_signals": {},
        }
        features = extract_features(record, date(2026, 6, 24))
        self.assertTrue(features["consulting_only_flag"])
        self.assertEqual(features["consulting_ratio"], 1.0)
        self.assertGreater(features["contradiction_score"], 40)


if __name__ == "__main__":
    unittest.main()
