from datetime import datetime
from typing import TypedDict, List


class RepositoryCommitsTypeDict(TypedDict):
    author: str
    commits: List[datetime]
