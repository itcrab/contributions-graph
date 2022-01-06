import os.path
from typing import Optional, Dict

from contributions_graph.git import Git, GitRepositorySwitch
from contributions_graph.obfuscate import Obfuscate
from contributions_graph.repository_list import RepositoryList
from contributions_graph.typing import RepositoryCommitsTypeDict


class ContributionsGraph:
    def __init__(self, repository_list: RepositoryList, git: Git, obfuscate: Optional[Obfuscate] = None) -> None:
        self.repository_list = repository_list
        self.git = git
        self.obfuscate = obfuscate

    def run(self) -> None:
        all_commits = self.get_commits_from_repositories()
        all_commits = self.sort_commits(all_commits)

        if self.obfuscate:
            all_commits = self.obfuscate.run(all_commits)

        if self.git.repository_exists():
            all_commits = self.get_subtraction_commits(all_commits)

        self.build_repo(all_commits)

    def get_commits_from_repositories(self) -> dict[str, RepositoryCommitsTypeDict]:
        all_commits = {}
        for repository in self.repository_list:
            with GitRepositorySwitch(new_repo_path=repository['repo_path'], new_repo_branch=repository['branch']):
                commits = self.git.get_commits(author=repository['author'])

            repo_name = str(os.path.basename(repository['repo_path']))
            all_commits[repo_name] = RepositoryCommitsTypeDict(author=repository['author'], commits=commits)

        return all_commits

    def sort_commits(self, all_commits: Dict[str, RepositoryCommitsTypeDict]) -> Dict[str, RepositoryCommitsTypeDict]:
        for repo_name in all_commits.keys():
            all_commits[repo_name]['commits'] = list(set(all_commits[repo_name]['commits']))
            all_commits[repo_name]['commits'].sort()

        return all_commits

    def get_subtraction_commits(self, all_commits: Dict[str, RepositoryCommitsTypeDict]) -> \
            Dict[str, RepositoryCommitsTypeDict]:
        with GitRepositorySwitch(new_repo_path=self.git.new_repo_path, new_repo_branch=self.git.new_repo_branch):
            exists_commits = self.git.get_commits(author=self.git.new_repo_author)
        exists_commits.sort()

        for repo_name in all_commits:
            skip_commit_idxs = []
            for idx, commit in enumerate(all_commits[repo_name]['commits']):
                try:
                    commit_index = exists_commits.index(commit)
                except ValueError:
                    continue

                skip_commit_idxs.append(idx)
                del exists_commits[commit_index]

            if skip_commit_idxs:
                for idx in skip_commit_idxs[::-1]:
                    del all_commits[repo_name]['commits'][idx]

        return all_commits

    def build_repo(self, all_commits: Dict[str, RepositoryCommitsTypeDict]) -> None:
        self.git.create_repository()
        self.git.create_readme()
        self.git.build_repository(all_commits)
