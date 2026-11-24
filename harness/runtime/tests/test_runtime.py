import importlib.util,json,tempfile,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"runner.py"
spec=importlib.util.spec_from_file_location("runner",p);r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
class Runtime(unittest.TestCase):
    def test_bootstrap_authority(self):
        b=r.bootstrap();self.assertFalse(b["state"]["approved_animation"]);self.assertEqual(b["contract"]["mode"],"replay_only")
    def test_ids(self):
        for s in ["../escape","a/b","", "a b"]:
            with self.assertRaises(ValueError):r.safe_id(s)
        self.assertEqual(r.safe_id("replay-01"),"replay-01")
    def test_atomic(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"s.json";r.atomic(p,{"v":1});r.atomic(p,{"v":2});self.assertEqual(r.read(p),{"v":2});self.assertFalse((Path(d)/"s.json.tmp").exists())
    def test_tamper_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=root/"source";p.write_bytes(b"good");h=r.sha(p);reg=root/"registry.json";r.atomic(reg,{"schema_version":1,"items":{"test":{"path":str(p),"sha256":h}},"python":str(p)})
            self.assertEqual(r.validate_registry(reg,{"inputs":[{"id":"test"}]})["schema_version"],1)
            p.write_bytes(b"bad")
            with self.assertRaisesRegex(ValueError,"hash mismatch"):r.validate_registry(reg,{"inputs":[{"id":"test"}]})
    def test_no_promotion(self):
        c=r.contract();self.assertFalse(c["acceptance"]["author_approval"]);self.assertIn("new animation",c["non_goals"])
if __name__=="__main__":unittest.main()
