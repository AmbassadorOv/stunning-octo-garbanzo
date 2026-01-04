class SealedConfiguration:
    """
    Represents the design object (The Blueprint/Placeholders) that must be sealed
    until the specific order for the final 'one-shot' value arrives.
    """
    def __init__(self, name="WatchtowerConfig"):
        self.name = name
        # Initial placeholders (simulating 'degrees' or fields awaiting the final value)
        self._config_data = {
            "degree_A": None,
            "degree_B": None,
            "degree_C": None
        }
        self._is_sealed = False

    def seal(self):
        """Seals the configuration, making it immutable until the order."""
        self._is_sealed = True
        print(f"[{self.name}] Configuration sealed.")

    def update_all_placeholders(self, new_value):
        """The 'one shot' insertion logic, triggered by the final order."""
        if not self._is_sealed:
            raise PermissionError("Error: Configuration must be sealed before one-shot update.")

        print(f"✅ Executing **ONE-SHOT INSERTION** for '{self.name}'...")
        # Insert the new value into all relevant placeholder fields
        for key in self._config_data:
            if self._config_data[key] is None:
                self._config_data[key] = new_value

        print("Update complete. Placeholders filled reflecting the final Outcome Shape.")
