
<p align="center">
<img src="https://huggingface.co/datasets/MakiAi/IconAssets/resolve/main/Gaiah_icon1.png" width="100%">
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

</h2>

<p align="center">
  <a href="https://hamaruki.com/"><b>[🌐 Website]</b></a> •
  <!-- <a href="https://arxiv.org/abs/2309.17452"><b>[📜 Paper]</b></a> • -->
  <!-- <a href="https://huggingface.co/llm-agents"><b>[🤗 HF Models]</b></a> • -->
  <a href="https://github.com/Sunwood-ai-labs/Gaiah"><b>[🐱 GitHub]</b></a>
  <!-- <a href="https://9557c5365a6f44dc84.gradio.live"><b>[🐯 Gradio Demo]</b></a> -->
  <a href="https://twitter.com/hAru_mAki_ch"><b>[🐦 Twitter]</b></a> •
  <!-- <a href="https://www.reddit.com/r/LocalLLaMA/comments/1703k6d/tora_a_toolintegrated_reasoning_agent_for/"><b>[💬 Reddit]</b></a> • -->
  <a href="https://hamaruki.com/how-to-control-git-with-python-example-of-using-the-gaiah-library/">[🍀 Official Blog]</a>
  <!-- <a href="#-quick-start">Quick Start</a> • -->
  <!-- <a href="#%EF%B8%8F-citation">Citation</a> -->
</p>

</p>

>[!IMPORTANT]
>このリポジトリは[SourceSage](https://github.com/Sunwood-ai-labs/SourceSage)を活用しており、リリースノートやREADME、コミットメッセージの9割は[SourceSage](https://github.com/Sunwood-ai-labs/SourceSage) ＋ [claude.ai](https://claude.ai/)で生成しています。

## 🌟 はじめに

Gaiahは、直感的でAIにやさしいメソッドを使用してGit操作を簡素化する革新的なPythonライブラリです。Gitリポジトリを制御するための高レベルなインターフェースを提供し、AIシステムがバージョン管理とシームレスに連携することを容易にします。新機能としてMarkdownから直接コミットを生成する機能が追加され、文書化されたコミットメッセージの管理がさらに効率的に行えます。

## 🚀 主な特徴

- 🤖 **AIフレンドリー**: AI主導の開発プロセスの独自の要件に対応するメソッドとユーティリティを提供し、AIを念頭に置いて設計されています。
- 🌐 **リモートリポジトリのサポート**: リモートリポジトリとのシームレスな連携を可能にし、GitHubやその他のGitホスティングプラットフォームにリポジトリを作成、クローン、プッシュできるようにします。 
- 📂 **リポジトリ管理**: 新しいリポジトリの初期化、ファイルの追加、コミットの作成、ブランチの管理をシンプルなPythonコードを介して簡単に行うことができます。
- 🔧 **カスタマイズ**: 柔軟性とカスタマイズオプションを提供し、特定のニーズと設定に合わせてGitワークフローを調整できます。
- 📘 **Markdownからのコミット生成**: Markdown形式のドキュメントから直接コミットを生成する機能を追加し、文書化されたコミットメッセージの効率的な管理を可能にします。

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
   pip install gitpython python-dotenv PyGithub termcolor art
   ```

## 🎉 使用方法

### CLI

GaiahのCLI機能により、コマンドラインから直接Git操作を行うことができます。例えば、以下のコマンドを使用してリポジトリにコミットを追加することができます:
```bash
gaiah
```

### 応用的な使い方

特定のプロジェクトディレクトリでGaiahを使用する場合、以下のようにリポジトリの場所やコミットメッセージのファイルパスを指定できます:

```bash
gaiah --repo_dir="C:\\Prj\\Gaiah_Sample02" --commit_msg_path=./tmp2.md
```

上記のコマンドでは、`--repo_dir`オプションでリポジトリのディレクトリを、`--commit_msg_path`オプションでコミットメッセージが記載されたMarkdownファイルのパスを指定しています。

## 🤝 コミットメッセージの一括自動コミット

Gaiahでは、LLMを用いて生成したコミットメッセージを一括自動コミットすることができます。以下の手順でコミットメッセージを生成し、コミットを行います:

1. [sourcesage/config/STAGE_INFO/STAGE_INFO_TEMPLATE_GAIAH.md](https://github.com/Sunwood-ai-labs/SourceSage/blob/main/sourcesage/config/STAGE_INFO/STAGE_INFO_TEMPLATE_GAIAH.md)というフォーマットで、ステージング情報をLLMに渡します。

2. LLMは以下のような形式でコミットメッセージを生成します:

   ```
   Commit Messages フォーマット

   ## Commit 1

   ### README.md

   ```commit-msg
   📝 [docs] READMEに応用的な使い方セクションを追加

   - `README.md`ファイルに新たなセクションとして「応用的な使い方」を追加しました。これにより、ユーザーはGaiahを特定のプロジェクトディレクトリで使用する方法を具体的に学べるようになります。特に、リポジトリの指定やコミットメッセージのファイルパスを設定する具体的なコマンド例を示しています。  
   ```

   ## Commit 2

   ### gaiah/__init__.py

   ```commit-msg
   🔖 [chore] Gaiahのバージョンを0.3.12に更新

   - `gaiah/__init__.py`でのバージョン番号を0.3.11から0.3.12へ更新しました。この更新は、最新の機能改善とバグ修正をユーザーに提供するためのものです。
   ```
   ```

3. 生成されたコミットメッセージを`.Gaiah.md`ファイルに貼り付けます。このファイルは、初回に`gaiah`コマンドを実行した際に自動で生成されます。

4. 再度`gaiah`コマンドを実行すると、`.Gaiah.md`ファイルからコミットメッセージが読み込まれ、自動的にコミットとプッシュが行われます。

## 🤝 貢献

Gaiahをさらに良くするために、コミュニティからの貢献を歓迎します。アイデア、提案、バグ報告がある場合は、[GitHubリポジトリ](https://github.com/Sunwood-ai-labs/Gaiah)で issue を開くか、プルリクエストを送信してください。

## 📄 ライセンス

Gaiahは、[MITライセンス](https://opensource.org/licenses/MIT)の下でリリースされており、ライブラリの自由かつオープンソースでの使用、変更、配布が可能です。

## 🙏 謝辞

Gaiahは、以下のライブラリの優れた機能に基づいて構築されています:

- [GitPython](https://github.com/gitpython-developers/GitPython)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [PyGithub](https://github.com/PyGithub/PyGithub)
- [termcolor](https://pypi.org/project/termcolor/)
- [art](https://pypi.org/project/art/)

これらのプロジェクトの開発者とコントリビューターの皆様が、オープンソースコミュニティに貴重な貢献をしてくださったことに感謝します。

---

Gaiahを使用してGitワークフローの自動化を開始し、AI主導の開発の力を解き放ちましょう! 🚀✨