from git import Repo
import os
from termcolor import colored
import re
from .config import load_config

def process_commits():
    config = load_config()
    repo_dir = config['repo_dir']
    commit_messages_path = config['commit_messages_path']

    # Repoオブジェクトの作成
    repo = Repo(repo_dir)

    # 現在のブランチ名を取得
    current_branch = repo.active_branch.name

    # commit_messages.mdファイルから情報を読み込む
    try:
        with open(commit_messages_path, "r", encoding="utf-8") as file:
            content = file.read()
    except FileNotFoundError:
        print(colored(f"Error: {commit_messages_path} not found.", "red"))
        raise
    except UnicodeDecodeError:
        print(colored(f"Error: Unable to decode {commit_messages_path}. Please ensure the file is saved with UTF-8 encoding.", "red"))
        raise

    # コミットごとに分割
    commits = re.split(r'(?m)^##\s', content)[1:]

    for commit in commits:
        # ファイル名を抽出
        filename_match = re.search(r'(?m)^###\s(.+)', commit)
        if filename_match:
            filename = filename_match.group(1).strip()
        else:
            print(colored("Error: File name not found in the commit section.", "red"))
            continue

        # コミットメッセージを抽出
        commit_message_match = re.search(r'```commit-msg\n(.*?)\n```', commit, re.DOTALL)
        if commit_message_match:
            commit_message = commit_message_match.group(1).strip()
        else:
            print(colored("Error: Commit message not found in the commit section.", "red"))
            continue

        print(colored(">"*60, "blue"))
        print(colored(f">>> filename: {filename}", "blue"))
        print(colored(f"----- commit_message: ----- \n{commit_message}", "green"))

        # ファイルの差分を取得
        diff_index = repo.index.diff(None)

        file_changed = False
        for diff in diff_index:
            if diff.a_path == filename:
                file_changed = True
                if diff.change_type == "A":
                    # ファイルが追加された場合
                    repo.index.add([filename])
                    print(colored(f"Added file: {filename}", "green"))
                elif diff.change_type == "D":
                    # ファイルが削除された場合
                    repo.index.remove([filename])
                    print(colored(f"Deleted file: {filename}", "red"))
                else:
                    # ファイルが変更された場合
                    repo.index.add([filename])
                    print(colored(f"Modified file: {filename}", "yellow"))

        if not file_changed:
            print(colored(f"No changes detected for file: {filename}", "magenta"))
        else:
            # 変更をコミット
            repo.index.commit(commit_message)

    # リモートリポジトリを取得
    origin = repo.remote("origin")

    # 現在のブランチをリモートリポジトリに紐付ける
    repo.git.push("--set-upstream", origin, current_branch)

    # 現在のブランチをリモートリポジトリにプッシュ
    origin.push()

    print(colored("-"*60, "red"))
    print(colored(f"すべてのファイルの更新、コミット、プッシュが完了しました。\n現在のブランチ: {current_branch}", "red"))
    print(colored("-"*60, "red"))