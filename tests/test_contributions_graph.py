import os

from contributions_graph import ContributionsGraph
from contributions_graph.git import GitConsole
from contributions_graph.obfuscate import Obfuscate
from contributions_graph.repositories import ExportRepositories, ImportRepository
from tests.helpers import git_create_repository


class TestContributionsGraph:
    def test_contributions_graph_with_obfuscate(self, tmpdir, datetime_objects, git_author, datetime_objects_obfuscate):
        git_repo_path = tmpdir.mkdir('git_repo').strpath
        os.chdir(git_repo_path)

        import_repository = git_create_repository(repo_path=git_repo_path, repo_author=git_author)
        export_commits = {'test_repo': {'author': git_author, 'file_ext': 'py', 'commits': [
            datetime_objects[0],
            datetime_objects[1],
        ]}}
        import_repository._apply_export_commits(export_commits)

        new_repo_path = tmpdir.mkdir('new_git_repo').strpath

        export_repositories = ExportRepositories()
        export_repositories.add(git_repo_path, 'master', git_author, file_ext='py')

        import_repository = ImportRepository(
            repo_path=new_repo_path,
            repo_branch='master',
            repo_author=git_author,
        )

        obfuscate = Obfuscate(11, 0, 0, 5)
        contributions_graph = ContributionsGraph(export_repositories, import_repository, obfuscate)
        contributions_graph.run()

        os.chdir(new_repo_path)

        export_commits = GitConsole.get_commits_by_author(git_author)

        del export_commits[-1]  # README.md
        assert os.path.isfile('README.md') is True

        assert export_commits == [datetime_objects_obfuscate[1], datetime_objects_obfuscate[0]]

    def test_contributions_graph_without_obfuscate(self, tmpdir, git_author, datetime_objects, datetime_objects_utc):
        git_repo_path = tmpdir.mkdir('git_repo').strpath
        os.chdir(git_repo_path)

        import_repository = git_create_repository(repo_path=git_repo_path, repo_author=git_author)
        export_commits = {'test_repo': {'author': git_author, 'file_ext': 'py', 'commits': [
            datetime_objects[0],
            datetime_objects[1],
        ]}}
        import_repository._apply_export_commits(export_commits)

        new_repo_path = tmpdir.mkdir('new_git_repo').strpath

        export_repositories = ExportRepositories()
        export_repositories.add(git_repo_path, 'master', git_author, file_ext='py')

        import_repository = ImportRepository(
            repo_path=new_repo_path,
            repo_branch='master',
            repo_author=git_author,
        )

        contributions_graph = ContributionsGraph(export_repositories, import_repository)
        contributions_graph.run()

        os.chdir(new_repo_path)

        export_commits = GitConsole.get_commits_by_author(git_author)

        del export_commits[-1]  # README.md
        assert os.path.isfile('README.md') is True

        assert export_commits == [datetime_objects_utc[1], datetime_objects_utc[0]]

    def test_contributions_graph_with_exists_repository_and_obfuscate(self, tmpdir, datetime_objects,
                                                                      git_author, datetime_objects_obfuscate):
        git_repo_path = tmpdir.mkdir('git_repo').strpath
        os.chdir(git_repo_path)

        import_repository = git_create_repository(repo_path=git_repo_path, repo_author=git_author)
        export_commits = {'test_repo': {'author': git_author, 'file_ext': 'py', 'commits': [
            datetime_objects[0],
            datetime_objects[1],
            datetime_objects[2],
            datetime_objects[3],
        ]}}
        import_repository._apply_export_commits(export_commits)

        new_repo_path = tmpdir.mkdir('new_git_repo').strpath
        import_repository = git_create_repository(repo_path=new_repo_path, repo_author=git_author)
        export_commits = {'test_repo': {'author': git_author, 'file_ext': 'py', 'commits': [
            datetime_objects_obfuscate[0],
            datetime_objects_obfuscate[1],
        ]}}
        import_repository._apply_export_commits(export_commits)

        export_commits = GitConsole.get_commits_by_author(git_author)

        assert export_commits == [datetime_objects_obfuscate[1], datetime_objects_obfuscate[0]]

        export_repositories = ExportRepositories()
        export_repositories.add(git_repo_path, 'master', git_author, file_ext='py')

        import_repository = ImportRepository(
            repo_path=new_repo_path,
            repo_branch='master',
            repo_author=git_author,
        )

        obfuscate = Obfuscate(11, 0, 0, 5)
        contributions_graph = ContributionsGraph(export_repositories, import_repository, obfuscate)
        contributions_graph.run()

        os.chdir(new_repo_path)

        export_commits = GitConsole.get_commits_by_author(git_author)

        del export_commits[-3]  # README.md
        assert os.path.isfile('README.md') is True

        assert export_commits == [
            datetime_objects_obfuscate[3],
            datetime_objects_obfuscate[2],
            datetime_objects_obfuscate[1],
            datetime_objects_obfuscate[0],
        ]

    def test_contributions_graph_with_exists_repository_and_without_obfuscate(self, tmpdir, git_author,
                                                                              datetime_objects, datetime_objects_utc):
        git_repo_path = tmpdir.mkdir('git_repo').strpath
        os.chdir(git_repo_path)

        import_repository = git_create_repository(repo_path=git_repo_path, repo_author=git_author)
        export_commits = {'test_repo': {'author': git_author, 'file_ext': 'py', 'commits': [
            datetime_objects[0],
            datetime_objects[1],
            datetime_objects[2],
            datetime_objects[3],
        ]}}
        import_repository._apply_export_commits(export_commits)

        new_repo_path = tmpdir.mkdir('new_git_repo').strpath

        import_repository = git_create_repository(repo_path=new_repo_path, repo_author=git_author)
        export_commits = {'test_repo': {'author': git_author, 'file_ext': 'py', 'commits': [
            datetime_objects[0],
            datetime_objects[1],
        ]}}
        import_repository._apply_export_commits(export_commits)

        export_commits = GitConsole.get_commits_by_author(git_author)

        assert export_commits == [datetime_objects_utc[1], datetime_objects_utc[0]]

        export_repositories = ExportRepositories()
        export_repositories.add(git_repo_path, 'master', git_author, file_ext='py')

        import_repository = ImportRepository(
            repo_path=new_repo_path,
            repo_branch='master',
            repo_author=git_author,
        )

        contributions_graph = ContributionsGraph(export_repositories, import_repository)
        contributions_graph.run()

        os.chdir(new_repo_path)

        export_commits = GitConsole.get_commits_by_author(git_author)

        del export_commits[-3]  # README.md
        assert os.path.isfile('README.md') is True

        assert export_commits == [
            datetime_objects_utc[3],
            datetime_objects_utc[2],
            datetime_objects_utc[1],
            datetime_objects_utc[0],
        ]
