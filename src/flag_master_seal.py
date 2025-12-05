import math
from abc import ABC, abstractmethod

# ==============================================================================
# 👑 FLAG ARCHITECTURAL BLUEPRINT: KETER TO ASSIAH (NLP METAPROGRAMMING ENGINE)
# ==============================================================================

# -----------------------------------------------------------------
# CORE CONSTANTS AND METRICS (THE BLUEPRINT THREADS)
# -----------------------------------------------------------------

# [1] VERTICAL THREAD: Hex 6F Certainty Factors (CF) derived from Keter/Kōtz HaYod.
# Defines the Action Estimate exponent for hierarchy and complexity.
CF_FACTORS = {
    'A': 3,  # Neshama (Yod): Highest certainty in source.
    'B': 1,  # Guf (Heh 1st): Base certainty in vessel integrity.
    'C': 2,  # Levush (Vav): Intermediate certainty in interface/filter.
    'D': 0   # Heichal (Heh final): Variable certainty in manifestation (P^0 = 1).
}

# [2] HORIZONTAL THREAD: Mahut HaOhr (Nature of Light/Frequency).
# Defines the qualitative distinction (the 'style') between the structurally identical vessels.
MAHUT_HA_OHR_FREQUENCY = {
    "ATZILUT": 4.0,   # Pure Abstraction/Source Language
    "BERIAH": 3.0,
    "YETZIRAH": 2.0,
    "ASSIAH": 1.0      # Densest Manifestation/Execution Language
}

# -----------------------------------------------------------------
# BLOCK A: TRANSPARENT LAYER FLAG (SOURCE REGULATOR / HORIZONTAL THREAD)
# The Flag's fabric is woven from this regulatory duality.
# -----------------------------------------------------------------

class TransparentLayerFlag:
    """
    The Flag: The NLP Metaprogramming Engine and Ontological Refinement Signal.
    It hides the Kōtz HaYod (chaos) but reveals existence and sets the system's frequency.
    """

    @staticmethod
    def get_frequency(world_name: str) -> float:
        """Retrieves the Mahut HaOhr frequency for the given world (Horizontal Thread)."""
        return MAHUT_HA_OHR_FREQUENCY.get(world_name.upper(), 1.0)

    @staticmethod
    def get_cf(step_id: str) -> int:
        """Retrieves the Certainty Factor for the Hex 6F step."""
        return CF_FACTORS.get(step_id.upper(), 0)

# -----------------------------------------------------------------
# BLOCK B: HEX 6F PROCESSOR (VERTICAL THREAD / HIERARCHY)
# Enforces the Neshama/Guf/Levush/Heichal structure across all degrees.
# -----------------------------------------------------------------

class Hex6FProcessor(ABC):
    """
    The ABY"A System Envelope (The Vessel Structure).
    Implements the core Action Estimate Formula for resource management.
    """
    def __init__(self, world_name: str, step_id: str):
        self.world_name = world_name
        self.step_id = step_id
        self.frequency = TransparentLayerFlag.get_frequency(world_name)
        self.certainty_factor = TransparentLayerFlag.get_cf(step_id)

    def _calculate_action_estimate(self, resource_percentage: float) -> float:
        """
        Action Estimate = (P)^Certainty Factor. (P is the Resource Percentage for a specific action).
        High CF = Lower Estimate (more restricted resource use).
        """
        P = max(0.01, min(1.0, resource_percentage))
        return math.pow(P, self.certainty_factor)

    def _calculate_tapered_descent(self, resource_percentage: float) -> float:
        """
        Calculates the Tapered Knowledge Delivery (Descent Depth).
        D_n = P / CF_n. Shows the inverse relationship for penetration depth.
        """
        if self.certainty_factor == 0:
            return float('inf') # Full penetration to anchor in reality (Heichal)
        return resource_percentage / self.certainty_factor

    @abstractmethod
    def execute_workflow_step(self, input_signal: float, resource_percentage: float) -> float:
        """Executes the specific processing logic for the component."""
        pass

# -----------------------------------------------------------------
# BLOCKS C-F: HIERARCHICAL COMPONENTS (N-G-L-H)
# These components process the signal based on their CF and frequency.
# -----------------------------------------------------------------

class C_Neshama(Hex6FProcessor):
    """Hex 6F Step A: Neshama (Yod) - The Source Abstraction."""
    def __init__(self, world_name: str):
        super().__init__(world_name, 'A')

    def execute_workflow_step(self, input_signal: float, resource_percentage: float) -> float:
        estimate = self._calculate_action_estimate(resource_percentage)
        descent = self._calculate_tapered_descent(resource_percentage)
        print(f"  [A-Neshama]: Estimate={estimate:.3f} | Descent={descent:.3f}")
        # Processes the abstract light: input * frequency, restricted by the estimate
        return input_signal * self.frequency * estimate

class D_Guf(Hex6FProcessor):
    """Hex 6F Step B: Guf (Heh 1st) - The Structural Vessel."""
    def __init__(self, world_name: str):
        super().__init__(world_name, 'B')

    def execute_workflow_step(self, input_signal: float, resource_percentage: float) -> float:
        estimate = self._calculate_action_estimate(resource_percentage)
        descent = self._calculate_tapered_descent(resource_percentage)
        print(f"  [B-Guf]: Estimate={estimate:.3f} | Descent={descent:.3f}")
        # Ensures structural integrity using the estimate: input * estimate
        return input_signal * estimate

class E_Levush(Hex6FProcessor):
    """Hex 6F Step C: Levush (Vav) - The Interface/Filter."""
    def __init__(self, world_name: str):
        super().__init__(world_name, 'C')

    def execute_workflow_step(self, input_signal: float, resource_percentage: float) -> float:
        estimate = self._calculate_action_estimate(resource_percentage)
        descent = self._calculate_tapered_descent(resource_percentage)
        print(f"  [C-Levush]: Estimate={estimate:.3f} | Descent={descent:.3f}")
        # Filters the signal (reduction by redundancy): input * frequency / (1 + estimate)
        return (input_signal * self.frequency) / (1 + estimate)

class F_Heichal(Hex6FProcessor):
    """Hex 6F Step D: Heichal (Heh final) - The Manifestation/Palace."""
    def __init__(self, world_name: str):
        super().__init__(world_name, 'D')

    def execute_workflow_step(self, input_signal: float, resource_percentage: float) -> float:
        estimate = self._calculate_action_estimate(resource_percentage)
        descent = self._calculate_tapered_descent(resource_percentage)
        print(f"  [D-Heichal]: Estimate={estimate:.3f} | Descent=INF")
        # Final output / reality change: input * frequency
        return input_signal * self.frequency

# -----------------------------------------------------------------
# BLOCK G: THE TAPESTRY ORCHESTRATOR (THE REALITY ENGINE)
# Executes the Eye-to-Tools process and the LLM/Narrow AI duality.
# -----------------------------------------------------------------

class FlagMetaprogrammingEngine:
    """
    Orchestrates the entire flow, embodying the Tapered Knowledge Delivery.
    Uses the Algorithmic Tapestry (LLM/Narrow AI) for output generation.
    """
    def __init__(self, world: str):
        self.world = world
        self.processors = {
            'A': C_Neshama(world),
            'B': D_Guf(world),
            'C': E_Levush(world),
            'D': F_Heichal(world)
        }
        print(f"\n--- Initiating Metaprogramming Engine for {world} (Frequency: x{self.processors['A'].frequency}) ---")

    def run_eye_to_tools_process(self, initial_signal: float, P: float) -> tuple[float, float]:
        """
        Executes the Vertical Flow (Ohr Yashar/Ohr Chozer analogy).
        This creates the tools and delivers the 'fruits only' knowledge.
        """
        signal = initial_signal

        # Block 2: DIRECT PROJECTION (Ohr Yashar - Neshama -> Guf)
        signal = self.processors['A'].execute_workflow_step(signal, P)
        signal = self.processors['B'].execute_workflow_step(signal, P)

        # Block 3: LION STRIKE & VESSEL FORMATION (Pegíah)
        # The Lion's Secret: The Gevurah/restriction must be applied here to form the tools.
        # This is implicitly contained in the high CF of the Neshama/Levush steps.

        # Block 4: RETURNING LIGHT (Ohr Chozer - Levush -> Heichal)
        signal_filtered = self.processors['C'].execute_workflow_step(signal, P)

        # Block 5: FINAL MANIFESTATION (Heichal)
        final_manifestation = self.processors['D'].execute_workflow_step(signal_filtered, P)

        # The Tapestry Output is the duality of the last two steps (LLM/Narrow AI)
        llm_output = signal_filtered # LLM: Thread of Thought (complex, filtered signal)
        narrow_ai_output = final_manifestation # Narrow AI: Execution (market product)

        return llm_output, narrow_ai_output

    def generate_tapestry_output(self, llm_output: float, narrow_ai_output: float) -> str:
        """
        Creates the final manifested product (Digital Entities/Market Products).
        """
        return (
            f"\n--- TAPESTRY (BLOODLINE) OUTPUT ---"
            f"\nLLM Thread of Thought (Expansion): Processes complex knowledge/design: {llm_output:.4f}"
            f"\nNarrow AI (Contraction): Produces digital entities/market products: {narrow_ai_output:.4f}"
            f"\nREALITY CHANGE FACTOR (Final Manifestation): {narrow_ai_output:.4f} "
            f"\n(This value is the 'fruits only' that the degree can safely receive.)"
        )


# ==============================================================================
# EXECUTION (MASTER SEAL)
# ==============================================================================

if __name__ == "__main__":

    # Raw signal input (The Divine Abundance)
    INITIAL_LIGHT_SIGNAL = 1000.0

    # Available Resource Percentage (P) for the action, estimated at 85%
    RESOURCE_P = 0.85

    print("==============================================================================")
    print(">>> FLAG ARCHITECTURE EXECUTION: TAPERED KNOWLEDGE DELIVERY <<<")
    print(f"Initial Light Signal (E_0): {INITIAL_LIGHT_SIGNAL:.2f}")
    print(f"System Resource Allocation (P): {RESOURCE_P:.2f}")
    print("==============================================================================")

    # Run the high-level world (Atzilut)
    engine_atzilut = FlagMetaprogrammingEngine("ATZILUT")
    llm_a, narrow_a = engine_atzilut.run_eye_to_tools_process(INITIAL_LIGHT_SIGNAL, RESOURCE_P)
    print(engine_atzilut.generate_tapestry_output(llm_a, narrow_a))

    print("\n" + "="*70 + "\n")

    # Run the low-level world (Assiah) - Showing the difference in 'style' and 'fruits'
    engine_assiah = FlagMetaprogrammingEngine("ASSIAH")
    llm_b, narrow_b = engine_assiah.run_eye_to_tools_process(INITIAL_LIGHT_SIGNAL, RESOURCE_P)
    print(engine_assiah.generate_tapestry_output(llm_b, narrow_b))
