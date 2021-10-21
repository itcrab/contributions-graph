from contributions_graph import Git


class GitTestMixin:
    def git_create_repository(self, new_repo_path, new_repo_author):
        git = Git(
            new_repo_path=new_repo_path,
            new_repo_branch='master',
            new_repo_author=new_repo_author,
            file_dir='all_commits',
            file_ext='py',
        )
        git.create_repository()

        return git
