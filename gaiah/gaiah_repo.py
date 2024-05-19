import os
import subprocess
from loguru import logger
from .gaiah_github import create_remote_repo, get_remote_repo
from .utils import run_command, tqdm_sleep
import shutil

class GaiahRepo:
    def __init__(self, repo_dir, commit_messages_path):
        self.repo_dir = repo_dir
        self.commit_messages_path = os.path.join(repo_dir, commit_messages_path) if commit_messages_path else None
        self.default_branch = "develop"

    def init_local_repo(self, repo_dir, initial_commit=True):
        """
        既存のディレクトリをGitリポジトリとして初期化する
        """
        if not os.path.exists(repo_dir):
            os.makedirs(repo_dir)
            logger.info(f"Created directory: {repo_dir}")
        else:
            logger.info(f"Directory already exists: {repo_dir}")
        try:
            run_command(["git", "init"], cwd=repo_dir)
            logger.success(f"Initialized Git repository in: {repo_dir}")

        except Exception as e:
            logger.error(f"Error while initializing Git repository in: {repo_dir} - {e}")
            raise

    def create_remote_repo(self, repo_name, repo_params):
        """
        GitHub上に新しいリモートリポジトリを作成する
        """
        create_remote_repo(repo_name, repo_params)
        repo = get_remote_repo(repo_name)
        if repo is not None:
            remote_url = repo.clone_url

            try:
                run_command(["git", "remote", "add", "origin", remote_url], cwd=self.repo_dir)
                logger.success(f"Added remote: {remote_url}")
            except Exception as e:
                logger.error(f"Error while adding remote: {remote_url} - {e}")
                raise

    def add_initial_files(self):
        """
        初期ファイルをリポジトリに追加する
        """
        try:
            # .gitignoreファイルをコピー
            gitignore_src = os.path.join(os.path.dirname(__file__), 'template', '.gitignore')
            gitignore_dst = os.path.join(self.repo_dir, '.gitignore')
            shutil.copyfile(gitignore_src, gitignore_dst)
            logger.info(f"Copied .gitignore file to: {gitignore_dst}")

            # DEMO_README.mdファイルをコピー
            readme_src = os.path.join(os.path.dirname(__file__), 'template', 'DEMO_README.md')
            readme_dst = os.path.join(self.repo_dir, 'README.md')
            shutil.copyfile(readme_src, readme_dst)
            logger.info(f"Copied DEMO_README.md file to: {readme_dst}")

            run_command(["git", "add", "."], cwd=self.repo_dir)
            logger.success("Added initial files.")
        except Exception as e:
            logger.error(f"Error while adding initial files: {e}")
            raise

    def create_branches(self):
        """
        mainブランチとdevelopブランチを作成する
        """
        try:
            # 現在のブランチを取得
            current_branch = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=self.repo_dir).strip()
        except:
            logger.error("現在のブランチを取得できません。")

        try:
            # mainブランチが存在しない場合はmainブランチを作成
            if "main" not in run_command(["git", "branch"], cwd=self.repo_dir):
                run_command(["git", "checkout", "-b", "main"], cwd=self.repo_dir)
                logger.info("mainブランチを作成しました。")
            else:
                logger.info("mainブランチは既に存在します。")

            # developブランチが存在しない場合はdevelopブランチを作成
            if "develop" not in run_command(["git", "branch"], cwd=self.repo_dir):
                run_command(["git", "checkout", "-b", "develop"], cwd=self.repo_dir)
                logger.info("developブランチを作成しました。")
            else:
                logger.info("developブランチは既に存在します。")

            # 元のブランチに戻る
            # run_command(["git", "checkout", self.default_branch], cwd=self.repo_dir)
        except Exception as e:
            logger.error(f"ブランチの作成中にエラーが発生しました: {e}")
            raise

    def push_initial_commit(self):
        """
        初期コミットをリモートリポジトリにプッシュする
        """
        try:
            run_command(["git", "push", "-u", "origin", "main"], cwd=self.repo_dir)
            logger.success("Pushed initial commit to remote repository.")
        except Exception as e:
            logger.error(f"Error while pushing initial commit to remote repository: {e}")
            raise

    def push_to_remote(self, branch_name):
        """
        変更をリモートリポジトリにプッシュする
        """
        try:
            run_command(["git", "push", "-u", "origin", branch_name], cwd=self.repo_dir)
            logger.success("Pushed changes to remote repository.")
        except Exception as e:
            logger.error(f"Error while pushing changes to remote repository: {e}")
            raise

    def commit_initial_files(self):
        """
        初期ファイルをコミットする
        """
        try:
            # developブランチをチェックアウト
            run_command(["git", "checkout", "-b", "develop"], cwd=self.repo_dir)
            logger.info("developブランチをチェックアウトしました。")

            # 初期ファイルをコミット
            run_command(["git", "add", "."], cwd=self.repo_dir)
            run_command(["git", "commit", "-m", '"🌟 初期ファイルを追加"'], cwd=self.repo_dir)
            logger.success("初期ファイルをコミットしました。")
        except Exception as e:
            logger.error(f"初期ファイルのコミット中にエラーが発生しました: {e}")
            raise

    def merge_branches(self):
        """
        mainブランチとdevelopブランチをマージする
        """
        try:
            # mainブランチをチェックアウト
            try:
                run_command(["git", "checkout", "-b", "main"], cwd=self.repo_dir)
                logger.info("mainブランチをチェックアウトしました。")
            except Exception as e:
                logger.warning(f"mainブランチのチェックアウトに失敗しました: {e}")
                logger.info("mainブランチを作成します。")
                run_command(["git", "checkout", "-b", "main"], cwd=self.repo_dir)
                logger.success("mainブランチを作成しました。")

            # developブランチをmainブランチにマージ
            try:
                run_command(["git", "merge", "develop"], cwd=self.repo_dir)
                logger.success("developブランチをmainブランチにマージしました。")
            except Exception as e:
                logger.warning(f"developブランチのマージに失敗しました: {e}")
                logger.info("developブランチを作成します。")
                run_command(["git", "checkout", "-b", "develop"], cwd=self.repo_dir)
                logger.success("developブランチを作成しました。")

        except Exception as e:
            logger.error(f"ブランチのマージ中にエラーが発生しました: {e}")
            raise

    def delete_branch(self, branch_name):
        """
        指定されたブランチをローカルとリモートから削除する
        """
        try:
            # developブランチに切り替え
            run_command(["git", "checkout", "develop"], cwd=self.repo_dir)
            logger.info(f"Switched to develop branch.")

            # ローカルブランチを削除
            run_command(["git", "branch", "-d", branch_name], cwd=self.repo_dir)
            logger.success(f"Deleted local branch: {branch_name}")

            # リモートブランチを削除
            # run_command(["git", "push", "origin", "--delete", branch_name], cwd=self.repo_dir)
            # logger.success(f"Deleted remote branch: {branch_name}")

        except Exception as e:
            logger.error(f"Error while deleting branch {branch_name}: {e}")
            raise

    def merge_to_develop(self, branch_name):
        """
        指定されたブランチの変更をdevelopブランチにマージする
        """
        try:
            # developブランチに切り替え
            run_command(["git", "checkout", "develop"], cwd=self.repo_dir)
            logger.info(f"Switched to develop branch.")

            # 指定されたブランチの変更をdevelopブランチにマージ
            # run_command(["git", "merge", branch_name], cwd=self.repo_dir)
            run_command(["git", "merge", "--no-ff", "-m", f"Merge {branch_name}", branch_name], cwd=self.repo_dir)
            
            logger.success(f"Merged {branch_name} into develop.")

            # developブランチをリモートにプッシュ
            self.push_to_remote(branch_name="develop")

        except Exception as e:
            logger.error(f"Error while merging {branch_name} into develop: {e}")
            raise

    def push_merged_branches(self):
        """
        マージしたブランチをリモートリポジトリにプッシュする
        """
        try:
            # mainブランチをプッシュ
            run_command(["git", "push", "-u", "origin", "main"], cwd=self.repo_dir)
            logger.success("mainブランチをリモートリポジトリにプッシュしました。")

            # developブランチをプッシュ
            run_command(["git", "push", "-u", "origin", "develop"], cwd=self.repo_dir)
            logger.success("developブランチをリモートリポジトリにプッシュしました。")
        except Exception as e:
            logger.error(f"マージしたブランチのプッシュ中にエラーが発生しました: {e}")
            raise