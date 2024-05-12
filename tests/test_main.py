import unittest
from unittest.mock import patch, MagicMock
from gaiah.main import process_commits

class TestMain(unittest.TestCase):
    @patch('gaiah.main.Repo')
    def test_process_commits(self, mock_repo):
        mock_repo.return_value.index.diff.return_value = [MagicMock(a_path="README.md", change_type="A")]
        process_commits('/fake/repo', '/fake/path/commit.txt')
        mock_repo.return_value.index.add.assert_called_once_with(['README.md'])

if __name__ == '__main__':
    unittest.main()