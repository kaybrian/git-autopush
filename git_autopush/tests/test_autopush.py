import unittest
from unittest.mock import patch
import tempfile
import shutil
import os
from io import StringIO

class TestDirectoryMonitor(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.git_dir= os.path.join(self.test_dir, ".git")
        os.makedirs(self.git_dir)
        self.file_path = os.path.join(self.test_dir, "tests")
        with open(self.file_path, 'w') as f:
            f.write("Test file")


    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_should_ignore(self):
        self.assertTrue(should_ignore(self.file_path))
        

