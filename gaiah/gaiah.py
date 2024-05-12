from git import Repo
import os
import re

class Gaiah:
    def __init__(self, repo_dir, commit_messages_path):
        self.repo_dir = repo_dir
        self.commit_messages_path = commit_messages_path
        self.repo = Repo(repo_dir)
        self.current_branch = self.repo.active_branch.name

    def process_commits(self):
        with open(self.commit_messages_path, "r", encoding="utf-8") as file:
            content = file.read()

        commits = re.split(r'(?m)^##\s', content)[1:]

        for commit in commits:
            filename_match = re.search(r'(?m)^###\s(.+)', commit)
            if filename_match:
                filename = filename_match.group(1).strip()
            else:
                continue

            commit_message_match = re.search(r'```commit-msg\n(.*?)\n```', commit, re.DOTALL)
            if commit_message_match:
                commit_message = commit_message_match.group(1).strip()
            else:
                continue

            self.process_file(filename, commit_message)

        self.push_to_remote()

    def process_file(self, filename, commit_message):
        diff_index = self.repo.index.diff(None)

        file_changed = False
        for diff in diff_index:
            if diff.a_path == filename:
                file_changed = True
                if diff.change_type == "A":
                    self.repo.index.add([filename])
                elif diff.change_type == "D":
                    self.repo.index.remove([filename])
                else:
                    self.repo.index.add([filename])

        if file_changed:
            self.repo.index.commit(commit_message)

    def push_to_remote(self):
        origin = self.repo.remote("origin")
        self.repo.git.push("--set-upstream", origin, self.current_branch)