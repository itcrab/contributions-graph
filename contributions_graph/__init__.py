from typing import Optional

from contributions_graph.git import Git
from contributions_graph.obfuscate import Obfuscate
from contributions_graph.repositories import ImportRepository, ExportRepositories


class ContributionsGraph:
    def __init__(self, export_repositories: ExportRepositories, import_repository: ImportRepository, obfuscate: Optional[Obfuscate] = None) -> None:
        self.import_repository = import_repository
        self.export_repositories = export_repositories

        self.obfuscate = obfuscate

    def run(self) -> None:
        self.import_repository.create()

        import_commits = self.import_repository.get_commits()
        for export_repository in self.export_repositories:
            for commit_dt in export_repository.get_commits():
                if commit_dt in import_commits:
                    continue

                # if self.obfuscate:
                #     all_commits = self.obfuscate.run(all_commits)

                self.import_repository.create_commit(commit_dt, export_repository.name)
