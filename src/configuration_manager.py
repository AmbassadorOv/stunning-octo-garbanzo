import pickle
import os

class SealedConfiguration:
    """
    Represents a configuration object that can be sealed to prevent
    further modifications. It holds 'placeholder' degrees/fields.
    """
    def __init__(self, name="DefaultConfig"):
        self.name = name
        # Initial placeholders (simulating 'degrees' or fields)
        self._config_data = {
            "degree_A": None,
            "degree_B": None,
            "degree_C": None,
            "last_update": "Initial Creation"
        }
        self._is_sealed = False

    def get_data(self):
        """Returns a copy of the configuration data."""
        return self._config_data.copy()

    def seal(self):
        """Seals the configuration, preventing future changes."""
        self._is_sealed = True
        print(f"Configuration '{self.name}' has been **SEALED**.")

    def update_all_placeholders(self, new_value):
        """
        The 'one shot' insertion logic. It updates all placeholder fields.
        This can only be done if the configuration is sealed.
        """
        if not self._is_sealed:
            print("🛑 Error: Configuration must be sealed before the one-shot update is performed.")
            return

        print(f"✅ Executing **ONE-SHOT INSERTION** for '{self.name}'...")

        # Insert the new value into all relevant fields
        for key in self._config_data:
            if key.startswith("degree_") and self._config_data[key] is None:
                self._config_data[key] = new_value

        self._config_data["last_update"] = "One-Shot Applied"
        print("Update complete. Placeholders filled.")

    # --- Standard Python methods for easy viewing ---
    def __str__(self):
        return f"[{'SEALED' if self._is_sealed else 'DRAFT'}] Config: {self.name} | Data: {self._config_data}"

    def __repr__(self):
        return self.__str__()


def save_config(config_obj, filename="sealed_config.pkl"):
    """Preserves the configuration object by saving it to a file using pickle."""
    try:
        with open(filename, 'wb') as f:
            pickle.dump(config_obj, f)
        print(f"💾 Configuration **PRESERVED** to: {filename}")
    except Exception as e:
        print(f"An error occurred while saving: {e}")

def load_config(filename="sealed_config.pkl"):
    """Loads and restores the configuration object from the file."""
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return None
    try:
        with open(filename, 'rb') as f:
            config_obj = pickle.load(f)
        print(f"📥 Configuration **RESTORED** from: {filename}")
        return config_obj
    except Exception as e:
        print(f"An error occurred while loading: {e}")
        return None

# --- Main Execution Logic ---
if __name__ == "__main__":
    CONFIG_FILENAME = "Hex6F_Final_Config.pkl"

    # 1. Configure and Seal
    print("--- STEP 1: CONFIGURING AND SEALING ---")
    initial_config = SealedConfiguration("Hex6F Workflow")
    print(f"Initial State: {initial_config}")
    initial_config.seal()

    # 2. Preserve (Save)
    print("\n--- STEP 2: PRESERVING TO FILE ---")
    save_config(initial_config, CONFIG_FILENAME)

    # --- SIMULATE A LATER ORDER/EXECUTION ---
    print("\n--- STEP 3: RESTORING AND EXECUTING ORDER ---")

    # Check if the file exists before attempting to load
    if os.path.exists(CONFIG_FILENAME):
        # 3. Restore (Load)
        restored_config = load_config(CONFIG_FILENAME)
        print(f"Restored State: {restored_config}")

        # 4. Execute the 'one shot' update
        if restored_config:
            # The 'order' has arrived!
            print("\n**ORDER RECEIVED:** Apply the final execution result (E^2) to all placeholders.")
            restored_config.update_all_placeholders(new_value="X1E^2SEQUENCESSTRUCTURES_Finalized")
            print(f"\nFinal State after update: {restored_config}")

            # Optional: Resave the updated config
            save_config(restored_config, CONFIG_FILENAME)

    # Clean up the created file (optional)
    # os.remove(CONFIG_FILENAME)
    # print(f"\nCleaned up file: {CONFIG_FILENAME}")
