import os
from github import Github, GithubException
from dotenv import load_dotenv
from loguru import logger
import time
from .utils import run_command, tqdm_sleep

def get_remote_repo(repo_name):
    load_dotenv()
    access_token = os.getenv("GITHUB_ACCESS_TOKEN")
    g = Github(access_token)
    
    repo = g.get_user().get_repo(repo_name)
    logger.warning(f"Repository {repo_name} get.")
    return repo

def create_remote_repo(repo_name, repo_params, debug=True):
    """
    新しいリポジトリをGitHub上に作成する
    """
    load_dotenv()
    access_token = os.getenv("GITHUB_ACCESS_TOKEN")
    g = Github(access_token)

    try:
        # リポジトリが存在するかどうかを確認する
        repo = get_remote_repo(repo_name)
        logger.warning(f"Repository {repo_name} already exists.")
        
        if debug:
            # debugモードの場合、リポジトリを削除する
            repo.delete()
            logger.warning(f"Repository {repo_name} deleted in debug mode.")
            tqdm_sleep(10)
        else:
            # debugモードでない場合、既存のリポジトリを返す
            return repo
        
    except GithubException as e:
        if e.status == 404:
            # リポジトリが存在しない場合は新しいリポジトリを作成する
            try:
                repo = g.get_user().create_repo(repo_name, **repo_params)
                logger.success(f"Successfully created repository: {repo_name}")
                tqdm_sleep(10)
            except GithubException as e:
                logger.error(f"Error while creating repository: {repo_name} - {e}")
        else:
            logger.error(f"Error while checking repository existence: {repo_name} - {e}")
            return None