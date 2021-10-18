![GitHub Actions CI](https://github.com/itcrab/contributions-graph/actions/workflows/ci.yml/badge.svg)

# Contributions Graph
Copy meta-data of all your commits from any repositories outside GitHub to one repository on GitHub.
It's a simple way to build the right GitHub Contributions Graph.

# Goal idea
Developers doing jobs in different environments. Not each project is hosted on GitHub.<br />
Some projects can be hosted on some services like GitHub (eq: GitLab, Gogs, Gitea, etc).<br />
Contribution Graph is the solution for all projects outside GitHub.<br />
It copies all your commits from any repositories to one new repository.<br />
The new repository can be pushed to a new private repository on GitHub.<br />
This action will fix your contribution graph on GitHub.<br />

# Quick start
`$ git clone https://github.com/itcrab/contributions-graph.git`<br />
`$ cd contributions-graph`<br />
`$ cat app.py`
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
```
