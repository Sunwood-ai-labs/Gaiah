import argparse
from art import tprint
from loguru import logger
from gaiah.gaiah import Gaiah
import sys
import os
import yaml
import shutil

logger.configure(
    handlers=[
        {
            "sink": sys.stderr,
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level:<8}</level> | <cyan>{name:<45}:{line:<5}</cyan> | <level>{message}</level>",
            "colorize": True,
        }
    ]
)

def parse_arguments():
    """
    コマンドライン引数を解析する
    """
    parser = argparse.ArgumentParser(description='Gaiah - シンプルなGitリポジトリ管理ツール')
    
    parser.add_argument('--config', default='.gaiah/config.yml', help='設定ファイルのパス')
    parser.add_argument('--mode', default='commit', help='処理モード')
    return parser.parse_args()

def load_config(config_path):
    """
    設定ファイルを読み込む
    """
    if not os.path.exists(config_path):
        # 設定ファイルが存在しない場合はテンプレートをコピー
        template_path = os.path.join(os.path.dirname(__file__), 'template', 'config.example.yml')
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        shutil.copyfile(template_path, config_path)
        logger.info(f"設定ファイルが存在しないため、テンプレートをコピーしました: {config_path}")

    with open(config_path, 'r', encoding="utf8") as f:
        config = yaml.safe_load(f)
        
    return config

def merge_configs(base_config, override_config):
    merged_config = base_config.copy()
    for key, value in override_config.items():
        if isinstance(value, dict):
            merged_config[key] = merge_configs(merged_config.get(key, {}), value)
        else:
            merged_config[key] = value
    return merged_config

def main():
    args = parse_arguments()
    gaiah_config = load_config(args.config)
    tprint("!   Welcome  to  Gaiah   !")
        
    if(args.mode == "make"):
        logger.info("mode is << make >>")
        gaiah_config["gaiah"] = merge_configs(gaiah_config["gaiah"], gaiah_config["gaiah"]["init"])
        gaiah = Gaiah(gaiah_config)
        gaiah.run()
        
    if(args.mode == "commit"):
        logger.info("mode is << commit >>")
        gaiah_config["gaiah"] = merge_configs(gaiah_config["gaiah"], gaiah_config["gaiah"]["dev"])
        gaiah = Gaiah(gaiah_config)
        gaiah.run()

if __name__ == "__main__":
    main()