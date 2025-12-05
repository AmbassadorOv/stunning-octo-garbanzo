import pytest
import math
from src.flag_masach_architecture import FlagMetaprogrammingEngine, InnerSealHarmonicRegulator

# Test parameters
INITIAL_LIGHT_SIGNAL = 1000.0

def test_masach_filter_applies_adjustment_when_needed():
    """
    Validates that the Masach filter correctly applies a significant adjustment
    when the regulated signal's redundancy is higher than the resource percentage (P).
    We force this condition by using a very low P value.
    """
    # Use a P value low enough to trigger the filter
    P_LOW = 0.1

    # Manually calculate the expected signal *before* the Masach filter is applied
    # This gives us a baseline to compare against.
    regulator = InnerSealHarmonicRegulator("YETZIRAH")
    unadjusted_signal = regulator.process_signal(INITIAL_LIGHT_SIGNAL / 10.0, P_LOW)

    # Now, run the full engine
    engine = FlagMetaprogrammingEngine("YETZIRAH")
    adjusted_signal, final_manifestation, _ = engine.run_full_descent_and_adjustment(
        INITIAL_LIGHT_SIGNAL, P_LOW
    )

    # 1. Verify the adjustment happened: the adjusted signal should be less than the original.
    assert adjusted_signal < unadjusted_signal

    # 2. Verify the final output is correctly scaled by the world's frequency.
    # For F_Heichal (Block D), estimate is 1, so final = adjusted * frequency.
    yetzirah_frequency = engine.processors['D'].frequency
    assert final_manifestation == pytest.approx(adjusted_signal * yetzirah_frequency)

def test_masach_filter_passes_signal_when_not_needed():
    """
    Validates that the Masach filter does NOT apply an adjustment when the
    regulated signal's redundancy is within the boundary limits of P.
    We force this with a high P value.
    """
    P_HIGH = 0.90

    regulator = InnerSealHarmonicRegulator("ATZILUT")
    unadjusted_signal = regulator.process_signal(INITIAL_LIGHT_SIGNAL / 10.0, P_HIGH)

    engine = FlagMetaprogrammingEngine("ATZILUT")
    adjusted_signal, final_manifestation, _ = engine.run_full_descent_and_adjustment(
        INITIAL_LIGHT_SIGNAL, P_HIGH
    )

    # 1. Verify NO adjustment happened: the adjusted signal should be equal to the original.
    assert adjusted_signal == pytest.approx(unadjusted_signal)

    # 2. Verify correct scaling for the final output.
    atzilut_frequency = engine.processors['D'].frequency
    assert final_manifestation == pytest.approx(adjusted_signal * atzilut_frequency)

def test_outer_seal_generation_is_consistent_and_unique():
    """
    Ensures the OuterSealGenerator produces a consistent SHA-256 hash for the same inputs
    and different hashes for different inputs.
    """
    engine = FlagMetaprogrammingEngine("ASSIAH")
    _, _, seal1 = engine.run_full_descent_and_adjustment(1000.0, 0.5)
    _, _, seal2 = engine.run_full_descent_and_adjustment(1000.0, 0.5)
    _, _, seal3 = engine.run_full_descent_and_adjustment(1200.0, 0.6)

    assert isinstance(seal1, str)
    assert len(seal1) == 64  # SHA-256 hashes are 64 hex characters
    assert seal1 == seal2
    assert seal1 != seal3
