import os
import subprocess

from contributions_graph import ContributionsGraph
from contributions_graph.git import Git
from contributions_graph.obfuscate import Obfuscate
from contributions_graph.repository_list import RepositoryList


class TestCommitsStore:
    def test_contributions_graph_with_obfuscate(self, tmpdir, datetime_string_first, datetime_string_second, git_author):
        git_repo_path = tmpdir.mkdir('git_repo')
        os.chdir(git_repo_path.strpath)

        new_repo_path = git_repo_path.strpath
        file_ext = 'py'
        new_repo_brach = 'master'
        new_repo_author = git_author
        git = Git(new_repo_path, new_repo_brach, new_repo_author, file_ext)
        git.create_repository()

        file_name = git.create_file(datetime_string_first)
        git.set_current_datetime(datetime_string_first)
        git.commit_file(file_name)

        file_name = git.create_file(datetime_string_second)
        git.set_current_datetime(datetime_string_second)
        git.commit_file(file_name)

        new_repo_path = tmpdir.mkdir('new_git_repo')

        repository_list = RepositoryList()
        repository_list.add(git_repo_path.strpath, 'master', git_author)

        new_repo_brach = 'master'
        new_repo_author = git_author
        git = Git(new_repo_path.strpath, new_repo_brach, new_repo_author, 'py')
        obfuscate = Obfuscate(11, 0, 0, 5)
        contributions_graph = ContributionsGraph(repository_list, git, obfuscate)
        contributions_graph.run()

        os.chdir(new_repo_path.strpath)

        cmd = 'git --no-pager log --pretty="%cI" --author="{}"'.format(git_author)
        all_commits = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        all_commits = all_commits.splitlines()

        del all_commits[-1]  # README.md
        assert os.path.isfile('README.md') is True

        assert all_commits == ['2018-06-30T11:10:00+05:00', '2018-06-30T11:05:00+05:00']

    def test_contributions_graph_without_obfuscate(self, tmpdir, datetime_string_first, datetime_string_second, git_author):
        git_repo_path = tmpdir.mkdir('git_repo')
        os.chdir(git_repo_path.strpath)

        new_repo_path = git_repo_path.strpath
        file_ext = 'py'
        new_repo_brach = 'master'
        new_repo_author = git_author
        git = Git(new_repo_path, new_repo_brach, new_repo_author, file_ext)
        git.create_repository()

        file_name = git.create_file(datetime_string_first)
        git.set_current_datetime(datetime_string_first)
        git.commit_file(file_name)

        file_name = git.create_file(datetime_string_second)
        git.set_current_datetime(datetime_string_second)
        git.commit_file(file_name)

        new_repo_path = tmpdir.mkdir('new_git_repo')

        repository_list = RepositoryList()
        repository_list.add(git_repo_path.strpath, 'master', git_author)

        new_repo_brach = 'master'
        new_repo_author = git_author
        git = Git(new_repo_path.strpath, new_repo_brach, new_repo_author, 'py')
        contributions_graph = ContributionsGraph(repository_list, git)
        contributions_graph.run()

        os.chdir(new_repo_path.strpath)

        cmd = 'git --no-pager log --pretty="%cI" --author="{}"'.format(git_author)
        all_commits = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        all_commits = all_commits.splitlines()

        del all_commits[-1]  # README.md
        assert os.path.isfile('README.md') is True

        assert all_commits == ['2018-06-30T23:22:01+05:00', '2018-06-30T20:12:09+05:00']
        assert all_commits == [datetime_string_second, datetime_string_first]

    def test_contributions_graph_with_exists_repository_and_obfuscate(self, tmpdir, datetime_string_first, datetime_string_second, datetime_string_third, datetime_string_fourth, datetime_string_first_obfuscate, datetime_string_second_obfuscate, datetime_string_third_obfuscate, datetime_string_fourth_obfuscate, git_author):
        git_repo_path = tmpdir.mkdir('git_repo')
        os.chdir(git_repo_path.strpath)

        new_repo_path = git_repo_path.strpath
        file_ext = 'py'
        new_repo_brach = 'master'
        new_repo_author = git_author
        git = Git(new_repo_path, new_repo_brach, new_repo_author, file_ext)
        git.create_repository()

        file_name = git.create_file(datetime_string_first)
        git.set_current_datetime(datetime_string_first)
        git.commit_file(file_name)

        file_name = git.create_file(datetime_string_second)
        git.set_current_datetime(datetime_string_second)
        git.commit_file(file_name)

        file_name = git.create_file(datetime_string_third)
        git.set_current_datetime(datetime_string_third)
        git.commit_file(file_name)

        file_name = git.create_file(datetime_string_fourth)
        git.set_current_datetime(datetime_string_fourth)
        git.commit_file(file_name)

        new_repo_path = tmpdir.mkdir('new_git_repo')

        git = Git(new_repo_path.strpath, new_repo_brach, new_repo_author, file_ext)
        git.create_repository()

        file_name = git.create_file(datetime_string_first_obfuscate)
        git.set_current_datetime(datetime_string_first_obfuscate)
        git.commit_file(file_name)

        file_name = git.create_file(datetime_string_second_obfuscate)
        git.set_current_datetime(datetime_string_second_obfuscate)
        git.commit_file(file_name)

        cmd = 'git --no-pager log --pretty="%cI" --author="{}"'.format(git_author)
        all_commits = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        all_commits = all_commits.splitlines()

        assert all_commits == ['2018-06-30T11:10:00+05:00', '2018-06-30T11:05:00+05:00']
        assert all_commits == [datetime_string_second_obfuscate, datetime_string_first_obfuscate]

        repository_list = RepositoryList()
        repository_list.add(git_repo_path.strpath, 'master', git_author)

        new_repo_brach = 'master'
        new_repo_author = git_author
        git = Git(new_repo_path.strpath, new_repo_brach, new_repo_author, 'py')
        obfuscate = Obfuscate(11, 0, 0, 5)
        contributions_graph = ContributionsGraph(repository_list, git, obfuscate)
        contributions_graph.run()

        os.chdir(new_repo_path.strpath)

        cmd = 'git --no-pager log --pretty="%cI" --author="{}"'.format(git_author)
        all_commits = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        all_commits = all_commits.splitlines()

        del all_commits[-3]  # README.md
        assert os.path.isfile('README.md') is True

        assert all_commits == [
            '2018-07-01T11:10:00+05:00',
            '2018-07-01T11:05:00+05:00',
            '2018-06-30T11:10:00+05:00',
            '2018-06-30T11:05:00+05:00',
        ]
        assert all_commits == [
            datetime_string_fourth_obfuscate,
            datetime_string_third_obfuscate,
            datetime_string_second_obfuscate,
            datetime_string_first_obfuscate,
        ]

    def test_contributions_graph_with_exists_repository_and_without_obfuscate(self, tmpdir, datetime_string_first, datetime_string_second, datetime_string_third, datetime_string_fourth, git_author):
        git_repo_path = tmpdir.mkdir('git_repo')
        os.chdir(git_repo_path.strpath)

        new_repo_path = git_repo_path.strpath
        file_ext = 'py'
        new_repo_brach = 'master'
        new_repo_author = git_author
        git = Git(new_repo_path, new_repo_brach, new_repo_author, file_ext)
        git.create_repository()

        file_name = git.create_file(datetime_string_first)
        git.set_current_datetime(datetime_string_first)
        git.commit_file(file_name)

        file_name = git.create_file(datetime_string_second)
        git.set_current_datetime(datetime_string_second)
        git.commit_file(file_name)

        file_name = git.create_file(datetime_string_third)
        git.set_current_datetime(datetime_string_third)
        git.commit_file(file_name)

        file_name = git.create_file(datetime_string_fourth)
        git.set_current_datetime(datetime_string_fourth)
        git.commit_file(file_name)

        new_repo_path = tmpdir.mkdir('new_git_repo')

        git = Git(new_repo_path.strpath, new_repo_brach, new_repo_author, file_ext)
        git.create_repository()

        file_name = git.create_file(datetime_string_first)
        git.set_current_datetime(datetime_string_first)
        git.commit_file(file_name)

        file_name = git.create_file(datetime_string_second)
        git.set_current_datetime(datetime_string_second)
        git.commit_file(file_name)

        cmd = 'git --no-pager log --pretty="%cI" --author="{}"'.format(git_author)
        all_commits = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        all_commits = all_commits.splitlines()

        assert all_commits == ['2018-06-30T23:22:01+05:00', '2018-06-30T20:12:09+05:00']
        assert all_commits == [datetime_string_second, datetime_string_first]

        repository_list = RepositoryList()
        repository_list.add(git_repo_path.strpath, 'master', git_author)

        new_repo_brach = 'master'
        new_repo_author = git_author
        git = Git(new_repo_path.strpath, new_repo_brach, new_repo_author, 'py')
        contributions_graph = ContributionsGraph(repository_list, git)
        contributions_graph.run()

        os.chdir(new_repo_path.strpath)

        cmd = 'git --no-pager log --pretty="%cI" --author="{}"'.format(git_author)
        all_commits = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        all_commits = all_commits.splitlines()

        del all_commits[-3]  # README.md
        assert os.path.isfile('README.md') is True

        assert all_commits == [
            '2018-07-01T17:59:08+05:00',
            '2018-07-01T17:43:04+05:00',
            '2018-06-30T23:22:01+05:00',
            '2018-06-30T20:12:09+05:00',
        ]
        assert all_commits == [
            datetime_string_fourth,
            datetime_string_third,
            datetime_string_second,
            datetime_string_first,
        ]
