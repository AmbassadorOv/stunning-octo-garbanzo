#!/usr/bin/env python3
"""
omnigatesgl.py
Single-file SGL 1.0 Omni-Gate X-Lattice Processor.
Implements A P T Q M I G L X pipeline with deterministic behavior and audit logging.
"""

import math
import json
import hashlib
from typing import Dict, Any, Tuple, Optional, List

# --- Constants ---
FMP_TARGET = 1.916058723815e10
AL231_FIDELITY = FMP_TARGET + 231.0231
P_STRUCTURAL = 0.9999999999999
UNITY_DEGREE = 7.0
HYPERPOINT_DENSITY = 3.636
ADAPTATION_THRESHOLD = 1e-4
CRITICAL_ERROR_THRESHOLD = 1e-15
ALPHA = 0.15
DEFAULT_LATTICE_DIM = 36

GEM_MAP = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9,
    'י': 10, 'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50, 'ס': 60, 'ע': 70, 'פ': 80,
    'צ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400
}

DMEState = Dict[str, float]

# --- Helpers ---
def gematria_calc(s: str) -> Tuple[int, int]:
    weight = 0
    unique_chars = set()
    for char in s:
        if char in GEM_MAP:
            weight += GEM_MAP[char]
            unique_chars.add(char)
    return weight, len(unique_chars)

def calculate_qev(depth: int) -> float:
    if not depth:
        return 0.0
    core = P_STRUCTURAL * math.sqrt(depth)
    inter_eff = 1.0
    return (core + inter_eff) * HYPERPOINT_DENSITY

def calculate_unity(weight: int, depth: int, qev_val: float, lattice_dim: int = DEFAULT_LATTICE_DIM) -> float:
    if not depth or not weight:
        return 0.0
    purity_scaled = P_STRUCTURAL * UNITY_DEGREE
    subspace = float(lattice_dim ** 2)
    return (purity_scaled / subspace) * qev_val * weight

def new_science_discovery(unity_metric: float) -> float:
    safe_metric = max(unity_metric, 1e-20)
    discovery = math.log(safe_metric) * float(DEFAULT_LATTICE_DIM)
    return AL231_FIDELITY + discovery + unity_metric * 1000.0

def process_state_update(incoming_state: DMEState, current_unity: float) -> Tuple[DMEState, float]:
    count = int(incoming_state.get('count', 0)) + 1
    prev_unity = float(incoming_state.get('exp_unity', 0.0))
    ema = prev_unity * (1 - ALPHA) + current_unity * ALPHA
    return {'exp_unity': ema, 'count': count}, ema

def checksum_state(state: Any) -> float:
    try:
        if isinstance(state, (list, tuple)):
            return float(sum([float(x) for x in state]))
        if isinstance(state, dict):
            return float(sum([float(v) for v in state.values() if isinstance(v, (int, float))]))
        return float(state)
    except Exception:
        h = hashlib.sha256(repr(state).encode()).hexdigest()
        return float(int(h[:12], 16) % (10**9))

# --- Omni Gate ---
def omnigaterun(
    code_input: str,
    incoming_state: Optional[DMEState] = None,
    context_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    logs: List[str] = []
    coherence_ratio = 0.0

    context = context_config or {}
    lattice_dim = int(context.get('lattice_dim', DEFAULT_LATTICE_DIM))
    logs.append(f"[X] LATTICEDIM={lattice_dim}")

    initial_state: DMEState = incoming_state if incoming_state is not None else {'exp_unity': 0.0, 'count': 0}
    logs.append(f"[I] Initial count={initial_state.get('count', 0)}")

    try:
        weight, depth = gematria_calc(code_input)
        q = calculate_qev(depth)
        u = calculate_unity(weight, depth, q, lattice_dim=lattice_dim)
        logs.append(f"[Q] Raw Unity={u:.6e} (W={weight}, D={depth})")

        corrected_unity = u
        status = "OK"
        if u < CRITICAL_ERROR_THRESHOLD:
            corrected_unity = AL231_FIDELITY
            status = "HERO-CORRECTION"
            logs.append("[M] HERO-CORRECTION triggered (coherence collapsed)")
        logs.append(f"[M] status={status}")

        coherence_ratio = corrected_unity / AL231_FIDELITY if AL231_FIDELITY != 0 else 0.0

        if corrected_unity == AL231_FIDELITY or coherence_ratio > ADAPTATION_THRESHOLD:
            if coherence_ratio > ADAPTATION_THRESHOLD:
                logs.append(f"[P] Adaptation allowed (coherence={coherence_ratio:.10f})")
                discovery_value = new_science_discovery(corrected_unity)
                logs.append(f"[P] Science discovery value={discovery_value:.6e}")
            else:
                logs.append("[P] HERO-CORRECTION enforced; skipping exploration")

            final_state, ema_unity = process_state_update(initial_state, corrected_unity)
            logs.append(f"[T] EMAunity={ema_unity:.6e} (count={final_state['count']})")
        else:
            final_state = initial_state.copy()
            logs.append(f"[P] Low coherence={coherence_ratio:.10f}; structural lock enforced (no learning)")

        logs.append("[G] Governance packaging complete")
        final_lock_value = AL231_FIDELITY
        logs.append(f"[A] AL231FIDELITY={final_lock_value:.12e}")

        return {
            "finalfidelity": final_lock_value,
            "logs": logs,
            "state": final_state,
            "coherenceratio": coherence_ratio,
            "psvchecksum": checksum_state(final_state)
        }

    except Exception as e:
        logs.append(f"[ERROR] {repr(e)}")
        return {
            "finalfidelity": AL231_FIDELITY,
            "logs": logs,
            "state": initial_state,
            "coherenceratio": coherence_ratio,
            "error": str(e)
        }

# Demo entrypoint
if __name__ == "__main__":
    sample = "אמתסודשקרכףעץחיה"
    print(json.dumps(omnigaterun(sample), indent=2, ensure_ascii=False))
