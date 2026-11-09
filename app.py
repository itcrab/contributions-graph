from contributions_graph import ContributionsGraph
from contributions_graph.obfuscate import Obfuscate
from contributions_graph.repositories import ExportRepositories, ImportRepository

export_repositories = ExportRepositories()
export_repositories.add(
    name='project_1',
    path='/path/to/project_1',
    branch='master',
    author='Arcady Usov <arcady.usov@project1.com>',
)
export_repositories.add(
    name='project_2',
    path='/path/to/project_2',
    branch='develop',
    author='Arcady Usov <arcady.usov@project2.com>',
)
export_repositories.add(
    name='project_3',
    path='/path/to/project_3',
    branch='testing',
    author='Arcady Usov <arcady.usov@project3.com>',
)

import_repository = ImportRepository(
    path='/path/to/contributions_graph',
    branch='master',
    author='Arcady Usov <arcady.usov@email.com>',
)

obfuscate_enabled = False
obfuscate = None if not obfuscate_enabled else Obfuscate(
    start_hour=11,
    start_minute=0,
    start_second=0,
    delta_minutes=5,
)

if __name__ == '__main__':
    contributions_graph = ContributionsGraph(export_repositories, import_repository, obfuscate)
    contributions_graph.run()
