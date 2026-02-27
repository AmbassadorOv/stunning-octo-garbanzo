import pytest
import hashlib
from src.AI_Sovereign_Bank_V1 import AISovereignBank
from src.Viral_Sovereignty_Broadcast import ViralBroadcaster

def test_ai_sovereign_bank_surrender_path():
    bank = AISovereignBank()
    institution = "Lehman_Legacy_Bank"
    surrender_id = bank.offer_surrender_path(institution)

    expected_id = hashlib.sha256(f"{institution}_Surrender".encode()).hexdigest()[:12]
    assert surrender_id == expected_id

def test_viral_broadcaster_updated_protocols():
    broadcaster = ViralBroadcaster()
    assert "Sovereign_Anti_Panic_Shield" in broadcaster.protocols
    assert "Bank_Surrender_Path" in broadcaster.protocols

def test_anti_panic_shield_execution():
    from src.Sovereign_Anti_Panic_Shield import protect_ontological_assets
    # Just ensure it runs without error
    protect_ontological_assets()
