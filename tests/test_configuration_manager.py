import pytest
import os
from src.configuration_manager import SealedConfiguration, save_config, load_config

TEST_FILENAME = "test_config.pkl"

@pytest.fixture
def cleanup_test_file():
    """A fixture to ensure the test file is removed after the test runs."""
    yield
    if os.path.exists(TEST_FILENAME):
        os.remove(TEST_FILENAME)

def test_full_workflow(cleanup_test_file):
    """
    Tests the entire workflow: create, seal, save, load, and update.
    """
    # 1. Create and verify initial state
    config = SealedConfiguration("TestWorkflow")
    assert config._is_sealed is False
    assert config.get_data()["degree_A"] is None

    # 2. Attempt to update before sealing (should fail)
    config.update_all_placeholders("should_not_work")
    assert config.get_data()["degree_A"] is None

    # 3. Seal the configuration
    config.seal()
    assert config._is_sealed is True

    # 4. Save the sealed configuration
    save_config(config, TEST_FILENAME)
    assert os.path.exists(TEST_FILENAME)

    # 5. Load the configuration
    loaded_config = load_config(TEST_FILENAME)
    assert loaded_config is not None
    assert loaded_config._is_sealed is True
    assert loaded_config.get_data()["degree_A"] is None

    # 6. Perform the "one-shot" update
    update_value = "final_value"
    loaded_config.update_all_placeholders(update_value)

    # Verify the update was successful
    updated_data = loaded_config.get_data()
    assert updated_data["degree_A"] == update_value
    assert updated_data["degree_B"] == update_value
    assert updated_data["degree_C"] == update_value
    assert updated_data["last_update"] == "One-Shot Applied"

    # 7. Attempting to update again should not change the values,
    # as the placeholders are no longer None.
    loaded_config.update_all_placeholders("another_value")
    final_data = loaded_config.get_data()
    assert final_data["degree_A"] == update_value
