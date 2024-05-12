import argparse
from .main import process_commits
from art import *

def main():
    parser = argparse.ArgumentParser(description='Gaiah - Simplified Git Repository Management Tool')
    parser.add_argument('--repo_dir', required=True, help='Directory of the repository')
    parser.add_argument('--commit_msg_path', required=True, help='Path to the commit message file')
    args = parser.parse_args()

    tprint("-- Gaiah --")
    process_commits(args.repo_dir, args.commit_msg_path)
    
    tprint("!! successfully !!")