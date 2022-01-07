from datetime import timedelta, datetime, timezone
from typing import Dict

from contributions_graph.exceptions import DayCapacityOverflowObfuscateError
from contributions_graph.typing import RepositoryCommitsTypedDict


class Obfuscate:
    def __init__(self, start_hour: int, start_minute: int, start_second: int, delta_minutes: int) -> None:
        self.start_hour = start_hour
        self.start_minute = start_minute
        self.start_second = start_second
        self.delta_minutes = timedelta(minutes=delta_minutes)

    def get_obfuscate_date(self, commit: datetime) -> datetime:
        return commit.replace(
            hour=self.start_hour,
            minute=self.start_minute,
            second=self.start_second,
            tzinfo=timezone.utc,
        )

    def run(self, all_commits: Dict[str, RepositoryCommitsTypedDict]) -> Dict[str, RepositoryCommitsTypedDict]:
        for repo_name in all_commits.keys():
            obfuscate_date = self.get_obfuscate_date(all_commits[repo_name]['commits'][0])
            for idx, commit in enumerate(all_commits[repo_name]['commits']):
                if commit.day != obfuscate_date.day:
                    obfuscate_date = self.get_obfuscate_date(commit)

                all_commits[repo_name]['commits'][idx] = obfuscate_date
                obfuscate_date += self.delta_minutes
                if obfuscate_date.day != commit.day:
                    raise DayCapacityOverflowObfuscateError(
                        f'Commit {commit} have overflow day {commit.day} (next commit: {obfuscate_date})'
                    )

        return all_commits
