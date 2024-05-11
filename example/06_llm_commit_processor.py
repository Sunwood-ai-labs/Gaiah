from git import Repo
import os
from termcolor import colored
import re

# リポジトリのパス
repo_dir = "C:\\Prj\\Gaiah_Sample02"

# Repoオブジェクトの作成
repo = Repo(repo_dir)

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

    # ファイルをインデックスに追加
    repo.index.add([filename])

    # 変更をコミット
    repo.index.commit(commit_message)

# リモートリポジトリを取得
origin = repo.remote("origin")

# リモートリポジトリにプッシュ
origin.push(refspec="master:master")

print(colored("すべてのファイルの更新、コミット、プッシュが完了しました。", "blue"))