from typing import List, Iterator, Dict


class RepositoryList:
    def __init__(self) -> None:
        self._repositories: List[Dict[str, str]] = []
        self._position = 0
        self._max_position = 0

        self.import_repo: Dict[str, str] = dict()

    def __next__(self) -> dict:
        if self._position == self._max_position:
            raise StopIteration

        repository = self._repositories[self._position]
        self._position += 1

        return repository

    def __iter__(self) -> Iterator[dict]:
        return self

    def export_from(self, repo_path: str, branch: str, author: str, file_ext: str) -> None:
        self._repositories.append(dict(
            repo_path=repo_path,
            branch=branch,
            author=author,
            file_ext=file_ext,
        ))
        self._max_position += 1

    def import_to(self, new_repo_path: str, new_repo_branch: str, new_repo_author: str) -> None:
        self.import_repo = dict(
            new_repo_path=new_repo_path,
            new_repo_branch=new_repo_branch,
            new_repo_author=new_repo_author,
        )
