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
    
    parser.add_argument('--process_commits', action='store_true', help='マークダウンファイルから複数のコミットを行う')
    parser.add_argument('--commit_msg_path', default='.Gaiah.md', help='コミットメッセージファイルのパス')

    return parser.parse_args()


def main():
    args = parse_arguments()

    tprint("!  Gaiahへようこそ  !")

    repo_dir = args.repo_dir if args.init_repo or args.process_commits else None
    commit_msg_path = args.commit_msg_path if args.process_commits else None
    gaiah = Gaiah(repo_dir, commit_msg_path)

    if args.init_repo:
        gaiah.init_local_repo(args.repo_dir, not args.no_initial_commit)

    if args.create_repo:
        repo_params = {
            'description': args.description,
            'private': args.private
        }
        logger.info(">>> リモートリポジトリを作成しています...")
        gaiah.create_remote_repo(args.repo_name, repo_params)
        
        logger.info(">>> ブランチを作成しています...")
        gaiah.create_branches()
        
        logger.info(">>> 初期ファイルを追加しています...")
        gaiah.add_initial_files()
        
        logger.info(">>> 初期ファイルをコミットしています...")
        gaiah.commit_initial_files()
        
        logger.info(">>> ブランチをマージしています...")
        gaiah.merge_branches()
        
        logger.info(">>> マージしたブランチをプッシュしています...")
        gaiah.push_merged_branches()

    if args.process_commits:
        gaiah.process_commits()

    logger.success("全ての操作が正常に完了しました!")

if __name__ == "__main__":
    main()