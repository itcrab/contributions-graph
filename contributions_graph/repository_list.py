from typing import List, Iterator


class RepositoryList:
    def __init__(self) -> None:
        self._repositories: List[dict] = []
        self._position = 0
        self._max_position = 0

    def __next__(self) -> dict:
        if self._position == self._max_position:
            raise StopIteration

        repository = self._repositories[self._position]
        self._position += 1

        return repository

    def __iter__(self) -> Iterator[dict]:
        return self

    def add(self, repo_path: str, branch: str, author: str) -> None:
        self._repositories.append(dict(
            repo_path=repo_path,
            branch=branch,
            author=author,
        ))
        self._max_position += 1
