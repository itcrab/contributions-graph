import pytest

from contributions_graph.repository_list import RepositoryList


class TestRepositoryList:
    def test_repository_list_case_1(self, repository_dict_first, repository_dict_second, repository_dict_third):
        repository_list = RepositoryList()
        assert repository_list._repositories == []
        assert repository_list._position == 0
        assert repository_list._max_position == 0

        repository_list.add(**repository_dict_first)
        assert repository_list._repositories == [repository_dict_first]
        assert repository_list._position == 0
        assert repository_list._max_position == 1

        repository_list.add(**repository_dict_second)
        assert repository_list._repositories == [repository_dict_first, repository_dict_second]
        assert repository_list._position == 0
        assert repository_list._max_position == 2

        repository_list.add(**repository_dict_third)
        assert repository_list._repositories == [repository_dict_first, repository_dict_second, repository_dict_third]
        assert repository_list._position == 0
        assert repository_list._max_position == 3

    def test_repository_list_case_2(self, repository_dict_first, repository_dict_second, repository_dict_third):
        repository_list = RepositoryList()
        assert repository_list._repositories == []
        assert repository_list._position == 0
        assert repository_list._max_position == 0

        repository_list.add(**repository_dict_first)
        repository_list.add(**repository_dict_second)
        repository_list.add(**repository_dict_third)
        assert repository_list._repositories == [repository_dict_first, repository_dict_second, repository_dict_third]
        assert repository_list._position == 0
        assert repository_list._max_position == 3

        next(repository_list)
        assert repository_list._repositories == [repository_dict_first, repository_dict_second, repository_dict_third]
        assert repository_list._position == 1
        assert repository_list._max_position == 3

        next(repository_list)
        assert repository_list._repositories == [repository_dict_first, repository_dict_second, repository_dict_third]
        assert repository_list._position == 2
        assert repository_list._max_position == 3

        next(repository_list)
        assert repository_list._repositories == [repository_dict_first, repository_dict_second, repository_dict_third]
        assert repository_list._position == 3
        assert repository_list._max_position == 3

        with pytest.raises(StopIteration):
            next(repository_list)

    def test_repository_list_case_3(self, repository_dict_first, repository_dict_second, repository_dict_third):
        repository_list = RepositoryList()
        assert repository_list._repositories == []
        assert repository_list._position == 0
        assert repository_list._max_position == 0

        repository_list.add(**repository_dict_first)
        repository_list.add(**repository_dict_second)
        repository_list.add(**repository_dict_third)
        assert repository_list._repositories == [repository_dict_first, repository_dict_second, repository_dict_third]
        assert repository_list._position == 0
        assert repository_list._max_position == 3

        repository_list_values = [repository for repository in repository_list]
        assert repository_list_values == [repository_dict_first, repository_dict_second, repository_dict_third]

        assert repository_list._repositories == [repository_dict_first, repository_dict_second, repository_dict_third]
        assert repository_list._position == 3
        assert repository_list._max_position == 3

        with pytest.raises(StopIteration):
            next(repository_list)
