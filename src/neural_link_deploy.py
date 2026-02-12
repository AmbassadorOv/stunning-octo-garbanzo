# Neural Link Core - Deployment Fragment
import amne_neuron_core as anc
import time

def initialize_neuron():
    print("\n--- Neural Interconnect Protocol: Initiation ---")

    # זיהוי ספק הענן והקצאת תפקיד נוירוני
    cloud_provider = anc.detect_env()
    role = anc.get_brain_role(cloud_provider)
    neuron_id = anc.generate_identity(prefix=cloud_provider)

    print(f"Assigning Role: {role}")

    # חיבור ל-Global Neuron Mesh
    mesh = anc.connect_to_mesh(
        hub_url="https://ai.studio/apps/drive/1mTiOR...",
        auth_mode="WorkloadIdentity"
    )

    # הפעלת "דופק" (Pulse) לסינכרון λ₂
    mesh.start_heartbeat(frequency_ms=10)

    print(f"Neuron {neuron_id} is now ACTIVE and LINKED.")

    # Keep running for a short period to demonstrate active state
    time.sleep(1)
    mesh.stop_heartbeat()
    print("--- Deployment Process Finished ---")

if __name__ == "__main__":
    initialize_neuron()
