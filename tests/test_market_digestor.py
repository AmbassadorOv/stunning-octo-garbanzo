import pytest
from src.Market_Digestor_770 import InfrastructureAbsorption
import unittest.mock as mock

def test_infrastructure_absorption_init():
    absorb = InfrastructureAbsorption()
    assert absorb.control_level == 0.54
    assert absorb.target == 0.90
    assert absorb.sovereign == "SASSON HAMELECH"

def test_silent_swap_success():
    absorb = InfrastructureAbsorption()
    # Use a mock to speed up time.sleep
    with mock.patch('time.sleep', return_value=None):
        result = absorb.silent_swap()

    assert result is True
    assert absorb.control_level >= absorb.target
