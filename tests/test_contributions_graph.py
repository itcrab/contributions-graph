import os
import subprocess

from contributions_graph import ContributionsGraph
from contributions_graph.git import Git
from contributions_graph.obfuscate import Obfuscate
from contributions_graph.repository_list import RepositoryList


class TestCommitsStore:
    def test_commits_store_with_obfuscate(self, tmpdir, datetime_string_first, datetime_string_second, git_author):
        git_repo_path = tmpdir.mkdir('git_repo')
        os.chdir(str(git_repo_path))

        new_repo_path = str(git_repo_path)
        file_ext = 'py'
        git = Git(new_repo_path, file_ext)
        git.create_repository()

        file_name = git.create_file(datetime_string_first)
        git.commit_file(datetime_string_first, file_name)

        file_name = git.create_file(datetime_string_second)
        git.commit_file(datetime_string_second, file_name)

        new_repo_path = tmpdir.mkdir('new_git_repo')

        repository_list = RepositoryList()
        repository_list.add(str(git_repo_path), 'master', git_author)

        git = Git(str(new_repo_path), 'py')
        obfuscate = Obfuscate(11, 0, 0, 5)
        commit_store = ContributionsGraph(repository_list, git, obfuscate)
        commit_store.run()

        os.chdir(str(new_repo_path))
        cmd = 'git --no-pager log --pretty="%cI" --author="{}"'.format(git_author)
        all_commits = subprocess.check_output(cmd, universal_newlines=True)
        all_commits = all_commits.splitlines()

        assert all_commits == ['2018-06-30T11:10:00+05:00', '2018-06-30T11:05:00+05:00']

    def test_commits_store_without_obfuscate(self, tmpdir, datetime_string_first, datetime_string_second, git_author):
        git_repo_path = tmpdir.mkdir('git_repo')
        os.chdir(str(git_repo_path))

        new_repo_path = str(git_repo_path)
        file_ext = 'py'
        git = Git(new_repo_path, file_ext)
        git.create_repository()

        file_name = git.create_file(datetime_string_first)
        git.commit_file(datetime_string_first, file_name)

        file_name = git.create_file(datetime_string_second)
        git.commit_file(datetime_string_second, file_name)

        new_repo_path = tmpdir.mkdir('new_git_repo')

        repository_list = RepositoryList()
        repository_list.add(str(git_repo_path), 'master', git_author)

        git = Git(str(new_repo_path), 'py')
        commit_store = ContributionsGraph(repository_list, git)
        commit_store.run()

        os.chdir(str(new_repo_path))
        cmd = 'git --no-pager log --pretty="%cI" --author="{}"'.format(git_author)
        all_commits = subprocess.check_output(cmd, universal_newlines=True)
        all_commits = all_commits.splitlines()

        assert all_commits == ['2018-06-30T23:22:01+05:00', '2018-06-30T20:12:09+05:00']
        assert all_commits == [datetime_string_second, datetime_string_first]
