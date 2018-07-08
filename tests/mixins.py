import subprocess


class GitTestMixin:
    def git_commit_file(self, git, datetime_string):
        file_name = git.create_file(datetime_string)
        git.set_current_datetime(datetime_string)
        git.commit_file(file_name)

    def git_log_commits(self, git_author):
        cmd = 'git --no-pager log --pretty="%cI" --author="{}"'.format(git_author)
        all_commits = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        all_commits = all_commits.splitlines()

        return all_commits
