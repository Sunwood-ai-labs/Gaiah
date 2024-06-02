from setuptools import setup, find_packages
import re

def get_version():
    with open("gaiah/__init__.py", "r") as f:
        content = f.read()
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.MULTILINE)
        if version_match:
            return version_match.group(1)
        else:
            raise RuntimeError("Unable to find version string.")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='gaiah_toolkit',
    version=get_version(),
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control",
    ],
    package_data={
        'gaiah': ['README.md',
                  'requirements.txt',
                  'template/*'], 
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/gaiah",
    install_requires=[
            'gitpython',
            'python-dotenv',
            'PyGithub',
            'termcolor',
            'art',
            'pyyaml',
        ],
    entry_points={
        'console_scripts': [
            'gaiah=gaiah.cli:main',
        ],
    },
)