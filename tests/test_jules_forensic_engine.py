import pytest
import os
import json
from src.kernel.jules_forensic_engine import JulesForensicEngine

def test_forensic_engine_initialization():
    engine = JulesForensicEngine("test@example.com")
    assert engine.target_email == "test@example.com"
    assert engine.app_id == "MOON_WHEEL_2026"
    assert len(engine.forensic_log) == 0

def test_scan_email_archives():
    engine = JulesForensicEngine("test@example.com")
    engine.scan_email_archives()
    assert len(engine.forensic_log) > 0
    for entry in engine.forensic_log:
        assert "timestamp" in entry
        assert "original_fragment" in entry
        assert "correlation" in entry
        assert entry["status"] == "ORIGIN_IDENTIFIED"

def test_generate_sovereignty_report():
    report_file = "sovereignty_report.json"
    if os.path.exists(report_file):
        os.remove(report_file)

    engine = JulesForensicEngine("test@example.com")
    engine.scan_email_archives()
    report = engine.generate_sovereignty_report()

    assert report["owner"] == "test@example.com"
    assert report["jules_verification"] == "Verified 2026-01-26"
    assert os.path.exists(report_file)

    with open(report_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["owner"] == "test@example.com"

    # Clean up
    if os.path.exists(report_file):
        os.remove(report_file)
