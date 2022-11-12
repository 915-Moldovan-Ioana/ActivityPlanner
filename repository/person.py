from iterable.iterable_repo import Iterable
from validator.person_validator import PersonRepositoryError


class PersonRepository:
    def __init__(self):
        self._person_list = Iterable()

    # @property
    # def person_list(self):
    #     return self.__person_list

    # @person_list.setter
    # def person_list(self, new_person_list):
    #     if isinstance(new_person_list, list) is False:
    #         raise PersonRepositoryError('The list of people was assigned an invalid data type.\n')
    #     for person in new_person_list:
    #         if isinstance(person, Person) is False:
    #             raise PersonRepositoryError('The list does not contain people.\n')
    #     self.__person_list = new_person_list

    def save_person(self, new_person):
        if new_person in self._person_list:
            raise PersonRepositoryError('This person already exists in the agenda.\n')
        self._person_list.append(new_person)

    def check_person_existence(self, searched_pid):
        id_list = [person.id for person in self._person_list]
        return searched_pid in id_list

    def find_person(self, searched_pid):
        for person in self._person_list:
            if person.id == searched_pid:
                return person
        return None

    def remove_person(self, pid_remove):
        person = self.find_person(pid_remove)
        if person is None:
            raise PersonRepositoryError('The person you are trying to delete does not exist in the agenda.\n')
        self._person_list.remove(person)

    def update_person(self, pid_to_update, new_inf):
        person_to_update = self.find_person(pid_to_update)
        if person_to_update is None:
            raise PersonRepositoryError('This person you want to update does not exist in the agenda.\n')
        person_to_update.name = new_inf.name
        person_to_update.phone_number = new_inf.phone_number

    def find_person_by_id(self, pid):
        for person in self._person_list:
            if person.id == pid:
                return person
        return None

    # def search_by_name(self, name):
    #     people = self.get_all_people()
    #     searched_people = [person for person in people if name in person.name]
    #     return searched_people

    # def search_by_phone(self, phone_number):
    #     people = self.get_all_people()
    #     searched_people = [person for person in people if phone_number in person.phone_number]
    #     return searched_people

    def get_all_people(self):
        return self._person_list

    def get_number_people(self):
        return len(self._person_list)

    def __len__(self):
        return len(self._person_list)
