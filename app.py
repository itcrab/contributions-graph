from contributions_graph import ContributionsGraph
from contributions_graph.git import Git
from contributions_graph.obfuscate import Obfuscate
from contributions_graph.repositories import ImportRepository
from contributions_graph.repository_list import RepositoryList

repository_list = RepositoryList()
repository_list.export_from(
    repo_path='/home/arcady/projects/project_1',
    branch='master',
    author='Arcady Usov <arcady.usov@example.email.com>',
    file_ext='py',
)
repository_list.export_from(
    repo_path='/home/arcady/projects/project_2',
    branch='develop',
    author='Arcady Usov <arcady.usov@example.email.com>',
    file_ext='py',
)
repository_list.export_from(
    repo_path='/home/arcady/projects/project_3',
    branch='testing',
    author='Arcady Usov <arcady.usov@example.email.com>',
    file_ext='py',
)

git = Git()
import_repository = ImportRepository(
    git=git,
    repo_path='D:\\Contribute\\contributions-graph\\git_repositories\\contributions_graph\\',
    repo_branch='master',
    repo_author='Arcady Usov <itcrab@gmail.com>',
)

obfuscate_enabled = False
obfuscate = None if not obfuscate_enabled else Obfuscate(
    start_hour=11,
    start_minute=0,
    start_second=0,
    delta_minutes=5,
)

if __name__ == '__main__':
    contributions_graph = ContributionsGraph(repository_list, import_repository, git, obfuscate)
    contributions_graph.run()
