from git import Repo
import os
from termcolor import colored
import re

# リポジトリのパス
repo_dir = "C:\\Prj\\Gaiah_Sample02"

# Repoオブジェクトの作成
repo = Repo(repo_dir)

# 現在のブランチ名を取得
current_branch = repo.active_branch.name

# commit_messages.mdファイルのパス
commit_messages_path = "tmp2.md"

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

    print(colored(f"filename: {filename}", "blue"))
    print(colored(f"----- commit_message: ----- \n{commit_message}", "green"))

    # ファイルの存在確認
    file_path = os.path.join(repo_dir, filename)
    if os.path.exists(file_path):
        # ファイルをインデックスに追加
        repo.index.add([filename])
    else:
        # ファイルが存在しない場合は削除として扱う
        repo.index.remove([filename])

    # 変更をコミット
    repo.index.commit(commit_message)

# リモートリポジトリを取得
origin = repo.remote("origin")

# 現在のブランチをリモートリポジトリに紐付ける
repo.git.push("--set-upstream", origin, current_branch)

# 現在のブランチをリモートリポジトリにプッシュ
origin.push()

print(colored(f"すべてのファイルの更新、コミット、プッシュが完了しました。現在のブランチ: {current_branch}", "red"))