import subprocess
from loguru import logger
import time
from tqdm import tqdm


def run_command(command, cwd=None, check=True):
    """
    コマンドを実行し、結果を返す
    """
    try:
        logger.info(f"実行コマンド： {' '.join(command)}")
        result = subprocess.run(command, cwd=cwd, check=check, capture_output=True, text=True, encoding='utf-8')
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip()
        logger.error(f"Error while running command: {' '.join(command)}")
        logger.error(f"Error message: {error_message}")
        raise

def tqdm_sleep(n):
    for _ in tqdm(range(n)):
        time.sleep(1)