# main_orchestrator.py
# Main script to demonstrate the integration of the callback-enabled handshake.

from src.app.agents.resurrection_engine_v2 import ResurrectionEngineV2
import src.app.agents.resurrection_envelope_v4 as envelope

def main():
    """
    Orchestrates the setup and execution of the integrated handshake protocol.
    """
    print("--- Main Orchestrator Initialized ---")

    # 1. Instantiate the Resurrection Engine
    # The SEAL is passed to the engine to ensure resonance calculations are anchored
    engine = ResurrectionEngineV2(seal=envelope.SEAL)

    # 2. Register the engine's processing method as the envelope's callback
    envelope.register_cycle_callback(engine.process_cycle)

    # 3. Start any background processes the engine might have (placeholder)
    engine.start_background()

    # 4. Run the Julius node handshake protocol
    # The envelope will now trigger the engine's callback on each sweep cycle.
    envelope.run_julius_node()

    print("\n--- Main Orchestrator Finished ---")

if __name__ == "__main__":
    main()
