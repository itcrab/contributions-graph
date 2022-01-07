from datetime import datetime
from typing import TypedDict, List


class RepositoryCommitsTypedDict(TypedDict):
    author: str
    commits: List[datetime]
