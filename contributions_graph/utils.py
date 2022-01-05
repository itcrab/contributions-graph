from datetime import datetime, timezone


def parse_iso_8601_string_to_datetime(date_string: str) -> datetime:
    return datetime.fromisoformat(date_string).astimezone(timezone.utc)


def write_file_data(file_name: str, file_data: str, file_mode: str) -> None:
    with open(file_name, file_mode) as f:
        f.write(file_data)
