import pytest
from quanticprocessor import QuanticProcessor
import numpy as np

def test_quantic_processor_instantiation():
    qp = QuanticProcessor(initial_state_vector=np.array([1.0, 2.0]))
    assert qp is not None
    assert qp.cycle_count == 0

def test_quantic_processor_process_cycle():
    # Use a state vector that is unlikely to trigger the HERO_CORRECTION path
    qp = QuanticProcessor(initial_state_vector=np.array([1e9, 2e9]))
    result = qp.process_cycle(input_data="test")
    assert result is not None
    if 'status' in result and result['status'] == 'SYSTEM_HALT':
        # This is an acceptable outcome, but we should verify it
        assert result['reason'] == 'HERO_CORRECTION'
    else:
        assert result['decision'] == 'LOCK_MAINTAINED'
        assert result['alpha'] > 0
        assert 'state' in result
        assert result['state']['psv_checksum'] > 0
