from contributions_graph import ContributionsGraph
from contributions_graph.git import Git
from contributions_graph.obfuscate import Obfuscate
from contributions_graph.repository_list import RepositoryList

repository_list = RepositoryList()
repository_list.add(
    repo_name='project_1',
    repo_path='/path/to/project_1',
    branch='master',
    author='Arcady Usov <arcady.usov@project1.com>',
)
repository_list.add(
    repo_name='project_2',
    repo_path='/path/to/project_2',
    branch='develop',
    author='Arcady Usov <arcady.usov@project2.com>',
)
repository_list.add(
    repo_name='project_3',
    repo_path='/path/to/project_3',
    branch='testing',
    author='Arcady Usov <arcady.usov@project3.com>',
)

git = Git(
    new_repo_path='/path/to/contributions_graph',
    new_repo_branch='master',
    new_repo_author='Arcady Usov <arcady.usov@email.com>',
)

obfuscate_enabled = False
obfuscate = None if not obfuscate_enabled else Obfuscate(
    start_hour=11,
    start_minute=0,
    start_second=0,
    delta_minutes=5,
)

if __name__ == '__main__':
    contributions_graph = ContributionsGraph(repository_list, git, obfuscate)
    contributions_graph.run()
