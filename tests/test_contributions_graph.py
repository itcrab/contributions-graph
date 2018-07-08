import os
import subprocess

from contributions_graph import ContributionsGraph
from contributions_graph.git import Git
from contributions_graph.obfuscate import Obfuscate
from contributions_graph.repository_list import RepositoryList


class TestCommitsStore:
    def test_contributions_graph_with_obfuscate(self, tmpdir, datetime_strings, git_author, datetime_strings_obfuscate):
        git_repo_path = tmpdir.mkdir('git_repo')
        os.chdir(git_repo_path.strpath)

        new_repo_path = git_repo_path.strpath
        file_ext = 'py'
        new_repo_brach = 'master'
        new_repo_author = git_author
        git = Git(new_repo_path, new_repo_brach, new_repo_author, file_ext)
        git.create_repository()

        file_name = git.create_file(datetime_strings[0])
        git.set_current_datetime(datetime_strings[0])
        git.commit_file(file_name)

        file_name = git.create_file(datetime_strings[1])
        git.set_current_datetime(datetime_strings[1])
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

        assert all_commits == [datetime_strings_obfuscate[1], datetime_strings_obfuscate[0]]

    def test_contributions_graph_without_obfuscate(self, tmpdir, datetime_strings, git_author):
        git_repo_path = tmpdir.mkdir('git_repo')
        os.chdir(git_repo_path.strpath)

        new_repo_path = git_repo_path.strpath
        file_ext = 'py'
        new_repo_brach = 'master'
        new_repo_author = git_author
        git = Git(new_repo_path, new_repo_brach, new_repo_author, file_ext)
        git.create_repository()

        file_name = git.create_file(datetime_strings[0])
        git.set_current_datetime(datetime_strings[0])
        git.commit_file(file_name)

        file_name = git.create_file(datetime_strings[1])
        git.set_current_datetime(datetime_strings[1])
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

        assert all_commits == [datetime_strings[1], datetime_strings[0]]

    def test_contributions_graph_with_exists_repository_and_obfuscate(self, tmpdir, datetime_strings, datetime_strings_obfuscate, git_author):
        git_repo_path = tmpdir.mkdir('git_repo')
        os.chdir(git_repo_path.strpath)

        new_repo_path = git_repo_path.strpath
        file_ext = 'py'
        new_repo_brach = 'master'
        new_repo_author = git_author
        git = Git(new_repo_path, new_repo_brach, new_repo_author, file_ext)
        git.create_repository()

        file_name = git.create_file(datetime_strings[0])
        git.set_current_datetime(datetime_strings[0])
        git.commit_file(file_name)

        file_name = git.create_file(datetime_strings[1])
        git.set_current_datetime(datetime_strings[1])
        git.commit_file(file_name)

        file_name = git.create_file(datetime_strings[2])
        git.set_current_datetime(datetime_strings[2])
        git.commit_file(file_name)

        file_name = git.create_file(datetime_strings[3])
        git.set_current_datetime(datetime_strings[3])
        git.commit_file(file_name)

        new_repo_path = tmpdir.mkdir('new_git_repo')

        git = Git(new_repo_path.strpath, new_repo_brach, new_repo_author, file_ext)
        git.create_repository()

        file_name = git.create_file(datetime_strings_obfuscate[0])
        git.set_current_datetime(datetime_strings_obfuscate[0])
        git.commit_file(file_name)

        file_name = git.create_file(datetime_strings_obfuscate[1])
        git.set_current_datetime(datetime_strings_obfuscate[1])
        git.commit_file(file_name)

        cmd = 'git --no-pager log --pretty="%cI" --author="{}"'.format(git_author)
        all_commits = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        all_commits = all_commits.splitlines()

        assert all_commits == [datetime_strings_obfuscate[1], datetime_strings_obfuscate[0]]

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
            datetime_strings_obfuscate[3],
            datetime_strings_obfuscate[2],
            datetime_strings_obfuscate[1],
            datetime_strings_obfuscate[0],
        ]

    def test_contributions_graph_with_exists_repository_and_without_obfuscate(self, tmpdir, datetime_strings, git_author):
        git_repo_path = tmpdir.mkdir('git_repo')
        os.chdir(git_repo_path.strpath)

        new_repo_path = git_repo_path.strpath
        file_ext = 'py'
        new_repo_brach = 'master'
        new_repo_author = git_author
        git = Git(new_repo_path, new_repo_brach, new_repo_author, file_ext)
        git.create_repository()

        file_name = git.create_file(datetime_strings[0])
        git.set_current_datetime(datetime_strings[0])
        git.commit_file(file_name)

        file_name = git.create_file(datetime_strings[1])
        git.set_current_datetime(datetime_strings[1])
        git.commit_file(file_name)

        file_name = git.create_file(datetime_strings[2])
        git.set_current_datetime(datetime_strings[2])
        git.commit_file(file_name)

        file_name = git.create_file(datetime_strings[3])
        git.set_current_datetime(datetime_strings[3])
        git.commit_file(file_name)

        new_repo_path = tmpdir.mkdir('new_git_repo')

        git = Git(new_repo_path.strpath, new_repo_brach, new_repo_author, file_ext)
        git.create_repository()

        file_name = git.create_file(datetime_strings[0])
        git.set_current_datetime(datetime_strings[0])
        git.commit_file(file_name)

        file_name = git.create_file(datetime_strings[1])
        git.set_current_datetime(datetime_strings[1])
        git.commit_file(file_name)

        cmd = 'git --no-pager log --pretty="%cI" --author="{}"'.format(git_author)
        all_commits = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        all_commits = all_commits.splitlines()

        assert all_commits == [datetime_strings[1], datetime_strings[0]]

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
            datetime_strings[3],
            datetime_strings[2],
            datetime_strings[1],
            datetime_strings[0],
        ]
