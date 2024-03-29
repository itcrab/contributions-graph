import os
from datetime import datetime

import pytest

from contributions_graph.utils import generate_full_file_name, write_file_data, parse_iso_8601_string_to_datetime


class TestUtils:
    def test_parse_iso_8601_string_to_datetime(self, datetime_strings, datetime_objects, datetime_objects_utc):
        for i in range(4):
            parsed_date = parse_iso_8601_string_to_datetime(datetime_strings[i])
            assert isinstance(parsed_date, datetime)
            assert parsed_date == datetime_objects_utc[i]

    @pytest.mark.parametrize("ext", ['py', 'cpp', 'java'])
    def test_generate_full_file_name(self, monkeypatch, ext):
        monkeypatch.setattr('uuid.uuid4', lambda: '2946f6aa-de86-42dc-a7e5-d6f278378741')

        full_file_name = generate_full_file_name(ext)
        assert full_file_name == f'2946f6aa-de86-42dc-a7e5-d6f278378741.{ext}'

    def test_write_file_data_case_1(self, tmpdir, datetime_strings):
        os.chdir(tmpdir.strpath)

        for i in range(2):
            file_name = f'2946f6aa-de86-42dc-a7e5-d6f27837874{i}.py'
            file_data = f'commit_datetime="{datetime_strings[i]}"'
            write_file_data(file_name, file_data)

            f = tmpdir.join(file_name)
            assert f.read() == f'commit_datetime="{datetime_strings[i]}"'
