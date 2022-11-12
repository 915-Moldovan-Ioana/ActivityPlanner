from iterable.sort import get_next_gap


class Iterable:
    def __init__(self):
        self.__entities = []

    def __getitem__(self, index):
        return self.__entities[index]

    def __setitem__(self, index, new_item):
        self.__entities[index] = new_item

    def __delitem__(self, index):
        del self.__entities[index]

    def __iter__(self):
        self.__position = 0
        return self.__entities.__iter__()

    def __len__(self):
        return len(self.__entities)

    def append(self, item):
        self.__entities.append(item)

    def remove(self, item):
        self.__entities.remove(item)

    def clear(self):
        self.__entities.clear()

    def get_all(self):
        return self.__entities


class Methods:

    @staticmethod
    def global_filter(object_list, relation):
        # for element in object_list:
        #     if relation(element) is False:
        #         object_list.remove(element)
        index = 0
        while index < len(object_list):
            if not relation(object_list[index]):
                del object_list[index]
            else:
                index += 1
        return object_list

    @staticmethod
    def comb_sort(arr, relation):
        """
        8, 4, 1, 56, 3, -44, 23, -6, 28, 0
        gap = 10
        after shrinking gap = 10 / 1.3 = 7
        *8*, 4, 1, 56, 3, -44, 23, *-6*, 28, 0 (swap 8 and -6)
        -6, *4*, 1, 56, 3, -44, 23, 8, *28*, 0 (don't swap)
        -6, 4, *1*, 56, 3, -44, 23, 8, 28, *0* (swap 1 and 0)
        -6, 4, 0, 56, 3, -44, 23, 8, 28, 1
        new gap = 7 / 1.3 = 5
        ...
        :param arr:
        :param relation:
        :return:
        """
        n = len(arr)
        change = True
        gap = n
        swapped = True
        while change:
            change = False
            while gap != 1 or swapped == 1:
                gap = get_next_gap(gap)
                swapped = False
                for i in range(0, n - gap):
                    if not relation(arr[i], arr[i + gap]):
                        arr[i], arr[i + gap] = arr[i + gap], arr[i]
                        swapped = True
                        change = True
        return arr
