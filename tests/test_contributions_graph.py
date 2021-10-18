import os

from contributions_graph import ContributionsGraph
from contributions_graph.git import Git
from contributions_graph.obfuscate import Obfuscate
from contributions_graph.repository_list import RepositoryList
from tests.mixins import GitTestMixin


class TestContributionsGraph(GitTestMixin):
    def test_contributions_graph_with_obfuscate(self, tmpdir, datetime_strings, git_author, datetime_strings_obfuscate):
        git_repo_path = tmpdir.mkdir('git_repo').strpath
        os.chdir(git_repo_path)

        git = Git(
            new_repo_path=git_repo_path,
            new_repo_branch='master',
            new_repo_author=git_author,
            file_dir='all_commits',
            file_ext='py',
        )
        git.create_repository()

        self.git_commit_file(git, datetime_strings[0])
        self.git_commit_file(git, datetime_strings[1])

        repository_list = RepositoryList()
        repository_list.add(git_repo_path, 'master', git_author)

        new_repo_path = tmpdir.mkdir('new_git_repo').strpath
        git = Git(
            new_repo_path=new_repo_path,
            new_repo_branch='master',
            new_repo_author=git_author,
            file_dir='all_commits',
            file_ext='py',
        )
        obfuscate = Obfuscate(11, 0, 0, 5)
        contributions_graph = ContributionsGraph(repository_list, git, obfuscate)
        contributions_graph.run()

        os.chdir(new_repo_path)

        all_commits = self.git_log_commits(git_author)

        del all_commits[-1]  # README.md
        assert os.path.isfile('README.md') is True

        assert all_commits == [datetime_strings_obfuscate[1], datetime_strings_obfuscate[0]]

    def test_contributions_graph_without_obfuscate(self, tmpdir, datetime_strings, git_author):
        git_repo_path = tmpdir.mkdir('git_repo').strpath
        os.chdir(git_repo_path)

        git = Git(
            new_repo_path=git_repo_path,
            new_repo_branch='master',
            new_repo_author=git_author,
            file_dir='all_commits',
            file_ext='py',
        )
        git.create_repository()

        self.git_commit_file(git, datetime_strings[0])
        self.git_commit_file(git, datetime_strings[1])

        repository_list = RepositoryList()
        repository_list.add(git_repo_path, 'master', git_author)

        new_repo_path = tmpdir.mkdir('new_git_repo').strpath
        git = Git(
            new_repo_path=new_repo_path,
            new_repo_branch='master',
            new_repo_author=git_author,
            file_dir='all_commits',
            file_ext='py',
        )
        contributions_graph = ContributionsGraph(repository_list, git)
        contributions_graph.run()

        os.chdir(new_repo_path)

        all_commits = self.git_log_commits(git_author)

        del all_commits[-1]  # README.md
        assert os.path.isfile('README.md') is True

        assert all_commits == [datetime_strings[1], datetime_strings[0]]

    def test_contributions_graph_with_exists_repository_and_obfuscate(self, tmpdir, datetime_strings,
                                                                      datetime_strings_obfuscate, git_author):
        git_repo_path = tmpdir.mkdir('git_repo').strpath
        os.chdir(git_repo_path)

        git = Git(
            new_repo_path=git_repo_path,
            new_repo_branch='master',
            new_repo_author=git_author,
            file_dir='all_commits',
            file_ext='py',
        )
        git.create_repository()

        self.git_commit_file(git, datetime_strings[0])
        self.git_commit_file(git, datetime_strings[1])
        self.git_commit_file(git, datetime_strings[2])
        self.git_commit_file(git, datetime_strings[3])

        new_repo_path = tmpdir.mkdir('new_git_repo').strpath

        git = Git(
            new_repo_path=new_repo_path,
            new_repo_branch='master',
            new_repo_author=git_author,
            file_dir='all_commits',
            file_ext='py',
        )
        git.create_repository()

        self.git_commit_file(git, datetime_strings_obfuscate[0])
        self.git_commit_file(git, datetime_strings_obfuscate[1])

        all_commits = self.git_log_commits(git_author)

        assert all_commits == [datetime_strings_obfuscate[1], datetime_strings_obfuscate[0]]

        repository_list = RepositoryList()
        repository_list.add(git_repo_path, 'master', git_author)

        git = Git(
            new_repo_path=new_repo_path,
            new_repo_branch='master',
            new_repo_author=git_author,
            file_dir='all_commits',
            file_ext='py',
        )
        obfuscate = Obfuscate(11, 0, 0, 5)
        contributions_graph = ContributionsGraph(repository_list, git, obfuscate)
        contributions_graph.run()

        os.chdir(new_repo_path)

        all_commits = self.git_log_commits(git_author)

        del all_commits[-3]  # README.md
        assert os.path.isfile('README.md') is True

        assert all_commits == [
            datetime_strings_obfuscate[3],
            datetime_strings_obfuscate[2],
            datetime_strings_obfuscate[1],
            datetime_strings_obfuscate[0],
        ]

    def test_contributions_graph_with_exists_repository_and_without_obfuscate(self, tmpdir, datetime_strings, git_author):
        git_repo_path = tmpdir.mkdir('git_repo').strpath
        os.chdir(git_repo_path)

        git = Git(
            new_repo_path=git_repo_path,
            new_repo_branch='master',
            new_repo_author=git_author,
            file_dir='all_commits',
            file_ext='py',
        )
        git.create_repository()

        self.git_commit_file(git, datetime_strings[0])
        self.git_commit_file(git, datetime_strings[1])
        self.git_commit_file(git, datetime_strings[2])
        self.git_commit_file(git, datetime_strings[3])

        new_repo_path = tmpdir.mkdir('new_git_repo').strpath

        git = Git(
            new_repo_path=new_repo_path,
            new_repo_branch='master',
            new_repo_author=git_author,
            file_dir='all_commits',
            file_ext='py',
        )
        git.create_repository()

        self.git_commit_file(git, datetime_strings[0])
        self.git_commit_file(git, datetime_strings[1])

        all_commits = self.git_log_commits(git_author)

        assert all_commits == [datetime_strings[1], datetime_strings[0]]

        repository_list = RepositoryList()
        repository_list.add(git_repo_path, 'master', git_author)

        git = Git(
            new_repo_path=new_repo_path,
            new_repo_branch='master',
            new_repo_author=git_author,
            file_dir='all_commits',
            file_ext='py',
        )
        contributions_graph = ContributionsGraph(repository_list, git)
        contributions_graph.run()

        os.chdir(new_repo_path)

        all_commits = self.git_log_commits(git_author)

        del all_commits[-3]  # README.md
        assert os.path.isfile('README.md') is True

        assert all_commits == [
            datetime_strings[3],
            datetime_strings[2],
            datetime_strings[1],
            datetime_strings[0],
        ]
