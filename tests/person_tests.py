import unittest
from repository.person import PersonRepository
from service.handlers import UndoHandler
from service.person_service import PersonService
from service.undo import UndoManager
from validator.person_validator import PersonValidator, PersonValidatorException, PersonRepositoryError


class PersonTestCase(unittest.TestCase):

    def AssertIDEqual(self, person, id):
        self.assertEqual(person.id, id)

    def AssertNameEqual(self, person, name):
        self.assertEqual(person.name, name)

    def AssertPhoneEqual(self, person, phone):
        self.assertEqual(person.phone_number, phone)


class PersonTest(PersonTestCase):

    def test_add_person(self):
        person_validator = PersonValidator()
        person_repo = PersonRepository()
        person_service = PersonService(person_repo, person_validator)
        person_service.add_person(1, 'Moldovan Ioana', '0734075321')
        people = person_repo.get_all_people()
        self.AssertNameEqual(people[0], 'Moldovan Ioana')
        self.AssertPhoneEqual(people[0], '0734075321')
        self.AssertIDEqual(people[0], 1)
        try:
            person_service.add_person(1, 'Moldovan Ioana', '0734075321')
            assert False
        except PersonRepositoryError:
            assert True
        try:
            person_service.add_person(-1, 'Ioana Moldovan', '0783456223')
            assert False
        except PersonValidatorException:
            assert True
        try:
            person_service.add_person(1, '', '0783456223')
            assert False
        except PersonValidatorException:
            assert True
        try:
            person_service.add_person(1, 'Ioana Moldovan', '')
            assert False
        except PersonValidatorException:
            assert True

    def test_remove_person(self):
        person_validator = PersonValidator()
        person_repo = PersonRepository()
        person_service = PersonService(person_repo, person_validator)
        person_service.add_person(1, 'Moldovan Ioana', '0734075321')
        person_service.add_person(2, 'Moldovan Ioana', '0734075321')
        person_service.remove_person(1)
        people = person_repo.get_all_people()
        assert person_repo.get_number_people() == 1
        self.AssertIDEqual(people[0], 2)
        person_service.remove_person(2)
        assert person_repo.get_number_people() == 0
        try:
            person_service.remove_person(1)
            assert False
        except PersonRepositoryError:
            assert True

    def test_find_person(self):
        person_validator = PersonValidator()
        person_repo = PersonRepository()
        person_service = PersonService(person_repo, person_validator)
        person_service.add_person(1, 'Moldovan Ioana', '0734075321')
        person_service.add_person(2, 'Motoc Simona', '0734075321')
        found_person = person_service.find_person(1)
        assert found_person[0] == 1
        assert found_person[1] == 'Moldovan Ioana'
        assert found_person[2] == '0734075321'

    def test_update_person(self):
        person_validator = PersonValidator()
        person_repo = PersonRepository()
        person_service = PersonService(person_repo, person_validator)
        person_service.add_person(1, 'Moldovan Ioana', '0734075321')
        person_service.update_person(1, 'Motoc Simona', '0789665701')
        people = person_repo.get_all_people()
        self.AssertNameEqual(people[0], 'Motoc Simona')
        self.AssertPhoneEqual(people[0], '0789665701')
        self.AssertIDEqual(people[0], 1)
        try:
            person_service.update_person(2, 'Motoc Simona', '0789665701')
            assert False
        except PersonRepositoryError:
            assert True
        try:
            person_service.update_person(1, 'Motoc Simona', '')
            assert False
        except PersonValidatorException:
            assert True

    def test_undo_add_person(self):
        person_validator = PersonValidator()
        person_repo = PersonRepository()
        person_service = PersonService(person_repo, person_validator)
        person_service.add_person(1, 'Moldovan Ioana', '0734075321')
        UndoManager.register_operation(person_service, UndoHandler.ADD_PERSON, 1)
        person_service.add_person(2, 'Motoc Simona', '0734075111')
        UndoManager.register_operation(person_service, UndoHandler.ADD_PERSON, 2)
        people = person_repo.get_all_people()
        assert len(people) == 2
        UndoManager.undo()
        assert len(people) == 1
        self.AssertIDEqual(people[0], 1)
        UndoManager.undo()
        assert len(people) == 0

    def test_undo_remove_person(self):
        person_validator = PersonValidator()
        person_repo = PersonRepository()
        person_service = PersonService(person_repo, person_validator)
        person_service.add_person(1, 'Moldovan Ioana', '0734075321')
        person_service.add_person(2, 'Motoc Simona', '0734075111')
        person_service.remove_person(2)
        UndoManager.register_operation(person_service, UndoHandler.DELETE_PERSON, 2, 'Motoc Simona', '0734075111')
        person_service.remove_person(1)
        UndoManager.register_operation(person_service, UndoHandler.DELETE_PERSON, 1, 'Moldovan Ioana', '0734075321')
        people = person_repo.get_all_people()
        assert len(people) == 0
        UndoManager.undo()
        assert len(people) == 1
        self.AssertIDEqual(people[0], 1)
        UndoManager.undo()
        assert len(people) == 2
        self.AssertIDEqual(people[1], 2)

    def test_undo_update_person(self):
        person_validator = PersonValidator()
        person_repo = PersonRepository()
        person_service = PersonService(person_repo, person_validator)
        person_service.add_person(1, 'Moldovan Ioana', '0734075321')
        person_service.add_person(2, 'Motoc Simona', '0734075111')
        person_service.update_person(1, 'Moldovan Diana', '0789888000')
        UndoManager.register_operation(person_service, UndoHandler.UPDATE_PERSON, 1, 'Moldovan Ioana', '0734075321')
        people = person_repo.get_all_people()
        UndoManager.undo()
        self.AssertNameEqual(people[0], 'Moldovan Ioana')
        self.AssertPhoneEqual(people[0], '0734075321')

    def test_list_people(self):
        person_validator = PersonValidator()
        person_repo = PersonRepository()
        person_service = PersonService(person_repo, person_validator)
        person_service.add_person(1, 'Moldovan Ioana', '0734075321')
        person_service.add_person(2, 'Motoc Simona', '0734075111')
        people = person_repo.get_all_people()
        list_people = person_service.list_people()
        assert people == list_people

    def test_search_by_name_and_phone_person(self):
        person_validator = PersonValidator()
        person_repo = PersonRepository()
        person_service = PersonService(person_repo, person_validator)
        person_service.add_person(1, 'Moldovan Ioana', '0734075321')
        person_service.add_person(2, 'Motoc Simona', '0734075111')
        people = person_repo.get_all_people()
        first = person_service.search_by_name('Ioa')
        assert people[0] == first[0]
        second = person_service.search_by_name('Mo')
        assert people == second
        third = person_service.search_by_phone('0734')
        assert people == third
        fourth = person_service.search_by_phone('07340753211')
        assert len(fourth) == 0

    def test_check_person_existence(self):
        person_validator = PersonValidator()
        person_repo = PersonRepository()
        person_service = PersonService(person_repo, person_validator)
        person_service.add_person(1, 'Moldovan Ioana', '0734075321')
        person_service.add_person(2, 'Motoc Simona', '0734075111')
        assert person_repo.check_person_existence(1) == 1


    # def test_domain(self):
    #     person_validator = PersonValidator()
    #     person_repo = PersonRepository()
    #     person_service = PersonService(person_repo, person_validator)
    #     person_service.add_person(1, 'Moldovan Ioana', '0734075321')
    #     person_service.add_person(2, 'Motoc Simona', '0734075111')
    #     people = person_repo.get_all_people()
    #     people[0].id]



    # def __add_activity(self):
    #     self.__activity_service.add_activity(1, [1, 2], '16.11.2020', '18:40-20:00', 'Seminar')
    #     UndoManager.register_operation(self.__activity_service, UndoHandler.ADD_ACTIVITY, 1)
    #
    #     self.__activity_service.add_activity(2, [3, 5], '16.11.2020', '10:00-12:00', 'Exam')
    #     UndoManager.register_operation(self.__activity_service, UndoHandler.ADD_ACTIVITY, 2)
    #
    #     self.__activity_service.add_activity(3, [1, 2, 6], '23.12.2020', '21:20-24:00', 'Christmas party')
    #     UndoManager.register_operation(self.__activity_service, UndoHandler.ADD_ACTIVITY, 3)
    #
    # def __remove_activity(self):
    #     self.__activity_service.remove_activity(3)
    #     UndoManager.register_operation(self.__activity_service, UndoHandler.DELETE_ACTIVITY, 3, [1, 2, 6], '23.12.2020',
    #                                    '21:20-24:00', 'Christmas party')

    # try:
    #     print("all activities:")
    #     self.list_ui('activities')
    #     self.__add_activity()
    #     self.list_ui('activities')
    #     self.__remove_activity()
    #     self.list_ui('activities')
    #
    #     print("undo...")
    #     UndoManager.undo()
    #     self.list_ui('activities')
    #
    #     print("undo...")
    #     UndoManager.undo()
    #     self.list_ui('activities')
    #
    #     print("undo...")
    #     UndoManager.undo()
    #     self.list_ui('activities')
    #
    # except StoreException as se:
    #     print("exception when adding entities: ", se)
    #     traceback.print_exc()

# def test_add_person():
#     person = Person
#     person_validator = PersonValidator()
#     person_repo = PersonRepository()
#     person_service = PersonService(person_repo, person_validator)
#     assert person_repo.get_number_people() == 0
#
#     person_service.add_person(1, 'Ioana Moldovan', '0789886745')
#     assert person_repo.get_number_people() == 1
#     people = person_repo.get_all_people()
#
#     try:
#         person_service.add_person(-1, 'Ioana Moldovan', '0783456223')
#         assert False
#     except ValueError:
#         assert True
#     try:
#         person_service.add_person(-1, '', '0783456223')
#         assert False
#     except ValueError:
#         assert True
