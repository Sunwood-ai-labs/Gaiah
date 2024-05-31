import argparse
from art import tprint
from loguru import logger
from gaiah.gaiah import Gaiah
import sys

logger.configure(
    handlers=[
        {
            "sink": sys.stderr,
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level:<8}</level> | <cyan>{name:<45}:{line:<5}</cyan> | <level>{message}</level>",
            "colorize": True,
        }
    ]
)

def parse_arguments():
    """
    コマンドライン引数を解析する
    """
    parser = argparse.ArgumentParser(description='Gaiah - シンプルなGitリポジトリ管理ツール')
    
    parser.add_argument('--create_repo', action='store_true', help='新しいリポジトリを作成する')
    parser.add_argument('--repo_name', help='作成するリポジトリ名')
    parser.add_argument('--description', default='', help='リポジトリの説明')
    parser.add_argument('--private', action='store_true', help='プライベートリポジトリとして作成する')
    
    parser.add_argument('--init_repo', action='store_true', help='既存のディレクトリをGitリポジトリとして初期化する')
    parser.add_argument('--repo_dir', default='./', help='初期化するディレクトリのパス')
    parser.add_argument('--no_initial_commit', action='store_true', help='初期コミットを作成しない')
    
    parser.add_argument('--branch_name', default=None, help='コミットに使用するブランチ名')
    parser.add_argument('--process_commits', action='store_true', help='マークダウンファイルから複数のコミットを行う')
    parser.add_argument('--commit_msg_path', default='.Gaiah.md', help='コミットメッセージファイルのパス')

    return parser.parse_args()

def main():
    args = parse_arguments()
    tprint("!  Welcome to Gaiah  !")
    gaiah = Gaiah(args)
    gaiah.run()

if __name__ == "__main__":
    main()