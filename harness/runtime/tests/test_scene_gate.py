import importlib.util,tempfile,unittest,struct
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scene_gate.py"
spec=importlib.util.spec_from_file_location("scene_gate",p);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
class Scene(unittest.TestCase):
    def test_contract(self):
        # Header-only fixture tests metadata; full PNG decoding is exercised by integration verifier.
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=root/"a.png";p.write_bytes(b"\x89PNG\r\n\x1a\n"+b"\x00\x00\x00\x0dIHDR"+struct.pack(">II",8,8))
            a={"file":"a.png","sha256":g.sha(p)}
            m={"schema_version":1,"scene_id":"fixture","size":[8,8],"source":a,"required_roles":{"page":"fixed","tool":"rigid"},"entities":{"page":{"behavior":"fixed","motion":"identity","asset":a},"tool":{"behavior":"rigid","motion":"rotation_translation_only","asset":a}},"hidden_surfaces":[],"occlusion_possible":False}
            self.assertEqual(g.inspect(m,root)["status"],"asset_contract_pass")
            m["occlusion_possible"]=True;self.assertEqual(g.inspect(m,root)["status"],"blocked")
            m["entities"]["page"]["motion"]="warp";self.assertEqual(g.inspect(m,root)["status"],"invalid")
            m["entities"]["page"]["motion"]="identity";m["entities"]["tool"]["motion"]="scale";self.assertEqual(g.inspect(m,root)["status"],"invalid")
            m["entities"]["tool"]["motion"]="rotation_translation_only";m["entities"]["page"]["depends_on"]=["tool"];m["entities"]["tool"]["depends_on"]=["page"];self.assertEqual(g.inspect(m,root)["status"],"invalid")
            m["entities"]["page"]["depends_on"]=[];m["entities"]["tool"]["depends_on"]=[];m["entities"]["tool"]["asset"]={"file":"../bad","sha256":"x"};self.assertEqual(g.inspect(m,root)["status"],"invalid")
if __name__=="__main__":unittest.main()
