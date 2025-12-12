#!/usr/bin/env python3
"""
thinking_machine.py

Single-file "thinking machine" prototype combining:
- GPU-aware orchestrator that routes GPT tasks to GPU or CPU based on GPU load threshold.
- Lattice (n-dimensional) of digital agents that call a GPT wrapper.
- GPT wrapper with two modes: local Hugging Face (if available) or a lightweight mock generator for offline/free use.
- Run/demo to produce JSON artifacts of runs.
- Comparison utility to compute midpoint (50%), percent differences, ratios, and a "re-engineered" third-result narrative.
- Optional: write example GitHub Actions workflow YAML / composite action files to disk.

Usage examples:
  # run a demo (creates run_result_<timestamp>.json)
  python thinking_machine.py demo --dims 3 3 --tasks 9

  # run a single text through automated GPT_TASK pipeline
  python thinking_machine.py run-text "hello world"

  # compare two run JSON files
  python thinking_machine.py compare runA.json runB.json

  # write sample GitHub Actions workflow + composite action files (local only)
  python thinking_machine.py write-workflow

Notes:
- By default this uses a simple mock GPT generator (no cloud, no charges).
- If you want local HF model inference, install transformers and torch and set env var USE_LOCAL_HF=1 and optionally HF_MODEL to a cached model name.
- Optional dependencies (for better GPU monitoring): pynvml, psutil
"""

from __future__ import annotations
import argparse
import asyncio
import concurrent.futures
import json
import os
import sys
import time
import random
import math
from typing import Any, Dict, List, Tuple, Optional
from datetime import datetime
from statistics import mean

# -----------------------
# Optional dependencies
# -----------------------
try:
    import pynvml
    pynvml.nvmlInit()
    NVML_AVAILABLE = True
except Exception:
    NVML_AVAILABLE = False

# If user wants to use HF local model:
USE_LOCAL_HF = os.getenv("USE_LOCAL_HF", "0") in ("1", "true", "True")
HF_MODEL = os.getenv("HF_MODEL", "distilgpt2")

# Try to import transformers & torch if requested
TRANSFORMERS_AVAILABLE = False
if USE_LOCAL_HF:
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch
        TRANSFORMERS_AVAILABLE = True
    except Exception:
        TRANSFORMERS_AVAILABLE = False

# Thread pool for blocking calls
THREAD_EXECUTOR = concurrent.futures.ThreadPoolExecutor(max_workers=6)

# -----------------------
# Utility: GPU monitoring
# -----------------------
def gpu_util_percent() -> float:
    """
    Return GPU utilization percent for GPU 0 if available, else 0.0.
    Requires pynvml installed to get accurate values. Graceful fallback to 0.0.
    """
    if not NVML_AVAILABLE:
        return 0.0
    try:
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        util = pynvml.nvmlDeviceGetUtilizationRates(handle)
        return float(util.gpu)
    except Exception:
        return 0.0

# -----------------------
# GPT Wrapper
# -----------------------
class GPTWrapper:
    """
    Abstraction for a GPT-like generator.
    Modes:
      - mock: simple local deterministic/stochastic text transform (default)
      - local HF: use transformers AutoModelForCausalLM (if USE_LOCAL_HF and transformers installed)
    """

    def __init__(self, mode: str = "auto"):
        # mode auto: prefer HF if USE_LOCAL_HF and available, else mock
        if mode not in ("auto", "mock", "local_hf"):
            raise ValueError("mode must be one of 'auto', 'mock', 'local_hf', 'auto'")
        if mode == "local_hf":
            self.mode = "local_hf"
        elif mode == "mock":
            self.mode = "mock"
        else:
            if USE_LOCAL_HF and TRANSFORMERS_AVAILABLE:
                self.mode = "local_hf"
            else:
                self.mode = "mock"

        self._init_local_hf()

    def _init_local_hf(self):
        self.tokenizer = None
        self.model = None
        self.device = None
        if self.mode == "local_hf" and TRANSFORMERS_AVAILABLE:
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(HF_MODEL)
                self.model = AutoModelForCausalLM.from_pretrained(HF_MODEL)
                import torch
                self.device = "cuda" if torch.cuda.is_available() else "cpu"
                self.model.to(self.device)
            except Exception as e:
                # fallback to mock
                print("Warning: failed to init HF model, falling back to mock. Error:", e, file=sys.stderr)
                self.mode = "mock"

    def _mock_generate(self, prompt: str, max_length: int = 64) -> str:
        # Deterministic-ish, cheap generation using prompt manipulation
        # Simulate different behavior than CPU fallback vs GPU path by sometimes reversing, uppercasing, etc.
        seed = sum(ord(c) for c in prompt) % 1000
        r = random.Random(seed)
        style = r.choice(["upper", "reverse", "echo", "shuffle"])
        base = prompt.strip()
        if style == "upper":
            out = base.upper()
        elif style == "reverse":
            out = base[::-1]
        elif style == "echo":
            out = (base + " ") * (1 + (r.randint(0, 2)))
        elif style == "shuffle":
            parts = base.split()
            r.shuffle(parts)
            out = " ".join(parts)
        else:
            out = base
        # truncate/extend to max_length words approx
        words = out.split()
        if len(words) > max_length:
            words = words[:max_length]
        return " ".join(words)

    def _sync_generate_local_hf(self, prompt: str, max_length: int = 64) -> str:
        # Blocking model generation (runs in executor)
        assert self.model is not None and self.tokenizer is not None
        import torch
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512).to(self.device)
        # generate with safety defaults
        out = self.model.generate(**inputs, max_new_tokens=max_length, do_sample=True, top_p=0.95, temperature=0.8)
        text = self.tokenizer.decode(out[0], skip_special_tokens=True)
        return text

    async def generate(self, prompt: str, max_length: int = 64) -> str:
        """
        Async wrapper that returns generated string.
        """
        loop = asyncio.get_running_loop()
        if self.mode == "mock":
            # fast synchronous mock
            return self._mock_generate(prompt, max_length)
        else:
            # run heavy local HF generation in blocking thread to avoid blocking loop
            return await loop.run_in_executor(THREAD_EXECUTOR, self._sync_generate_local_hf, prompt, max_length)

# -----------------------
# Lattice (N-D grid)
# -----------------------
class Lattice:
    def __init__(self, dims: Tuple[int, ...]):
        """
        dims: tuple of ints, e.g., (3,3) for 2D lattice 3x3
        Nodes labeled n0, n1, ...
        """
        import itertools
        self.dims = tuple(dims)
        self.nodes: Dict[str, Dict[str, Any]] = {}
        idx = 0
        for coord in itertools.product(*[range(d) for d in self.dims]):
            nid = f"n{idx}"
            self.nodes[nid] = {"id": nid, "coord": coord, "memory": {}, "meta": {}}
            idx += 1

    def neighbors(self, node_id: str) -> List[str]:
        coord = self.nodes[node_id]["coord"]
        neigh = []
        for nid, info in self.nodes.items():
            if nid == node_id:
                continue
            dist = sum(abs(a - b) for a, b in zip(coord, info["coord"]))
            if dist == 1:
                neigh.append(nid)
        return neigh

    def get_node_ids(self) -> List[str]:
        return list(self.nodes.keys())

# -----------------------
# Agent
# -----------------------
class Agent:
    def __init__(self, id: str, lattice: Lattice, orchestrator: "Orchestrator", memory: Optional[Dict] = None):
        self.id = id
        self.lattice = lattice
        self.orchestrator = orchestrator
        self.memory = memory or {}

    async def handle_message(self, message: str) -> Dict[str, Any]:
        """
        Create prompt using memory and call GPT wrapper via orchestrator's generator.
        """
        t0 = time.perf_counter()
        prompt = f"Agent {self.id} memory: {self.memory}\nInput: {message}\nRespond concisely:"
        # Use orchestrator's gpt wrapper for generation
        gen = await self.orchestrator.gpt.generate(prompt, max_length=64)
        # Update memory (simple update)
        self.memory["last_input"] = message
        self.memory["last_response"] = gen
        t1 = time.perf_counter()
        return {"agent": self.id, "input": message, "response": gen, "latency_s": t1 - t0}

    async def forward_to_neighbors(self, message: str):
        for nid in self.lattice.neighbors(self.id):
            # fire-and-forget forwarding
            asyncio.create_task(self.orchestrator.send_to_agent(nid, f"Forward from {self.id}: {message}"))

# -----------------------
# Orchestrator
# -----------------------
class Orchestrator:
    def __init__(self, lattice: Lattice, gpt: GPTWrapper, cpu_workers: int = 4, gpu_threshold: float = 70.0):
        self.lattice = lattice
        self.gpt = gpt
        self.cpu_executor = concurrent.futures.ProcessPoolExecutor(max_workers=cpu_workers)
        self.gpu_threshold = gpu_threshold
        self.agents: Dict[str, Agent] = {}
        self.metrics: Dict[str, Any] = {"routes": {"cpu": 0, "gpu": 0}, "tasks": []}

    def register_agent(self, agent: Agent):
        self.agents[agent.id] = agent

    def register_all_agents(self):
        for nid in self.lattice.get_node_ids():
            a = Agent(nid, self.lattice, self)
            self.register_agent(a)

    async def _cpu_fallback_sync(self, agent_id: str, message: str) -> Dict[str, Any]:
        """
        CPU fallback synchronous handler executed inside a process pool.
        This function must be picklable: keep minimal imports.
        We'll implement a simple deterministic "CPU fallback" behavior to avoid heavy dependencies.
        """
        # Simple deterministic transformation
        resp = f"CPU_FALLBACK[{agent_id}]: {message.upper()}"
        return {"agent": agent_id, "input": message, "response": resp, "latency_s": 0.0}

    async def send_to_agent(self, agent_id: str, message: str) -> Dict[str, Any]:
        """
        Decide routing based on GPU load. If GPU > threshold -> route to CPU fallback (process pool).
        Else run agent.handle_message coroutine (which internally calls GPT wrapper).
        """
        ts0 = time.perf_counter()
        gutil = gpu_util_percent()
        route_to_cpu = gutil > self.gpu_threshold
        if route_to_cpu:
            self.metrics["routes"]["cpu"] += 1
            loop = asyncio.get_running_loop()
            # run cpu fallback in executor; use run_in_executor with ProcessPoolExecutor
            res = await loop.run_in_executor(self.cpu_executor, self._cpu_fallback_sync_blocking, agent_id, message)
        else:
            self.metrics["routes"]["gpu"] += 1
            res = await self.agents[agent_id].handle_message(message)
        ts1 = time.perf_counter()
        res["routed_to"] = "cpu" if route_to_cpu else "gpu"
        res["total_latency_s"] = ts1 - ts0
        self.metrics["tasks"].append(res)
        return res

    @staticmethod
    def _cpu_fallback_sync_blocking(agent_id: str, message: str) -> Dict[str, Any]:
        """
        Blocking wrapper for CPU fallback to be executed in a separate process.
        Keep it top-level static/picklable.
        """
        # Emulate some CPU work
        time.sleep(0.05 + random.random() * 0.05)
        resp = f"CPU_FALLBACK[{agent_id}]: {message.upper()}"
        return {"agent": agent_id, "input": message, "response": resp, "latency_s": 0.05}

# -----------------------
# GPT Task automation (personal instruction integrated)
# -----------------------
# Personal instruction: DEFINE GPT_TASK = CALL GPT(AI231) AUTOMATE GPT_TASK ON INPUT(TEXT)
# IF LOAD(GPU) > 70% THEN DISTRIBUTE(TASK, CPU)asyncio.ensure_future(gpt_task_automation("abc")) else: ...

async def gpt_task_automation(orchestrator: Orchestrator, input_text: str) -> Dict[str, Any]:
    """
    Automates scheduling a single GPT_TASK according to the rule:
      - If GPU load > orchestrator.gpu_threshold -> distribute to CPU fallback
      - else run normal generator path (agent.handle_message)
    Returns result dict.
    """
    # Choose a target agent (simple round-robin or random)
    agent_id = random.choice(orchestrator.lattice.get_node_ids())
    # Schedule via orchestrator's send_to_agent which internally routes by GPU
    result = await orchestrator.send_to_agent(agent_id, input_text)
    return result

# Convenience wrapper to schedule multiple tasks, as in personal instruction example
def schedule_async_tasks(loop: asyncio.AbstractEventLoop, coro_futures: List[asyncio.Task]):
    # Ensure futures are scheduled (similar to asyncio.ensure_future)
    for t in coro_futures:
        asyncio.ensure_future(t, loop=loop)

# -----------------------
# Demo runner and persistence
# -----------------------
def write_json_file(obj: Any, filename: str):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, default=str)

async def run_demo(dims: Tuple[int, ...], num_tasks: int, use_local_hf: bool = False, gpu_threshold: float = 70.0) -> str:
    """
    Run a single demo execution: build lattice, orchestrator, dispatch tasks equal to num_tasks,
    gather results and write a run_result_{timestamp}.json file. Returns filename.
    """
    # Initialize GPT wrapper
    mode = "auto"
    if use_local_hf:
        mode = "local_hf"
    gpt = GPTWrapper(mode=mode)
    lattice = Lattice(dims)
    orchestrator = Orchestrator(lattice, gpt, cpu_workers=4, gpu_threshold=gpu_threshold)
    orchestrator.register_all_agents()

    # Build tasks (one message per node up to num_tasks)
    node_ids = lattice.get_node_ids()
    tasks = []
    for i in range(num_tasks):
        text = f"demo message {i}"
        # schedule gpt_task_automation
        tasks.append(gpt_task_automation(orchestrator, text))

    results = await asyncio.gather(*tasks)
    timestamp = int(time.time())
    out = {"timestamp": timestamp, "dims": dims, "metrics": orchestrator.metrics, "results": results}
    filename = f"run_result_{timestamp}.json"
    write_json_file(out, filename)
    print(f"Wrote {filename}")
    return filename

# -----------------------
# Comparison utility
# -----------------------
def summarize_run(run: Dict[str, Any]) -> Dict[str, Any]:
    metrics = run.get("metrics", {})
    tasks = metrics.get("tasks", [])
    num_tasks = len(tasks)
    avg_latency = None
    try:
        latencies = [float(t.get("total_latency_s", 0.0)) for t in tasks if t.get("total_latency_s") is not None]
        avg_latency = mean(latencies) if latencies else None
    except Exception:
        avg_latency = None
    cpu_routes = metrics.get("routes", {}).get("cpu", 0)
    gpu_routes = metrics.get("routes", {}).get("gpu", 0)
    return {"num_tasks": num_tasks, "avg_latency": avg_latency, "cpu_routes": cpu_routes, "gpu_routes": gpu_routes}

def compare_runs(file_a: str, file_b: str) -> Dict[str, Any]:
    """
    Compare two run JSON files and compute:
    - absolute differences
    - relative difference percent vs A
    - midpoint (50%) for numeric metrics
    - ratio B/A
    - "third result" as midpoint and a re-engineered perception narrative
    Returns a dict with metrics and narrative.
    """
    a = json.load(open(file_a, "r", encoding="utf-8"))
    b = json.load(open(file_b, "r", encoding="utf-8"))
    sa = summarize_run(a)
    sb = summarize_run(b)
    keys = set(sa.keys()) | set(sb.keys())
    report = {"A_file": file_a, "B_file": file_b, "comparison": {}, "narrative": ""}
    comp_lines = []
    for k in sorted(keys):
        va = sa.get(k)
        vb = sb.get(k)
        entry = {"A": va, "B": vb}
        if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
            abs_diff = vb - va
            ratio = None
            rel_pct = None
            if va != 0:
                ratio = vb / va
                rel_pct = (abs_diff / va) * 100.0
            midpoint = (va + vb) / 2.0
            # percent distance of each value to midpoint
            dist_a_to_mid_pct = None
            dist_b_to_mid_pct = None
            if midpoint != 0:
                dist_a_to_mid_pct = ((midpoint - va) / midpoint) * 100.0
                dist_b_to_mid_pct = ((vb - midpoint) / midpoint) * 100.0
            entry.update({
                "absolute_difference": abs_diff,
                "relative_difference_pct_vs_A": rel_pct,
                "ratio_B_over_A": ratio,
                "midpoint_50pct": midpoint,
                "distance_A_to_mid_pct": dist_a_to_mid_pct,
                "distance_B_to_mid_pct": dist_b_to_mid_pct
            })
            comp_lines.append(f"{k}: A={va}, B={vb}, diff={abs_diff}, rel%={rel_pct}, midpoint={midpoint}, ratio={ratio}")
        else:
            entry["note"] = "non-numeric or missing"
            comp_lines.append(f"{k}: non-numeric or missing (A={va}, B={vb})")
        report["comparison"][k] = entry

    # Build narrative: emphasize differences and produce a "re-engineered perception" (third result = midpoint)
    narrative_parts = []
    narrative_parts.append("Comparison summary:")
    narrative_parts.extend(comp_lines)
    narrative_parts.append("")
    narrative_parts.append("Re-engineered third result (per metric midpoint = 50% point) and interpretation:")
    for k, v in report["comparison"].items():
        if "midpoint_50pct" in v and v["midpoint_50pct"] is not None:
            a = v["A"]
            b = v["B"]
            mid = v["midpoint_50pct"]
            # Evaluate which side closer to midpoint
            da = abs(mid - a)
            db = abs(b - mid) if b is not None else None
            closer = "A" if (db is None or da <= db) else "B"
            narrative_parts.append(f"- {k}: midpoint={mid:.6f}. Closer to {closer}. Ratio(B/A)={v.get('ratio_B_over_A')}.")
        else:
            narrative_parts.append(f"- {k}: cannot compute midpoint (non-numeric).")
    # Precision: compute percent precision of ratio where applicable
    narrative_parts.append("")
    narrative_parts.append("Precision summary (ratio percent and midpoint precision):")
    for k, v in report["comparison"].items():
        ratio = v.get("ratio_B_over_A")
        mid = v.get("midpoint_50pct")
        if ratio is not None:
            narrative_parts.append(f"- {k}: ratio={ratio:.6f}, ratio_pct={ratio*100.0:.3f}%")
        if mid is not None:
            # compute decimal precision suggestion
            narrative_parts.append(f"- {k}: midpoint approximated as {mid:.6f}")
    report["narrative"] = "\n".join(narrative_parts)
    # write summary file
    timestamp = int(time.time())
    outfn = f"compare_report_{timestamp}.json"
    write_json_file(report, outfn)
    print(f"Wrote {outfn}")
    print(report["narrative"])
    return report

# -----------------------
# Optional: generate example GitHub Actions workflow + composite action (writes files locally)
# -----------------------
EXAMPLE_WORKFLOW = """name: Branches managers

on:
  push:
    branches:
      - feature/structure-repository
  workflow_dispatch:

jobs:
  test-and-jules:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Install npm dependencies
        run: npm ci

      - name: Run tests and save log
        run: |
          mkdir -p logs
          npm run test 2>&1 | tee logs/test.log

      - name: Install Jules CLI globally
        run: |
          npm install -g @google/jules
          jules --version || true

      - name: Jules login (optional, uses secret)
        env:
          JULES_TOKEN: ${{{{ secrets.JULES_TOKEN }}}}
        run: |
          if [ -n "$JULES_TOKEN" ]; then
            jules login --token "$JULES_TOKEN" > logs/jules-login.log 2>&1 || jules login --stdin <<< "$JULES_TOKEN" >> logs/jules-login.log 2>&1 || true
          else
            echo "JULES_TOKEN not set; skipping automated jules login"
          fi

      - name: Jules remote list for this repo
        run: |
          jules remote list --repo "${{{{ github.repository }}}}" > logs/jules-remote-list.log 2>&1 || true

      - name: Upload logs
        uses: actions/upload-artifact@v4
        with:
          name: branches-managers-logs-${{{{ github.run_id }}}}
          path: logs/
"""

EXAMPLE_ACTION_YML = """name: "Setup Jules CLI"
description: "Install @google/jules globally and optionally perform login using a token"
inputs:
  token:
    description: 'Jules token (optional). If not provided, login is skipped.'
    required: false
runs:
  using: "composite"
  steps:
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
    - name: Install Jules CLI globally
      shell: bash
      run: |
        npm install -g @google/jules
        jules --version || true
    - name: Jules login (optional)
      if: ${{{{ inputs.token }}}}
      shell: bash
      run: |
        echo "${{{{ inputs.token }}}}" | jules login --stdin || jules login --token "${{{{ inputs.token }}}}" || true
"""

def write_workflow_files(dest_dir: str = "."):
    workflows_dir = os.path.join(dest_dir, ".github", "workflows")
    actions_dir = os.path.join(dest_dir, ".github", "actions", "setup-jules")
    os.makedirs(workflows_dir, exist_ok=True)
    os.makedirs(actions_dir, exist_ok=True)
    wf_path = os.path.join(workflows_dir, "branches-managers.yml")
    action_yml_path = os.path.join(actions_dir, "action.yml")
    with open(wf_path, "w", encoding="utf-8") as f:
        f.write(EXAMPLE_WORKFLOW)
    with open(action_yml_path, "w", encoding="utf-8") as f:
        f.write(EXAMPLE_ACTION_YML)
    print(f"Wrote workflow to {wf_path} and action to {action_yml_path}")

# -----------------------
# CLI
# -----------------------
def parse_args():
    p = argparse.ArgumentParser(prog="thinking_machine.py")
    sub = p.add_subparsers(dest="cmd", required=True)

    dsp = sub.add_parser("demo", help="Run demo and produce run_result JSON")
    dsp.add_argument("--dims", nargs="+", type=int, default=[3,3], help="Lattice dimensions (e.g., --dims 3 3)")
    dsp.add_argument("--tasks", type=int, default=9, help="Number of tasks to dispatch")
    dsp.add_argument("--use-local-hf", action="store_true", help="Use local HF model if installed (may download big models)")
    dsp.add_argument("--gpu-threshold", type=float, default=70.0, help="GPU usage % threshold to route to CPU fallback")

    rp = sub.add_parser("run", help="Run the agent")
    rp.add_argument("--csv", type=str, help="Path to phenons.csv")
    rp.add_argument("--json", type=str, help="Path to experiments.json")
    rp.add_argument("--out", type=str, help="Path to output report.html")
    rp.add_argument("--out-csv", type=str, help="Path to output merged.csv")
    rp.add_argument("--interval-minutes", type=int, default=60, help="Interval in minutes")

    rtp = sub.add_parser("run-text", help="Run single text through GPT_TASK automation")
    rtp.add_argument("text", type=str, help="Input text")
    rtp.add_argument("--dims", nargs="+", type=int, default=[3,3])
    rtp.add_argument("--use-local-hf", action="store_true")
    rtp.add_argument("--gpu-threshold", type=float, default=70.0)

    cmp = sub.add_parser("compare", help="Compare two run JSON files")
    cmp.add_argument("fileA", type=str)
    cmp.add_argument("fileB", type=str)

    wf = sub.add_parser("write-workflow", help="Write example GitHub Actions workflow and action to .github/")
    wf.add_argument("--dest", type=str, default=".")

    return p.parse_args()

def main_cli():
    args = parse_args()
    if args.cmd == "demo":
        dims = tuple(args.dims)
        asyncio.run(run_demo(dims, args.tasks, use_local_hf=args.use_local_hf, gpu_threshold=args.gpu_threshold))
    elif args.cmd == "run":
        # For now, just run the demo. Later, we can use the arguments to customize the run.
        dims = (3,3)
        tasks = 9
        asyncio.run(run_demo(dims, tasks))
    elif args.cmd == "run-text":
        dims = tuple(args.dims)
        # setup orchestrator environment and run one automation task
        async def run_one():
            gpt = GPTWrapper(mode="auto" if not args.use_local_hf else "local_hf")
            lattice = Lattice(dims)
            orch = Orchestrator(lattice, gpt, cpu_workers=2, gpu_threshold=args.gpu_threshold)
            orch.register_all_agents()
            result = await gpt_task_automation(orch, args.text)
            print(json.dumps(result, indent=2))
        asyncio.run(run_one())
    elif args.cmd == "compare":
        compare_runs(args.fileA, args.fileB)
    elif args.cmd == "write-workflow":
        write_workflow_files(args.dest)
    else:
        print("Unknown command", args.cmd)

if __name__ == "__main__":
    main_cli()
