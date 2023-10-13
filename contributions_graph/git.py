import os
import subprocess
from datetime import datetime
from typing import List

from contributions_graph.exceptions import GitBranchNotFoundError
from contributions_graph.utils import parse_iso_8601_string_to_datetime


class GitConsole:
    @classmethod
    def init_repo(cls, email: str, name: str) -> None:
        os.system('git init')
        os.system(f'git config user.email "{email}"')
        os.system(f'git config user.name "{name}"')

    @staticmethod
    def create_branch(branch: str) -> None:
        os.system(f'git checkout -b {branch}')

    @staticmethod
    def switch_branch(branch: str) -> None:
        os.system(f'git checkout {branch}')

    @classmethod
    def add_file(cls, file_name: str) -> None:
        os.system(f'git add {file_name}')

    @classmethod
    def commit_file(cls, file_name: str, commit_datetime: str) -> None:
        os.system(f'git commit -m "Commit file {file_name} by datetime {commit_datetime}"')

    @classmethod
    def set_current_datetime(cls, date_string: str) -> None:
        os.environ['GIT_AUTHOR_DATE'] = date_string
        os.environ['GIT_COMMITTER_DATE'] = date_string

    @staticmethod
    def get_current_branch() -> str:
        cmd = 'git branch --show-current'
        current_branch = subprocess.check_output(cmd, shell=True, universal_newlines=True)

        return current_branch.strip()

    @classmethod
    def get_commits_by_author(cls, author: str) -> List[datetime]:
        cmd = f'git --no-pager log --pretty="%cI" --author="{author}"'
        export_commits = subprocess.check_output(cmd, shell=True, universal_newlines=True).splitlines()

        return list(map(parse_iso_8601_string_to_datetime, export_commits))

    @staticmethod
    def get_committers() -> List[str]:  # only for testing
        cmd = 'git --no-pager log --pretty="%cn <%ce>"'
        committers = subprocess.check_output(cmd, shell=True, universal_newlines=True)

        return committers.splitlines()


class GitRepositorySwitch:
    def __init__(self, new_repo_path: str, new_repo_branch: str) -> None:
        self.new_repo_path = new_repo_path
        self.new_repo_branch = new_repo_branch

        self.base_branch = 'master'
        self.base_path = os.getcwd()

    def __enter__(self) -> None:
        os.chdir(self.new_repo_path)

        self.base_branch = GitConsole.get_current_branch()
        if self.base_branch != self.new_repo_branch:
            GitConsole.switch_branch(self.new_repo_branch)

            selected_branch = GitConsole.get_current_branch()
            if selected_branch != self.new_repo_branch:
                raise GitBranchNotFoundError(f'Git branch "{self.new_repo_branch}" not found!')

    def __exit__(self, *exc) -> None:
        selected_branch = GitConsole.get_current_branch()
        if self.base_branch != selected_branch:
            GitConsole.switch_branch(self.base_branch)

        os.chdir(self.base_path)
