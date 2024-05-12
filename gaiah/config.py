import os

# デフォルトの設定値
DEFAULT_CONFIG = {
    'repo_dir': '',
    'commit_messages_path': 'tmp2.md',
}

# 設定ファイルのパス
CONFIG_FILE = 'gaiah.conf'

def load_config():
    config = DEFAULT_CONFIG.copy()
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    return config