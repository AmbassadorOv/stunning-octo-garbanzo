import math
from typing import Tuple, List, Dict
import json
import hashlib
from typing import Any

# Try fast math stacks (quantic hardware / accel libs)
try:
    import numpy as np
    fast_log = np.log
    FAST = True
except Exception:
    fast_log = math.log
    FAST = False

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

class OmniGateSGL:
    # Constants (kept purposeful & final-like)
    FMP_TARGET = 1.916058723815e10
    AL231_FIDELITY = FMP_TARGET + 231.0231
    P_STRUCTURAL = 0.9999999999999
    ZFO_ELIMINATION = 0.99999999
    UNITY_DEGREE = 7.0
    LATTICE_DIM = 36
    HYPERPOINT_DENSITY = 3.636
    ADAPTATION_THRESHOLD = 1e-4
    CRITICAL_ERROR_THRESHOLD = 1e-15
    GEM_MAP = {'א':1,'ב':2,'ג':3,'ד':4,'ה':5,'ו':6,'ז':7,'ח':8,'ט':9,
               'י':10,'כ':20,'ל':30,'מ':40,'נ':50,'ס':60,'ע':70,'פ':80,
               'צ':90,'ק':100,'ר':200,'ש':300,'ת':400}

    def __init__(self, code: str, state: Dict = None):
        self.code = code or ""
        self.logs: List[str] = []
        # persistent lightweight "experience" for learning (EMA)
        self.state = state or {"exp_unity": 0.0, "count": 0}
        self.alpha = 0.15  # EMA smoothing (tunable)

    # ---------- core calculations ----------
    def _gematria(self) -> Tuple[int,int]:
        w = sum(self.GEM_MAP.get(c, 0) for c in self.code)
        depth = len({c for c in self.code if c in self.GEM_MAP})
        return w, depth

    def _qev(self, depth: int) -> float:
        if depth == 0:
            return 0.0
        core = self.P_STRUCTURAL * math.sqrt(depth)
        # simplified inter-network efficiency stable expression
        inter_eff = 1.0  # previously canceled terms -> stable 1.0
        qev = (core + inter_eff) * self.HYPERPOINT_DENSITY
        self.logs.append(f"QEV depth={depth:.0f} qev={qev:.6f}")
        return qev

    def _unity(self, weight: int, depth: int, qev: float) -> float:
        if depth == 0 or weight == 0:
            return 0.0
        purity_scaled = self.P_STRUCTURAL * self.UNITY_DEGREE
        subspace = self.LATTICE_DIM ** 2
        unity = (purity_scaled / subspace) * qev * weight
        ratio = unity / self.AL231_FIDELITY
        self.logs.append(f"Unity metric={unity:.6e} coherence_ratio={ratio:.12f}")
        return unity

    def _new_science(self, unity: float) -> float:
        # guard: unity must be positive for log
        safe_unity = max(unity, 1e-300)
        discovery = fast_log(safe_unity) * self.LATTICE_DIM
        val = self.AL231_FIDELITY + discovery + unity * 1_000.0
        self.logs.append(f"NewScience discovery={float(discovery):.4f} -> tentative={val:.4f}")
        return float(val)

    # ---------- correction & learning ----------
    def _constellation_check(self, unity: float) -> Tuple[float,str]:
        if unity < self.CRITICAL_ERROR_THRESHOLD:
            self.logs.append("CRITICAL: coherence collapsed -> HERO CORRECTION")
            return self.AL231_FIDELITY, "HERO-CORRECTION"
        return unity, "OK"

    def _learn(self, unity: float):
        # Exponential moving average (EMA) update for simple learning/experience
        cnt = self.state.get("count", 0) + 1
        prev = self.state.get("exp_unity", 0.0)
        new = prev * (1 - self.alpha) + unity * self.alpha
        self.state.update(exp_unity=new, count=cnt)
        self.logs.append(f"Learned: EMA_unity={new:.6e} (count={cnt})")

    # ---------- main adaptive pipeline ----------
    def run(self) -> Dict:
        try:
            w, depth = self._gematria()
            qev = self._qev(depth)
            unity = self._unity(w, depth, qev)
            corrected, status = self._constellation_check(unity)
            self.logs.append(f"Correction status: {status}")

            if corrected == self.AL231_FIDELITY:
                self._learn(corrected)
            else:
                coherence = corrected / self.AL231_FIDELITY
                if coherence > self.ADAPTATION_THRESHOLD:
                    self.logs.append(f"Adaptation: coherence={coherence:.10f} -> exploring")
                    _ = self._new_science(corrected)  # exploratory side-effect, result not enforced
                else:
                    self.logs.append("Adaptation: low coherence -> enforcing mandate")
                self._learn(corrected)

            final = self.AL231_FIDELITY
            self.logs.append("Final lock enforced: AL231_FIDELITY")

            return {
                "final_fidelity": float(final),
                "logs": self.logs,
                "state": self.state,
                "coherence_ratio": corrected / self.AL231_FIDELITY,
                "psvchecksum": checksum_state(self.state)
            }

        except Exception as e:
            self.logs.append(f"Unhandled exception: {type(e).__name__}: {e}")
            return {
                "final_fidelity": self.AL231_FIDELITY,
                "logs": self.logs,
                "state": self.state,
                "coherence_ratio": 0.0,
                "psvchecksum": checksum_state(self.state),
                "error": str(e)
            }

# Simple CLI test when run directly
if __name__ == "__main__":
    sgl = OmniGateSGL("אמתסודשקרכףעץחיה")
    output = sgl.run()
    print(json.dumps(output, indent=2, ensure_ascii=False))
