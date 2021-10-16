![GitHub Actions CI](https://github.com/itcrab/contributions-graph/actions/workflows/ci.yml/badge.svg)

# Contributions Graph
Move all your commits from any repositories to one repository. It's simple way build and save right GitHub Contributions Graph.

# Goal idea
Developers works with many projects hosted sources on some services like GitHub (eq: GitLab, Gogs, etc).<br />
But many developers loves GitHub and want see all works in GitHub Contributions Graph.<br />
For projects hosted on GitHub we don't have any problems - all works automatically.<br />
Suddenly projects on GitHub maybe lost - customer give you permissions for working with repository, then delete this permissions (you done good job) and at the moment customer decides to remove this repository... Your amazing GitHub Contributions Graph in one second was be so bad (lost works activities).<br />
But for all projects hosted outside GitHub we don't see GitHub Contributions Graph, but we worked on projects hardly and every day try to doing good job with our customers and solving their tasks.<br />
We must fix it! And we have solution for this!

# Features
- [x] merge all commits from your repositories to new one repository
- [x] append new commits from your repositories to existing one repository
- [x] selected branches in your repositories don't changed on any new branch names
- [x] enable or disable obfuscate feature for datetime commits data (samples in `app.py` and `app_obfuscate.py`)

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

obfuscate = Obfuscate(
    start_hour=11,
    start_minute=0,
    start_second=0,
    delta_minutes=5,
)


if __name__ == '__main__':
    obfuscate_enabled = False
    if not obfuscate_enabled:
        obfuscate = None

    contributions_graph = ContributionsGraph(repository_list, git, obfuscate)
    contributions_graph.run()
```
