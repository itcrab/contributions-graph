import os
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
def tz_info_utc():
    return timezone.utc


@pytest.fixture
def datetime_objects(tz_info_0500, tz_info_0300):
    return [
        datetime(2018, 6, 30, 20, 12, 9, tzinfo=tz_info_0500),
        datetime(2018, 6, 30, 23, 22, 1, tzinfo=tz_info_0500),
        datetime(2018, 7, 1, 17, 43, 4, tzinfo=tz_info_0300),
        datetime(2018, 7, 1, 17, 59, 8, tzinfo=tz_info_0300),
    ]


@pytest.fixture
def datetime_strings(datetime_objects):
    return [dt.isoformat() for dt in datetime_objects]


@pytest.fixture
def datetime_objects_utc(tz_info_utc):
    return [
        datetime(2018, 6, 30, 15, 12, 9, tzinfo=tz_info_utc),
        datetime(2018, 6, 30, 18, 22, 1, tzinfo=tz_info_utc),
        datetime(2018, 7, 1, 14, 43, 4, tzinfo=tz_info_utc),
        datetime(2018, 7, 1, 14, 59, 8, tzinfo=tz_info_utc),
    ]


@pytest.fixture
def datetime_strings_utc(datetime_objects_utc):
    return [dt.isoformat() for dt in datetime_objects_utc]


@pytest.fixture
def datetime_objects_obfuscate(tz_info_utc):
    return [
        datetime(2018, 6, 30, 11, 0, 0, tzinfo=tz_info_utc),
        datetime(2018, 6, 30, 11, 5, 0, tzinfo=tz_info_utc),
        datetime(2018, 7, 1, 11, 0, 0, tzinfo=tz_info_utc),
        datetime(2018, 7, 1, 11, 5, 0, tzinfo=tz_info_utc),
    ]


@pytest.fixture
def datetime_strings_obfuscate(datetime_objects_obfuscate):
    return [dt.isoformat() for dt in datetime_objects_obfuscate]


@pytest.fixture
def repository_dicts(tmpdir):
    return [
        dict(
            repo_path=tmpdir,
            branch='branch-name-first',
            author='Developer Name <e-first@mail.com>',
        ),
        dict(
            repo_path=tmpdir,
            branch='branch-name-second',
            author='Developer Name <e-second@mail.com>',
        ),
        dict(
            repo_path=tmpdir,
            branch='branch-name-third',
            author='Developer Name <e-third@mail.com>',
        )
    ]


@pytest.fixture
def git_author():
    user_name = 'Arcady Usov'
    user_email = 'arcady.usov@example.email.com'

    os.environ['GIT_AUTHOR_NAME'] = user_name
    os.environ['GIT_AUTHOR_EMAIL'] = user_email

    return f'{user_name} <{user_email}>'
