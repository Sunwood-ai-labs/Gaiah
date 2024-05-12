from git import Repo
import os
from termcolor import colored
import re

def process_commits(repo_dir, commit_messages_path):
    # Repoオブジェクトの作成
    repo = Repo(repo_dir)
    print(colored("リポジトリオブジェクトが作成されました。", "cyan"))

    # 現在のブランチ名を取得
    current_branch = repo.active_branch.name
    print(colored(f"現在のブランチ: {current_branch}", "cyan"))

    # commit_messages.mdファイルから情報を読み込む
    try:
        with open(commit_messages_path, "r", encoding="utf-8") as file:
            content = file.read()
            print(colored(f"{commit_messages_path} からコミットメッセージを読み込みました。", "cyan"))
    except FileNotFoundError:
        print(colored(f"エラー: {commit_messages_path} が見つかりません。", "red"))
        return
    except UnicodeDecodeError:
        print(colored(f"エラー: {commit_messages_path} のデコードに失敗しました。ファイルがUTF-8で保存されていることを確認してください。", "red"))
        return

    # コミットごとに分割
    commits = re.split(r'(?m)^##\s', content)[1:]

    for commit in commits:
        # ファイル名を抽出
        filename_match = re.search(r'(?m)^###\s(.+)', commit)
        if filename_match:
            filename = filename_match.group(1).strip()
            print(colored(f"ファイル {filename} を処理中...", "blue"))
        else:
            print(colored("エラー: コミットセクションにファイル名が見つかりません。", "red"))
            continue

        # コミットメッセージを抽出
        commit_message_match = re.search(r'```commit-msg\n(.*?)\n```', commit, re.DOTALL)
        if commit_message_match:
            commit_message = commit_message_match.group(1).strip()
            print(colored(f"------- コミットメッセージ: -------\n{commit_message}", "green"))
            print(colored(f"-----------------------------------", "green"))
        else:
            print(colored("エラー: コミットセクションにコミットメッセージが見つかりません。", "red"))
            continue

        # ファイルの差分を取得
        diff_index = repo.index.diff(None)

        file_changed = False
        for diff in diff_index:
            if diff.a_path == filename:
                file_changed = True
                if diff.change_type == "A":
                    # ファイルが追加された場合
                    repo.index.add([filename])
                    print(colored(f"ファイル {filename} を追加しました。", "green"))
                elif diff.change_type == "D":
                    # ファイルが削除された場合
                    repo.index.remove([filename])
                    print(colored(f"ファイル {filename} を削除しました。", "red"))
                else:
                    # ファイルが変更された場合
                    repo.index.add([filename])
                    print(colored(f"ファイル {filename} を変更しました。", "yellow"))

        if not file_changed:
            print(colored(f"ファイル {filename} に変更はありませんでした。", "magenta"))
        else:
            # 変更をコミット
            repo.index.commit(commit_message)
            print(colored("変更をコミットしました。", "green"))

    # リモートリポジトリを取得
    origin = repo.remote("origin")

    # コミットとプッシュ
    try:
        repo.git.push("--set-upstream", origin, current_branch)
        print(colored("リモートリポジトリにプッシュしました。", "cyan"))
    except Exception as e:
        print(colored(f"リモートへのプッシュエラー: {e}", "red"))

    print(colored("-" * 60, "red"))
    print(colored(f"すべてのファイルの更新、コミット、プッシュが完了しました。\n現在のブランチ: {current_branch}", "red"))
    print(colored("-" * 60, "red"))
