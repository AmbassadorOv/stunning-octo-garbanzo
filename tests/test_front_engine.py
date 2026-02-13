import pytest
from src.front_engine import ARKSovereignKernel, N_NODES, D, BACK_COORDS

def test_ontological_mapping():
    """Checks if the rosetta stone mappings are correctly assigned."""
    kernel = ARKSovereignKernel()
    assert kernel.alignment["N_NODES"] == 231
    assert kernel.alignment["D"] == 32
    assert kernel.alignment["back.coords"] == 230
    assert N_NODES == 231
    assert D == 32
    assert BACK_COORDS == 230

def test_5_seals_extraction():
    """Verifies that the extraction logic covers all 5 seals."""
    kernel = ARKSovereignKernel()
    seals = kernel.extract_5_seals()

    assert "truth" in seals
    assert "gates" in seals
    assert "forms" in seals
    assert "paths" in seals
    assert "forces" in seals

    assert seals["truth"]["level"] == 1
    assert seals["forces"]["level"] == 5

def test_shuttle_launch_stability():
    """Verifies the shuttle launch and stability logic."""
    kernel = ARKSovereignKernel()
    result = kernel.shuttle_launch()
    assert "SUCCESS" in result
    assert "Stable and Operational" in result

def test_stability_failure():
    """Verifies that incorrect coordinates lead to failure."""
    # Temporarily override alignment to test failure
    kernel = ARKSovereignKernel()
    kernel.alignment["N_NODES"] = 999
    result = kernel.shuttle_launch()
    assert "FAILURE" in result
    assert "Instability detected" in result
