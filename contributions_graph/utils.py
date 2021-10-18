import uuid
from datetime import datetime


def parse_iso_8601_string_to_datetime(date_string: str) -> datetime:
    date_string = '{}{}'.format(date_string[:-3], date_string[-2:])
    return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%z')


def generate_full_file_name(file_ext: str) -> str:
    return '{}.{}'.format(uuid.uuid4(), file_ext)


def write_file_data(file_name: str, file_data: str) -> None:
    with open(file_name, 'w') as f:
        f.write(file_data)
