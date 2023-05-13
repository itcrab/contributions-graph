import os.path
from typing import Optional, Dict

from contributions_graph.git import Git, GitRepositorySwitch
from contributions_graph.obfuscate import Obfuscate
from contributions_graph.repositories import ImportRepository
from contributions_graph.repository_list import RepositoryList
from contributions_graph.typing import RepositoryCommitsTypedDict
from contributions_graph.utils import repository_exists


class ContributionsGraph:
    def __init__(self, repository_list: RepositoryList, import_repository: ImportRepository, git: Git,
                 obfuscate: Optional[Obfuscate] = None) -> None:
        self.repository_list = repository_list
        self.import_repository = import_repository
        self.git = git
        self.obfuscate = obfuscate

    def run(self) -> None:
        all_commits = self.get_commits_from_repositories()
        all_commits = self.sort_commits(all_commits)

        if self.obfuscate:
            all_commits = self.obfuscate.run(all_commits)

        if repository_exists(repo_path=self.import_repository.repository['repo_path']):
            all_commits = self.get_subtraction_commits(all_commits)

        self.import_repository.build_repository(all_commits)

    def get_commits_from_repositories(self) -> Dict[str, RepositoryCommitsTypedDict]:
        all_commits = {}
        for repository in self.repository_list:
            with GitRepositorySwitch(new_repo_path=repository['repo_path'], new_repo_branch=repository['branch']):
                commits = self.git.get_commits(author=repository['author'])

            repo_name = str(os.path.basename(repository['repo_path']))
            all_commits[repo_name] = RepositoryCommitsTypedDict(
                author=repository['author'],
                file_ext=repository['file_ext'],
                commits=commits,
            )

        return all_commits

    def sort_commits(self, all_commits: Dict[str, RepositoryCommitsTypedDict]) -> Dict[str, RepositoryCommitsTypedDict]:
        for repo_name in all_commits.keys():
            all_commits[repo_name]['commits'] = list(set(all_commits[repo_name]['commits']))
            all_commits[repo_name]['commits'].sort()

        return all_commits

    def get_subtraction_commits(self, all_commits: Dict[str, RepositoryCommitsTypedDict]) -> \
            Dict[str, RepositoryCommitsTypedDict]:
        new_repo = self.import_repository.repository
        with GitRepositorySwitch(new_repo_path=new_repo['repo_path'], new_repo_branch=new_repo['repo_branch']):
            exists_commits = self.git.get_commits(author=self.import_repository.repository['repo_author'])
        exists_commits.sort()

        for repo_name in all_commits:
            if not exists_commits:
                break

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
