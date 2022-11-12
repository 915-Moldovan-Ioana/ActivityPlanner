import unittest
from iterable.sort import comb_sort


def smaller_or_equal(x, y):
    return x <= y


def greater_or_equal(x, y):
    return x >= y


class SortTest(unittest.TestCase):

    def test_sort(self):
        object_list = [4, 5, 1, 12, 7, 15]
        relation = smaller_or_equal
        comb_sort(object_list, relation)
        assert object_list == [1, 4, 5, 7, 12, 15]
        object_list = [4, 5, 1, 12, 7, 15]
        relation_2 = greater_or_equal
        comb_sort(object_list, relation_2)
        assert object_list == [15, 12, 7, 5, 4, 1]
