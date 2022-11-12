import unittest
from iterable.filter import global_filter


def even_numbers(x):
    return x % 2 == 0


def contains_a(x):
    return True if x.find('a') != -1 else False


class FilterTest(unittest.TestCase):

    def test_filter(self):
        numbers = [1, 2, 3, 4, 5, 6, 7, 8]
        global_filter(numbers, even_numbers)
        assert numbers == [2, 4, 6, 8]
        txt = ['ioana', 'simo']
        global_filter(txt, contains_a)
        assert txt == ['ioana']
