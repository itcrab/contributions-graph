import pytest

from contributions_graph.git import Git
from contributions_graph.repositories import ExportRepositories


class TestExportRepositories:
    def test_export_repositories_case_1(self, repository_dicts):
        git = Git()
        export_repositories = ExportRepositories(git=git)
        assert export_repositories._repositories == []
        assert export_repositories._position == 0
        assert export_repositories._max_position == 0

        export_repositories.add(**repository_dicts[0])
        assert export_repositories._repositories == [repository_dicts[0]]
        assert export_repositories._position == 0
        assert export_repositories._max_position == 1

        export_repositories.add(**repository_dicts[1])
        assert export_repositories._repositories == [
            repository_dicts[0],
            repository_dicts[1],
        ]
        assert export_repositories._position == 0
        assert export_repositories._max_position == 2

        export_repositories.add(**repository_dicts[2])
        assert export_repositories._repositories == [
            repository_dicts[0],
            repository_dicts[1],
            repository_dicts[2],
        ]
        assert export_repositories._position == 0
        assert export_repositories._max_position == 3

    def test_export_repositories_case_2(self, repository_dicts):
        git = Git()
        export_repositories = ExportRepositories(git=git)
        assert export_repositories._repositories == []
        assert export_repositories._position == 0
        assert export_repositories._max_position == 0

        export_repositories.add(**repository_dicts[0])
        export_repositories.add(**repository_dicts[1])
        export_repositories.add(**repository_dicts[2])
        assert export_repositories._repositories == [
            repository_dicts[0],
            repository_dicts[1],
            repository_dicts[2],
        ]
        assert export_repositories._position == 0
        assert export_repositories._max_position == 3

        next(export_repositories)
        assert export_repositories._repositories == [
            repository_dicts[0],
            repository_dicts[1],
            repository_dicts[2],
        ]
        assert export_repositories._position == 1
        assert export_repositories._max_position == 3

        next(export_repositories)
        assert export_repositories._repositories == [
            repository_dicts[0],
            repository_dicts[1],
            repository_dicts[2],
        ]
        assert export_repositories._position == 2
        assert export_repositories._max_position == 3

        next(export_repositories)
        assert export_repositories._repositories == [
            repository_dicts[0],
            repository_dicts[1],
            repository_dicts[2],
        ]
        assert export_repositories._position == 3
        assert export_repositories._max_position == 3

        with pytest.raises(StopIteration):
            next(export_repositories)

    def test_export_repositories_case_3(self, repository_dicts):
        git = Git()
        export_repositories = ExportRepositories(git=git)
        assert export_repositories._repositories == []
        assert export_repositories._position == 0
        assert export_repositories._max_position == 0

        export_repositories.add(**repository_dicts[0])
        export_repositories.add(**repository_dicts[1])
        export_repositories.add(**repository_dicts[2])
        assert export_repositories._repositories == [
            repository_dicts[0],
            repository_dicts[1],
            repository_dicts[2],
        ]
        assert export_repositories._position == 0
        assert export_repositories._max_position == 3

        export_repositories_values = [repo for repo in export_repositories]
        assert export_repositories_values == [
            repository_dicts[0],
            repository_dicts[1],
            repository_dicts[2],
        ]

        assert export_repositories._repositories == [
            repository_dicts[0],
            repository_dicts[1],
            repository_dicts[2],
        ]
        assert export_repositories._position == 3
        assert export_repositories._max_position == 3

        with pytest.raises(StopIteration):
            next(export_repositories)
