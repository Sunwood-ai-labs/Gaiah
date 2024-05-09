import os
from git import Repo

# 初期化するフォルダのパス
repo_dir = "C:\\Prj\\Gaiah_Sample01"


# Repoオブジェクトの作成
repo = Repo.init(repo_dir)

# ファイルをインデックスに追加
file_path = os.path.join(repo_dir, "sample.txt")
open(file_path, "w").close()  # 空のファイルを作成
repo.index.add([file_path])

# 変更をコミット
repo.index.commit("Initial commit")