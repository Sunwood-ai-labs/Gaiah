import os
from dotenv import load_dotenv
from github import Github

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からアクセストークンを取得
access_token = os.getenv("GITHUB_ACCESS_TOKEN")

# GitHubオブジェクトの作成
g = Github(access_token)

# リポジトリ名
repo_name = "Gaiah_Sample02"

# リポジトリの説明
repo_description = "Gaiah_Sample02 repo"

# リポジトリを作成
repo = g.get_user().create_repo(repo_name, description=repo_description)

print(f"リポジトリ '{repo_name}' が作成されました。")