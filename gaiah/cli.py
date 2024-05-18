import argparse
from art import *
import os
from termcolor import colored
from .gaiah import Gaiah

def main():
    parser = argparse.ArgumentParser(description='Gaiah - シンプルなGitリポジトリ管理ツール')
    subparsers = parser.add_subparsers(dest='command', help='利用可能なコマンド')

    # process-commitsコマンド
    process_commits_parser = subparsers.add_parser('process-commits', help='マークダウンファイルから複数のコミットを行う')
    process_commits_parser.add_argument('--repo_dir', default='./', help='リポジトリのディレクトリ')
    process_commits_parser.add_argument('--commit_msg_path', default='.Gaiah.md', help='コミットメッセージファイルのパス')

    # create-repoコマンド
    create_repo_parser = subparsers.add_parser('create-repo', help='新しいリポジトリを作成する')
    create_repo_parser.add_argument('repo_name', help='作成するリポジトリ名')
    create_repo_parser.add_argument('--description', default='', help='リポジトリの説明')
    create_repo_parser.add_argument('--private', action='store_true', help='プライベートリポジトリとして作成する')

    args = parser.parse_args()

    tprint("!  Welcome  to  Gaiah  !")

    if args.command == 'process-commits':
        commit_msg_path = args.commit_msg_path
        if not os.path.exists(commit_msg_path):
            open(commit_msg_path, 'w', encoding="utf8").close()
        
        with open(commit_msg_path, 'r', encoding="utf8") as file:
            content = file.read().strip()
            if not content:
                print(colored("-" * 60, "red"))
                print(colored("コミットメッセージファイルが空です。終了します。", "red"))
                print(colored("-" * 60, "red"))
                return

        gaiah = Gaiah(args.repo_dir, args.commit_msg_path)
        gaiah.process_commits()

    elif args.command == 'create-repo':
        repo_params = {
            'description': args.description,
            'private': args.private
        }
        gaiah = Gaiah()
        gaiah.create_repo(args.repo_name, repo_params)

    else:
        parser.print_help()
        return

    tprint("!! successfully !!")