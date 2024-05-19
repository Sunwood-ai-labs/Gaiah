from loguru import logger
from .gaiah_repo import GaiahRepo
from .gaiah_commit import GaiahCommit

class Gaiah:
    def __init__(self, repo_dir, commit_messages_path):
        self.repo_dir = repo_dir
        self.commit_messages_path = commit_messages_path
        self.repo = GaiahRepo(repo_dir, commit_messages_path)
        self.commit = GaiahCommit(self.repo)

    def init_local_repo(self, repo_dir, initial_commit=True):
        self.repo.init_local_repo(repo_dir, initial_commit)

    def create_remote_repo(self, repo_name, repo_params):
        self.repo.create_remote_repo(repo_name, repo_params)

    def add_initial_files(self):
        self.repo.add_initial_files()

    def create_branches(self):
        self.repo.create_branches()

    def commit_initial_files(self):
        self.repo.commit_initial_files()

    def merge_branches(self):
        self.repo.merge_branches()

    def push_merged_branches(self):
        self.repo.push_merged_branches()

    def process_commits(self):
        self.commit.process_commits()