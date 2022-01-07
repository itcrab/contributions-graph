from contributions_graph import Git


class GitTestMixin:
    def git_create_repository(self, new_repo_path, new_repo_author, new_repo_branch='master'):
        git = Git(
            file_ext='py',
        )
        git.create_repository(
            new_repo_path=new_repo_path,
            new_repo_branch=new_repo_branch,
            new_repo_author=new_repo_author,
        )

        return git
