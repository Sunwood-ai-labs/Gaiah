from git import Repo
from dotenv import load_dotenv
import os

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からアクセストークンを取得
access_token = os.getenv("GITHUB_ACCESS_TOKEN")

# リモートリポジトリのURL
remote_url = f"https://{access_token}@github.com/Sunwood-ai-labs/Gaiah_Sample01"

# Repoオブジェクトの作成
repo = Repo("C:\\Prj\\Gaiah_Sample01")

# 既存のリモートリポジトリを取得
origin = repo.remote("origin")

# リモートリポジトリのURLを設定
origin.set_url(remote_url)

# リモートリポジトリにプッシュ
origin.push(refspec="master:master")