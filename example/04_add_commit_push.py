from git import Repo
import os

# リポジトリのパス
repo_dir = "C:\\Prj\\Gaiah_Sample02"

# Repoオブジェクトの作成
repo = Repo(repo_dir)

# README.mdファイルのパス
readme_path = os.path.join(repo_dir, "README.md")

# README.mdファイルの内容
readme_content = "# Gaiah Sample Repository\n\nThis is a sample repository created using GitPython."

# README.mdファイルを作成し、内容を書き込む
with open(readme_path, "w") as file:
    file.write(readme_content)

# ファイルをインデックスに追加
repo.index.add(["README.md"])

# 変更をコミット
commit_message = "Add README.md file"
repo.index.commit(commit_message)

# リモートリポジトリを取得
origin = repo.remote("origin")

# リモートリポジトリにプッシュ
origin.push(refspec="master:master")

print("README.mdファイルを追加し、コミットとプッシュが完了しました。")