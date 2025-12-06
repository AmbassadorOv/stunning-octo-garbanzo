import pytest
import os
import subprocess
import sys
import time

from src.governor.constants import TemporalGoverningConstant
from src.governor.configuration import SealedConfiguration
from src.governor.observer import ExecutionObserver
from src.governor.persistence import seal_and_preserve, load_component

# --- Unit Tests for Individual Modules ---

def test_temporal_governing_constant():
    """Tests the TemporalGoverningConstant class."""
    constant = TemporalGoverningConstant()
    assert constant.rule_version == "1.0"
    assert "World of Thought" in constant.INTELLECTUAL_ACCOUNTING["DOMAIN"]
    assert "Sequential Execution" in constant.REALITY_CONSTRAINT["DOMAIN"]

def test_sealed_configuration():
    """Tests the SealedConfiguration class."""
    config = SealedConfiguration()
    assert not config._is_sealed
    # Should raise an error if updating before sealing
    with pytest.raises(PermissionError):
        config.update_all_placeholders("test_value")

    # Sealing and then updating should work
    config.seal()
    assert config._is_sealed
    config.update_all_placeholders("test_value_2")
    assert config._config_data["degree_A"] == "test_value_2"


def test_execution_observer():
    """Tests the ExecutionObserver class."""
    observer = ExecutionObserver("test_design")
    observer.record_stage_start("test_stage")
    time.sleep(0.01)
    observer.record_stage_finish("test_stage", True)
    assert observer.sequential_stages["test_stage"]["status"] == "COMPLETED"
    assert observer.quality_adherence_factor == 1.0
    observer.record_stage_start("failed_stage")
    observer.record_stage_finish("failed_stage", False)
    assert observer.quality_adherence_factor < 1.0

def test_persistence(cleanup_test_files):
    """Tests the persistence functions."""
    constant = TemporalGoverningConstant()
    filename = "test_constant.pkl"
    seal_and_preserve(constant, filename)
    assert os.path.exists(filename)
    loaded_constant = load_component(filename)
    assert loaded_constant is not None
    assert loaded_constant.rule_version == "1.0"
    os.remove(filename)

# --- Black-Box Test for the Entire Script ---

# Define the filenames that will be created by the script
GOV_CONSTANT_FILE = "governing_rule.pkl"
CONFIG_FILE = "target_blueprint.pkl"
# Since the script will run from within 'src', the files will be created there
GOV_CONSTANT_FILE_PATH = os.path.join("src", GOV_CONSTANT_FILE)
CONFIG_FILE_PATH = os.path.join("src", CONFIG_FILE)


@pytest.fixture
def cleanup_test_files():
    """A fixture to ensure the test files are removed after the test runs."""
    yield
    # Teardown: remove the files from the 'src' directory
    if os.path.exists(GOV_CONSTANT_FILE_PATH):
        os.remove(GOV_CONSTANT_FILE_PATH)
    if os.path.exists(CONFIG_FILE_PATH):
        os.remove(CONFIG_FILE_PATH)

def test_full_script_execution_as_black_box(cleanup_test_files):
    """
    Tests the entire workflow of the main.py script
    by running it as a subprocess from within the 'src' directory.
    """
    result = subprocess.run(
        [sys.executable, "-m", "main"],
        capture_output=True,
        text=True,
        encoding='utf-8',
        cwd="src"  # Run the command from the 'src' directory
    )

    # 1. Check that the script ran successfully
    assert result.returncode == 0, f"Script failed with error:\n{result.stderr}"

    # 2. Check for key output phrases to ensure each major step was executed
    assert "GOVERNING CONSTANT CLARIFICATION" in result.stdout
    assert "EXECUTION REALITY REPORT" in result.stdout
    assert "ONE-SHOT INSERTION TRIGGERED" in result.stdout
    assert "Final Configuration State" in result.stdout
    assert "Finalized_Adherence" in result.stdout

    # 3. Verify that the final .pkl files were created in the 'src' directory
    assert os.path.exists(GOV_CONSTANT_FILE_PATH)
    assert os.path.exists(CONFIG_FILE_PATH)
