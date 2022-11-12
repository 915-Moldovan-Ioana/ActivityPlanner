import unittest

from domain.person import Person
from iterable.iterable_repo import Iterable, Methods


class CustomIterableTest(unittest.TestCase):
    def setUp(self):
        self.__custom_iterable = Iterable()
        self.__custom_iterable.append(Person(432, "Rob", "5385439843"))
        self.__custom_iterable.append(Person(843, "Joshua", "5348438993"))
        self.__custom_iterable.append(Person(439, "Andrew", "54998348"))

    def test_custom_iterable(self):
        self.assertEqual(len(self.__custom_iterable), 3)
        self.assertEqual(self.__custom_iterable[0].id, 432)
        self.assertTrue(self.__custom_iterable[1].name == "Joshua")
        self.assertFalse(self.__custom_iterable[2].phone_number == "49034833")
        self.assertTrue(Person(432, "Rob", "5385439843") in self.__custom_iterable)
        self.__custom_iterable[0] = Person(845, "Lia", "5948344334")
        self.assertTrue(Person(432, "Rob", "5385439843") not in self.__custom_iterable)
        self.assertTrue(Person(845, "Lia", "5948344334") in self.__custom_iterable)
        self.assertTrue(len(self.__custom_iterable), 3)
        del self.__custom_iterable[0]
        self.assertTrue(len(self.__custom_iterable), 2)
        self.assertFalse(Person(845, "Lia", "5948344334") in self.__custom_iterable)

        self.setUp()
        expected_list = [
            Person(432, "Rob", "5385439843"),
            Person(843, "Joshua", "5348438993"),
            Person(439, "Andrew", "54998348")
        ]
        self.assertEqual(self.__custom_iterable.get_all(), expected_list)
        self.__custom_iterable.clear()
        self.assertEqual(self.__custom_iterable.get_all(), [])

        self.setUp()
        self.assertTrue(Person(432, "Rob", "5385439843") in self.__custom_iterable)
        self.__custom_iterable.remove(Person(432, "Rob", "5385439843"))
        self.assertTrue(Person(432, "Rob", "5385439843") not in self.__custom_iterable)

        self.setUp()
        iterator = iter(self.__custom_iterable)
        self.assertEqual(next(iterator), Person(432, "Rob", "5385439843"))
        next(iterator)
        next(iterator)
        with self.assertRaises(StopIteration):
            next(iterator)


class CustomSortTest(unittest.TestCase):
    def setUp(self):
        self.__custom_iterable = Iterable()

        self.__custom_iterable.append(Person(345, "Fernando Torres", "0438755874"))
        self.__custom_iterable.append(Person(987, "Andrea Pirlo", "5834757348"))
        self.__custom_iterable.append(Person(833, "Cristiano Ronaldo", "9865349683"))
        self.__custom_iterable.append(Person(945, "Pele", "5349059403543"))
        self.__custom_iterable.append(Person(478, "Pele", "98485498543"))

    @staticmethod
    def alphabetical_order(person1, person2):
        return person1.name <= person2.name if person1.name != person2.name else person1.id < person2.id

    def test_custom_sort(self):
        sorted_custom_iterable = Methods.comb_sort(self.__custom_iterable, self.alphabetical_order)
        index = 0
        for person in sorted_custom_iterable:
            if index == 0:
                self.assertEqual(person, Person(987, "Andrea Pirlo", "5834757348"))
            elif index == 1:
                self.assertEqual(person, Person(833, "Cristiano Ronaldo", "9865349683"))
            elif index == 2:
                self.assertEqual(person, Person(345, "Fernando Torres", "0438755874"))
            elif index == 3:
                self.assertEqual(person, Person(478, "Pele", "98485498543"))
            else:
                self.assertEqual(person, Person(945, "Pele", "5349059403543"))
            index += 1


class CustomFilterTest(unittest.TestCase):
    def setUp(self):
        self.__custom_iterable = Iterable()
        self.__custom_iterable.append(Person(321, "Alex", "0547548753"))
        self.__custom_iterable.append(Person(543, "Robert", "085747833"))
        self.__custom_iterable.append(Person(679, "Mihai", "08724782549"))
        self.__custom_iterable.append(Person(958, "Karl", "0342677464"))

    @staticmethod
    def acceptance_condition_1(person):
        if len(person.phone_number) == 10:
            return True
        return False

    @staticmethod
    def acceptance_condition_2(person):
        if "a" in person.name.lower():
            return True
        return False

    def test_global_filter(self):
        filtered_list = Methods.global_filter(self.__custom_iterable, self.acceptance_condition_1)
        self.assertTrue(Person(321, "Alex", "0547548753") in filtered_list)
        self.assertTrue(Person(958, "Karl", "0342677464") in filtered_list)
        self.assertTrue(Person(679, "Mihai", "08724782549") not in filtered_list)
        self.assertTrue(Person(543, "Robert", "085747833") not in filtered_list)

        self.setUp()
        filtered_list_2 = Methods.global_filter(self.__custom_iterable, self.acceptance_condition_2)
        self.assertTrue(Person(321, "Alex", "0547548753") in filtered_list_2)
        self.assertTrue(Person(679, "Mihai", "08724782549") in filtered_list_2)
        self.assertTrue(Person(958, "Karl", "0342677464") in filtered_list_2)
        self.assertTrue(Person(543, "Robert", "085747833") not in filtered_list_2)
