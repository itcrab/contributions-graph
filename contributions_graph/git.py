import os
import subprocess
from datetime import datetime
from typing import List, Dict

from contributions_graph.exceptions import GitBranchNotFoundError
from contributions_graph.typing import RepositoryCommitsTypedDict
from contributions_graph.utils import parse_iso_8601_string_to_datetime, write_file_data


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
    def get_commits_by_author(cls, author: str) -> List[str]:
        cmd = f'git --no-pager log --pretty="%cI" --author="{author}"'
        all_commits = subprocess.check_output(cmd, shell=True, universal_newlines=True)

        return all_commits.splitlines()

    @staticmethod
    def get_committers() -> List[str]:  # only for testing
        cmd = 'git --no-pager log --pretty="%cn <%ce>"'
        all_committers = subprocess.check_output(cmd, shell=True, universal_newlines=True)

        return all_committers.splitlines()


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


class Git:
    def __init__(self) -> None:
        self.base_path = os.getcwd()

    def repository_exists(self, new_repo_path) -> bool:
        return os.path.isdir(os.path.join(new_repo_path, '.git'))

    def get_commits(self, author: str) -> List[datetime]:
        all_commits = GitConsole.get_commits_by_author(author)

        return list(map(parse_iso_8601_string_to_datetime, all_commits))

    def create_repository(self, new_repo_path: str, new_repo_author: str, new_repo_branch: str) -> None:
        if not os.path.isdir(new_repo_path):
            os.mkdir(new_repo_path)

        os.chdir(new_repo_path)
        if not self.repository_exists(new_repo_path=new_repo_path):
            repo_author = new_repo_author.split('<')

            GitConsole.init_repo(email=repo_author[1][:-1], name=repo_author[0])
            GitConsole.create_branch(new_repo_branch)

    def create_readme(self) -> None:
        file_name = 'README.md'
        if os.path.isfile(file_name):
            return

        file_data = '# Contribution Graph Repository'
        write_file_data(file_name, file_data, file_mode='w')

        commit_datetime = datetime.today().isoformat()
        self.commit_file(commit_datetime, file_name)

    def build_repository(self, all_commits: Dict[str, RepositoryCommitsTypedDict]) -> None:
        for repo_name in all_commits.keys():
            file_ext = all_commits[repo_name]['file_ext']
            file_name = f'{repo_name}.{file_ext}'
            commit_author = all_commits[repo_name]['author']

            for commit in all_commits[repo_name]['commits']:
                commit_datetime = commit.isoformat()

                file_data = f'{commit_datetime}\t{commit_author}\n'
                write_file_data(file_name, file_data, file_mode='a')

                self.commit_file(commit_datetime, file_name)

    def commit_file(self, commit_datetime, file_name):
        GitConsole.set_current_datetime(commit_datetime)
        GitConsole.add_file(file_name)
        GitConsole.commit_file(file_name, commit_datetime)
