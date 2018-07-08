from datetime import timedelta


class Obfuscate:
    def __init__(self, start_hour, start_minute, start_second, delta_minutes):
        self.start_hour = start_hour
        self.start_minute = start_minute
        self.start_second = start_second
        self.delta_minutes = timedelta(minutes=delta_minutes)

    def get_obfuscate_date(self, commit):
        return commit.replace(
            hour=self.start_hour,
            minute=self.start_minute,
            second=self.start_second,
        )

    def run(self, all_commits):
        ofuscate_date = self.get_obfuscate_date(all_commits[0])
        for idx, commit in enumerate(all_commits):
            if commit.day != ofuscate_date.day:
                ofuscate_date = self.get_obfuscate_date(commit)

            all_commits[idx] = ofuscate_date
            ofuscate_date += self.delta_minutes

        return all_commits
