import os
from datetime import datetime
from typing import Dict

from contributions_graph.git import GitConsole
from contributions_graph.typing import RepositoryCommitsTypedDict
from contributions_graph.utils import write_file_data, repository_exists


class ImportRepository:
    def __init__(self, repo_path: str, repo_branch: str, repo_author: str) -> None:
        self.repository = dict(
            repo_path=repo_path,
            repo_branch=repo_branch,
            repo_author=repo_author,
        )

    def build_repository(self, all_commits: Dict[str, RepositoryCommitsTypedDict]) -> None:
        self._create_repository()
        self._create_readme()
        self._apply_all_commits(all_commits)

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

    def _apply_all_commits(self, all_commits: Dict[str, RepositoryCommitsTypedDict]) -> None:
        for repo_name in all_commits.keys():
            file_ext = all_commits[repo_name]['file_ext']
            file_name = f'{repo_name}.{file_ext}'
            commit_author = all_commits[repo_name]['author']

            for commit in all_commits[repo_name]['commits']:
                commit_datetime = commit.isoformat()

                file_data = f'{commit_datetime}\t{commit_author}\n'
                write_file_data(file_name, file_data, file_mode='a')

                self._commit_file(commit_datetime, file_name)

    def _commit_file(self, commit_datetime, file_name):
        GitConsole.set_current_datetime(commit_datetime)
        GitConsole.add_file(file_name)
        GitConsole.commit_file(file_name, commit_datetime)
