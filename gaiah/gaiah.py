from git import Repo
import os
import re
from termcolor import colored
import subprocess


def get_modified_files(repo_dir):
    """
    リポジトリ内の変更されているファイルの一覧を取得する
    """
    try:
        result = subprocess.run(["git", "status", "--porcelain"], cwd=repo_dir, text=True, capture_output=True, check=True)
        output = result.stdout
        modified_files = []

        for line in output.splitlines():
            parts = line.split()
            if parts:
                status = parts[0]
                file_path = ' '.join(parts[1:])
                modified_files.append((status, file_path))

        return modified_files
    except subprocess.CalledProcessError as e:
        print(colored(f"エラー: {e}", "red"))
        return []


class Gaiah:
    COMMIT_SECTION_REGEX = r'(?m)^##\s'
    FILENAME_REGEX = r'(?m)^###\s(.+)'
    COMMIT_MESSAGE_REGEX = r'```commit-msg\n(.*?)\n```'

    def __init__(self, repo_dir, commit_messages_path):
        self.repo_dir = repo_dir
        self.commit_messages_path = commit_messages_path
        self.repo = Repo(repo_dir)
        self.current_branch = self.repo.active_branch.name
        print(colored("リポジトリオブジェクトが作成されました。", "cyan"))
        print(colored(f"現在のブランチ: {self.current_branch}", "cyan"))

    def unstage_files(self):
        """
        ステージにある全てのファイルをアンステージする
        """
        msg = "-" * 20 + " unstage " + "-" * 20
        print(colored(f"{msg}", "green"))

        diff_index = self.repo.index.diff("HEAD")
        staged_files = [diff.a_path for diff in diff_index]
        if staged_files:
            for file_path in staged_files:
                try:
                    subprocess.run(["git", "reset", "HEAD", file_path], check=True, cwd=self.repo_dir)
                    print(colored(f"ファイル {file_path} がアンステージされました。", "green"))
                except subprocess.CalledProcessError as e:
                    print(colored(f"アンステージエラー: {e}", "red"))
                    return False
        else:
            print(colored("ステージされたファイルはありません。", "magenta"))

        print(colored(f"-" * len(msg), "green"))
        return True

    def process_commits(self):
        try:
            with open(self.commit_messages_path, "r", encoding="utf-8") as file:
                content = file.read()
                print(colored(f"{self.commit_messages_path} からコミットメッセージを読み込みました。", "cyan"))
        except FileNotFoundError:
            print(colored(f"エラー: {self.commit_messages_path} が見つかりません。", "red"))
            return
        except UnicodeDecodeError:
            print(colored(f"エラー: {self.commit_messages_path} のデコードに失敗しました。ファイルがUTF-8で保存されていることを確認してください。", "red"))
            return

        commits = re.split(self.COMMIT_SECTION_REGEX, content)[1:]

        for commit in commits:
            filename_match = re.search(self.FILENAME_REGEX, commit)
            if filename_match:
                filename = filename_match.group(1).strip()
                print(colored(f"ファイル [{filename}] を処理中...", "blue"))
            else:
                print(colored("エラー: コミットセクションにファイル名が見つかりません。", "red"))
                continue

            commit_message_match = re.search(self.COMMIT_MESSAGE_REGEX, commit, re.DOTALL)
            if commit_message_match:
                commit_message = commit_message_match.group(1).strip()
                print(colored(f"------- コミットメッセージ: -------\n{commit_message}", "green"))
                print(colored(f"-----------------------------------", "green"))
            else:
                print(colored("エラー: コミットセクションにコミットメッセージが見つかりません。", "red"))
                continue

            self.process_file(filename, commit_message)

        self.push_to_remote()

    def process_file(self, filename, commit_message):
        try:
            result = subprocess.run(
                ["git", "diff", "--name-status", "HEAD"],
                cwd=self.repo_dir,
                text=True,
                capture_output=True,
                check=True
            )

            lines = result.stdout.splitlines()
            file_changed = False
            for line in lines:
                status, path = line.split(maxsplit=1)
                if path == filename:
                    file_changed = True
                    if status == "A":
                        self.stage_file(filename, "added")
                    elif status == "D":
                        self.stage_file(filename, "deleted")
                    else:  # Modified or other changes
                        self.stage_file(filename, "modified")

            if file_changed:
                self.commit_changes(commit_message)
            else:
                print(colored(f"ファイル {filename} に変更はありませんでした。", "magenta"))

        except subprocess.CalledProcessError as e:
            print(colored(f"Git コマンドの実行中にエラーが発生しました: {e}", "red"))

    def stage_file(self, filename, action):
        try:
            if action == "deleted":
                subprocess.run(["git", "rm", filename], cwd=self.repo_dir)
                print(colored(f"ファイル {filename} を削除しました。", "red"))
            else:
                subprocess.run(["git", "add", filename], cwd=self.repo_dir)
                print(colored(f"ファイル {filename} を{action}しました。", "green"))
        except subprocess.CalledProcessError as e:
            print(colored(f"ファイルのステージング中にエラーが発生しました: {e}", "red"))

    def commit_changes(self, commit_message):
        try:
            subprocess.run(["git", "commit", "-m", commit_message], cwd=self.repo_dir)
            print(colored("変更をコミットしました。", "green"))
        except subprocess.CalledProcessError as e:
            print(colored(f"変更のコミット中にエラーが発生しました: {e}", "red"))

    def push_to_remote(self):
        origin = self.repo.remote("origin")
        try:
            self.repo.git.push("--set-upstream", origin, self.current_branch)
            print(colored("リモートリポジトリにプッシュしました。", "cyan"))
        except Exception as e:
            print(colored(f"リモートへのプッシュエラー: {e}", "red"))

        print(colored("-" * 60, "red"))
        print(colored(f"すべてのファイルの更新、コミット、プッシュが完了しました。\n現在のブランチ: {self.current_branch}", "red"))
        print(colored("-" * 60, "red"))