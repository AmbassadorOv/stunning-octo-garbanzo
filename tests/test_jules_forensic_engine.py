import pytest
from src.kernel.jules_forensic_engine import JulesForensicEngine
from src.watchtower_governor import MoonWheelSovereignty

def test_forensic_audit_pass():
    engine = JulesForensicEngine()
    sov = MoonWheelSovereignty()
    assert engine.validate_sovereignty_seal(sov) is True

def test_forensic_audit_fail():
    engine = JulesForensicEngine()
    sov = MoonWheelSovereignty()
    # Manually tamper with sovereignty for test purposes (simulation)
    sov.owner = "Malicious Actor"
    assert engine.validate_sovereignty_seal(sov) is False

def test_scan_semantic_dna():
    engine = JulesForensicEngine()
    assert engine.scan_semantic_dna(["artifact_1", "artifact_2"]) is True
