import os
from github import Github
from dotenv import load_dotenv
from loguru import logger

def create_remote_repo(repo_name, repo_params):
    """
    新しいリポジトリをGitHub上に作成する
    """
    load_dotenv()
    access_token = os.getenv("GITHUB_ACCESS_TOKEN")
    g = Github(access_token)

    try:
        repo = g.get_user().create_repo(repo_name, **repo_params)
        logger.success(f"Successfully created repository: {repo_name}")
        return repo
    except Exception as e:
        logger.error(f"Error while creating repository: {repo_name} - {e}")
        raise