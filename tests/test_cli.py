import unittest
from unittest.mock import patch
from gaiah.cli import main

class TestCLI(unittest.TestCase):
    @patch('argparse.ArgumentParser.parse_args')
    @patch('gaiah.main.process_commits')
    def test_main_commit(self, mock_process_commits, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(repo_dir='/path/to/repo', commit_msg_path='/path/to/commit.txt')
        main()
        mock_process_commits.assert_called_once_with('/path/to/repo', '/path/to/commit.txt')

if __name__ == '__main__':
    unittest.main()