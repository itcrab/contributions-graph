from datetime import datetime, timezone, timedelta

import pytest

from contributions_graph.exceptions import DayCapacityOverflowObfuscateError
from contributions_graph.obfuscate import Obfuscate


class TestObfuscate:
    def test_get_obfuscate_date(self, datetime_objects, datetime_objects_obfuscate):
        obfuscate = Obfuscate(
            start_hour=11,
            start_minute=0,
            start_second=0,
            delta_minutes=5,
        )

        datetime_obfuscate = obfuscate.get_obfuscate_date(datetime_objects[0])
        assert datetime_obfuscate == datetime_objects_obfuscate[0]

        datetime_obfuscate = obfuscate.get_obfuscate_date(datetime_objects[2])
        assert datetime_obfuscate == datetime_objects_obfuscate[2]

    def test_obfuscate_case_1(self, datetime_objects, datetime_objects_obfuscate):
        obfuscate = Obfuscate(
            start_hour=11,
            start_minute=0,
            start_second=0,
            delta_minutes=5,
        )

        all_commits = [
            datetime_objects[0],
            datetime_objects[1]
        ]
        obfuscate_commits = obfuscate.run(all_commits)
        assert obfuscate_commits == [
            datetime_objects_obfuscate[0],
            datetime_objects_obfuscate[1],
        ]

    def test_obfuscate_case_2(self, datetime_objects, datetime_objects_obfuscate):
        obfuscate = Obfuscate(
            start_hour=11,
            start_minute=0,
            start_second=0,
            delta_minutes=5,
        )

        all_commits = [
            datetime_objects[0],
            datetime_objects[1],
            datetime_objects[2],
        ]
        obfuscate_commits = obfuscate.run(all_commits)
        assert obfuscate_commits == [
            datetime_objects_obfuscate[0],
            datetime_objects_obfuscate[1],
            datetime_objects_obfuscate[2],
        ]

    def test_obfuscate_case_3(self, datetime_objects, datetime_objects_obfuscate):
        obfuscate = Obfuscate(
            start_hour=11,
            start_minute=0,
            start_second=0,
            delta_minutes=5,
        )

        all_commits = [
            datetime_objects[0],
            datetime_objects[1],
            datetime_objects[2],
            datetime_objects[3],
        ]
        obfuscate_commits = obfuscate.run(all_commits)
        assert obfuscate_commits == [
            datetime_objects_obfuscate[0],
            datetime_objects_obfuscate[1],
            datetime_objects_obfuscate[2],
            datetime_objects_obfuscate[3],
        ]

    def test_obfuscate_case_day_max_capacity(self, datetime_objects, datetime_objects_obfuscate):
        obfuscate = Obfuscate(
            start_hour=23,
            start_minute=0,
            start_second=0,
            delta_minutes=10,
        )

        all_commits = [
            datetime(2021, 11, 14, 0, 18, 1, tzinfo=timezone(timedelta(hours=5))),
            datetime(2021, 11, 14, 0, 18, 2, tzinfo=timezone(timedelta(hours=5))),
            datetime(2021, 11, 14, 0, 18, 3, tzinfo=timezone(timedelta(hours=5))),
            datetime(2021, 11, 14, 0, 18, 4, tzinfo=timezone(timedelta(hours=5))),
            datetime(2021, 11, 14, 0, 18, 5, tzinfo=timezone(timedelta(hours=5))),
        ]
        obfuscate_commits = obfuscate.run(all_commits)
        assert obfuscate_commits == [
            datetime(2021, 11, 14, 23, 0, tzinfo=timezone.utc),
            datetime(2021, 11, 14, 23, 10, tzinfo=timezone.utc),
            datetime(2021, 11, 14, 23, 20, tzinfo=timezone.utc),
            datetime(2021, 11, 14, 23, 30, tzinfo=timezone.utc),
            datetime(2021, 11, 14, 23, 40, tzinfo=timezone.utc),
        ]

    def test_obfuscate_case_day_overflow(self, datetime_objects, datetime_objects_obfuscate):
        obfuscate = Obfuscate(
            start_hour=23,
            start_minute=0,
            start_second=0,
            delta_minutes=10,
        )

        all_commits = [
            datetime(2021, 11, 14, 0, 18, 1, tzinfo=timezone(timedelta(hours=5))),
            datetime(2021, 11, 14, 0, 18, 2, tzinfo=timezone(timedelta(hours=5))),
            datetime(2021, 11, 14, 0, 18, 3, tzinfo=timezone(timedelta(hours=5))),
            datetime(2021, 11, 14, 0, 18, 4, tzinfo=timezone(timedelta(hours=5))),
            datetime(2021, 11, 14, 0, 18, 5, tzinfo=timezone(timedelta(hours=5))),
            datetime(2021, 11, 14, 0, 18, 6, tzinfo=timezone(timedelta(hours=5))),
        ]
        with pytest.raises(DayCapacityOverflowObfuscateError) as exc:
            obfuscate.run(all_commits)
        assert str(exc.value) == 'Commit 2021-11-14 00:18:06+05:00 have overflow day 14 ' \
                                 '(next commit: 2021-11-15 00:00:00+00:00)'
