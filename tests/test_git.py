import os
import subprocess

from contributions_graph.git import Git
from contributions_graph.utils import parse_iso_8601_string_to_datetime


class TestGit:
    def test_get_commits(self, tmpdir, datetime_string_first, datetime_string_second, git_author):
        git_repo_path = tmpdir.mkdir('get_commits')
        os.chdir(git_repo_path.strpath)
        os.system('git init')

        new_repo_path = os.path.join(git_repo_path.strpath, 'sub_dir')
        file_ext = 'py'
        new_repo_brach = 'master'
        new_repo_author = git_author
        git = Git(new_repo_path, new_repo_brach, new_repo_author, file_ext)

        file_name = git.create_file(datetime_string_first)
        git.set_current_datetime(datetime_string_first)
        git.commit_file(file_name)

        file_name = git.create_file(datetime_string_second)
        git.set_current_datetime(datetime_string_second)
        git.commit_file(file_name)

        all_commits = git.get_commits(
            repo_path=git_repo_path.strpath,
            branch='master',
            author=git_author,
        )
        assert all_commits == ['2018-06-30T23:22:01+05:00', '2018-06-30T20:12:09+05:00']
        assert all_commits == [datetime_string_second, datetime_string_first]

    def test_create_repository(self, tmpdir, git_author):
        new_repo_path = tmpdir.strpath
        file_ext = 'py'
        new_repo_brach = 'master'
        new_repo_author = git_author
        git = Git(new_repo_path, file_ext, new_repo_brach, new_repo_author)

        git_repo_path = os.path.join(new_repo_path, '.git')
        assert os.path.isdir(git_repo_path) is False

        git.create_repository()
        assert os.path.isdir(git_repo_path) is True

    def test_create_repository_with_wrong_path(self, tmpdir, git_author):
        new_repo_path = os.path.join(tmpdir.strpath, 'wrong')
        file_ext = 'py'
        new_repo_brach = 'master'
        new_repo_author = git_author
        git = Git(new_repo_path, file_ext, new_repo_brach, new_repo_author)

        git_repo_path = new_repo_path
        assert os.path.isdir(git_repo_path) is False

        git.create_repository()
        assert os.path.isdir(git_repo_path) is True

    def test_build_repository(self, tmpdir, datetime_string_first, datetime_string_second, git_author):
        git_repo_path = tmpdir.mkdir('builg_git_repository')
        os.chdir(git_repo_path.strpath)

        all_commits = [
            parse_iso_8601_string_to_datetime(datetime_string_first),
            parse_iso_8601_string_to_datetime(datetime_string_second),
        ]

        new_repo_path = git_repo_path.strpath
        file_ext = 'py'
        new_repo_brach = 'master'
        new_repo_author = git_author
        git = Git(new_repo_path, new_repo_brach, new_repo_author, file_ext)
        git.create_repository()
        git.build_repository(all_commits)

        cmd = 'git --no-pager log --pretty="%cI" --author="{}"'.format(git_author)
        all_commits = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        all_commits = all_commits.splitlines()

        assert all_commits == ['2018-06-30T23:22:01+05:00', '2018-06-30T20:12:09+05:00']
        assert all_commits == [datetime_string_second, datetime_string_first]
        assert os.path.isdir('all_commits') is True
