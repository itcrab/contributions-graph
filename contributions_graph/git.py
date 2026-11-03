import os
import subprocess
from datetime import datetime
from typing import List

from contributions_graph.exceptions import GitBranchNotFoundError
from contributions_graph.utils import write_file_data, parse_iso_8601_string_to_datetime


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
            subprocess.run(f'git checkout {branch}')

            selected_branch = self.get_repo_branch()
            if selected_branch != branch:
                raise GitBranchNotFoundError(
                    'Git branch "{}" not found!'.format(branch)
                )

        all_commits = self.get_all_commits(author)

        if repo_branch != branch:
            subprocess.run(f'git checkout {repo_branch}')

        os.chdir(self.current_path)

        return all_commits

    def get_repo_branches(self) -> List[str]:
        cmd = 'git branch'
        repo_branches = subprocess.check_output(cmd, shell=True, universal_newlines=True)

        return repo_branches.splitlines()

    def get_repo_branch(self) -> str:
        repo_branches = self.get_repo_branches()

        repo_branch = [rb for rb in repo_branches if rb.startswith('* ')][0]
        repo_branch = repo_branch[2:]

        return repo_branch

    def get_all_commits(self, author: str) -> List[datetime]:
        cmd = 'git --no-pager log --pretty="%cI" --author="{}"'.format(author)
        all_commits = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        all_commits_list = all_commits.splitlines()

        return list(map(parse_iso_8601_string_to_datetime, all_commits_list))

    def get_committers(self) -> List[str]:
        cmd = 'git --no-pager log --pretty="%cn <%ce>"'
        all_commits = subprocess.check_output(cmd, shell=True, universal_newlines=True)

        return all_commits.splitlines()

    def create_repository(self) -> None:
        if not os.path.isdir(self.new_repo_path):
            os.mkdir(self.new_repo_path)
        os.chdir(self.new_repo_path)
        if not self.repository_exists():
            repo_author = self.new_repo_author.split('<')

            subprocess.run('git init')
            subprocess.run(f'git config user.email "{repo_author[1][:-1]}"')
            subprocess.run(f'git config user.name "{repo_author[0]}"')

    def create_readme(self) -> None:
        file_name = 'README.md'
        if not os.path.isfile(file_name):
            file_data = '# Contribution Graph Repository'
            write_file_data(file_name, file_data)

            self.set_current_datetime(datetime.today())
            self.commit_file(file_name)

    def build_repository(self, all_commits: List[datetime]) -> None:
        if not os.path.isdir(self.file_dir):
            os.mkdir(self.file_dir)
        os.chdir(self.file_dir)

        for commit in all_commits:
            file_path = self.create_file(commit)
            self.set_current_datetime(commit)
            self.commit_file(file_path)

        os.chdir(self.current_path)

    def create_file(self, commit: datetime) -> str:
        dir_path = commit.strftime('%Y/%m')
        os.makedirs(dir_path, exist_ok=True)
        file_name = commit.strftime('%Y_%m_%d__%H_%M_%S')
        tz_str = commit.strftime('%z')
        tz_str_in_path = tz_str.replace('+', 'p').replace('-', 'm')
        file_path = f'{dir_path}/{file_name}__{tz_str_in_path}.{self.file_ext}'

        file_data = f'commit_datetime="{file_name}_{tz_str}"'
        write_file_data(file_path, file_data)

        return file_path

    def set_current_datetime(self, commit: datetime) -> None:
        date_string = commit.isoformat()
        os.environ['GIT_AUTHOR_DATE'] = date_string
        os.environ['GIT_COMMITTER_DATE'] = date_string

    def commit_file(self, file_name: str) -> None:
        subprocess.run(f'git add {file_name}')
        subprocess.run(f'git commit -m "Commit file {file_name}"')
