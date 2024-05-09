from git import Repo
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からアクセストークンを取得
access_token = os.getenv("GITHUB_ACCESS_TOKEN")

# リモートリポジトリのURL
remote_url = f"https://{access_token}@github.com/Sunwood-ai-labs/Gaiah_Sample01"

# Repoオブジェクトの作成
repo = Repo("C:\\Prj\\Gaiah_Sample01")

# リモートリポジトリを追加
origin = repo.create_remote("origin", remote_url)

# リモートリポジトリにプッシュ
origin.push(refspec="master:master")