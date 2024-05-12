import argparse
from .main import process_commits
from art import *
import os
from termcolor import colored
from .gaiah import Gaiah

def main():
    parser = argparse.ArgumentParser(description='Gaiah - シンプルなGitリポジトリ管理ツール')
    parser.add_argument('--repo_dir', default='./', help='リポジトリのディレクトリ')
    parser.add_argument('--commit_msg_path', default='.Gaiah.md', help='コミットメッセージファイルのパス')
    args = parser.parse_args()

    commit_msg_path = args.commit_msg_path
    if not os.path.exists(commit_msg_path):
        open(commit_msg_path, 'w', encoding="utf8").close()
    
    tprint("-- Gaiah --")
    
    with open(commit_msg_path, 'r', encoding="utf8") as file:
        content = file.read().strip()
        if not content:
            print(colored("-" * 60, "red"))
            print(colored("コミットメッセージファイルが空です。終了します。", "red"))
            print(colored("-" * 60, "red"))
            return

    gaiah = Gaiah(args.repo_dir, args.commit_msg_path)
    gaiah.process_commits()
    
    tprint("!! successfully !!")