import os
import sys
import unittest
from glob import glob

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.a1b2_host import app

class HandshakeTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.lattice_dir = os.path.join(os.path.dirname(__file__), '..', 'Lattice')
        # Ensure the lattice directory exists
        if not os.path.exists(self.lattice_dir):
            os.makedirs(self.lattice_dir)

    def tearDown(self):
        # Clean up log files
        for f in glob(os.path.join(self.lattice_dir, '*.log')):
            os.remove(f)

    def test_handshake_creates_log(self):
        """Test that a POST to /handshake creates a log file with the correct content."""
        # Ensure the directory is empty before the test
        self.tearDown()

        response = self.app.post('/handshake')
        self.assertEqual(response.status_code, 200)

        log_files = glob(os.path.join(self.lattice_dir, '*.log'))
        self.assertEqual(len(log_files), 1, "A single log file should be created.")

        with open(log_files[0], 'r') as f:
            content = f.read()
        self.assertEqual(content, 'BREATH_INHALE', "The log file content should be 'BREATH_INHALE'.")

if __name__ == '__main__':
    unittest.main()
