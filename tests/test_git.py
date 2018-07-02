import os
import subprocess

import pytest

from contributions_graph.exceptions import GitRepositoryExistsError
from contributions_graph.git import Git
from contributions_graph.utils import parse_iso_8601_string_to_datetime


class TestGit:
    def test_new_repo_path_exists(self, tmpdir):
        tmpdir.mkdir('.git')

        new_repo_path = str(tmpdir)
        file_ext = 'py'
        with pytest.raises(GitRepositoryExistsError):
            Git(new_repo_path, file_ext)

    def test_get_commits(self, tmpdir, datetime_string_first, datetime_string_second, git_author):
        git_repo_path = tmpdir.mkdir('get_commits')
        os.chdir(str(git_repo_path))
        os.system('git init')

        new_repo_path = os.path.join(str(git_repo_path), 'sub_dir')
        file_ext = 'py'
        git = Git(new_repo_path, file_ext)

        file_name = git.create_file(datetime_string_first)
        git.commit_file(datetime_string_first, file_name)

        file_name = git.create_file(datetime_string_second)
        git.commit_file(datetime_string_second, file_name)

        all_commits = git.get_commits(
            repo_path=str(git_repo_path),
            branch='master',
            author=git_author
        )
        assert all_commits == ['2018-06-30T23:22:01+05:00', '2018-06-30T20:12:09+05:00']
        assert all_commits == [datetime_string_second, datetime_string_first]

    def test_create_repository(self, tmpdir):
        new_repo_path = str(tmpdir)
        file_ext = 'py'
        git = Git(new_repo_path, file_ext)

        git_repo_path = os.path.join(str(new_repo_path), '.git')
        assert os.path.isdir(git_repo_path) is False

        git.create_repository()
        assert os.path.isdir(git_repo_path) is True

    def test_create_repository_with_wrong_path(self, tmpdir):
        new_repo_path = os.path.join(str(tmpdir), 'wrong')
        file_ext = 'py'
        git = Git(new_repo_path, file_ext)

        git_repo_path = new_repo_path
        assert os.path.isdir(git_repo_path) is False

        git.create_repository()
        assert os.path.isdir(git_repo_path) is True

    def test_build_repository(self, tmpdir, datetime_string_first, datetime_string_second, git_author):
        git_repo_path = tmpdir.mkdir('builg_git_repository')
        os.chdir(str(git_repo_path))

        all_commits = [
            parse_iso_8601_string_to_datetime(datetime_string_first),
            parse_iso_8601_string_to_datetime(datetime_string_second),
        ]

        new_repo_path = str(git_repo_path)
        file_ext = 'py'
        git = Git(new_repo_path, file_ext)
        git.create_repository()
        git.build_repository(all_commits)

        cmd = 'git --no-pager log --pretty="%cI" --author="{}"'.format(git_author)
        all_commits = subprocess.check_output(cmd, shell=True).decode('utf-8')
        all_commits = all_commits.splitlines()

        assert all_commits == ['2018-06-30T23:22:01+05:00', '2018-06-30T20:12:09+05:00']
        assert all_commits == [datetime_string_second, datetime_string_first]
