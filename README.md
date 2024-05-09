
<p align="center">
<img src="docs/Gaiah_icon1.png" width="100%">
<br>
<h1 align="center">Gaiah</h1>
<h2 align="center">
  ～Python Git Automation with Innovative Heuristics～

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/MakiAi/Gaiah)
[![Gaiah - Sunwood-ai-labs](https://img.shields.io/static/v1?label=Gaiah&message=Sunwood-ai-labs&color=blue&logo=github)](https://github.com/Gaiah/Sunwood-ai-labs "Go to GitHub repo")
[![stars - Sunwood-ai-labs](https://img.shields.io/github/stars/Gaiah/Sunwood-ai-labs?style=social)](https://github.com/Gaiah/Sunwood-ai-labs)
[![forks - Sunwood-ai-labs](https://img.shields.io/github/forks/Gaiah/Sunwood-ai-labs?style=social)](https://github.com/Gaiah/Sunwood-ai-labs)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/Sunwood-ai-labs/Gaiah)](https://github.com/Sunwood-ai-labs/Gaiah)
[![GitHub Top Language](https://img.shields.io/github/languages/top/Sunwood-ai-labs/Gaiah)](https://github.com/Sunwood-ai-labs/Gaiah)
[![GitHub Release](https://img.shields.io/github/v/release/Sunwood-ai-labs/Gaiah?sort=date&color=red)](https://github.com/Sunwood-ai-labs/Gaiah)
[![GitHub Tag](https://img.shields.io/github/v/tag/Sunwood-ai-labs/Gaiah?color=orange)](https://github.com/Sunwood-ai-labs/Gaiah)

  <br>

</h2>



</p>

>[!IMPORTANT]
>このリポジトリは[SourceSage](https://github.com/Sunwood-ai-labs/SourceSage)を活用しており、リリースノートやREADME、コミットメッセージの9割は[SourceSage](https://github.com/Sunwood-ai-labs/SourceSage) ＋ [claude.ai](https://claude.ai/)で生成しています。

## 🌟 はじめに

Gaiahは、直感的でAIにやさしいメソッドを使用してGit操作を簡素化する革新的なPythonライブラリです。Gitリポジトリを制御するための高レベルなインターフェースを提供し、AIシステムがバージョン管理とシームレスに連携することを容易にします。

Gaiahを使用すると、リポジトリの作成、変更のコミット、リモートリポジトリへの更新のプッシュなど、さまざまなGitタスクを自動化できます。

## 🚀 主な特徴

- 🤖 **AIフレンドリー**: このライブラリは、AI主導の開発プロセスの独自の要件に対応するメソッドとユーティリティを提供し、AIを念頭に置いて設計されています。

- 🌐 **リモートリポジトリのサポート**: Gaiahは、リモートリポジトリとのシームレスな連携を可能にし、AIシステムがGitHubやその他のGitホスティングプラットフォームにリポジトリを作成、クローン、プッシュできるようにします。

- 📂 **リポジトリ管理**: Gaiahを使用すると、シンプルなPythonコードを介して、新しいリポジトリの初期化、ファイルの追加、コミットの作成、ブランチの管理を簡単に行うことができます。

- 🔧 **カスタマイズ**: このライブラリは、柔軟性とカスタマイズオプションを提供し、特定のニーズと設定に合わせてGitワークフローを調整できます。

## 📦 インストール

Gaiahの使用を開始するには、次の手順に従ってください:

1. 新しいconda環境を作成します:
   ```
   conda create -n gaiah python=3.11
   ```

2. conda環境をアクティベートします:
   ```
   conda activate gaiah
   ```

3. 必要な依存関係をインストールします:
   ```
   pip install gitpython
   pip install python-dotenv
   pip install PyGithub
   ```

## 🎉 使用方法

Gaiahは、一般的なGit操作を実行するための簡単で直感的なメソッドを提供します。いくつかの例を以下に示します:

1. 新しいリポジトリを初期化する:
   ```python
   from gaiah import Gaiah

   repo_dir = "path/to/repository"
   gaiah = Gaiah(repo_dir)
   gaiah.init()
   ```

2. リモートリポジトリを作成する:
   ```python
   gaiah.create_remote_repo("Gaiah_Sample", "サンプルリポジトリ")
   ```

3. ファイルを追加し、変更をコミットする:
   ```python
   gaiah.add_file("README.md", "# サンプルリポジトリ")
   gaiah.commit("README.mdを追加")
   ```

4. 変更をリモートリポジトリにプッシュする:
   ```python
   gaiah.push()
   ```

詳細な使用方法と例については、[ドキュメント](https://gaiah.readthedocs.io)を参照してください。

## 🤝 貢献

Gaiahをさらに良くするために、コミュニティからの貢献を歓迎します。アイデア、提案、バグ報告がある場合は、[GitHubリポジトリ](https://github.com/Sunwood-ai-labs/Gaiah)で issue を開くか、プルリクエストを送信してください。

## 📄 ライセンス

Gaiahは、[MITライセンス](https://opensource.org/licenses/MIT)の下でリリースされており、ライブラリの自由かつオープンソースでの使用、変更、配布が可能です。

## 🙏 謝辞

Gaiahは、以下のライブラリの優れた機能に基づいて構築されています:

- [GitPython](https://github.com/gitpython-developers/GitPython)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [PyGithub](https://github.com/PyGithub/PyGithub)

これらのプロジェクトの開発者とコントリビューターの皆様が、オープンソースコミュニティに貴重な貢献をしてくださったことに感謝します。

---

Gaiahを使用してGitワークフローの自動化を開始し、AI主導の開発の力を解き放ちましょう! 🚀✨