import unittest
import subprocess
import os

class BackupTestCase(unittest.TestCase):
    def test_backup_db_script_exists(self):
        self.assertTrue(os.path.exists('db/backup_db.py'))

    def test_backup_software_script_exists(self):
        self.assertTrue(os.path.exists('db/backup_software.py'))

    # Puedes mockear subprocess si quieres probar la ejecución

if __name__ == '__main__':
    unittest.main()