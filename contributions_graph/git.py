import os
import subprocess

from contributions_graph.exceptions import GitRepositoryExistsError
from contributions_graph.utils import generate_full_file_name, write_file_data


class Git:
    def __init__(self, new_repo_path, file_ext):
        if os.path.exists(os.path.join(new_repo_path, '.git')):
            raise GitRepositoryExistsError('Error: Git repository is exists!')

        self.new_repo_path = new_repo_path
        self.file_ext = file_ext

        self.current_path = os.getcwd()

    def get_commits(self, repo_path, branch, author):
        os.chdir(repo_path)

        os.system('git checkout {}'.format(branch))

        cmd = 'git --no-pager log --pretty="%cI" --author="{}"'.format(author)
        all_commits = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        all_commits = all_commits.splitlines()

        os.chdir(self.current_path)

        return all_commits

    def create_repository(self):
        if not os.path.exists(self.new_repo_path):
            os.mkdir(self.new_repo_path)
        os.chdir(self.new_repo_path)
        os.system('git init')

    def create_readme(self):
        file_name = 'README.md'
        file_data = '# Contribution Graph Repository'
        write_file_data(file_name, file_data)

        self.commit_file(file_name)

    def build_repository(self, all_commits):
        for commit in all_commits:
            date_string = commit.isoformat()

            file_name = self.create_file(date_string)
            self.set_current_datetime(date_string)
            self.commit_file(file_name)

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
