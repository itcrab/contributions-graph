from datetime import datetime

from contributions_graph.obfuscate import Obfuscate


class TestObfuscate:
    def test_get_obfuscate_date(self, datetime_first, datetime_third, tz_info_0500, tz_info_0300):
        obfuscate = Obfuscate(
            start_hour=11,
            start_minute=0,
            start_second=0,
            delta_minutes=5,
        )

        datetime_obfuscate = obfuscate.get_obfuscate_date(datetime_first)
        assert datetime_obfuscate == datetime(2018, 6, 30, 11, 0, tzinfo=tz_info_0500)

        datetime_obfuscate = obfuscate.get_obfuscate_date(datetime_third)
        assert datetime_obfuscate == datetime(2018, 7, 1, 11, 0, tzinfo=tz_info_0300)

    def test_obfuscate_case_1(self, datetime_first, datetime_second, tz_info_0500):
        obfuscate = Obfuscate(
            start_hour=11,
            start_minute=0,
            start_second=0,
            delta_minutes=5,
        )

        all_commits = [
            datetime_first,
            datetime_second
        ]
        obfuscate_commits = obfuscate.run(all_commits)
        assert obfuscate_commits == [
            datetime(2018, 6, 30, 11, 5, 0, tzinfo=tz_info_0500),
            datetime(2018, 6, 30, 11, 10, 0, tzinfo=tz_info_0500),
        ]

    def test_obfuscate_case_2(self, datetime_first, datetime_second, datetime_third, tz_info_0500, tz_info_0300):
        obfuscate = Obfuscate(
            start_hour=11,
            start_minute=0,
            start_second=0,
            delta_minutes=5,
        )

        all_commits = [
            datetime_first,
            datetime_second,
            datetime_third,
        ]
        obfuscate_commits = obfuscate.run(all_commits)
        assert obfuscate_commits == [
            datetime(2018, 6, 30, 11, 5, 0, tzinfo=tz_info_0500),
            datetime(2018, 6, 30, 11, 10, 0, tzinfo=tz_info_0500),
            datetime(2018, 7, 1, 11, 5, 0, tzinfo=tz_info_0300),
        ]

    def test_obfuscate_case_3(self, datetime_first, datetime_second, datetime_third, datetime_fourth, tz_info_0500, tz_info_0300):
        obfuscate = Obfuscate(
            start_hour=11,
            start_minute=0,
            start_second=0,
            delta_minutes=5,
        )

        all_commits = [
            datetime_first,
            datetime_second,
            datetime_third,
            datetime_fourth,
        ]
        obfuscate_commits = obfuscate.run(all_commits)
        assert obfuscate_commits == [
            datetime(2018, 6, 30, 11, 5, 0, tzinfo=tz_info_0500),
            datetime(2018, 6, 30, 11, 10, 0, tzinfo=tz_info_0500),
            datetime(2018, 7, 1, 11, 5, 0, tzinfo=tz_info_0300),
            datetime(2018, 7, 1, 11, 10, 0, tzinfo=tz_info_0300),
        ]
