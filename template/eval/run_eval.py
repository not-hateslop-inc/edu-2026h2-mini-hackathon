# 10회차 채점 스크립트와 같은 방식입니다. 팀 케이스를 10개로 늘려 주세요.
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from langgraph.errors import GraphRecursionError
from agent import graph

HERE = Path(__file__).resolve().parent
cases = [json.loads(l) for l in (HERE / "cases.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
passed = 0
for c in cases:
    e = c["expect"]
    cfg = {"configurable": {"thread_id": f"{c['id']}-{time.time()}"}, "recursion_limit": 2 * e.get("max_steps", 8)}
    calls, inter, steps = [], False, 0
    try:
        for ev in graph.stream({"messages": [("user", c["question"])]}, cfg, stream_mode="updates"):
            steps += 1
            if "__interrupt__" in ev:
                inter = True; break
            for u in ev.values():
                for m in u.get("messages", []):
                    calls += [tc["name"] for tc in getattr(m, "tool_calls", [])]
    except GraphRecursionError:
        pass
    ok = all(t in calls for t in e.get("must_call", [])) and inter == e.get("must_interrupt", False) and steps <= e.get("max_steps", 8)
    passed += ok
    print(c["id"], "PASS" if ok else "FAIL", calls)
print(f"{passed}/{len(cases)}")
