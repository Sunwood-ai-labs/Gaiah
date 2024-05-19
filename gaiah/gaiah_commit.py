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

    def commit_changes(self, commit_message, branch_name=None):
        """
        変更をコミットする
        """
        try:
            if branch_name:
                try:
                    run_command(["git", "checkout", "-b", branch_name], cwd=self.repo.repo_dir)
                except:
                    pass
                    
            # 複数行のコミットメッセージに対応
            commit_message_lines = commit_message.split("\n")
            commit_message_file = os.path.join(self.repo.repo_dir, ".gaiah_commit_message.txt")
            with open(commit_message_file, "w", encoding="utf-8") as f:
                f.write(commit_message)
            
            run_command(["git", "commit", "-F", commit_message_file], cwd=self.repo.repo_dir)
            os.remove(commit_message_file)
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

        branch_sections = re.split(r'(?m)^##\s(.+)', content)[1:]

        for i in range(0, len(branch_sections), 2):
            branch_name = branch_sections[i].strip()
            branch_content = branch_sections[i + 1]

            commits = re.split(self.FILENAME_REGEX, branch_content)
            if commits and not commits[0].strip():
                commits = commits[1:]

            for j in range(0, len(commits), 2):
                filename = commits[j].strip()
                commit_message_section = commits[j + 1]
                self.process_commit_section(filename, commit_message_section, branch_name)

            # self.repo.push_to_remote(branch_name=branch_name)
            
            # developブランチにマージ
            self.repo.merge_to_develop(branch_name)
            
            # マージ後のブランチを削除
            self.repo.delete_branch(branch_name)

    def process_commit_section(self, filename, commit_message_section, branch_name):
        """
        コミットセクションを処理する
        """
        commit_message_match = re.search(self.COMMIT_MESSAGE_REGEX, commit_message_section, re.DOTALL)
        if commit_message_match:
            commit_message = commit_message_match.group(1)
            # 絵文字を削除する
            # commit_message = re.sub(r'[^\x00-\x7F]+', '', commit_message)
            msg = f"{'-'*10} Commit message: [{branch_name}][{filename}]{'-'*10} "
            self.logger.info(f"{msg}")
            for commit_msg in commit_message.split("\n"):
                self.logger.info(f"{commit_msg}")
            commit_message = commit_message.strip()
            self.logger.info(f"{'-'*len(msg)}")
        else:
            self.logger.warning("No commit message found in the commit section. Skipping...")
            return

        self.process_file(filename, commit_message, branch_name)

    def process_file(self, filename, commit_message, branch_name=None):
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
                self.commit_changes(commit_message, branch_name)
                # self.repo.push_to_remote(branch_name=branch_name)
            else:
                self.logger.info(f"No changes detected in file: {filename}")
                self.unstage_files()

        except Exception as e:
            self.logger.error(f"Error while processing file: {filename} - {e}")
            raise