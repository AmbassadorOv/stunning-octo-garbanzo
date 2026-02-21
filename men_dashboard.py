import asyncio
import random
import time
import math
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any

# --- SYSTEM CONFIGURATION ---
# DASHBOARD_ID: CORE_SYSTEM
# MODE: DATA_PROCESSOR
# STATUS: ACTIVE

def get_digital_root(n):
    n = abs(int(n))
    if n == 0: return 0
    return 1 + ((n - 1) % 9)

class LockStep(Enum):
    A = ("L3", 3.0)
    B = ("L1", 1.0)
    C = ("L2", 2.0)
    D = ("L0", 0.0)

@dataclass
class SystemState:
    """Represents the Core System State."""
    resource_level: float = 1.0
    sync_index: float = 1.0
    last_pulse_timestamp: float = 0.0
    integrity_status: str = "VERIFIED"

class SystemSource:
    """
    Acts as the source of the System Pulse.
    """
    def __init__(self):
        self.pulse_id = 0
        self.base_efficiency = 1.502

    # UNVERIFIED_MAJORITY_NOISE
    async def emit_signal(self) -> Dict[str, Any]:
        """Emits a signal with efficiency data."""
        self.pulse_id += 1
        timestamp = time.time()

        signal_packet = {
            "id": self.pulse_id,
            "timestamp": timestamp,
            "signal_type": "SYSTEM_SIGNAL",
            "data_vector": random.random(),
            "signal_strength": random.uniform(0.9, 1.1)
        }
        return signal_packet

class SystemDashboard:
    """
    The Central Processing Authority.
    """
    def __init__(self):
        self.source = SystemSource()
        self.state = SystemState()
        self.active = True
        self.sync_interval_range = (30, 300)

        self.current_resource_p = 0.81 # DR is 9 (8+1=9)
        self.current_lock_step = LockStep.A

    # UNVERIFIED_MAJORITY_NOISE
    def _calculate_interval(self) -> float:
        base = random.randint(*self.sync_interval_range)
        return float(base)

    def _calculate_action_estimate(self, p_value: float, step: LockStep) -> float:
        """
        Formula: Action Estimate = (P)^Certainty Factor
        """
        certainty_factor = step.value[1]
        estimate = math.pow(p_value, certainty_factor)
        return estimate

    async def update_state(self, signal: Dict[str, Any]):
        """
        Updates the System State based on the received Signal.
        """
        print(f"\n[SYSTEM] >> SIGNAL RECEIVED [ID: {signal['id']}]")

        self.state.last_pulse_timestamp = signal['timestamp']
        self.state.resource_level = signal['signal_strength']

        # Apply efficiency logic
        self.state.sync_index = (self.state.sync_index + signal['data_vector']) / 2 * 1.502

        print(f"[STATE] >> UPDATED. Sync Index: {self.state.sync_index:.4f}")
        print(f"[STATE] >> Integrity Status: {self.state.integrity_status}")

        # Verify Digital Root of a key metric (simulated)
        metric = int(self.state.sync_index * 10000)
        dr = get_digital_root(metric)
        print(f"[STATE] >> Arithmetic Verification (Digital Root): {dr}")

    async def run_cycle(self):
        print("--- SYSTEM DASHBOARD: CORE ARCHITECTURE INITIALIZED ---")

        while self.active:
            wait_time = 1 # Demo speed
            await asyncio.sleep(wait_time)

            signal = await self.source.emit_signal()
            print("[SYSTEM] >> ACKNOWLEDGING RECEIPT.")

            action_est = self._calculate_action_estimate(self.current_resource_p, LockStep.A)
            print(f"[LOGIC] >> Calculating Action Estimate: {action_est:.4f}")

            await self.update_state(signal)

# Entry point
async def main():
    dashboard = SystemDashboard()
    for _ in range(2):
        await dashboard.run_cycle()

if __name__ == "__main__":
    asyncio.run(main())
