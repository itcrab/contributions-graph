import os
import subprocess
from datetime import datetime

from contributions_graph.exceptions import GitBranchNotFoundError
from contributions_graph.utils import generate_full_file_name, write_file_data


class Git:
    def __init__(self, new_repo_path, new_repo_branch, new_repo_author, file_dir, file_ext):
        self.new_repo_path = new_repo_path
        self.new_repo_branch = new_repo_branch
        self.new_repo_author = new_repo_author

        self.file_dir = file_dir
        self.file_ext = file_ext

        self.current_path = os.getcwd()

    def repository_exists(self):
        return os.path.isdir(os.path.join(self.new_repo_path, '.git'))

    def get_commits_exists(self):
        return self.get_commits(
            repo_path=self.new_repo_path,
            branch=self.new_repo_branch,
            author=self.new_repo_author,
        )

    def get_commits(self, repo_path, branch, author):
        os.chdir(repo_path)

        repo_branch = self.get_repo_branch()

        if repo_branch != branch:
            os.system('git checkout {}'.format(branch))

            selected_branch = self.get_repo_branch()
            if selected_branch != branch:
                raise GitBranchNotFoundError(
                    'Git branch "{}" not found!'.format(branch)
                )

        all_commits = self.get_all_commits(author)

        if repo_branch != branch:
            os.system('git checkout {}'.format(repo_branch))

        os.chdir(self.current_path)

        return all_commits

    def get_repo_branch(self):
        cmd = 'git branch'
        repo_branches = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        repo_branches = repo_branches.splitlines()

        repo_branch = [rb for rb in repo_branches if rb.startswith('* ')][0]
        repo_branch = repo_branch[2:]

        return repo_branch

    def get_all_commits(self, author):
        cmd = 'git --no-pager log --pretty="%cI" --author="{}"'.format(author)
        all_commits = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        all_commits = all_commits.splitlines()

        return all_commits

    def create_repository(self):
        if not os.path.isdir(self.new_repo_path):
            os.mkdir(self.new_repo_path)
        os.chdir(self.new_repo_path)
        if not self.repository_exists():
            os.system('git init')

    def create_readme(self):
        file_name = 'README.md'
        if not os.path.isfile(file_name):
            file_data = '# Contribution Graph Repository'
            write_file_data(file_name, file_data)

            self.set_current_datetime(datetime.today().isoformat())
            self.commit_file(file_name)

    def build_repository(self, all_commits):
        if not os.path.isdir(self.file_dir):
            os.mkdir(self.file_dir)
        os.chdir(self.file_dir)

        for commit in all_commits:
            date_string = commit.isoformat()

            file_name = self.create_file(date_string)
            self.set_current_datetime(date_string)
            self.commit_file(file_name)

        os.chdir(self.current_path)

    def create_file(self, date_string):
        file_name = generate_full_file_name(self.file_ext)
        file_data = 'commit_datetime="{}"'.format(date_string)
        write_file_data(file_name, file_data)

        return file_name

    def set_current_datetime(self, date_string):
        os.environ['GIT_AUTHOR_DATE'] = date_string
        os.environ['GIT_COMMITTER_DATE'] = date_string

    def commit_file(self, file_name):
        os.system('git add {}'.format(file_name))
        os.system('git commit -m "Commit file {}"'.format(file_name))
