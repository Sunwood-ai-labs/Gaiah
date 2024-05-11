import unittest
from unittest.mock import patch
from gaiah.cli import main

class TestCLI(unittest.TestCase):
    @patch('argparse.ArgumentParser.parse_args')
    @patch('gaiah.cli.process_commits')
    def test_main_commit(self, mock_process_commits, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(action='commit')
        main()
        mock_process_commits.assert_called_once()

    @patch('argparse.ArgumentParser.parse_args')
    @patch('gaiah.cli.process_commits')
    def test_main_invalid_action(self, mock_process_commits, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(action='invalid')
        main()
        mock_process_commits.assert_not_called()

if __name__ == '__main__':
    unittest.main()