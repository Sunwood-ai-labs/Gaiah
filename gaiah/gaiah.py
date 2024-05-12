from git import Repo
import os
import re
from termcolor import colored
import subprocess

class Gaiah:
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
        msg = "-"*20 + " unstage " + "-"*20
        print(colored(f"{msg}", "green"))
        
        diff_index = self.repo.index.diff("HEAD")
        staged_files = [diff.a_path for diff in diff_index]
        if staged_files:
            # アンステージするファイルがある場合
            for file_path in staged_files:
                try:
                    subprocess.run(["git", "reset", "HEAD", file_path], check=True, cwd=self.repo_dir)
                    print(colored(f"ファイル {file_path} がアンステージされました。", "green"))
                except subprocess.CalledProcessError as e:
                    print(colored(f"アンステージエラー: {e}", "red"))
                    return False
        else:
            print(colored("ステージされたファイルはありません。", "magenta"))
        
        print(colored(f"-"*len(msg), "green"))
        return True

    def process_commits(self):
        self.unstage_files()  # ステージされたファイルをアンステージ

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

        # 最後のコードブロックの終わり以降の文字列を削除
        # content = re.sub(r'```.*$', '', content, flags=re.DOTALL)

        commits = re.split(r'(?m)^##\s', content)[1:]

        for commit in commits:
            filename_match = re.search(r'(?m)^###\s(.+)', commit)
            if filename_match:
                filename = filename_match.group(1).strip()
                print(colored(f"ファイル [{filename}] を処理中...", "blue"))
            else:
                print(colored("エラー: コミットセクションにファイル名が見つかりません。", "red"))
                continue

            commit_message_match = re.search(r'```commit-msg\n(.*?)\n```', commit, re.DOTALL)
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
        diff_index = self.repo.index.diff(None)
        print(diff_index)
        # diff_index = self.repo.index.diff(None)
        # print(diff_index)
        # raise
        file_changed = False
        for diff in diff_index:
            print(diff.a_path)
            print("-------------------------")
            if diff.a_path == filename:
                file_changed = True
                if diff.change_type == "A":
                    self.repo.index.add([filename])
                    print(colored(f"ファイル {filename} を追加しました。", "green"))
                elif diff.change_type == "D":
                    self.repo.index.remove([filename])
                    print(colored(f"ファイル {filename} を削除しました。", "red"))
                else:
                    self.repo.index.add([filename])
                    print(colored(f"ファイル {filename} を変更しました。", "yellow"))

        if file_changed:
            self.repo.index.commit(commit_message)
            print(colored("変更をコミットしました。", "green"))
        else:
            print(colored(f"ファイル {filename} に変更はありませんでした。", "magenta"))

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