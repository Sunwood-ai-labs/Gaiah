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

# 現在のブランチを取得
current_branch = repo.active_branch

# 現在のブランチの最新コミットを取得
latest_commit = current_branch.commit

# 現在のブランチの差分を取得
diff_index = latest_commit.diff()

# 差分を表示
for diff in diff_index:
    print(colored(f"Diff: {diff.change_type} - {    }", "yellow"))
    print(colored(diff.a_path, "cyan"))
    print("=======================================================")
    print(colored(f"lhs: {diff.a_blob}", "green"))
    print(colored(f"rhs: {diff.b_blob}", "green"))
    
    if diff.change_type == "A":
        print(colored("file added in rhs", "red"))
    elif diff.change_type == "D":
        print(colored("file deleted in lhs", "red"))
    else:
        # 差分の詳細を表示
        if diff.diff:
            print(colored(diff.diff, "white"))
        else:
            print(colored("No changes in diff content.", "magenta"))