from contributions_graph.utils import parse_iso_8601_string_to_datetime


class ContributionsGraph:
    def __init__(self, repository_list, git, obfuscate=False):
        self.repository_list = repository_list
        self.git = git
        self.obfuscate = obfuscate
    
    def run(self):
        all_commits = self.get_all_commits()
        all_commits = self.sort_commits(all_commits)

        if self.obfuscate:
            all_commits = self.obfuscate.run(all_commits)

        self.build_repo(all_commits)

    def get_all_commits(self):
        all_commits = []
        for repository in self.repository_list:
            commits = self.git.get_commits(
                repo_path=repository['repo_path'],
                branch=repository['branch'],
                author=repository['author'],
            )
            all_commits.extend(commits)

        return all_commits

    def sort_commits(self, all_commits):
        for idx, commit in enumerate(all_commits):
            all_commits[idx] = parse_iso_8601_string_to_datetime(commit)

        all_commits.sort()

        return all_commits

    def build_repo(self, all_commits):
        self.git.create_repository()
        self.git.build_repository(all_commits)
