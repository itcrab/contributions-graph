import pytest

from contributions_graph.repository_list import RepositoryList


class TestRepositoryList:
    def test_repository_list_case_1(self, repository_dicts):
        repository_list = RepositoryList()
        assert repository_list._repositories == []
        assert repository_list._position == 0
        assert repository_list._max_position == 0

        repository_list.add(**repository_dicts[0])
        assert repository_list._repositories == [repository_dicts[0]]
        assert repository_list._position == 0
        assert repository_list._max_position == 1

        repository_list.add(**repository_dicts[1])
        assert repository_list._repositories == [repository_dicts[0], repository_dicts[1]]
        assert repository_list._position == 0
        assert repository_list._max_position == 2

        repository_list.add(**repository_dicts[2])
        assert repository_list._repositories == [repository_dicts[0], repository_dicts[1], repository_dicts[2]]
        assert repository_list._position == 0
        assert repository_list._max_position == 3

    def test_repository_list_case_2(self, repository_dicts):
        repository_list = RepositoryList()
        assert repository_list._repositories == []
        assert repository_list._position == 0
        assert repository_list._max_position == 0

        repository_list.add(**repository_dicts[0])
        repository_list.add(**repository_dicts[1])
        repository_list.add(**repository_dicts[2])
        assert repository_list._repositories == [repository_dicts[0], repository_dicts[1], repository_dicts[2]]
        assert repository_list._position == 0
        assert repository_list._max_position == 3

        next(repository_list)
        assert repository_list._repositories == [repository_dicts[0], repository_dicts[1], repository_dicts[2]]
        assert repository_list._position == 1
        assert repository_list._max_position == 3

        next(repository_list)
        assert repository_list._repositories == [repository_dicts[0], repository_dicts[1], repository_dicts[2]]
        assert repository_list._position == 2
        assert repository_list._max_position == 3

        next(repository_list)
        assert repository_list._repositories == [repository_dicts[0], repository_dicts[1], repository_dicts[2]]
        assert repository_list._position == 3
        assert repository_list._max_position == 3

        with pytest.raises(StopIteration):
            next(repository_list)

    def test_repository_list_case_3(self, repository_dicts):
        repository_list = RepositoryList()
        assert repository_list._repositories == []
        assert repository_list._position == 0
        assert repository_list._max_position == 0

        repository_list.add(**repository_dicts[0])
        repository_list.add(**repository_dicts[1])
        repository_list.add(**repository_dicts[2])
        assert repository_list._repositories == [repository_dicts[0], repository_dicts[1], repository_dicts[2]]
        assert repository_list._position == 0
        assert repository_list._max_position == 3

        repository_list_values = [repository for repository in repository_list]
        assert repository_list_values == [repository_dicts[0], repository_dicts[1], repository_dicts[2]]

        assert repository_list._repositories == [repository_dicts[0], repository_dicts[1], repository_dicts[2]]
        assert repository_list._position == 3
        assert repository_list._max_position == 3

        with pytest.raises(StopIteration):
            next(repository_list)
