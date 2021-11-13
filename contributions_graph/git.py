import os
import subprocess
from datetime import datetime
from typing import List

from contributions_graph.exceptions import GitBranchNotFoundError
from contributions_graph.utils import generate_full_file_name, write_file_data, parse_iso_8601_string_to_datetime


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
    def commit_file(cls, file_name: str) -> None:
        os.system(f'git commit -m "Commit file {file_name}"')

    @classmethod
    def set_current_datetime(cls, date_string: str) -> None:
        os.environ['GIT_AUTHOR_DATE'] = date_string
        os.environ['GIT_COMMITTER_DATE'] = date_string

    @staticmethod
    def get_branches() -> List[str]:
        cmd = 'git branch'
        repo_branches = subprocess.check_output(cmd, shell=True, universal_newlines=True)

        return repo_branches.splitlines()

    @classmethod
    def get_commits_by_author(cls, author: str) -> List[str]:
        cmd = f'git --no-pager log --pretty="%cI" --author="{author}"'
        all_commits = subprocess.check_output(cmd, shell=True, universal_newlines=True)

        return all_commits.splitlines()

    @staticmethod
    def get_committers() -> List[str]:  # only for testing
        cmd = 'git --no-pager log --pretty="%cn <%ce>"'
        all_committers = subprocess.check_output(cmd, shell=True, universal_newlines=True)

        return all_committers.splitlines()


class Git:
    def __init__(self, new_repo_path: str, new_repo_branch: str, new_repo_author: str, file_dir: str, file_ext: str) -> None:
        self.new_repo_path = new_repo_path
        self.new_repo_branch = new_repo_branch
        self.new_repo_author = new_repo_author

        self.file_dir = file_dir
        self.file_ext = file_ext

        self.current_path = os.getcwd()

    def repository_exists(self) -> bool:
        return os.path.isdir(os.path.join(self.new_repo_path, '.git'))

    def get_commits_exists(self) -> List[datetime]:
        return self.get_commits(
            repo_path=self.new_repo_path,
            branch=self.new_repo_branch,
            author=self.new_repo_author,
        )

    def get_commits(self, repo_path: str, branch: str, author: str) -> List[datetime]:
        os.chdir(repo_path)

        repo_branch = self.get_repo_branch()

        if repo_branch != branch:
            GitConsole.switch_branch(branch)

            selected_branch = self.get_repo_branch()
            if selected_branch != branch:
                raise GitBranchNotFoundError(
                    'Git branch "{}" not found!'.format(branch)
                )

        all_commits = self.get_all_commits(author)

        if repo_branch != branch:
            GitConsole.switch_branch(branch)

        os.chdir(self.current_path)

        return all_commits

    def get_repo_branch(self) -> str:
        repo_branches = GitConsole.get_branches()

        repo_branch = [rb for rb in repo_branches if rb.startswith('* ')][0]
        repo_branch = repo_branch[2:]

        return repo_branch

    def get_all_commits(self, author: str) -> List[datetime]:
        all_commits = GitConsole.get_commits_by_author(author)

        return list(map(parse_iso_8601_string_to_datetime, all_commits))

    def create_repository(self) -> None:
        if not os.path.isdir(self.new_repo_path):
            os.mkdir(self.new_repo_path)

        os.chdir(self.new_repo_path)
        if not self.repository_exists():
            repo_author = self.new_repo_author.split('<')

            GitConsole.init_repo(email=repo_author[1][:-1], name=repo_author[0])
            GitConsole.create_branch(self.new_repo_branch)

    def create_readme(self) -> None:
        file_name = 'README.md'
        if not os.path.isfile(file_name):
            file_data = '# Contribution Graph Repository'
            write_file_data(file_name, file_data)

            GitConsole.set_current_datetime(datetime.today().isoformat())
            GitConsole.add_file(file_name)
            GitConsole.commit_file(file_name)

    def build_repository(self, all_commits: List[datetime]) -> None:
        if not os.path.isdir(self.file_dir):
            os.mkdir(self.file_dir)
        os.chdir(self.file_dir)

        for commit in all_commits:
            date_string = commit.isoformat()

            file_name = self.create_file(date_string)
            GitConsole.set_current_datetime(date_string)
            GitConsole.add_file(file_name)
            GitConsole.commit_file(file_name)

        os.chdir(self.current_path)

    def create_file(self, date_string: str) -> str:
        file_name = generate_full_file_name(self.file_ext)
        file_data = 'commit_datetime="{}"'.format(date_string)
        write_file_data(file_name, file_data)

        return file_name
