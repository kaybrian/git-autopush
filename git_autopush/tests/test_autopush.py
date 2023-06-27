import unittest
from unittest.mock import patch
import tempfile
import shutil
import os
from io import StringIO

class TestDirectoryMonitor(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.path = os.path.join(self.test_dir, "test")

