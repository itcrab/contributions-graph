import os

import pytest

from contributions_graph.exceptions import GitBranchNotFoundError
from contributions_graph.git import Git, GitConsole, GitRepositorySwitch
from tests.mixins import GitTestMixin


class TestGit(GitTestMixin):
    def test_get_commits(self, tmpdir, datetime_strings, git_author, datetime_objects, datetime_objects_utc):
        git_repo_path = tmpdir.mkdir('get_commits').strpath
        os.chdir(git_repo_path)

        git = self.git_create_repository(new_repo_path=git_repo_path, new_repo_author=git_author)
        for i in range(2):
            file_name = git.create_file(datetime_strings[i])
            GitConsole.set_current_datetime(datetime_strings[i])
            GitConsole.add_file(file_name)
            GitConsole.commit_file(file_name)

        with GitRepositorySwitch(new_repo_path=git_repo_path, new_repo_branch='master'):
            all_commits = git.get_commits(author=git_author)

        assert all_commits == [datetime_objects_utc[1], datetime_objects_utc[0]]

    def test_get_commits_with_different_base_branch(self, tmpdir, datetime_strings, git_author, datetime_objects,
                                                    datetime_objects_utc):
        git_repo_path = tmpdir.mkdir('get_commits').strpath
        os.chdir(git_repo_path)

        git = self.git_create_repository(new_repo_path=git_repo_path, new_repo_author=git_author)
        for i in range(2):
            file_name = git.create_file(datetime_strings[i])
            GitConsole.set_current_datetime(datetime_strings[i])
            GitConsole.add_file(file_name)
            GitConsole.commit_file(file_name)

        GitConsole.create_branch('new-branch')
        assert GitConsole.get_current_branch() == 'new-branch'

        with GitRepositorySwitch(new_repo_path=git_repo_path, new_repo_branch='master'):
            all_commits = git.get_commits(author=git_author)

            assert GitConsole.get_current_branch() == 'master'
            assert all_commits == [datetime_objects_utc[1], datetime_objects_utc[0]]

    def test_get_commits_with_read_only_master_commits_case_1(self, tmpdir, datetime_strings, git_author,
                                                              datetime_objects, datetime_objects_utc):
        git_repo_path = tmpdir.mkdir('get_commits').strpath
        os.chdir(git_repo_path)

        git = self.git_create_repository(new_repo_path=git_repo_path, new_repo_author=git_author)

        file_name = git.create_file(datetime_strings[0])
        GitConsole.set_current_datetime(datetime_strings[0])
        GitConsole.add_file(file_name)
        GitConsole.commit_file(file_name)

        GitConsole.create_branch('new-branch')

        file_name = git.create_file(datetime_strings[1])
        GitConsole.set_current_datetime(datetime_strings[1])
        GitConsole.add_file(file_name)
        GitConsole.commit_file(file_name)

        GitConsole.switch_branch('master')

        file_name = git.create_file(datetime_strings[2])
        GitConsole.set_current_datetime(datetime_strings[2])
        GitConsole.add_file(file_name)
        GitConsole.commit_file(file_name)

        with GitRepositorySwitch(new_repo_path=git_repo_path, new_repo_branch='master'):
            all_commits = git.get_commits(author=git_author)

        assert all_commits == [datetime_objects_utc[2], datetime_objects_utc[0]]

    def test_get_commits_with_read_only_master_commits_case_2(self, tmpdir, datetime_strings, git_author,
                                                              datetime_objects, datetime_objects_utc):
        git_repo_path = tmpdir.mkdir('get_commits').strpath
        os.chdir(git_repo_path)

        git = self.git_create_repository(new_repo_path=git_repo_path, new_repo_author=git_author)

        file_name = git.create_file(datetime_strings[0])
        GitConsole.set_current_datetime(datetime_strings[0])
        GitConsole.add_file(file_name)
        GitConsole.commit_file(file_name)

        GitConsole.create_branch('new-branch')

        for i in range(1, 3):
            file_name = git.create_file(datetime_strings[i])
            GitConsole.set_current_datetime(datetime_strings[i])
            GitConsole.add_file(file_name)
            GitConsole.commit_file(file_name)

        with GitRepositorySwitch(new_repo_path=git_repo_path, new_repo_branch='master'):
            all_commits = git.get_commits(author=git_author)

        assert all_commits == [datetime_objects_utc[0]]

    def test_get_commits_with_read_only_master_commits_case_3(self, tmpdir, datetime_strings, git_author,
                                                              datetime_objects, datetime_objects_utc):
        git_repo_path = tmpdir.mkdir('get_commits').strpath
        os.chdir(git_repo_path)

        git = self.git_create_repository(new_repo_path=git_repo_path, new_repo_author=git_author)

        GitConsole.create_branch('new-branch')

        file_name = git.create_file(datetime_strings[0])
        GitConsole.set_current_datetime(datetime_strings[0])
        GitConsole.add_file(file_name)
        GitConsole.commit_file(file_name)

        GitConsole.create_branch('master')

        for i in range(1, 3):
            file_name = git.create_file(datetime_strings[i])
            GitConsole.set_current_datetime(datetime_strings[i])
            GitConsole.add_file(file_name)
            GitConsole.commit_file(file_name)

        with GitRepositorySwitch(new_repo_path=git_repo_path, new_repo_branch='master'):
            all_commits = git.get_commits(author=git_author)

        assert all_commits == [datetime_objects_utc[2], datetime_objects_utc[1], datetime_objects_utc[0]]

    def test_get_commits_with_read_only_new_branch_commits_case_1(self, tmpdir, datetime_strings, git_author,
                                                                  datetime_objects, datetime_objects_utc):
        git_repo_path = tmpdir.mkdir('get_commits').strpath
        os.chdir(git_repo_path)

        git = self.git_create_repository(new_repo_path=git_repo_path, new_repo_author=git_author)

        GitConsole.create_branch('new-branch')

        file_name = git.create_file(datetime_strings[0])
        GitConsole.set_current_datetime(datetime_strings[0])
        GitConsole.add_file(file_name)
        GitConsole.commit_file(file_name)

        GitConsole.create_branch('master')

        for i in range(1, 3):
            file_name = git.create_file(datetime_strings[i])
            GitConsole.set_current_datetime(datetime_strings[i])
            GitConsole.add_file(file_name)
            GitConsole.commit_file(file_name)

        with GitRepositorySwitch(new_repo_path=git_repo_path, new_repo_branch='new-branch'):
            all_commits = git.get_commits(author=git_author)

        assert all_commits == [datetime_objects_utc[0]]

    def test_get_commits_with_read_only_new_branch_commits_case_2(self, tmpdir, datetime_strings, git_author,
                                                                  datetime_objects, datetime_objects_utc):
        git_repo_path = tmpdir.mkdir('get_commits').strpath
        os.chdir(git_repo_path)

        git = self.git_create_repository(new_repo_path=git_repo_path, new_repo_author=git_author)

        file_name = git.create_file(datetime_strings[0])
        GitConsole.set_current_datetime(datetime_strings[0])
        GitConsole.add_file(file_name)
        GitConsole.commit_file(file_name)

        GitConsole.create_branch('new-branch')

        file_name = git.create_file(datetime_strings[1])
        GitConsole.set_current_datetime(datetime_strings[1])
        GitConsole.add_file(file_name)
        GitConsole.commit_file(file_name)

        GitConsole.switch_branch('master')

        file_name = git.create_file(datetime_strings[2])
        GitConsole.set_current_datetime(datetime_strings[2])
        GitConsole.add_file(file_name)
        GitConsole.commit_file(file_name)

        with GitRepositorySwitch(new_repo_path=git_repo_path, new_repo_branch='new-branch'):
            all_commits = git.get_commits(author=git_author)

        assert all_commits == [datetime_objects_utc[1], datetime_objects_utc[0]]

    def test_get_commits_with_wrong_branch(self, tmpdir, datetime_strings, git_author):
        git_repo_path = tmpdir.mkdir('get_commits').strpath
        os.chdir(git_repo_path)

        git = self.git_create_repository(new_repo_path=git_repo_path, new_repo_author=git_author)
        for i in range(2):
            file_name = git.create_file(datetime_strings[i])
            GitConsole.set_current_datetime(datetime_strings[i])
            GitConsole.add_file(file_name)
            GitConsole.commit_file(file_name)

        with pytest.raises(GitBranchNotFoundError):
            with GitRepositorySwitch(new_repo_path=git_repo_path, new_repo_branch='wrong-branch'):
                git.get_commits()

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
        git_repo_path = tmpdir.mkdir('build_git_repository').strpath
        os.chdir(git_repo_path)

        all_commits = {'test_reoo': [
            datetime_objects[0],
            datetime_objects[1],
        ]}

        git = self.git_create_repository(new_repo_path=git_repo_path, new_repo_author=git_author)
        git.build_repository(all_commits)

        all_commits = git.get_commits(git_author)

        assert all_commits == [datetime_objects[1], datetime_objects[0]]
        assert os.path.isdir('test_reoo') is True

        committers = GitConsole.get_committers()
        assert committers == [git_author, git_author]

    def test_build_repository_with_commits_directory_exists(self, tmpdir, datetime_objects, datetime_strings,
                                                            git_author, datetime_objects_utc):
        tmpdir.mkdir('commits_directory_exists').mkdir('test_repo')
        git_repo_path = tmpdir.join('commits_directory_exists').strpath
        os.chdir(git_repo_path)

        assert os.path.isdir('test_repo') is True

        all_commits = {'test_repo': [
            datetime_objects[0],
            datetime_objects[1],
        ]}

        git = self.git_create_repository(new_repo_path=git_repo_path, new_repo_author=git_author)
        git.build_repository(all_commits)

        all_commits = git.get_commits(git_author)

        assert all_commits == [datetime_objects_utc[1], datetime_objects_utc[0]]
        assert os.listdir('.') == ['.git', 'test_repo']
        assert len(os.listdir('test_repo')) == 2

    @pytest.mark.parametrize("branch_name", ['master', 'staging', 'testing'])
    def test_create_repository_with_custom_branch_name(self, tmpdir, git_author, datetime_objects, branch_name):
        git_repo_path = tmpdir.mkdir(branch_name).strpath
        os.chdir(git_repo_path)

        all_commits = {'test_repo': [
            datetime_objects[0],
            datetime_objects[1],
        ]}

        git = Git(
            new_repo_path=git_repo_path,
            new_repo_branch=branch_name,
            new_repo_author=git_author,
            file_ext='py',
        )
        git.create_repository()
        git.build_repository(all_commits)
        assert GitConsole.get_current_branch() == branch_name
