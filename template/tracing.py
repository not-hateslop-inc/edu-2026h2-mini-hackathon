import json, time
from pathlib import Path


class Trace:
    def __init__(self, run_id: str, root: str = "traces"):
        Path(root).mkdir(exist_ok=True)
        self.path = Path(root) / f"{run_id}.jsonl"
        self.t0 = time.time()

    def log(self, step: int, kind: str, **data):
        rec = {"t": round(time.time() - self.t0, 2), "step": step, "kind": kind, **data}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
