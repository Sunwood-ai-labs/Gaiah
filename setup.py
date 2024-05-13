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

def get_requirements():
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
        return requirements

setup(
    # name='gaiah_toolkit',
    name='gaiah',
    version=get_version(),
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control",
    ],
    package_data={
        'gaiah': ['README.md',
                  'requirements.txt'],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/gaiah",
    # install_requires=requirements,
    # install_requires=get_requirements(),
    install_requires=[
            'gitpython',
            'python-dotenv',
            'PyGithub',
            'termcolor',
            'art',
        ],
    entry_points={
        'console_scripts': [
            'gaiah=gaiah.cli:main',
        ],
    },
)