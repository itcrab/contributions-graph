import os

from contributions_graph import ContributionsGraph
from contributions_graph.git import Git
from contributions_graph.obfuscate import Obfuscate
from contributions_graph.repository_list import RepositoryList
from tests.mixins import GitTestMixin


class TestContributionsGraph(GitTestMixin):
    def test_contributions_graph_with_obfuscate(self, tmpdir, datetime_objects, git_author, datetime_objects_obfuscate):
        git_repo_path = tmpdir.mkdir('git_repo').strpath
        os.chdir(git_repo_path)

        git = self.git_create_repository(new_repo_path=git_repo_path, new_repo_author=git_author)
        all_commits = {'test_repo': [
            datetime_objects[0],
            datetime_objects[1],
        ]}
        git.build_repository(all_commits)

        repository_list = RepositoryList()
        repository_list.add(git_repo_path, 'master', git_author)

        new_repo_path = tmpdir.mkdir('new_git_repo').strpath
        git = Git(
            new_repo_path=new_repo_path,
            new_repo_branch='master',
            new_repo_author=git_author,
            file_ext='py',
        )
        obfuscate = Obfuscate(11, 0, 0, 5)
        contributions_graph = ContributionsGraph(repository_list, git, obfuscate)
        contributions_graph.run()

        os.chdir(new_repo_path)

        all_commits = git.get_commits(git_author)

        del all_commits[-1]  # README.md
        assert os.path.isfile('README.md') is True

        assert all_commits == [datetime_objects_obfuscate[1], datetime_objects_obfuscate[0]]

    def test_contributions_graph_without_obfuscate(self, tmpdir, git_author, datetime_objects, datetime_objects_utc):
        git_repo_path = tmpdir.mkdir('git_repo').strpath
        os.chdir(git_repo_path)

        git = self.git_create_repository(new_repo_path=git_repo_path, new_repo_author=git_author)
        all_commits = {'test_repo': [
            datetime_objects[0],
            datetime_objects[1],
        ]}
        git.build_repository(all_commits)

        repository_list = RepositoryList()
        repository_list.add(git_repo_path, 'master', git_author)

        new_repo_path = tmpdir.mkdir('new_git_repo').strpath
        git = Git(
            new_repo_path=new_repo_path,
            new_repo_branch='master',
            new_repo_author=git_author,
            file_ext='py',
        )
        contributions_graph = ContributionsGraph(repository_list, git)
        contributions_graph.run()

        os.chdir(new_repo_path)

        all_commits = git.get_commits(git_author)

        del all_commits[-1]  # README.md
        assert os.path.isfile('README.md') is True

        assert all_commits == [datetime_objects_utc[1], datetime_objects_utc[0]]

    def test_contributions_graph_with_exists_repository_and_obfuscate(self, tmpdir, datetime_objects,
                                                                      git_author, datetime_objects_obfuscate):
        git_repo_path = tmpdir.mkdir('git_repo').strpath
        os.chdir(git_repo_path)

        git = self.git_create_repository(new_repo_path=git_repo_path, new_repo_author=git_author)
        all_commits = {'test_repo': [
            datetime_objects[0],
            datetime_objects[1],
            datetime_objects[2],
            datetime_objects[3],
        ]}
        git.build_repository(all_commits)

        new_repo_path = tmpdir.mkdir('new_git_repo').strpath
        git = self.git_create_repository(new_repo_path=new_repo_path, new_repo_author=git_author)
        all_commits = {'test_repo': [
            datetime_objects_obfuscate[0],
            datetime_objects_obfuscate[1],
        ]}
        git.build_repository(all_commits)

        all_commits = git.get_commits(git_author)

        assert all_commits == [datetime_objects_obfuscate[1], datetime_objects_obfuscate[0]]

        repository_list = RepositoryList()
        repository_list.add(git_repo_path, 'master', git_author)

        git = Git(
            new_repo_path=new_repo_path,
            new_repo_branch='master',
            new_repo_author=git_author,
            file_ext='py',
        )
        obfuscate = Obfuscate(11, 0, 0, 5)
        contributions_graph = ContributionsGraph(repository_list, git, obfuscate)
        contributions_graph.run()

        os.chdir(new_repo_path)

        all_commits = git.get_commits(git_author)

        del all_commits[-3]  # README.md
        assert os.path.isfile('README.md') is True

        assert all_commits == [
            datetime_objects_obfuscate[3],
            datetime_objects_obfuscate[2],
            datetime_objects_obfuscate[1],
            datetime_objects_obfuscate[0],
        ]

    def test_contributions_graph_with_exists_repository_and_without_obfuscate(self, tmpdir, git_author,
                                                                              datetime_objects, datetime_objects_utc):
        git_repo_path = tmpdir.mkdir('git_repo').strpath
        os.chdir(git_repo_path)

        git = self.git_create_repository(new_repo_path=git_repo_path, new_repo_author=git_author)
        all_commits = {'test_repo': [
            datetime_objects[0],
            datetime_objects[1],
            datetime_objects[2],
            datetime_objects[3],
        ]}
        git.build_repository(all_commits)

        new_repo_path = tmpdir.mkdir('new_git_repo').strpath

        git = self.git_create_repository(new_repo_path=new_repo_path, new_repo_author=git_author)
        all_commits = {'test_repo': [
            datetime_objects[0],
            datetime_objects[1],
        ]}
        git.build_repository(all_commits)

        all_commits = git.get_commits(git_author)

        assert all_commits == [datetime_objects_utc[1], datetime_objects_utc[0]]

        repository_list = RepositoryList()
        repository_list.add(git_repo_path, 'master', git_author)

        git = Git(
            new_repo_path=new_repo_path,
            new_repo_branch='master',
            new_repo_author=git_author,
            file_ext='py',
        )
        contributions_graph = ContributionsGraph(repository_list, git)
        contributions_graph.run()

        os.chdir(new_repo_path)

        all_commits = git.get_commits(git_author)

        del all_commits[-3]  # README.md
        assert os.path.isfile('README.md') is True

        assert all_commits == [
            datetime_objects_utc[3],
            datetime_objects_utc[2],
            datetime_objects_utc[1],
            datetime_objects_utc[0],
        ]
