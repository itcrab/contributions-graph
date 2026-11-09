import os
import subprocess
from datetime import datetime

from contributions_graph.exceptions import GitBranchNotFoundError


class GitConsole:
    def __init__(self, path: str) -> None:
        self.path = path

    def exec(self, cmd: str, env_override: dict | None = None):
        run_kwargs = {'shell': True}
        if env_override:
            run_kwargs['env'] = os.environ | env_override

        subprocess.run(f'cd {self.path} && git {cmd}', **run_kwargs)


class Git:
    def __init__(self, new_repo_path: str, new_repo_branch: str, new_repo_author: str) -> None:
        self.new_repo_path = new_repo_path
        self.new_repo_branch = new_repo_branch
        self.new_repo_author = new_repo_author

        self.current_path = os.getcwd()

    def get_commits(self, repo_path: str, branch: str, author: str) -> list[datetime]:
        os.chdir(repo_path)

        repo_branch = self.get_repo_branch()

        if repo_branch != branch:
            subprocess.run(f'git checkout {branch}', shell=True)

            selected_branch = self.get_repo_branch()
            if selected_branch != branch:
                raise GitBranchNotFoundError(
                    'Git branch "{}" not found!'.format(branch)
                )

        all_commits = self.get_all_commits(author)

        if repo_branch != branch:
            subprocess.run(f'git checkout {repo_branch}', shell=True)

        os.chdir(self.current_path)

        return all_commits

    def get_repo_branches(self) -> list[str]:
        cmd = 'git branch'
        repo_branches = subprocess.check_output(cmd, shell=True, universal_newlines=True)

        return repo_branches.splitlines()

    def get_repo_branch(self) -> str:
        repo_branches = self.get_repo_branches()

        repo_branch = [rb for rb in repo_branches if rb.startswith('* ')][0]
        repo_branch = repo_branch[2:]

        return repo_branch
