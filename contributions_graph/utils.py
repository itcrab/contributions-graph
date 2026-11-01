import uuid
from datetime import datetime, timezone


def parse_iso_8601_string_to_datetime(date_string: str) -> datetime:
    return datetime.fromisoformat(date_string).astimezone(timezone.utc)


def generate_full_file_name(file_ext: str) -> str:
    return '{}.{}'.format(uuid.uuid4(), file_ext)


def write_file_data(file_name: str, file_data: str) -> None:
    with open(file_name, 'w') as f:
        f.write(file_data)
