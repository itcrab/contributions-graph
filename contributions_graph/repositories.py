import os
import subprocess
from typing import Generator, Iterator

from contributions_graph.git import GitConsole


class ExportRepository:
    def __init__(self, name: str, path: str, branch: str, author: str):
        self.name = name
        self.path = path
        self.branch = branch
        self.author = author

    def get_commits(self) -> Generator[str]:
        cmd = f'cd {self.path} && git --no-pager log --pretty="%cI" --author="{self.author}"'
        all_commits = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        for commit_dt in all_commits.splitlines():
            yield commit_dt


class ExportRepositories:
    def __init__(self):
        self._repositories: list[ExportRepository] = []
        self._position = 0
        self._max_position = 0

    def __next__(self) -> ExportRepository:
        if self._position == self._max_position:
            raise StopIteration

        repository = self._repositories[self._position]
        self._position += 1

        return repository

    def __iter__(self) -> Iterator[ExportRepository]:
        return self

    def add(self, name: str, path: str, branch: str, author: str):
        self._repositories.append(ExportRepository(
            name=name,
            path=path,
            branch=branch,
            author=author,
        ))
        self._max_position += 1


class ImportRepository:
    def __init__(self, path: str, branch: str, author: str) -> None:
        self.path = path
        self.branch = branch
        self.author = author

        self.git_console = GitConsole(
            path=self.path,
        )

    def create(self) -> None:
        if not os.path.isdir(self.path):
            os.mkdir(self.path)

        if not os.path.isdir(os.path.join(self.path, '.git')):
            author_split = self.author.split('<')
            repo_user_name = author_split[0]
            repo_user_email = author_split[1][:-1]

            self.git_console.exec('init')
            self.git_console.exec(f'config user.name "{repo_user_name}"')
            self.git_console.exec(f'config user.email "{repo_user_email}"')

            readme_file_name = f'{self.path}/README.md'
            if not os.path.isfile(readme_file_name):
                readme_content = '# Contribution Graph Repository\n\n'
                with open(readme_file_name, 'w') as f:
                    f.write(readme_content)

            self.git_console.exec(f'add {readme_file_name}')
            self.git_console.exec(f'commit -m "Initial commit: add file {readme_file_name}"')

    def get_commits(self) -> set[str]:
        cmd = f'cd {self.path} && git --no-pager log --pretty="%cI" --author="{self.author}"'
        all_commits = subprocess.check_output(cmd, shell=True, universal_newlines=True)

        return set(all_commits.splitlines())

    def create_commit(self, commit_dt: str, repo_name: str) -> None:
        commit_year = commit_dt[:4]
        commit_month = commit_dt[5:7]

        dir_path = f'{self.path}/{repo_name}/{commit_year}/{commit_month}'
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path, exist_ok=True)

        replace_map = str.maketrans({  # 2026-11-08T12:24:59+02:00
            '-': '_',
            'T': '__',
            ':': '_',
            '+': '__',
        })
        commit_dt_name = commit_dt.translate(replace_map)
        file_name = f'{commit_dt_name}.commit'
        file_path = f'{dir_path}/{file_name}'
        with open(file_path, 'w') as f:
            f.write(commit_dt)

        git_date_override_vars = {
            'GIT_AUTHOR_DATE': commit_dt,
            'GIT_COMMITTER_DATE': commit_dt,
        }

        self.git_console.exec(f'add {file_path}', env_override=git_date_override_vars)
        self.git_console.exec(f'commit -m "Commit file {file_name}"', env_override=git_date_override_vars)
