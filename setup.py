from setuptools import setup, find_packages
from gaiah.version import __version__

# READMEファイルの内容を読み込む
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 依存関係を読み込む
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    # パッケージの名前
    name='gaiah',
    
    # パッケージのバージョン
    version=__version__,
    
    # パッケージに含めるモジュールを自動的に探す
    packages=find_packages(),
    
    # パッケージの分類情報
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control",
    ],
    
    # パッケージに含めるデータファイル
    package_data={
        'gaiah': ['README.md',
                  'requirements.txt'],
    },
    
    # PyPIに表示される長い説明文
    long_description=long_description,
    
    # 長い説明文のフォーマット
    long_description_content_type="text/markdown",
    
    # プロジェクトのURL
    url="https://github.com/your_username/gaiah",
    
    # パッケージのインストールに必要な依存関係
    install_requires=requirements,

    # エントリーポイントの設定
    entry_points={
        'console_scripts': [
            'gaiah=gaiah.cli:main',
        ],
    },
)