import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Ensure src is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import amne_neuron_core as anc

class TestNeuralLink(unittest.TestCase):

    def test_detect_env_default(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(anc.detect_env(), "GCP")

    def test_detect_env_aws(self):
        with patch.dict(os.environ, {"CLOUD_PROVIDER": "AWS"}):
            self.assertEqual(anc.detect_env(), "AWS")

    def test_generate_identity(self):
        identity = anc.generate_identity("TEST")
        self.assertTrue(identity.startswith("TEST-"))
        self.assertEqual(len(identity.split('-')[1]), 6)

    def test_brain_role_mapping(self):
        self.assertEqual(anc.get_brain_role("AWS"), "The Parietal Lobe (Spatial/Topological Processing)")
        self.assertEqual(anc.get_brain_role("GCP"), "The Prefrontal Cortex (Logical Decision - AMNE Core)")
        self.assertEqual(anc.get_brain_role("Azure"), "The Temporal Lobe (Semantic Memory/Knowledge Graph)")
        self.assertEqual(anc.get_brain_role("OCI"), "The Brainstem (Data Flow/Pulse Regulation)")
        self.assertEqual(anc.get_brain_role("UNKNOWN"), "General Purpose Neuron")

    def test_connect_to_mesh(self):
        mesh = anc.connect_to_mesh("https://hub.url", "TestAuth")
        self.assertEqual(mesh.hub_url, "https://hub.url")
        self.assertEqual(mesh.auth_mode, "TestAuth")

    @patch('time.sleep', return_value=None)
    def test_heartbeat(self, mock_sleep):
        mesh = anc.connect_to_mesh("https://hub.url", "TestAuth")
        mesh.start_heartbeat(frequency_ms=10)
        self.assertTrue(mesh.active)
        mesh.stop_heartbeat()
        self.assertFalse(mesh.active)

if __name__ == "__main__":
    unittest.main()
