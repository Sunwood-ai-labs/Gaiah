import os
import re
import subprocess
from dotenv import load_dotenv
from github import Github
from termcolor import colored
import shutil
import time
class Gaiah:
    """
    Gaiahクラス - Gitリポジトリの管理を行う
    """
    COMMIT_SECTION_REGEX = r'(?m)^##\s'
    FILENAME_REGEX = r'(?m)^###\s(.+)'
    COMMIT_MESSAGE_REGEX = r'```commit-msg\n(.*?)\n```'

    def __init__(self, repo_dir, commit_messages_path):
        """
        コンストラクタ
        """
        self.repo_dir = repo_dir
        self.commit_messages_path = os.path.join(repo_dir, commit_messages_path) if commit_messages_path else None
        os.makedirs(repo_dir, exist_ok=True)
        
        if self.commit_messages_path and not os.path.exists(self.commit_messages_path):
            with open(self.commit_messages_path, 'w') as f:
                pass
            print(colored(f"空の {commit_messages_path} ファイルを作成しました。", "yellow"))
        
        try:
            self.current_branch = self.run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
            print(colored(f"現在のブランチ: {self.current_branch}", "cyan"))
        except:
            print(colored(f"現在のブランチを取得できません。", "red"))
        # if repo_dir:
        #     self.initialize_repository()
        # else:
        #     self.repo_dir = None
        #     self.current_branch = None

    def initialize_repository(self):
        """
        リポジトリを初期化する
        """
        try:
            self.run_command(["git", "rev-parse", "--is-inside-work-tree"], check=True, capture_output=False)
            self.current_branch = self.run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
            print(colored("リポジトリオブジェクトが作成されました。", "cyan"))
            print(colored(f"現在のブランチ: {self.current_branch}", "cyan"))
        except subprocess.CalledProcessError:
            print(colored(f"{self.repo_dir} はGitリポジトリではありません。", "red"))
            print(colored("リポジトリを初期化します...", "yellow"))
            self.init_repo(self.repo_dir)
            self.current_branch = "main"  # デフォルトのブランチ名を設定

    def init_repo(self, repo_dir, initial_commit=True):
        """
        新しいリポジトリを初期化する
        """
        if not os.path.exists(repo_dir):
            os.makedirs(repo_dir)
            print(colored(f"ディレクトリ '{repo_dir}' を作成しました。", "green"))

        self.run_command(["git", "init"], cwd=repo_dir)
        self.run_command(["git", "config", "user.name", "Maki"], cwd=repo_dir)
        self.run_command(["git", "config", "user.email", "sunwood.ai.labs@gmail.com"], cwd=repo_dir)

        load_dotenv()
        access_token = os.getenv("GITHUB_ACCESS_TOKEN")
        repo_name = os.path.basename(repo_dir)
        remote_url = f"https://{access_token}@github.com/Sunwood-ai-labs/{repo_name}.git"

        try:
            self.run_command(["git", "remote", "add", "origin", remote_url], cwd=repo_dir)
            print(colored(f"リモートリポジトリ '{remote_url}' を追加しました。", "green"))
        except:
            print(colored(f"リモートリポジトリ '{remote_url}' は登録済です。", "green"))
            
        if initial_commit:
            readme_path = os.path.join(repo_dir, "README.md")
            demo_readme_path = os.path.join(os.path.dirname(__file__), "template", "DEMO_README.md")
            shutil.copy(demo_readme_path, readme_path)
            self.run_command(["git", "add", "README.md"], cwd=repo_dir)

            readme_path = os.path.join(repo_dir, ".gitignore")
            demo_readme_path = os.path.join(os.path.dirname(__file__), "template", ".gitignore")
            shutil.copy(demo_readme_path, readme_path)
            self.run_command(["git", "add", ".gitignore"], cwd=repo_dir)
            print(colored(f"ファイル '.gitignore' をインデックスに追加しました。", "green"))

            # mainブランチの名前を設定
            self.run_command(["git", "branch", "-M", "main"], cwd=repo_dir)
            print(colored("mainブランチの名前を 'main' に設定しました。", "green"))

            self.current_branch = "main"  # デフォルトのブランチ名を設定

            self.run_command(["git", "commit", "-m", "Initial commit"], cwd=repo_dir)
            try:
                self.run_command(["git", "push", "-u", "origin", "main"], cwd=repo_dir)
            except:
                self.run_command(["git", "push", "-f", "origin", "main"], cwd=repo_dir)
            print(colored("初期コミットをリモートリポジトリにプッシュしました。", "green"))

        self.current_branch = "main"

    def create_repo(self, repo_name, repo_params):
        """
        新しいリポジトリをGitHub上に作成する
        """
        try:
            load_dotenv()
            access_token = os.getenv("GITHUB_ACCESS_TOKEN")
            g = Github(access_token)
            repo = g.get_user().create_repo(repo_name, **repo_params)
            print(colored(f"リポジトリ '{repo_name}' が作成されました。", "green"))
            time.sleep(2)
            
        except Exception as e:
            print(colored(f"リポジトリの作成中にエラーが発生しました: {e}", "red"))

    def process_commits(self):
        """
        コミットメッセージファイルからコミットを処理する
        """
        # コミット処理の実装をここに記述します
        pass

    def run_command(self, command, cwd=None, check=True, capture_output=True):
        print(colored(f"実行コマンド: {' '.join(command)}", "yellow"))
        result = subprocess.run(command, cwd=cwd or self.repo_dir, check=check, capture_output=capture_output, text=True, encoding='utf-8')
        return result.stdout.strip() if capture_output else None


    def unstage_files(self):
        """
        ステージにある全てのファイルをアンステージする
        """
        msg = "-" * 20 + " unstage " + "-" * 20
        print(colored(f"{msg}", "green"))

        try:
            staged_files = self.run_command(["git", "diff", "--name-only", "--cached"]).splitlines()

            if staged_files:
                self.run_command(["git", "reset", "HEAD", "--"] + staged_files)
                print(colored(f"ステージされたファイルをアンステージしました: {', '.join(staged_files)}", "green"))
            else:
                print(colored("ステージされたファイルはありません。", "magenta"))

        except subprocess.CalledProcessError as e:
            print(colored(f"アンステージエラー: {e}", "red"))
            return False

        print(colored(f"-" * len(msg), "green"))
        return True

    def process_commits(self):
        """
        コミットメッセージファイルからコミットを処理する
        """
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

        self.unstage_files()

        commits = re.split(self.COMMIT_SECTION_REGEX, content)[1:]

        for commit in commits:
            self.process_commit_section(commit)

        self.push_to_remote()

    def process_commit_section(self, commit_section):
        """
        コミットセクションを処理する
        """
        filename_match = re.search(self.FILENAME_REGEX, commit_section)
        if filename_match:
            filename = filename_match.group(1).strip()
            print(colored(f"ファイル [{filename}] を処理中...", "blue"))
        else:
            print(colored("エラー: コミットセクションにファイル名が見つかりません。", "red"))
            return

        commit_message_match = re.search(self.COMMIT_MESSAGE_REGEX, commit_section, re.DOTALL)
        if commit_message_match:
            commit_message = commit_message_match.group(1).strip()
            print(colored(f"------- コミットメッセージ: -------\n{commit_message}", "green"))
            print(colored(f"-----------------------------------", "green"))
        else:
            print(colored("エラー: コミットセクションにコミットメッセージが見つかりません。", "red"))
            return

        self.process_file(filename, commit_message)

    def process_file(self, filename, commit_message):
        """
        ファイルを処理する
        """
        try:
            if os.path.exists(os.path.join(self.repo_dir, filename)):
                self.stage_file(filename, "modified")
            else:
                self.stage_file(filename, "deleted")

            changed_files = self.run_command(["git", "diff", "--staged", "--name-only"]).splitlines()

            if filename in changed_files:
                self.commit_changes(commit_message)
            else:
                print(colored(f"ファイル {filename} に変更はありませんでした。", "magenta"))
                self.unstage_files()

        except subprocess.CalledProcessError as e:
            print(colored(f"Git コマンドの実行中にエラーが発生しました: {e}", "red"))

    def stage_file(self, filename, action):
        """
        ファイルをステージする
        """
        try:
            if action == "deleted":
                self.run_command(["git", "rm", filename])
                print(colored(f"ファイル {filename} を削除しました。", "red"))
            else:
                self.run_command(["git", "add", filename])
                print(colored(f"ファイル {filename} を{action}しました。", "green"))
        except subprocess.CalledProcessError as e:
            print(colored(f"ファイルのステージング中にエラーが発生しました: {e}", "red"))

    def commit_changes(self, commit_message):
        """
        変更をコミットする
        """
        try:
            self.run_command(["git", "commit", "-m", commit_message])
            print(colored("変更をコミットしました。", "green"))
        except subprocess.CalledProcessError as e:
            print(colored(f"変更のコミット中にエラーが発生しました: {e}", "red"))

    def push_to_remote(self):
        """
        リモートリポジトリにプッシュする
        """
        try:
            self.run_command(["git", "push", "--set-upstream", "origin", self.current_branch])
            print(colored("リモートリポジトリにプッシュしました。", "cyan"))
        except subprocess.CalledProcessError as e:
            print(colored(f"リモートへのプッシュエラー: {e}", "red"))

        print(colored("-" * 60, "red"))
        print(colored(f"すべてのファイルの更新、コミット、プッシュが完了しました。\n現在のブランチ: {self.current_branch}", "red"))
        print(colored("-" * 60, "red"))