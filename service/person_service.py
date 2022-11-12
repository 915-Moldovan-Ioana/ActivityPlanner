from domain.person import Person
from iterable.iterable_repo import Methods


class PersonService:
    def __init__(self, person_repo, validator):
        self.__validator = validator
        self.__person_repo = person_repo

    # save_person

    def add_person(self, pid, name, phone_number):
        """
        This function adds a new person to the agenda.
        :param pid: Person's id.
        :param name: Person's name.
        :param phone_number: Person's phone number.
        :return:
        """
        person = Person(pid, name, phone_number)
        self.__validator.validate(person)
        self.__person_repo.save_person(person)

    # remove_person

    def remove_person(self, pid):
        """
        This function removes an existing person from the agenda.
        :param pid: Person's id.
        :return:
        """
        self.__person_repo.remove_person(pid)

    # update_person

    def update_person(self, pid, name, phone_number):
        """
        This function updates the person's personal information, excepts the id.
        :param pid: Person's id.
        :param name: New name.
        :param phone_number: New phone number.
        :return:
        """
        person = Person(pid, name, phone_number)
        self.__validator.validate(person)
        self.__person_repo.update_person(pid, person)

    def list_people(self):
        """
        This function returns the list of people from the agenda to later on it can be listed.
        :return: list of people
        """
        return self.__person_repo.get_all_people()

    # def find_person(self, pid):
    #     person = self.__person_repo.find_person_by_id(pid)
    #     return person

    def find_person(self, pid):
        person = self.__person_repo.find_person_by_id(pid)
        return [person.id, person.name, person.phone_number]

    def search_by_name(self, name):
        persons_list = self.__person_repo.get_all_people()
        searched_persons = Methods.global_filter(persons_list, lambda person: name in person.name.lower())
        return searched_persons

    def search_by_phone(self, phone_number):
        persons_list = self.__person_repo.get_all_people()
        searched_persons = Methods.global_filter(persons_list, lambda person: phone_number in person.phone_number)
        return searched_persons
