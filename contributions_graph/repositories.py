import os
from datetime import datetime
from typing import List, Dict, Iterator

from contributions_graph.git import GitConsole, GitRepositorySwitch
from contributions_graph.typing import RepositoryCommitsTypedDict
from contributions_graph.utils import write_file_data, repository_exists


class ExportRepositories:
    def __init__(self) -> None:
        self._repositories: List[Dict[str, str]] = []
        self._position = 0
        self._max_position = 0

    def __next__(self) -> dict:
        if self._position == self._max_position:
            raise StopIteration

        repository = self._repositories[self._position]
        self._position += 1

        return repository

    def __iter__(self) -> Iterator[dict]:
        return self

    def add(self, repo_path: str, branch: str, author: str, file_ext: str) -> None:
        self._repositories.append(dict(
            repo_path=repo_path,
            branch=branch,
            author=author,
            file_ext=file_ext,
        ))
        self._max_position += 1

    def get_export_commits(self):
        export_commits = self._get_commits_from_repositories()
        export_commits = self._sort_commits(export_commits)

        return export_commits

    def _get_commits_from_repositories(self) -> Dict[str, RepositoryCommitsTypedDict]:
        export_commits = {}
        for repository in self:
            with GitRepositorySwitch(new_repo_path=repository['repo_path'], new_repo_branch=repository['branch']):
                commits = GitConsole.get_commits_by_author(author=repository['author'])

            repo_name = str(os.path.basename(repository['repo_path']))
            export_commits[repo_name] = RepositoryCommitsTypedDict(
                author=repository['author'],
                file_ext=repository['file_ext'],
                commits=commits,
            )

        return export_commits

    def _sort_commits(self, export_commits: Dict[str, RepositoryCommitsTypedDict]) -> Dict[str, RepositoryCommitsTypedDict]:
        for repo_name in export_commits.keys():
            export_commits[repo_name]['commits'] = list(set(export_commits[repo_name]['commits']))
            export_commits[repo_name]['commits'].sort()

        return export_commits


class ImportRepository:
    def __init__(self, repo_path: str, repo_branch: str, repo_author: str) -> None:
        self.repository = dict(
            repo_path=repo_path,
            repo_branch=repo_branch,
            repo_author=repo_author,
        )

    def build_repository(self, export_commits: Dict[str, RepositoryCommitsTypedDict]) -> None:
        if repository_exists(repo_path=self.repository['repo_path']):
            export_commits = self._get_subtraction_commits(export_commits)

        self._create_repository()
        self._create_readme()
        self._apply_export_commits(export_commits)

    def _get_subtraction_commits(self, export_commits: Dict[str, RepositoryCommitsTypedDict]) -> \
            Dict[str, RepositoryCommitsTypedDict]:
        with GitRepositorySwitch(new_repo_path=self.repository['repo_path'], new_repo_branch=self.repository['repo_branch']):
            exists_commits = GitConsole.get_commits_by_author(author=self.repository['repo_author'])
        exists_commits.sort()

        for repo_name in export_commits:
            if not exists_commits:
                break

            skip_commit_idxs = []
            for idx, commit in enumerate(export_commits[repo_name]['commits']):
                try:
                    commit_index = exists_commits.index(commit)
                except ValueError:
                    continue

                skip_commit_idxs.append(idx)
                del exists_commits[commit_index]

            if skip_commit_idxs:
                for idx in skip_commit_idxs[::-1]:
                    del export_commits[repo_name]['commits'][idx]

        return export_commits

    def _create_repository(self) -> None:
        if not os.path.isdir(self.repository['repo_path']):
            os.mkdir(self.repository['repo_path'])

        os.chdir(self.repository['repo_path'])
        if not repository_exists(repo_path=self.repository['repo_path']):
            repo_author = self.repository['repo_author'].split('<')

            GitConsole.init_repo(email=repo_author[1][:-1], name=repo_author[0])
            GitConsole.create_branch(self.repository['repo_branch'])

    def _create_readme(self) -> None:
        file_name = 'README.md'
        if os.path.isfile(file_name):
            return

        file_data = '# Contribution Graph Repository'
        write_file_data(file_name, file_data, file_mode='w')

        commit_datetime = datetime.today().isoformat()
        self._commit_file(commit_datetime, file_name)

    def _apply_export_commits(self, export_commits: Dict[str, RepositoryCommitsTypedDict]) -> None:
        for repo_name in export_commits.keys():
            file_ext = export_commits[repo_name]['file_ext']
            file_name = f'{repo_name}.{file_ext}'
            commit_author = export_commits[repo_name]['author']

            for commit in export_commits[repo_name]['commits']:
                commit_datetime = commit.isoformat()

                file_data = f'{commit_datetime}\t{commit_author}\n'
                write_file_data(file_name, file_data, file_mode='a')

                self._commit_file(commit_datetime, file_name)

    def _commit_file(self, commit_datetime, file_name):
        GitConsole.set_current_datetime(commit_datetime)
        GitConsole.add_file(file_name)
        GitConsole.commit_file(file_name, commit_datetime)
