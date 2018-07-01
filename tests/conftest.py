import subprocess
from datetime import datetime
from datetime import timezone, timedelta

import pytest


@pytest.fixture
def tz_info_0500():
    return timezone(timedelta(hours=5))


@pytest.fixture
def tz_info_0300():
    return timezone(timedelta(hours=3))


@pytest.fixture
def datetime_string_first():
    return '2018-06-30T20:12:09+05:00'


@pytest.fixture
def datetime_string_second():
    return '2018-06-30T23:22:01+05:00'


@pytest.fixture
def datetime_first(tz_info_0500):
    return datetime(2018, 6, 30, 20, 12, 9, tzinfo=tz_info_0500)


@pytest.fixture
def datetime_second(tz_info_0500):
    return datetime(2018, 6, 30, 23, 22, 1, tzinfo=tz_info_0500)


@pytest.fixture
def datetime_third(tz_info_0300):
    return datetime(2018, 7, 1, 17, 43, 4, tzinfo=tz_info_0300)


@pytest.fixture
def datetime_fourth(tz_info_0300):
    return datetime(2018, 7, 1, 17, 59, 8, tzinfo=tz_info_0300)


@pytest.fixture
def repository_dict_first(tmpdir):
    return dict(
        repo_path=tmpdir,
        branch='branch-name-first',
        author='Developer Name <e-first@mail.com>',
    )


@pytest.fixture
def repository_dict_second(tmpdir):
    return dict(
        repo_path=tmpdir,
        branch='branch-name-second',
        author='Developer Name <e-second@mail.com>',
    )


@pytest.fixture
def repository_dict_third(tmpdir):
    return dict(
        repo_path=tmpdir,
        branch='branch-name-third',
        author='Developer Name <e-third@mail.com>',
    )


@pytest.fixture
def git_author():
    user_name = subprocess.check_output('git config --global user.name', universal_newlines=True).strip()
    user_email = subprocess.check_output('git config --global user.email', universal_newlines=True).strip()
    return '{} <{}>'.format(user_name, user_email)
