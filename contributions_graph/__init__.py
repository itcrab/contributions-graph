from typing import Optional

from contributions_graph.obfuscate import Obfuscate
from contributions_graph.repositories import ExportRepositories, ImportRepository
from contributions_graph.typing import RepositoryCommitsTypedDict
from contributions_graph.utils import repository_exists


class ContributionsGraph:
    def __init__(self, export_repositories: ExportRepositories, import_repository: ImportRepository,
                 obfuscate: Optional[Obfuscate] = None) -> None:
        self.export_repositories = export_repositories
        self.import_repository = import_repository
        self.obfuscate = obfuscate

    def run(self) -> None:
        export_commits = self.export_repositories.get_export_commits()

        if self.obfuscate:
            export_commits = self.obfuscate.run(export_commits)

        self.import_repository.build_repository(export_commits)
