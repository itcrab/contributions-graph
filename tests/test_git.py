import os

from contributions_graph.git import Git
from tests.mixins import GitTestMixin


class TestGit(GitTestMixin):
    def test_get_commits(self, tmpdir, datetime_strings, git_author):
        tmpdir.mkdir('get_commits').mkdir('sub_dir')

        git_repo_path = tmpdir.join('get_commits').strpath
        sub_git_repo_path = tmpdir.join('get_commits', 'sub_dir').strpath
        os.chdir(git_repo_path)
        os.system('git init')

        git = Git(
            new_repo_path=sub_git_repo_path,
            new_repo_branch='master',
            new_repo_author=git_author,
            file_ext='py',
        )

        file_name = git.create_file(datetime_strings[0])
        git.set_current_datetime(datetime_strings[0])
        git.commit_file(file_name)

        file_name = git.create_file(datetime_strings[1])
        git.set_current_datetime(datetime_strings[1])
        git.commit_file(file_name)

        all_commits = git.get_commits(
            repo_path=git_repo_path,
            branch='master',
            author=git_author,
        )
        assert all_commits == [datetime_strings[1], datetime_strings[0]]

    def test_create_repository(self, tmpdir, git_author):
        new_repo_path = tmpdir.strpath
        git = Git(
            new_repo_path=new_repo_path,
            new_repo_branch='master',
            new_repo_author=git_author,
            file_ext='py',
        )

        git_repo_path = os.path.join(new_repo_path, '.git')
        assert os.path.isdir(git_repo_path) is False

        git.create_repository()
        assert os.path.isdir(git_repo_path) is True

    def test_create_repository_with_wrong_path(self, tmpdir, git_author):
        new_repo_path = os.path.join(tmpdir.strpath, 'wrong')
        git = Git(
            new_repo_path=new_repo_path,
            new_repo_branch='master',
            new_repo_author=git_author,
            file_ext='py',
        )

        git_repo_path = new_repo_path
        assert os.path.isdir(git_repo_path) is False

        git.create_repository()
        assert os.path.isdir(git_repo_path) is True

    def test_build_repository(self, tmpdir, datetime_objects, datetime_strings, git_author):
        git_repo_path = tmpdir.mkdir('builg_git_repository').strpath
        os.chdir(git_repo_path)

        all_commits = [
            datetime_objects[0],
            datetime_objects[1],
        ]

        git = Git(
            new_repo_path=git_repo_path,
            new_repo_branch='master',
            new_repo_author=git_author,
            file_ext='py',
        )
        git.create_repository()
        git.build_repository(all_commits)

        all_commits = self.git_log_commits(git_author)

        assert all_commits == [datetime_strings[1], datetime_strings[0]]
        assert os.path.isdir('all_commits') is True
