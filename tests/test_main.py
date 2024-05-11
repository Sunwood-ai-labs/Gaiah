import unittest
from unittest.mock import patch
from gaiah.main import process_commits

class TestMain(unittest.TestCase):
    @patch('gaiah.main.Repo')
    def test_process_commits(self, mock_repo):
        # テストケースを記述
        pass

if __name__ == '__main__':
    unittest.main()