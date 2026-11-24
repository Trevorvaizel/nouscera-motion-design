import sys,unittest,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from handoff_check import evaluate,FIELDS
class HandoffTests(unittest.TestCase):
    def test_valid_fixture(self):self.assertEqual(evaluate(json.dumps(FIELDS))["status"],"pass")
    def test_model_cannot_approve(self):
        obj=dict(FIELDS,animation_approved=True)
        self.assertEqual(evaluate(json.dumps(obj))["status"],"fail")
    def test_nonresponse_not_pass(self):
        self.assertEqual(evaluate("",1)["status"],"invocation_failed")
        self.assertEqual(evaluate("")["status"],"invalid_response")
    def test_wrong_type(self):
        obj=dict(FIELDS,creative_test_allowed=0)
        self.assertEqual(evaluate(json.dumps(obj))["status"],"fail")
