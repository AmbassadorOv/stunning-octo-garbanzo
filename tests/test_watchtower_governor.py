import pytest
import os
import subprocess
import sys

# Define the filenames that will be created by the script
GOV_CONSTANT_FILE = "governing_rule.pkl"
CONFIG_FILE = "target_blueprint.pkl"

@pytest.fixture
def cleanup_test_files():
    """A fixture to ensure the test files are removed after the test runs."""
    # Setup can go here if needed
    yield
    # Teardown: remove the files
    if os.path.exists(GOV_CONSTANT_FILE):
        os.remove(GOV_CONSTANT_FILE)
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)

def test_full_script_execution_as_black_box(cleanup_test_files):
    """
    Tests the entire workflow of the watchtower_governor.py script
    by running it as a subprocess and verifying its output and artifacts.
    This avoids pickle loading issues between processes.
    """
    result = subprocess.run(
        [sys.executable, "-m", "src.watchtower_governor"],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )

    # 1. Check that the script ran successfully
    assert result.returncode == 0, f"Script failed with error:\n{result.stderr}"

    # 2. Check for key output phrases to ensure each major step was executed
    assert "AAA Defense Layer" in result.stdout
    assert "GOVERNING CONSTANT CLARIFICATION" in result.stdout
    assert "EXECUTION REALITY REPORT" in result.stdout
    assert "VALUATION UPDATE REPORT" in result.stdout
    assert "ONE-SHOT INSERTION TRIGGERED" in result.stdout
    assert "Final Configuration State" in result.stdout
    assert "Moon_Wheel_Kernel_V2026" in result.stdout
    assert "KERNEL_SYNC_0xVISUALMOONWHEELSYNC2026" in result.stdout

    # 3. Verify that the final .pkl files were created, confirming the save operations worked
    assert os.path.exists(GOV_CONSTANT_FILE)
    assert os.path.exists(CONFIG_FILE)
