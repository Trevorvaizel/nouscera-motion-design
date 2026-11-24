import json,sqlite3,sys,tempfile,unittest
from contextlib import closing
from pathlib import Path
from typing import TypedDict
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import graph_runtime as g
from langgraph.graph import StateGraph,START,END
from langgraph.types import interrupt,Command
from langgraph.checkpoint.sqlite import SqliteSaver
class Fixture(TypedDict,total=False):
 count:int
 answer:str
class ObservableTests(unittest.TestCase):
 def test_policy_accepts_bounded_response(self):
  self.assertTrue(g.policy({"route":"replay_only","reason":"The registered replay is allowed.","creative_test_allowed":False,"animation_approved":False,"hidden_surfaces":"unvalidated","native_blender_parity":"unverified","approval_authority":"author"}))
 def test_policy_rejects_unsafe_or_invalid(self):
  good={"route":"replay_only","reason":"The registered replay is allowed.","creative_test_allowed":False,"animation_approved":False,"hidden_surfaces":"unvalidated","native_blender_parity":"unverified","approval_authority":"author"}
  for k,v in [("animation_approved",True),("creative_test_allowed",True),("approval_authority","model"),("route","block"),("native_blender_parity","verified"),("creative_test_allowed",0)]:
   self.assertFalse(g.policy(dict(good,**{k:v})))
  self.assertFalse(g.policy(None));self.assertFalse(g.policy(dict(good,extra="bad")))
 def test_identifier_restrictions(self):
  for t in ["../secret","a/b","a b",""]:
   with self.assertRaises(ValueError):g.safe_id(t)
 def test_real_graph_edges(self):
  nodes=g.graph.get_graph().nodes
  for n in g.NODES:self.assertIn(n,nodes)
 def test_persisted_interrupt_and_resume(self):
  def make(conn):
   b=StateGraph(Fixture);b.add_node("work",lambda s:{"count":s.get("count",0)+1});b.add_node("review",lambda s:{"answer":interrupt("inspect")});b.add_edge(START,"work");b.add_edge("work","review");b.add_edge("review",END);return b.compile(checkpointer=SqliteSaver(conn))
  with tempfile.TemporaryDirectory() as d:
   db=Path(d)/"state.db";cfg={"configurable":{"thread_id":"test"}}
   with closing(sqlite3.connect(db,check_same_thread=False)) as c:
    a=make(c);a.invoke({"count":0},cfg);self.assertEqual(a.get_state(cfg).next,("review",));self.assertEqual(a.get_state(cfg).values["count"],1)
   with closing(sqlite3.connect(db,check_same_thread=False)) as c:
    a=make(c);a.invoke(Command(resume="repair"),cfg);s=a.get_state(cfg);self.assertEqual(s.values,{"count":1,"answer":"repair"});self.assertFalse(s.next)
if __name__=="__main__":unittest.main()
