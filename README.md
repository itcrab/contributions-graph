[![codecov](https://codecov.io/gh/itcrab/contributions-graph/branch/master/graph/badge.svg)](https://codecov.io/gh/itcrab/contributions-graph)

# Contributions Graph
Move all your commits from any repositories to one repository. It's simple way build and save right GitHub Contributions Graph.

# Goal idea
Developers works with many projects on some services like GitHub (eq: GitLab, Gogs, etc).<br />
But many developers loves GitHub and want see GitHub Contributions Graph is correct and saved.<br />
For projects places on GitHub we don't have problems with build and save right GitHub Contributions Graph.<br />
Suddenly projects on GitHub maybe lost - customer give you permissions for working with repository, then delete this permitions (you done good job) and at one moment customer decides to remove this repository... Your amazing GitHub Contributions Graph in one second was be so bad.<br />
But for all projects located outside GitHub we don't see GitHub Contributions Graph but we worked on projects and every day try do good job for done all tasks for customers.<br />
We must fix it! And we have solution for this!

# Features
- [x] merge all commits from your project repositories to one repository
- [x] enable or disable obfuscate feature for datetime commits data (samples in `app.py` and `app_obfuscate.py`)

# Quick start
`$ git clone https://github.com/itcrab/contributions-graph.git`<br />
`$ cd contributions-graph`<br />
`$ cat app.py`
```python
from contributions_graph import ContributionsGraph
from contributions_graph.git import Git
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


if __name__ == '__main__':
    contributions_graph = ContributionsGraph(repository_list, git)
    contributions_graph.run()
```
`$ cat app_obfuscate.py`
```python
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
```
