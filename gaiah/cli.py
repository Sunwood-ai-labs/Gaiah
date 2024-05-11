import argparse
from .main import process_commits

def main():
    parser = argparse.ArgumentParser(description='Gaiah - Git Repository Management Tool')
    parser.add_argument('action', choices=['commit'], help='Action to perform')
    args = parser.parse_args()

    if args.action == 'commit':
        process_commits()
    else:
        print('Invalid action')