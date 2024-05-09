

<p align="center">
<img src="https://media.githubusercontent.com/media/Sunwood-ai-labs/Gaiah/main/docs/example_icon.png" width="100%">
</p>

# Gaiah サンプルドキュメント

このドキュメントでは、Gaiahライブラリに含まれるサンプルファイルの概要と説明を提供します。これらのサンプルは、PythonでGaiahを使用してさまざまなGit操作を実行する方法を示しています。

## 目次

1. [リポジトリの初期化](#リポジトリの初期化)
2. [リモートリポジトリの作成](#リモートリポジトリの作成)
3. [リモートリポジトリへのプッシュ](#リモートリポジトリへのプッシュ)
4. [変更の追加、コミット、プッシュ](#変更の追加コミットプッシュ)

## リポジトリの初期化

`01_init_repo.py`ファイルは、Gaiahを使用して新しいGitリポジトリを初期化する方法を示しています。

```python
import os
from git import Repo

# リポジトリが初期化されるフォルダのパス
repo_dir = "C:\\Prj\\Gaiah_Sample02"

# フォルダが存在しない場合は作成する
if not os.path.exists(repo_dir):
    os.makedirs(repo_dir)

# Repoオブジェクトを作成する
repo = Repo.init(repo_dir)

# ファイルをインデックスに追加する
file_path = os.path.join(repo_dir, "sample.txt")
open(file_path, "w").close()  # 空のファイルを作成する
repo.index.add([file_path])

# 変更をコミットする
repo.index.commit("Initial commit")
```

このサンプルでは、以下の手順を実行しています:
1. リポジトリが初期化されるフォルダのパスを指定します。
2. フォルダが存在しない場合は作成します。
3. `Repo.init()`を使用して新しいGitリポジトリを初期化します。
4. `sample.txt`という名前のファイルをリポジトリのインデックスに追加します。
5. "Initial commit"というメッセージで変更をコミットします。

## リモートリポジトリの作成

`02_create_remote_repo.py`ファイルは、Gaiahを使用してGitHub上にリモートリポジトリを作成する方法を示しています。

```python
import os
from dotenv import load_dotenv
from github import Github

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からアクセストークンを取得する
access_token = os.getenv("GITHUB_ACCESS_TOKEN")

# Githubオブジェクトを作成する
g = Github(access_token)

# リポジトリ名
repo_name = "Gaiah_Sample02"

# リポジトリの説明
repo_description = "Gaiah_Sample02 repo"

# リポジトリを作成する
repo = g.get_user().create_repo(repo_name, description=repo_description)

print(f"リポジトリ '{repo_name}' が正常に作成されました。")
```

このサンプルでは、以下の手順を実行しています:
1. `.env`ファイルから環境変数を読み込みます。
2. 環境変数からGitHubアクセストークンを取得します。
3. アクセストークンを使用して`Github`オブジェクトを作成します。
4. リポジトリの名前と説明を指定します。
5. `g.get_user().create_repo()`を使用してリポジトリを作成します。

## リモートリポジトリへのプッシュ

`03_push_to_remote.py`ファイルは、Gaiahを使用してリモートリポジトリに変更をプッシュする方法を示しています。

```python
from git import Repo
from dotenv import load_dotenv
import os

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からアクセストークンを取得する
access_token = os.getenv("GITHUB_ACCESS_TOKEN")

# リモートリポジトリのURL
remote_url = f"https://{access_token}@github.com/Sunwood-ai-labs/Gaiah_Sample02"

# Repoオブジェクトを作成する
repo = Repo("C:\\Prj\\Gaiah_Sample02")

# 新しいリモートを作成する
origin = repo.create_remote("origin", remote_url)

# リモートリポジトリにプッシュする
origin.push(refspec="master:master")
```

このサンプルでは、以下の手順を実行しています:
1. `.env`ファイルから環境変数を読み込みます。
2. 環境変数からGitHubアクセストークンを取得します。
3. アクセストークンを使用してリモートリポジトリのURLを構築します。
4. ローカルリポジトリの`Repo`オブジェクトを作成します。
5. リモートリポジトリのURLを使用して、"origin"という名前の新しいリモートを作成します。
6. リモートリポジトリに変更をプッシュします。

## 変更の追加、コミット、プッシュ

`04_add_commit_push.py`ファイルは、Gaiahを使用して新しいファイルを追加し、変更をコミットし、リモートリポジトリにプッシュする方法を示しています。

```python
from git import Repo
import os

# リポジトリのパス
repo_dir = "C:\\Prj\\Gaiah_Sample02"

# Repoオブジェクトを作成する
repo = Repo(repo_dir)

# README.mdファイルのパス
readme_path = os.path.join(repo_dir, "README.md")

# README.mdファイルの内容
readme_content = "# Gaiah Sample Repository\n\nこれはGitPythonを使用して作成されたサンプルリポジトリです。"

# README.mdファイルを作成し、内容を書き込む
with open(readme_path, "w") as file:
    file.write(readme_content)

# ファイルをインデックスに追加する
repo.index.add(["README.md"])

# 変更をコミットする
commit_message = "Add README.md file"
repo.index.commit(commit_message)

# リモートリポジトリを取得する
origin = repo.remote("origin")

# リモートリポジトリにプッシュする
origin.push(refspec="master:master")

print("README.mdファイルが正常に追加、コミット、プッシュされました。")
```

このサンプルでは、以下の手順を実行しています:
1. リポジトリのパスを指定します。
2. リポジトリの`Repo`オブジェクトを作成します。
3. `README.md`ファイルのパスと内容を指定します。
4. `README.md`ファイルを作成し、内容を書き込みます。
5. `README.md`ファイルをリポジトリのインデックスに追加します。
6. "Add README.md file"というメッセージで変更をコミットします。
7. "origin"という名前のリモートリポジトリを取得します。
8. リモートリポジトリに変更をプッシュします。

これらのサンプルは、PythonでGaiahを使用して一般的なGit操作を実行するための基本的な使用方法を示しています。これらのサンプルを出発点として使用し、特定の要件に応じてカスタマイズすることができます。