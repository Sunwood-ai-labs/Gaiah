import re
from loguru import logger
from .utils import run_command
import os

class GaiahCommit:
    FILENAME_REGEX = r'(?m)^###\s(.+)'
    COMMIT_MESSAGE_REGEX = r'```commit-msg\n(.*?)\n```'

    def __init__(self, repo):
        self.repo = repo
        self.logger = logger

    def unstage_files(self):
        """
        ステージにある全てのファイルをアンステージする
        """
        self.logger.info("Unstaging all files...")
        try:
            staged_files = run_command(["git", "diff", "--name-only", "--cached"], cwd=self.repo.repo_dir).splitlines()

            if staged_files:
                run_command(["git", "reset", "HEAD", "--"] + staged_files, cwd=self.repo.repo_dir)
                self.logger.success(f"Unstaged files: {', '.join(staged_files)}")
            else:
                self.logger.info("No staged files found.")

        except Exception as e:
            self.logger.error(f"Error while unstaging files: {e}")
            raise

    def stage_file(self, filename, action):
        """
        ファイルをステージする
        """
        try:
            if action == "deleted":
                run_command(["git", "rm", filename], cwd=self.repo.repo_dir)
                self.logger.info(f"Deleted file: {filename}")
            else:
                run_command(["git", "add", filename], cwd=self.repo.repo_dir)
                self.logger.info(f"Staged file: {filename}")
        except Exception as e:
            self.logger.error(f"Error while staging file: {filename} - {e}")
            raise

    def commit_changes(self, commit_message):
        """
        変更をコミットする
        """
        try:
            run_command(["git", "commit", "-m", commit_message], cwd=self.repo.repo_dir)
            self.logger.success("Committed changes.")
        except Exception as e:
            self.logger.error(f"Error while committing changes: {e}")
            raise

    def process_commits(self):
        """
        コミットメッセージファイルからコミットを処理する
        """
        try:
            with open(self.repo.commit_messages_path, "r", encoding="utf-8") as file:
                content = file.read()
        except FileNotFoundError:
            self.logger.warning(f"Commit messages file not found: {self.repo.commit_messages_path}")
            self.logger.info(f"Creating an empty commit messages file: {self.repo.commit_messages_path}")
            with open(self.repo.commit_messages_path, "w", encoding="utf-8") as file:
                file.write("")
            return

        commits = re.split(self.FILENAME_REGEX, content)[1:]
        for i in range(0, len(commits), 2):
            filename = commits[i].strip()
            commit_message_section = commits[i + 1]
            self.process_commit_section(filename, commit_message_section)

        self.repo.push_to_remote(branch_name="develop")



    def process_commit_section(self, filename, commit_message_section):
        """
        コミットセクションを処理する
        """
        commit_message_match = re.search(self.COMMIT_MESSAGE_REGEX, commit_message_section, re.DOTALL)
        if commit_message_match:
            commit_message = commit_message_match.group(1)
            msg = f"{'-'*20} Commit message: [{filename}]{'-'*20} "
            self.logger.info(f"{msg}")
            for commit_msg in commit_message.split("\n"):
                self.logger.info(f"{commit_msg}")
            commit_message =commit_message.strip()
            self.logger.info(f"{'-'*len(msg)}")
        else:
            self.logger.warning("No commit message found in the commit section. Skipping...")
            return

        self.process_file(filename, commit_message)

    def process_file(self, filename, commit_message):
        """
        ファイルを処理する
        """
        try:
            if os.path.exists(os.path.join(self.repo.repo_dir, filename)):
                self.stage_file(filename, "modified")
            else:
                self.stage_file(filename, "deleted")

            changed_files = run_command(["git", "diff", "--staged", "--name-only"], cwd=self.repo.repo_dir).splitlines()

            if filename in changed_files:
                self.commit_changes(commit_message)
            else:
                self.logger.info(f"No changes detected in file: {filename}")
                self.unstage_files()

        except Exception as e:
            self.logger.error(f"Error while processing file: {filename} - {e}")
            raise