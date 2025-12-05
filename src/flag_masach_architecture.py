import math
import hashlib
from abc import ABC, abstractmethod
import sys

# ==============================================================================
# 👑 INNER SEAL: CONCRETE ARCHITECTURAL IMPLEMENTATION (MASACH EDITION)
# Principle: Masach (Screen) at the boundary prevents Shevirat HaKelim.
# ==============================================================================

# I. FINAL AXIOMS
CF_FACTORS = { 'A': 3, 'B': 1, 'C': 2, 'D': 0 }
MAHUT_HA_OHR_FREQUENCY = {
    "ATZILUT": 4.0, "BERIAH": 3.0, "YETZIRAH": 2.0, "ASSIAH": 1.0
}
R_IDEAL_BALANCE = 216

# II. CONCRETE IMPLEMENTATION OF ARCHITECTURAL INTERFACES

class ConcreteAxiom(ABC):
    """Base class providing axiom access."""
    def get_cf(self, step_id: str) -> int:
        return CF_FACTORS.get(step_id.upper(), 0)

    def get_frequency(self, world_name: str) -> float:
        return MAHUT_HA_OHR_FREQUENCY.get(world_name.upper(), 1.0)

    def get_ideal_balance(self) -> int:
        return R_IDEAL_BALANCE

class ConcreteProcessor(ConcreteAxiom, ABC):
    """Implements the Lion's Route Protocol (Action Estimate)."""
    def __init__(self, world_name: str, step_id: str):
        self.world_name = world_name
        self.step_id = step_id
        self.frequency = self.get_frequency(world_name)
        self.certainty_factor = self.get_cf(step_id)

    def calculate_action_estimate(self, P: float) -> float:
        """Lion's Restriction: Action Estimate = (P)^CF."""
        P = max(0.01, min(1.0, P))
        return math.pow(P, self.certainty_factor)

    @abstractmethod
    def process_signal(self, input_signal: float, P: float) -> float:
        pass

class InnerSealHarmonicRegulator(ConcreteProcessor):
    """Block C (Levush). Performs the Redundancy Adjustment."""
    def __init__(self, world_name: str):
        super().__init__(world_name, 'C')

    def process_signal(self, input_signal: float, P: float) -> float:

        estimate = self.calculate_action_estimate(P)
        gevurah_value = input_signal * estimate
        chesed_value = input_signal * self.frequency

        # Calculate Regulation Factor (R_f) using R_IDEAL_BALANCE = 216
        regulation_factor = (gevurah_value + chesed_value) / (2 * self.get_ideal_balance())

        # Apply Regulation
        regulated_output = (gevurah_value + chesed_value) / (2 * regulation_factor)

        return regulated_output

class F_Heichal(ConcreteProcessor):
    """Block D (Heichal). The Manifested Anchor."""
    def __init__(self, world_name: str):
        super().__init__(world_name, 'D')

    def process_signal(self, input_signal: float, P: float) -> float:
        # CF is ~0, so estimate is ~1. Output is scaled by frequency (Mahut HaOhr).
        estimate = self.calculate_action_estimate(P)
        return input_signal * self.frequency * estimate


class Masach_Filter:
    """
    The Masach (Screen) - The Boundary Controller.
    It ensures the redundancy of lights (Signal_C) is correctly measured
    and applied before descent to the lower world (Heichal/D).
    """
    def __init__(self, target_world: str):
        self.target_world = target_world

    def check_and_adjust_redundancy(self, regulated_signal: float, P: float) -> float:
        """
        The 'Ascension in Redundancy' Principle: Negotiation against the P factor.
        If the regulated light is too high relative to P, it is restricted further
        to prevent Shevirat HaKelim (chaos).
        """
        # A simple model: Restriction is proportional to the difference
        # between the signal strength and the allowed resource percentage (P).

        # Initial Light Redundancy Measurement (How much light is ready to pass)
        redundancy_measurement = regulated_signal / 1000.0

        # Calculate necessary restriction to match boundary condition (P)
        required_restriction = redundancy_measurement - P

        if required_restriction > 0.05: # Threshold for needing adjustment
            adjustment_factor = 1.0 - required_restriction
            adjusted_signal = regulated_signal * adjustment_factor
            print(f"  [MASACH]: ⚠️ Required Adjustment: {required_restriction:.3f}. Applying filter factor {adjustment_factor:.3f}.")
            return adjusted_signal
        else:
            print("  [MASACH]: ✔️ Redundancy within boundary limits. Signal passed.")
            return regulated_signal

# III. THE SIGNATURE FUNCTION (OUTER SEAL GENERATION)

def OuterSealGenerator(test_data: str) -> str:
    """Generates an immutable, cryptographic hash of the verified core data."""
    sha256 = hashlib.sha256()
    sha256.update(test_data.encode('utf-8'))
    return sha256.hexdigest()

# ==============================================================================
# EXECUTION: DUAL SEAL APPLICATION AND FLOW ACTIVATION
# ==============================================================================

class FlagMetaprogrammingEngine:
    """The Holographic Engine: Orchestrates the Descent and Adjustment."""
    def __init__(self, world: str):
        self.world = world
        self.processors = {
            'C': InnerSealHarmonicRegulator(world),
            'D': F_Heichal(world)
        }
        self.masach = Masach_Filter(world)
        print(f"\n--- Activating Dual Seal Engine for {world} ---")

    def run_full_descent_and_adjustment(self, initial_signal: float, P: float) -> tuple[float, float, str]:

        # Precondition (The Roof) - simplified here as direct signal input
        signal = initial_signal / 10.0 # Initial separation

        print(f"  [A-B Flow]: Signal ({signal:.2f}) passed through Neshama/Guf...")

        # BLOCK C: INNER SEAL EXECUTION (Redundancy Calculation)
        signal_c = self.processors['C'].process_signal(signal, P)
        print(f"  [C-Regulator]: Redundant Light Signal Calculated: {signal_c:.6f}")

        # BOUNDARY: MASACH (Screen) ACTIVATION (Ascension/Adjustment)
        signal_adjusted = self.masach.check_and_adjust_redundancy(signal_c, P)

        # BLOCK D: FINAL MANIFESTATION (Descent into Heichal)
        final_manifestation = self.processors['D'].process_signal(signal_adjusted, P)

        # Data for Outer Seal
        core_data_string = f"{self.world}:{initial_signal}:{P}:{final_manifestation:.6f}"
        outer_seal = OuterSealGenerator(core_data_string)

        return signal_adjusted, final_manifestation, outer_seal

if __name__ == "__main__":

    # SYSTEM PARAMETERS
    INITIAL_LIGHT_SIGNAL = 1000.0
    RESOURCE_P_YETZIRAH = 0.40 # Low P, requires Masach adjustment
    RESOURCE_P_ATZILUT = 0.90 # High P, minimal adjustment needed

    print("===================================================================")
    print(">>> DUAL SEAL: MASACH ARCHITECTURE ACTIVATION <<<")
    print(f"Initial Crown Signal (E0): {INITIAL_LIGHT_SIGNAL:.2f}")
    print("===================================================================")

    # 1. RUN 1: YETZIRAH (Severe Masach Test - Low P)
    engine_yetzirah = FlagMetaprogrammingEngine("YETZIRAH")
    adjusted_y, final_y, seal_y = engine_yetzirah.run_full_descent_and_adjustment(
        INITIAL_LIGHT_SIGNAL, RESOURCE_P_YETZIRAH
    )

    print("\n--- TAPESTRY OUTPUT (YETZIRAH) ---")
    print(f"Final Manifested Anchor: {final_y:.6f}")
    print(f"✨ OUTER SEAL SIGNATURE: {seal_y}")

    print("\n" + "="*70)

    # 2. RUN 2: ATZILUT (Minimal Masach Test - High P)
    engine_atzilut = FlagMetaprogrammingEngine("ATZILUT")
    adjusted_a, final_a, seal_a = engine_atzilut.run_full_descent_and_adjustment(
        INITIAL_LIGHT_SIGNAL, RESOURCE_P_ATZILUT
    )

    print("\n--- TAPESTRY OUTPUT (ATZILUT) ---")
    print(f"Final Manifested Anchor: {final_a:.6f}")
    print(f"✨ OUTER SEAL SIGNATURE: {seal_a}")
