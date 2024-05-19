import os
import subprocess
from loguru import logger
from .gaiah_github import create_remote_repo
from .utils import run_command

class GaiahRepo:
    def __init__(self, repo_dir, commit_messages_path):
        self.repo_dir = repo_dir
        self.commit_messages_path = os.path.join(repo_dir, commit_messages_path) if commit_messages_path else None

    def init_local_repo(self, repo_dir, initial_commit=True):
        """
        既存のディレクトリをGitリポジトリとして初期化する
        """
        if not os.path.exists(repo_dir):
            os.makedirs(repo_dir)
            logger.info(f"Created directory: {repo_dir}")

        try:
            run_command(["git", "init"], cwd=repo_dir)
            logger.success(f"Initialized Git repository in: {repo_dir}")

            if initial_commit:
                self.make_initial_commit()
        except Exception as e:
            logger.error(f"Error while initializing Git repository in: {repo_dir} - {e}")
            raise

    def make_initial_commit(self):
        """
        初期コミットを作成する
        """
        try:
            run_command(["git", "add", "."], cwd=self.repo_dir)
            run_command(["git", "commit", "-m", "Initial commit"], cwd=self.repo_dir)
            logger.success("Created initial commit.")
        except Exception as e:
            logger.error(f"Error while creating initial commit: {e}")
            raise

    def create_remote_repo(self, repo_name, repo_params):
        """
        GitHub上に新しいリモートリポジトリを作成する
        """
        repo = create_remote_repo(repo_name, repo_params)
        remote_url = repo.clone_url

        try:
            run_command(["git", "remote", "add", "origin", remote_url], cwd=self.repo_dir)
            logger.success(f"Added remote: {remote_url}")
        except Exception as e:
            logger.error(f"Error while adding remote: {remote_url} - {e}")
            raise

    def push_to_remote(self):
        """
        変更をリモートリポジトリにプッシュする
        """
        try:
            run_command(["git", "push", "-u", "origin", "main"], cwd=self.repo_dir)
            logger.success("Pushed changes to remote repository.")
        except Exception as e:
            logger.error(f"Error while pushing changes to remote repository: {e}")
            raise