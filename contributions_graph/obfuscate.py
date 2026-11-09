from collections import defaultdict
from datetime import timedelta, datetime


class Obfuscate:
    def __init__(self, start_hour: int, start_minute: int, start_second: int, delta_minutes: int) -> None:
        self.start_hour = start_hour
        self.start_minute = start_minute
        self.start_second = start_second
        self.delta_minutes = delta_minutes

        self._obfuscate_counts = defaultdict(int)

    def run(self, commit_dt: str) -> str:
        date_year = int(commit_dt[:4])
        date_month = int(commit_dt[5:7])
        date_day = int(commit_dt[8:10])
        date_tz = datetime.strptime(commit_dt[-(1 + 2 + 1 + 2):], '%z').tzinfo

        date_str = f'{date_year}-{date_month}-{date_day}'

        obfuscate_dt = datetime(date_year, date_month, date_day, self.start_hour, self.start_minute, self.start_second, tzinfo=date_tz)
        obfuscate_dt += timedelta(minutes=self.delta_minutes * self._obfuscate_counts[date_str])

        self._obfuscate_counts[date_str] += 1

        return obfuscate_dt.isoformat()
