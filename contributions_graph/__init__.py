from datetime import datetime
from typing import Optional, List

from contributions_graph.git import Git
from contributions_graph.obfuscate import Obfuscate
from contributions_graph.repository_list import RepositoryList
from contributions_graph.utils import parse_iso_8601_string_to_datetime


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

    def get_all_commits(self) -> List[datetime]:
        all_commits = []
        for repository in self.repository_list:
            commits = self.git.get_commits(
                repo_path=repository['repo_path'],
                branch=repository['branch'],
                author=repository['author'],
            )
            all_commits.extend(commits)

        return all_commits

    def sort_commits(self, all_commits: List[datetime]) -> List[datetime]:
        all_commits = list(set(all_commits))
        all_commits.sort()

        return all_commits

    def get_subtraction_commits(self, all_commits: List[datetime]) -> List[datetime]:
        exists_commits = self.git.get_commits_exists()
        exists_commits = self.sort_commits(exists_commits)

        if self.obfuscate:
            all_commits = self.obfuscate.run(all_commits)

        all_commits = list(set(set(all_commits) - set(exists_commits)))
        all_commits.sort()

        return all_commits

    def build_repo(self, all_commits: List[datetime]) -> None:
        if self.git.repository_exists():
            all_commits = self.get_subtraction_commits(all_commits)

        self.git.create_repository()
        self.git.create_readme()
        self.git.build_repository(all_commits)
