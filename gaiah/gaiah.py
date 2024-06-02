from loguru import logger
from .gaiah_repo import GaiahRepo
from .gaiah_commit import GaiahCommit

class Gaiah:
    def __init__(self, config):
        self.config = config
        self.repo_dir = self.config['gaiah']['local']['repo_dir']
        print(self.repo_dir)
        self.repo = GaiahRepo(self.repo_dir, self.config)
        self.commit = GaiahCommit(self.repo)

    def run(self):
        if self.config['gaiah']['local']['init_repo']:
            self.init_local_repo(self.repo_dir, not self.config['gaiah']['local']['no_initial_commit'])

        if self.config['gaiah']['repo']['create_repo']:
            repo_params = {
                'description': self.config['gaiah']['repo']['description'],
                'private': self.config['gaiah']['repo']['private']
            }
            self.create_remote_repo(self.config['gaiah']['repo']['repo_name'], repo_params)

        if self.config['gaiah']['commit']['process_commits']:
            self.process_commits()    

        logger.success("successfully!")
        
    def process_commits(self):
        self.commit.process_commits(branch_name=self.config['gaiah']['commit']['branch_name'])

    def init_local_repo(self, repo_dir, initial_commit=True):
        self.repo.init_local_repo(repo_dir, initial_commit)

    def create_remote_repo(self, repo_name, repo_params):
        logger.info(">>> リモートリポジトリを作成しています...")
        self.repo.create_remote_repo(repo_name, repo_params)
        
        logger.info(">>> ブランチを作成しています...")
        self.repo.create_branches()
        
        logger.info(">>> 初期ファイルを追加しています...")
        self.repo.add_initial_files()
        
        logger.info(">>> 初期ファイルをコミットしています...")
        self.repo.commit_initial_files()
        
        logger.info(">>> ブランチをマージしています...")
        self.repo.merge_branches()
        
        logger.info(">>> マージしたブランチをプッシュしています...")
        self.repo.push_merged_branches()
        
    def checkout_and_merge_branches(self):
        self.repo.merge_branches()
        
    def push(self):
        self.repo.push_merged_branches()
        