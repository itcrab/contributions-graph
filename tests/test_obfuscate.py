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
