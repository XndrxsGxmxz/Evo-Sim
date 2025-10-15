import os

def test_backup_db_script_exists():
    assert os.path.exists('db/backup_db.py')

def test_backup_software_script_exists():
    assert os.path.exists('db/backup_software.py')