from git import Repo
import os
from termcolor import colored

# リポジトリのパス
repo_dir = "C:\\Prj\\Gaiah_Sample02"

# Repoオブジェクトの作成
repo = Repo(repo_dir)

# tmp.mdファイルのパス
tmp_path = "tmp.md"

# tmp.mdファイルから情報を読み込む
try:
    with open(tmp_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
except FileNotFoundError:
    print(colored(f"Error: {tmp_path} not found.", "red"))
    raise
except UnicodeDecodeError:
    print(colored(f"Error: Unable to decode {tmp_path}. Please ensure the file is saved with UTF-8 encoding.", "red"))
    raise

# ファイル名とコミットメッセージを抽出
filename = None
commit_message = None
content = []

for i, line in enumerate(lines):
    if line.startswith("`"):
        if filename is None:
            filename = line.strip("`\n")
        else:
            break
    elif "[" in line and "]" in line:
        commit_message_start = i
        for j in range(i + 1, len(lines)):
            if lines[j].startswith("`"):
                commit_message_end = j
                break
        else:
            commit_message_end = len(lines)
        commit_message = "".join(lines[commit_message_start:commit_message_end]).strip()
        break

for line in lines[commit_message_end:]:
    content.append(line)

print(colored(f"filename: {filename}", "blue"))
print(colored(f"commit_message: {commit_message}", "green"))

# # ファイルの内容を更新
# file_path = os.path.join(repo_dir, filename)
# with open(file_path, "w", encoding="utf-8") as file:
#     file.writelines(content)

# ファイルをインデックスに追加
repo.index.add([filename])

# 変更をコミット
repo.index.commit(commit_message)

# リモートリポジトリを取得
origin = repo.remote("origin")

# リモートリポジトリにプッシュ
origin.push(refspec="master:master")

print(colored(f"{filename}ファイルを更新し、コミットとプッシュが完了しました。", "blue"))