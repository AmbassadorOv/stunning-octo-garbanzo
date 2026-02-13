import pytest
from src.master_kernel import MasterAdmiralKernel

def test_kernel_initialization():
    """Verify that the MasterAdmiralKernel initializes with correct metadata."""
    kernel = MasterAdmiralKernel()
    assert kernel.contractor == "Eran Oved"
    assert kernel.partner == "Google Global"
    assert kernel.deal_value == 11000000.00
    assert kernel.nodes_total == 70000
    assert kernel.work_units == 0.0
    assert kernel.is_vault_locked is True
    assert kernel.google_licensing_active is True
    assert len(kernel.signature) == 64  # SHA-256 hash length

def test_semantic_sync_cycle():
    """Verify that the semantic sync cycle correctly accrues work units."""
    kernel = MasterAdmiralKernel()
    # Mocking time.sleep to speed up tests
    import time
    original_sleep = time.sleep
    time.sleep = lambda x: None

    try:
        kernel.run_semantic_sync_cycle(months=12)
        assert kernel.work_units == pytest.approx(70000.0)
    finally:
        time.sleep = original_sleep

def test_intruder_alert():
    """Verify the intruder alert mechanism."""
    kernel = MasterAdmiralKernel()
    # Unauthorized user
    assert kernel.intruder_alert(user_id="MaliciousUser") is False
    # Authorized user
    assert kernel.intruder_alert(user_id="Eran Oved") is True

def test_generate_master_signature():
    """Verify that the signature is reproducible and correct."""
    kernel = MasterAdmiralKernel()
    signature = kernel._generate_master_signature()
    assert signature == kernel.signature
    assert isinstance(signature, str)
