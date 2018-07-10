from contributions_graph import ContributionsGraph
from contributions_graph.git import Git
from contributions_graph.obfuscate import Obfuscate
from contributions_graph.repository_list import RepositoryList

repository_list = RepositoryList()
repository_list.add(
    repo_path='/home/arcady/projects/project_1',
    branch='master',
    author='Arcady Usov <arcady.usov@example.email.com>',
)
repository_list.add(
    repo_path='/home/arcady/projects/project_2',
    branch='develop',
    author='Arcady Usov <arcady.usov@example.email.com>',
)
repository_list.add(
    repo_path='/home/arcady/projects/project_3',
    branch='testing',
    author='Arcady Usov <arcady.usov@example.email.com>',
)

git = Git(
    new_repo_path='/home/arcady/projects/contributions_graph',
    new_repo_branch='master',
    new_repo_author='Arcady Usov <arcady.usov@example.email.com>',
    file_dir='all_commits',
    file_ext='py',
)
obfuscate = Obfuscate(
    start_hour=11,
    start_minute=0,
    start_second=0,
    delta_minutes=5,
)


if __name__ == '__main__':
    contributions_graph = ContributionsGraph(repository_list, git, obfuscate)
    contributions_graph.run()
