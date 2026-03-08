from datetime import datetime
from typing import TypedDict, List


class RepositoryCommitsTypedDict(TypedDict):
    author: str
    file_ext: str
    commits: List[datetime]
