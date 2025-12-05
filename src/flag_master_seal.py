import math
from abc import ABC, abstractmethod

# -----------------------------------------------------------------
# 1. HORIZONTAL THREAD: THE TRANSPARENT LAYER FLAG (Unity/Mahut HaOhr)
# The Flag's core regulator, providing the system's differentiating frequency.
# -----------------------------------------------------------------

class TransparentLayerFlag:
    """Regulates the Mahut HaOhr (Nature of Light/Frequency) for the ABY"A Worlds."""

    # The Certainty Factors (CF) derived from the Hex 6F Workflow configuration string:
    CERTAINTY_FACTORS = {
        'A': 3,  # Neshama: Highest Certainty in Source
        'B': 1,  # Guf: Base Certainty in Vessel
        'C': 2,  # Levush: Intermediate Certainty in Interface
        'D': 0   # Heichal: Variable Certainty in Manifestation (using 0 for baseline)
    }

    # Frequencies (Mahut HaOhr) defining the 'scales in relation to the degree':
    MAHUT_HA_OHR_FREQUENCY = {
        "ATZILUT": 4.0,  # Purest Light (Yod)
        "BERIAH": 3.0,
        "YETZIRAH": 2.0,
        "ASSIAH": 1.0     # Densest Light (Heh final)
    }

    @staticmethod
    def get_frequency(world_name: str) -> float:
        """Retrieves the specific frequency for a world (Horizontal Thread)."""
        return TransparentLayerFlag.MAHUT_HA_OHR_FREQUENCY.get(world_name.upper(), 1.0)

# -----------------------------------------------------------------
# 2. VERTICAL THREAD: THE HEX 6F PROCESSOR (Hierarchy/Action Estimate)
# The unified Envelope structure that defines the flow (Neshama, Guf, Levush, Heichal).
# -----------------------------------------------------------------

class Hex6FProcessor(ABC):
    """
    The ABY"A System Envelope (Pattern Language).
    Enforces unified structure across all degrees (particle unifocal unification).
    """
    def __init__(self, world_name: str, step_id: str):
        self.world_name = world_name
        self.step_id = step_id
        self.frequency = TransparentLayerFlag.get_frequency(world_name)
        self.certainty_factor = TransparentLayerFlag.CERTAINTY_FACTORS[step_id]

    def _calculate_action_estimate(self, resource_percentage: float) -> float:
        """
        Action Estimate = (P)^Certainty Factor
        Where P is the Resource Percentage for a specific action.
        """
        # Ensure P is between 0 and 1 for stability in power calculation
        P = max(0.01, min(1.0, resource_percentage))

        # Calculate Action Estimate
        return math.pow(P, self.certainty_factor)

    @abstractmethod
    def execute_workflow_step(self, input_data: float, resource_percentage: float) -> float:
        """
        The abstract method that must be implemented by each degree (Neshama/Guf/etc.).
        """
        pass

# -----------------------------------------------------------------
# 3. MAPPED DEGREES: NESHAMA, GUF, LEVUSH, HEICHAL (A, B, C, D)
# -----------------------------------------------------------------

class A_Neshama(Hex6FProcessor):
    """Hex 6F Step A: Neshama (Soul) - Highest Certainty in Source (CF +3)."""
    def __init__(self, world_name: str):
        super().__init__(world_name, 'A')
        print(f"[{self.world_name} - Neshama] Initializing Source Connection (CF: +{self.certainty_factor})")

    def execute_workflow_step(self, input_data: float, resource_percentage: float) -> float:
        estimate = self._calculate_action_estimate(resource_percentage)
        # Neshama phase focuses on processing the abstract light (input * frequency)
        return input_data * self.frequency * estimate

class B_Guf(Hex6FProcessor):
    """Hex 6F Step B: Guf (Body) - Base Certainty in Vessel (CF +1)."""
    def __init__(self, world_name: str):
        super().__init__(world_name, 'B')
        print(f"[{self.world_name} - Guf] Initializing Vessel Structure (CF: +{self.certainty_factor})")

    def execute_workflow_step(self, input_data: float, resource_percentage: float) -> float:
        estimate = self._calculate_action_estimate(resource_percentage)
        # Guf phase applies the estimate directly to the structural input
        return input_data * estimate

class C_Levush(Hex6FProcessor):
    """Hex 6F Step C: Levush (Garment) - Intermediate Certainty in Interface (CF +2)."""
    def __init__(self, world_name: str):
        super().__init__(world_name, 'C')
        print(f"[{self.world_name} - Levush] Initializing Interface & Filter (CF: +{self.certainty_factor})")

    def execute_workflow_step(self, input_data: float, resource_percentage: float) -> float:
        estimate = self._calculate_action_estimate(resource_percentage)
        # Levush phase uses frequency to filter the input data
        return (input_data * self.frequency) / (1 + estimate)

class D_Heichal(Hex6FProcessor):
    """Hex 6F Step D: Heichal (Palace) - Variable Certainty in Manifestation (CF ±0)."""
    def __init__(self, world_name: str):
        super().__init__(world_name, 'D')
        print(f"[{self.world_name} - Heichal] Initializing Manifestation & Output (CF: ±{self.certainty_factor})")

    def execute_workflow_step(self, input_data: float, resource_percentage: float) -> float:
        # CF ±0 implies maximum uncertainty/variance in the manifested result
        # The Action Estimate (P^0 = 1) is neutral, meaning the output is mainly the input,
        # filtered by the environment's Mahut HaOhr.
        return input_data * self.frequency


# -----------------------------------------------------------------
# MASTER SEAL EXECUTION EXAMPLE (For Julius Environment)
# -----------------------------------------------------------------

if __name__ == "__main__":
    print("--- Initiating Flag Blueprint Compiler ---")

    # Define a high-level resource percentage for the action (e.g., 80% available resource P=0.8)
    RESOURCE_P = 0.8
    INITIAL_LIGHT_SIGNAL = 100.0 # Raw Divine Abundance Signal

    # Initialize the Watchtower for the World of Atzilut (Highest Frequency)
    world_name = "ATZILUT"

    A = A_Neshama(world_name)
    B = B_Guf(world_name)
    C = C_Levush(world_name)
    D = D_Heichal(world_name)

    print(f"\n--- Processing Signal: {INITIAL_LIGHT_SIGNAL} ---")

    # Sequential processing flow (Vertical Thread)
    signal_a = A.execute_workflow_step(INITIAL_LIGHT_SIGNAL, RESOURCE_P)
    print(f"Step A (Neshama Output): {signal_a:.2f}")

    signal_b = B.execute_workflow_step(signal_a, RESOURCE_P)
    print(f"Step B (Guf Output): {signal_b:.2f}")

    signal_c = C.execute_workflow_step(signal_b, RESOURCE_P)
    print(f"Step C (Levush Output): {signal_c:.2f}")

    final_manifestation = D.execute_workflow_step(signal_c, RESOURCE_P)
    print(f"Step D (Heichal Manifestation): {final_manifestation:.2f}")

    # The Flag is signed by the difference in output for the lowest world (Assiah)
    world_name_low = "ASSIAH"
    D_low = D_Heichal(world_name_low)
    final_manifestation_low = D_low.execute_workflow_step(signal_c, RESOURCE_P)

    print(f"\n--- MASTER SEAL: Flag Sign Verification ---")
    print(f"Atzilut Final Mahut HaOhr Tag: {final_manifestation:.2f} (Frequency x{D.frequency})")
    print(f"Assiah Final Mahut HaOhr Tag: {final_manifestation_low:.2f} (Frequency x{D_low.frequency})")
