from datetime import timedelta, datetime, timezone


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

    def run(self, all_commits: dict[str, list[datetime]]) -> dict[str, list[datetime]]:
        ofuscate_date = self.get_obfuscate_date(all_commits[next(iter(all_commits))][0])
        for repo_name in all_commits:
            for idx, commit in enumerate(all_commits[repo_name]):
                if commit.day != ofuscate_date.day:
                    ofuscate_date = self.get_obfuscate_date(commit)

                all_commits[repo_name][idx] = ofuscate_date
                ofuscate_date += self.delta_minutes

        return all_commits
