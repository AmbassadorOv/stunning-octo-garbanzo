import pytest
import os
import json
from src.kernel.jules_forensic_engine import JulesForensicEngine

def test_jules_forensic_engine_report_generation():
    target_email = "test@example.com"
    scanner = JulesForensicEngine(target_email)
    scanner.scan_email_archives()
    report = scanner.generate_sovereignty_report()

    assert report["owner"] == target_email
    assert "findings" in report
    assert len(report["findings"]) > 0
    assert os.path.exists("sovereignty_report.json")

    # Cleanup
    if os.path.exists("sovereignty_report.json"):
        os.remove("sovereignty_report.json")

def test_jules_forensic_engine_metadata():
    scanner = JulesForensicEngine("test@example.com")
    report = scanner.generate_sovereignty_report()

    assert report["sovereign_txid"] == "0xAWZ_ZERO_777"
    assert report["kernel_hash"] == "0xVISUALMOONWHEELSYNC2026"

    if os.path.exists("sovereignty_report.json"):
        os.remove("sovereignty_report.json")
