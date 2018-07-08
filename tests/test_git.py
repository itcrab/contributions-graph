import os
import subprocess

from contributions_graph.git import Git


class TestGit:
    def test_get_commits(self, tmpdir, datetime_strings, git_author):
        git_repo_path = tmpdir.mkdir('get_commits')
        os.chdir(git_repo_path.strpath)
        os.system('git init')

        new_repo_path = os.path.join(git_repo_path.strpath, 'sub_dir')
        file_ext = 'py'
        new_repo_brach = 'master'
        new_repo_author = git_author
        git = Git(new_repo_path, new_repo_brach, new_repo_author, file_ext)

        file_name = git.create_file(datetime_strings[0])
        git.set_current_datetime(datetime_strings[0])
        git.commit_file(file_name)

        file_name = git.create_file(datetime_strings[1])
        git.set_current_datetime(datetime_strings[1])
        git.commit_file(file_name)

        all_commits = git.get_commits(
            repo_path=git_repo_path.strpath,
            branch='master',
            author=git_author,
        )
        assert all_commits == [datetime_strings[1], datetime_strings[0]]

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

    def test_build_repository(self, tmpdir, datetime_objects, datetime_strings, git_author):
        git_repo_path = tmpdir.mkdir('builg_git_repository')
        os.chdir(git_repo_path.strpath)

        all_commits = [
            datetime_objects[0],
            datetime_objects[1],
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

        assert all_commits == [datetime_strings[1], datetime_strings[0]]
        assert os.path.isdir('all_commits') is True
