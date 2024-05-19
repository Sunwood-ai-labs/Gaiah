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

    def process_commits(self):
        self.commit.process_commits()