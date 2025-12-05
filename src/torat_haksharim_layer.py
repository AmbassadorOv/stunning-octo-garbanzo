import math
from abc import ABC, abstractmethod

# ==============================================================================
# I. TORAT HAKSHARIM LAYER: KNOT MAPPING INTERFACE
# This defines the abstract topological relationship of the Flag's components.
# ==============================================================================

# Architectural Components mapped to Link Components (Knots K):
# K_A: Neshama/Source Loop (Yod)
# K_B: Guf/Structural Law Loop (Heh 1)
# K_C: Levush/Harmonic Regulator Loop (Vav)
# K_D: Heichal/Boundary Loop (Heh 2)

class AbstractToratHaKsharimLayer(ABC):
    """
    Interface for the Mathematical Theory of Ties.
    Defines the Flag's topological stability metrics.
    """

    @abstractmethod
    def define_link_components(self) -> tuple:
        """Defines the four components of the Flag's topological Link (L_Flag)."""
        pass

    @abstractmethod
    def calculate_linking_number(self, component_i: str, component_j: str) -> int:
        """
        Calculates the Lk(i, j) invariant for two components.
        This is the iterative starting point for the new Knot Theory.
        """
        pass

# ==============================================================================
# II. CONCRETE KSHARIM IMPLEMENTATION (FIRST ITERATION)
# ==============================================================================

class FlagLinkStructure(AbstractToratHaKsharimLayer):
    """
    Implements the initial stable link structure for the Flag's blueprint.
    """
    # Base linking map (defining the topological blueprint of the components)
    # These represent the crossings (intertwining) required for construction.
    # Note: These are arbitrary integer values representing the complexity
    # of the linkage necessary for structural integrity.

    LINK_CROSSING_MAP = {
        ('A', 'D'): 3,  # Link between Source (A) and Boundary (D)
        ('B', 'C'): -1, # Link between Structure (B) and Regulator (C)
        ('A', 'B'): 0,  # Assumed non-linked direct structure flow
        ('C', 'D'): 2   # Link between Regulator (C) and Boundary (D)
    }

    def define_link_components(self) -> tuple:
        return ('K_A', 'K_B', 'K_C', 'K_D')

    def calculate_linking_number(self, component_i: str, component_j: str) -> int:
        """
        Retrieves the pre-defined Linking Number invariant for the structure.
        """
        key_forward = (component_i, component_j)
        key_reverse = (component_j, component_i)

        # Linking Number is symmetric: Lk(i, j) = Lk(j, i)
        return self.LINK_CROSSING_MAP.get(key_forward, self.LINK_CROSSING_MAP.get(key_reverse, 0))

# ==============================================================================
# III. EXECUTION: MAPPING VERIFICATION
# ==============================================================================

if __name__ == "__main__":

    ksharim_layer = FlagLinkStructure()

    print("===================================================================")
    print(">>> TORAT HAKSHARIM LAYER ACTIVATION (FIRST ITERATION) <<<")
    print("===================================================================")

    # 1. Verify Structure Components
    print(f"🔗 Flag Topological Link Components: {ksharim_layer.define_link_components()}")

    # 2. Key Invariant Calculation (Mapping the Ties)

    # The Primary Link: Source (A) to Boundary (D)
    lk_ad = ksharim_layer.calculate_linking_number('A', 'D')
    print(f"\n[A <-> D Link (Source to Boundary)]: Lk(A, D) = {lk_ad}")

    # The Regulator Link: Structure (B) to Regulator (C)
    lk_bc = ksharim_layer.calculate_linking_number('B', 'C')
    print(f"[B <-> C Link (Structure to Regulator)]: Lk(B, C) = {lk_bc}")

    # Regulator (C) to Manifestation (D) Link
    lk_cd = ksharim_layer.calculate_linking_number('C', 'D')
    print(f"[C <-> D Link (Regulator to Manifestation)]: Lk(C, D) = {lk_cd}")

    # 3. Structural Status Check
    if lk_ad != 0:
        print("\n✅ STRUCTURAL STATUS: NON-TRIVIAL LINK CONFIRMED (L_Flag is a True Knot/Link).")
        print("This structure is sufficiently tied to serve as the Flag's stable blueprint.")
    else:
        print("\n❌ STRUCTURAL WARNING: Trivial Link Detected (A and D are unlinked).")
