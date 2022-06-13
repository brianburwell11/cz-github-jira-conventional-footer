from os import path
from setuptools import setup
from yaml import full_load


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, ".cz.yaml"), "r") as f:
    try:
        config_values = full_load(f)
        __version__ = config_values["commitizen"]["version"]
    except:
        raise
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="cz_github_jira_conventional_footer",
    version=__version__,
    py_modules=["cz_github_jira_conventional_footer"],
    author="Brian Burwell",
    author_email="brianburwell11@gmail.com",
    license="MIT",
    url="https://github.com/brianburwell/cz-github-jira-conventional-footer",
    install_requires=["commitizen"],
    description="Extend the commitizen tools to create conventional commits and changelog that link to Jira and GitHub.",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
