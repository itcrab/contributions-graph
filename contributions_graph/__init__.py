from collections import defaultdict
from datetime import datetime
from typing import Optional

from contributions_graph.git import Git
from contributions_graph.obfuscate import Obfuscate
from contributions_graph.repository_list import RepositoryList


class ContributionsGraph:
    def __init__(self, repository_list: RepositoryList, git: Git, obfuscate: Optional[Obfuscate] = None) -> None:
        self.repository_list = repository_list
        self.git = git
        self.obfuscate = obfuscate

    def run(self) -> None:
        all_commits = self.get_all_commits()
        all_commits = self.sort_commits(all_commits)

        if self.obfuscate:
            all_commits = self.obfuscate.run(all_commits)

        self.build_repo(all_commits)

    def get_all_commits(self) -> dict[str, list[datetime]]:
        all_commits = defaultdict(list)
        for repository in self.repository_list:
            commits = self.git.get_commits(
                repo_path=repository['repo_path'],
                branch=repository['branch'],
                author=repository['author'],
            )
            all_commits[repository['repo_name']].extend(commits)

        return all_commits

    def sort_commits(self, all_commits: dict[str, list[datetime]]) -> dict[str, list[datetime]]:
        for repo_name in all_commits:
            all_commits[repo_name] = list(set(all_commits[repo_name]))
            all_commits[repo_name].sort()

        return all_commits

    def get_subtraction_commits(self, all_commits: dict[str, list[datetime]]) -> dict[str, list[datetime]]:
        exists_commits = self.git.get_commits_exists()
        exists_commits = list(set(exists_commits))
        exists_commits.sort()

        if self.obfuscate:
            all_commits = self.obfuscate.run(all_commits)

        for repo_name in all_commits:
            all_commits[repo_name] = list(set(set(all_commits[repo_name]) - set(exists_commits)))
            all_commits[repo_name].sort()

        return all_commits

    def build_repo(self, all_commits: dict[str, list[datetime]]) -> None:
        if self.git.repository_exists():
            all_commits = self.get_subtraction_commits(all_commits)

        self.git.create_repository()
        self.git.create_readme()
        self.git.build_repository(all_commits)
