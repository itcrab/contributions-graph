import pytest

from contributions_graph.obfuscate import Obfuscate


class TestObfuscate:
    @classmethod
    def setup_class(cls):
        cls.obfuscate = Obfuscate(
            start_hour=11,
            start_minute=0,
            start_second=0,
            delta_minutes=5,
        )

    @pytest.mark.parametrize("item_idx", [0, 1, 2, 3])
    def test_get_obfuscate_date(self, item_idx, datetime_strings, datetime_strings_obfuscate):
        commit_dt_obfuscate = self.obfuscate.run(datetime_strings[item_idx])
        assert commit_dt_obfuscate == datetime_strings_obfuscate[item_idx]
