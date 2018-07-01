import uuid
from datetime import datetime


def parse_iso_8601_string_to_datetime(date_string):
    date_string = '{}{}'.format(date_string[:-3], date_string[-2:])
    return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%z')


def generate_full_file_name(file_ext):
    return '{}.{}'.format(uuid.uuid4(), file_ext)


def write_file_data(file_name, date_string):
    with open(file_name, 'w') as f:
        f.write('commit_datetime="{}"'.format(date_string))
