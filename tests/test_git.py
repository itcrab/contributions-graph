import os

import pytest

from contributions_graph.exceptions import GitBranchNotFoundError
from contributions_graph.git import GitConsole, GitRepositorySwitch, Git
from tests.helpers import git_create_repository


class TestGit:
    def test_get_commits(self, tmpdir, git_author, datetime_objects, datetime_objects_utc):
        git_repo_path = tmpdir.mkdir('get_commits').strpath
        os.chdir(git_repo_path)

        import_repository = git_create_repository(repo_path=git_repo_path, repo_author=git_author)
        export_commits = {'test_repo': {'author': git_author, 'file_ext': 'py', 'commits': [
            datetime_objects[0],
            datetime_objects[1],
        ]}}
        import_repository._apply_export_commits(export_commits)

        git = Git()
        with GitRepositorySwitch(new_repo_path=git_repo_path, new_repo_branch='master'):
            export_commits = git.get_commits(author=git_author)

        assert export_commits == [datetime_objects_utc[1], datetime_objects_utc[0]]

    def test_get_commits_with_different_base_branch(self, tmpdir, git_author, datetime_objects, datetime_objects_utc):
        git_repo_path = tmpdir.mkdir('get_commits').strpath
        os.chdir(git_repo_path)

        import_repository = git_create_repository(repo_path=git_repo_path, repo_author=git_author)
        export_commits = {'test_repo': {'author': git_author, 'file_ext': 'py', 'commits': [
            datetime_objects[0],
            datetime_objects[1],
        ]}}
        import_repository._apply_export_commits(export_commits)

        GitConsole.create_branch('new-branch')
        assert GitConsole.get_current_branch() == 'new-branch'

        git = Git()
        with GitRepositorySwitch(new_repo_path=git_repo_path, new_repo_branch='master'):
            export_commits = git.get_commits(author=git_author)

            assert GitConsole.get_current_branch() == 'master'
            assert export_commits == [datetime_objects_utc[1], datetime_objects_utc[0]]

    def test_get_commits_with_read_only_master_commits_case_1(self, tmpdir, git_author, datetime_objects,
                                                              datetime_objects_utc):
        git_repo_path = tmpdir.mkdir('get_commits').strpath
        os.chdir(git_repo_path)

        import_repository = git_create_repository(repo_path=git_repo_path, repo_author=git_author)

        export_commits = {'test_repo': {'author': git_author, 'file_ext': 'py', 'commits': [
            datetime_objects[0],
        ]}}
        import_repository._apply_export_commits(export_commits)

        GitConsole.create_branch('new-branch')

        export_commits = {'test_repo': {'author': git_author, 'file_ext': 'py', 'commits': [
            datetime_objects[1],
        ]}}
        import_repository._apply_export_commits(export_commits)

        GitConsole.switch_branch('master')

        export_commits = {'test_repo': {'author': git_author, 'file_ext': 'py', 'commits': [
            datetime_objects[2],
        ]}}
        import_repository._apply_export_commits(export_commits)

        git = Git()
        with GitRepositorySwitch(new_repo_path=git_repo_path, new_repo_branch='master'):
            export_commits = git.get_commits(author=git_author)

        assert export_commits == [datetime_objects_utc[2], datetime_objects_utc[0]]

    def test_get_commits_with_read_only_master_commits_case_2(self, tmpdir, git_author, datetime_objects,
                                                              datetime_objects_utc):
        git_repo_path = tmpdir.mkdir('get_commits').strpath
        os.chdir(git_repo_path)

        import_repository = git_create_repository(repo_path=git_repo_path, repo_author=git_author)

        export_commits = {'test_repo': {'author': git_author, 'file_ext': 'py', 'commits': [
            datetime_objects[0],
        ]}}
        import_repository._apply_export_commits(export_commits)

        GitConsole.create_branch('new-branch')

        export_commits = {'test_repo': {'author': git_author, 'file_ext': 'py', 'commits': [
            datetime_objects[1],
            datetime_objects[2],
            datetime_objects[3],
        ]}}
        import_repository._apply_export_commits(export_commits)

        git = Git()
        with GitRepositorySwitch(new_repo_path=git_repo_path, new_repo_branch='master'):
            export_commits = git.get_commits(author=git_author)

        assert export_commits == [datetime_objects_utc[0]]

    def test_get_commits_with_read_only_master_commits_case_3(self, tmpdir, git_author, datetime_objects,
                                                              datetime_objects_utc):
        git_repo_path = tmpdir.mkdir('get_commits').strpath
        os.chdir(git_repo_path)

        import_repository = git_create_repository(repo_path=git_repo_path, repo_author=git_author)

        GitConsole.create_branch('new-branch')

        export_commits = {'test_repo': {'author': git_author, 'file_ext': 'py', 'commits': [
            datetime_objects[0],
        ]}}
        import_repository._apply_export_commits(export_commits)

        GitConsole.create_branch('master')

        export_commits = {'test_repo': {'author': git_author, 'file_ext': 'py', 'commits': [
            datetime_objects[1],
            datetime_objects[2],
        ]}}
        import_repository._apply_export_commits(export_commits)

        git = Git()
        with GitRepositorySwitch(new_repo_path=git_repo_path, new_repo_branch='master'):
            export_commits = git.get_commits(author=git_author)

        assert export_commits == [datetime_objects_utc[2], datetime_objects_utc[1], datetime_objects_utc[0]]

    def test_get_commits_with_read_only_new_branch_commits_case_1(self, tmpdir, git_author, datetime_objects,
                                                                  datetime_objects_utc):
        git_repo_path = tmpdir.mkdir('get_commits').strpath
        os.chdir(git_repo_path)

        import_repository = git_create_repository(repo_path=git_repo_path, repo_author=git_author)

        GitConsole.create_branch('new-branch')

        export_commits = {'test_repo': {'author': git_author, 'file_ext': 'py', 'commits': [
            datetime_objects[0],
        ]}}
        import_repository._apply_export_commits(export_commits)

        GitConsole.create_branch('master')

        export_commits = {'test_repo': {'author': git_author, 'file_ext': 'py', 'commits': [
            datetime_objects[1],
            datetime_objects[2],
        ]}}
        import_repository._apply_export_commits(export_commits)

        git = Git()
        with GitRepositorySwitch(new_repo_path=git_repo_path, new_repo_branch='new-branch'):
            export_commits = git.get_commits(author=git_author)

        assert export_commits == [datetime_objects_utc[0]]

    def test_get_commits_with_read_only_new_branch_commits_case_2(self, tmpdir, git_author, datetime_objects,
                                                                  datetime_objects_utc):
        git_repo_path = tmpdir.mkdir('get_commits').strpath
        os.chdir(git_repo_path)

        import_repository = git_create_repository(repo_path=git_repo_path, repo_author=git_author)

        export_commits = {'test_repo': {'author': git_author, 'file_ext': 'py', 'commits': [
            datetime_objects[0],
        ]}}
        import_repository._apply_export_commits(export_commits)

        GitConsole.create_branch('new-branch')

        export_commits = {'test_repo': {'author': git_author, 'file_ext': 'py', 'commits': [
            datetime_objects[1],
        ]}}
        import_repository._apply_export_commits(export_commits)

        GitConsole.switch_branch('master')

        export_commits = {'test_repo': {'author': git_author, 'file_ext': 'py', 'commits': [
            datetime_objects[2],
        ]}}
        import_repository._apply_export_commits(export_commits)

        git = Git()
        with GitRepositorySwitch(new_repo_path=git_repo_path, new_repo_branch='new-branch'):
            export_commits = git.get_commits(author=git_author)

        assert export_commits == [datetime_objects_utc[1], datetime_objects_utc[0]]

    def test_get_commits_with_wrong_branch(self, tmpdir, datetime_objects, git_author):
        git_repo_path = tmpdir.mkdir('get_commits').strpath
        os.chdir(git_repo_path)

        import_repository = git_create_repository(repo_path=git_repo_path, repo_author=git_author)
        export_commits = {'test_repo': {'author': git_author, 'file_ext': 'py', 'commits': [
            datetime_objects[0],
            datetime_objects[1],
        ]}}
        import_repository._apply_export_commits(export_commits)

        git = Git()
        with pytest.raises(GitBranchNotFoundError):
            with GitRepositorySwitch(new_repo_path=git_repo_path, new_repo_branch='wrong-branch'):
                git.get_commits()

    def test_create_repository(self, tmpdir, git_author):
        new_repo_path = tmpdir.strpath
        git_repo_path = os.path.join(new_repo_path, '.git')

        assert os.path.isdir(git_repo_path) is False
        git_create_repository(
            repo_path=new_repo_path,
            repo_branch='master',
            repo_author=git_author,
        )
        assert os.path.isdir(git_repo_path) is True

    def test_create_repository_with_wrong_path(self, tmpdir, git_author):
        new_repo_path = os.path.join(tmpdir.strpath, 'wrong')
        git_repo_path = new_repo_path

        assert os.path.isdir(git_repo_path) is False
        git_create_repository(
            repo_path=new_repo_path,
            repo_branch='master',
            repo_author=git_author,
        )
        assert os.path.isdir(git_repo_path) is True

    def test_build_repository(self, tmpdir, datetime_objects, git_author):
        git_repo_path = tmpdir.mkdir('build_git_repository').strpath
        os.chdir(git_repo_path)

        export_commits = {'test_repo': {'author': git_author, 'file_ext': 'py', 'commits': [
            datetime_objects[0],
            datetime_objects[1],
        ]}}

        import_repository = git_create_repository(repo_path=git_repo_path, repo_author=git_author)
        import_repository._apply_export_commits(export_commits)

        git = Git()
        export_commits = git.get_commits(git_author)

        assert export_commits == [datetime_objects[1], datetime_objects[0]]
        assert os.path.isfile('test_repo.py') is True

        committers = GitConsole.get_committers()
        assert committers == [git_author, git_author]

    @pytest.mark.parametrize("branch_name", ['master', 'staging', 'testing'])
    def test_create_repository_with_custom_branch_name(self, tmpdir, git_author, datetime_objects, branch_name):
        git_repo_path = tmpdir.mkdir(branch_name).strpath
        os.chdir(git_repo_path)

        export_commits = {'test_repo': {'author': git_author, 'file_ext': 'py', 'commits': [
            datetime_objects[0],
            datetime_objects[1],
        ]}}

        import_repository = git_create_repository(
            repo_path=git_repo_path,
            repo_branch=branch_name,
            repo_author=git_author,
        )
        import_repository._apply_export_commits(export_commits)
        assert GitConsole.get_current_branch() == branch_name
