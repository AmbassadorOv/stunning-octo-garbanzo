import os
import unittest

class TestWorkflowFilenames(unittest.TestCase):
    def test_workflow_filenames_are_valid(self):
        """
        Tests that all files and directories in .github/workflows have valid names.
        A valid name should not contain a colon ':'.
        """
        workflows_dir = ".github/workflows"
        if not os.path.exists(workflows_dir):
            # If the directory doesn't exist, the test passes.
            return

        for filename in os.listdir(workflows_dir):
            self.assertNotIn(":", filename, f"Invalid character ':' found in filename '{filename}'")

if __name__ == "__main__":
    unittest.main()
