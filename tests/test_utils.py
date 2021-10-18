import os
from datetime import datetime

from contributions_graph.utils import generate_full_file_name, write_file_data, parse_iso_8601_string_to_datetime


class TestUtils:
    def test_parse_iso_8601_string_to_datetime_case_1(self, datetime_strings, datetime_objects):
        parsed_date = parse_iso_8601_string_to_datetime(datetime_strings[0])
        assert isinstance(parsed_date, datetime)
        assert parsed_date == datetime_objects[0]

    def test_parse_iso_8601_string_to_datetime_case_2(self, datetime_strings, datetime_objects):
        parsed_date = parse_iso_8601_string_to_datetime(datetime_strings[1])
        assert isinstance(parsed_date, datetime)
        assert parsed_date == datetime_objects[1]

    def test_parse_iso_8601_string_to_datetime_case_3(self, datetime_strings, datetime_objects):
        parsed_date = parse_iso_8601_string_to_datetime(datetime_strings[2])
        assert isinstance(parsed_date, datetime)
        assert parsed_date == datetime_objects[2]

    def test_parse_iso_8601_string_to_datetime_case_4(self, datetime_strings, datetime_objects):
        parsed_date = parse_iso_8601_string_to_datetime(datetime_strings[3])
        assert isinstance(parsed_date, datetime)
        assert parsed_date == datetime_objects[3]

    def test_generate_full_file_name_case_1(self, monkeypatch):
        monkeypatch.setattr('uuid.uuid4', lambda: '2946f6aa-de86-42dc-a7e5-d6f278378741')

        full_file_name = generate_full_file_name('py')
        assert full_file_name == '2946f6aa-de86-42dc-a7e5-d6f278378741.py'

    def test_generate_full_file_name_case_2(self, monkeypatch):
        monkeypatch.setattr('uuid.uuid4', lambda: '2946f6aa-de86-42dc-a7e5-d6f278378742')

        full_file_name = generate_full_file_name('cpp')
        assert full_file_name == '2946f6aa-de86-42dc-a7e5-d6f278378742.cpp'

    def test_write_file_data_case_1(self, tmpdir, datetime_strings):
        os.chdir(tmpdir.strpath)

        file_name = '2946f6aa-de86-42dc-a7e5-d6f278378741.py'
        file_data = 'commit_datetime="{}"'.format(datetime_strings[0])
        write_file_data(file_name, file_data)

        f = tmpdir.join(file_name)
        assert f.read() == 'commit_datetime="2018-06-30T20:12:09+05:00"'

    def test_write_file_data_case_2(self, tmpdir, datetime_strings):
        os.chdir(tmpdir.strpath)

        file_name = '2946f6aa-de86-42dc-a7e5-d6f278378742.py'
        file_data = 'commit_datetime="{}"'.format(datetime_strings[1])
        write_file_data(file_name, file_data)

        f = tmpdir.join(file_name)
        assert f.read() == 'commit_datetime="2018-06-30T23:22:01+05:00"'
