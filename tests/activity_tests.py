import unittest
from repository.activity import ActivityRepository
from service.activity_service import ActivityService
from service.handlers import UndoHandler
from service.undo import UndoManager
from validator.activity_validator import ActivityValidator, ActivityRepositoryError, ActivityValidatorException


class ActivityTestCase(unittest.TestCase):

    def AssertAIDEqual(self, activity, aid):
        self.assertEqual(activity.aid, aid)

    def AssertPIDEqual(self, activity, pid):
        self.assertEqual(activity.pid, pid)

    def AssertDateEqual(self, activity, date):
        self.assertEqual(activity.date, date)

    def AssertTimeEqual(self, activity, time):
        self.assertEqual(activity.time, time)

    def AssertDescriptionEqual(self, activity, description):
        self.assertEqual(activity.description, description)


class ActivityTest(ActivityTestCase):

    def test_add_activity(self):
        activity_validator = ActivityValidator()
        activity_repo = ActivityRepository()
        activity_service = ActivityService(activity_repo, activity_validator)
        assert activity_repo.get_number_activities() == 0
        activity_service.add_activity(1, [1, 2], '21.11.2020', '20:00-21:00', 'party la simona')
        assert activity_repo.get_number_activities() == 1
        activities = activity_repo.get_all_activities()
        self.AssertAIDEqual(activities[0], 1)
        self.AssertPIDEqual(activities[0], [1, 2])
        self.AssertDateEqual(activities[0], '21.11.2020')
        self.AssertTimeEqual(activities[0], '20:00-21:00')
        self.AssertDescriptionEqual(activities[0], 'party la simona')
        try:
            activity_service.add_activity(1, [1, 2, 3], '11.09.2019', '12:00-13:00', 'pizza')
            assert False
        except ActivityRepositoryError:
            assert True

        try:
            activity_service.add_activity(-4, [1, 2, 3], '33.19.2060', '13:00-14:00', 'pizza')
            assert False
        except ActivityValidatorException:
            assert True

    def test_remove_activity(self):
        activity_validator = ActivityValidator()
        activity_repo = ActivityRepository()
        activity_service = ActivityService(activity_repo, activity_validator)
        activity_service.add_activity(1, [1, 2], '21.11.2020', '20:00-21:00', 'party la simona')
        activity_service.add_activity(2, [2, 3], '24.12.2020', '12:00-13:00', 'Craciun')
        list = activity_service.list_activities()
        self.AssertAIDEqual(list[0], 1)
        self.AssertAIDEqual(list[1], 2)
        activity_service.remove_activity(1)
        activities = activity_repo.get_all_activities()
        assert activity_repo.get_number_activities() == 1
        self.AssertAIDEqual(activities[0], 2)
        try:
            activity_service.remove_activity(3)
            assert False
        except ActivityRepositoryError:
            assert True

    def test_update_activity(self):
        activity_validator = ActivityValidator()
        activity_repo = ActivityRepository()
        activity_service = ActivityService(activity_repo, activity_validator)
        activity_service.add_activity(1, [1, 2], '21.11.2020', '20:00-21:00', 'party la simona')
        activity_service.update_activity(1, [2, 3], '22.11.2020', '22:30-23:00', 'bere')
        activities = activity_repo.get_all_activities()
        self.AssertPIDEqual(activities[0], [2, 3])
        self.AssertDateEqual(activities[0], '22.11.2020')
        self.AssertTimeEqual(activities[0], '22:30-23:00')
        self.AssertDescriptionEqual(activities[0], 'bere')
        try:
            activity_service.update_activity(2, [2, 3], '22.11.2020', '22:30-23:00', 'bere')
            assert False
        except ActivityRepositoryError:
            assert True

    def test_search_by_date(self):
        activity_validator = ActivityValidator()
        activity_repo = ActivityRepository()
        activity_service = ActivityService(activity_repo, activity_validator)
        assert activity_repo.get_number_activities() == 0
        activity_service.add_activity(1, [1, 2], '21.11.2020', '20:00-21:00', 'party la simona')
        activity_service.add_activity(2, [1, 2, 3], '11.09.2019', '12:00-13:00', 'pizza')
        searched_activities = activity_service.search_by_date('11')
        self.AssertAIDEqual(searched_activities[0], 1)
        self.AssertAIDEqual(searched_activities[1], 2)

    def test_search_by_description(self):
        activity_validator = ActivityValidator()
        activity_repo = ActivityRepository()
        activity_service = ActivityService(activity_repo, activity_validator)
        assert activity_repo.get_number_activities() == 0
        activity_service.add_activity(1, [1, 2], '21.11.2020', '20:00-21:00', 'party la simona')
        activity_service.add_activity(2, [1, 2, 3], '11.09.2019', '12:00-13:00', 'pizza')
        searched_activities = activity_service.search_by_description('pi')
        self.AssertAIDEqual(searched_activities[0], 2)

    def test_sort(self):
        activity_validator = ActivityValidator()
        activity_repo = ActivityRepository()
        activity_service = ActivityService(activity_repo, activity_validator)
        activity_service.add_activity(1, [1, 2], '21.11.2020', '20:00-21:00', 'party la simona')
        activity_service.add_activity(2, [1, 2, 3], '11.09.2019', '12:00-12:30', 'pizza')
        activity_service.add_activity(3, [1, 2, 3], '11.09.2019', '12:40-14:00', 'pizza')
        activities = activity_repo.get_all_activities()
        sorted_activities = activity_service.sort_activities_by_time(activities)
        self.AssertAIDEqual(sorted_activities[0], 2)
        self.AssertAIDEqual(sorted_activities[1], 3)
        self.AssertAIDEqual(sorted_activities[2], 1)

    def test_activity_with(self):
        activity_validator = ActivityValidator()
        activity_repo = ActivityRepository()
        activity_service = ActivityService(activity_repo, activity_validator)
        activity_service.add_activity(1, [1, 2], '21.11.2020', '20:00-21:00', 'party la simona')
        activity_service.add_activity(2, [1, 2, 3], '11.09.2019', '12:00-12:30', 'pizza')
        activity_service.add_activity(3, [1, 2, 3], '11.09.2019', '12:40-14:00', 'pizza')
        activities = activity_service.activity_with(3)
        self.AssertAIDEqual(activities[0], 2)
        self.AssertAIDEqual(activities[1], 3)

    def test_busiest_days(self):
        activity_validator = ActivityValidator()
        activity_repo = ActivityRepository()
        activity_service = ActivityService(activity_repo, activity_validator)
        activity_service.add_activity(1, [1, 2], '21.11.2020', '20:00-21:00', 'party la simona')
        activity_service.add_activity(2, [1, 2, 3], '11.09.2019', '12:00-12:30', 'pizza')
        activity_service.add_activity(3, [1, 2, 3], '11.09.2019', '12:40-13:00', 'pizza')
        dates = activity_service.busiest_days()
        assert dates[0] == {'date': '21.11.2020', 'busy_time': 1}

    def test_find_undo(self):
        activity_validator = ActivityValidator()
        activity_repo = ActivityRepository()
        activity_service = ActivityService(activity_repo, activity_validator)
        activity_service.add_activity(1, [1, 2], '21.11.2020', '20:00-21:00', 'party la simona')
        activity_service.add_activity(2, [1, 2, 3], '11.09.2019', '12:00-12:30', 'pizza')
        activity_service.add_activity(3, [1, 2, 3], '11.09.2019', '12:40-13:00', 'pizza')
        activity = activity_service.find_activity_for_undo(1)
        assert activity[0] == 1
        assert activity[1] == [1, 2]
        assert activity[2] == '21.11.2020'
        assert activity[3] == '20:00-21:00'
        assert activity[4] == 'party la simona'

    def test_undo_add_activity(self):
        activity_validator = ActivityValidator()
        activity_repo = ActivityRepository()
        activity_service = ActivityService(activity_repo, activity_validator)
        activity_service.add_activity(1, [1, 2], '21.11.2020', '20:00-21:00', 'party la simona')
        UndoManager.register_operation(activity_service, UndoHandler.ADD_ACTIVITY, 1)
        activity_service.add_activity(2, [1, 2, 3], '11.09.2019', '12:00-12:30', 'pizza')
        UndoManager.register_operation(activity_service, UndoHandler.ADD_ACTIVITY, 2)
        activities = activity_repo.get_all_activities()
        assert len(activities) == 2
        UndoManager.undo()
        assert len(activities) == 1
        UndoManager.undo()
        assert len(activities) == 0

    def test_undo_remove_activity(self):
        activity_validator = ActivityValidator()
        activity_repo = ActivityRepository()
        activity_service = ActivityService(activity_repo, activity_validator)
        activity_service.add_activity(1, [1, 2], '21.11.2020', '20:00-21:00', 'party la simona')
        activity_service.add_activity(2, [1, 2, 3], '11.09.2019', '12:00-12:30', 'pizza')
        activity_service.remove_activity(2)
        activity_service.remove_activity(1)
        UndoManager.register_operation(activity_service, UndoHandler.DELETE_ACTIVITY, 2, [1, 2, 3], '11.09.2019',
                                       '12:00-12:30', 'pizza')
        UndoManager.register_operation(activity_service, UndoHandler.DELETE_ACTIVITY, 1, [1, 2], '21.11.2020',
                                       '20:00-21:00', 'party la simona')
        activities = activity_repo.get_all_activities()
        assert len(activities) == 0
        UndoManager.undo()
        assert len(activities) == 1
        UndoManager.undo()
        assert len(activities) == 2

    def test_undo_update_activity(self):
        activity_validator = ActivityValidator()
        activity_repo = ActivityRepository()
        activity_service = ActivityService(activity_repo, activity_validator)
        activity_service.add_activity(1, [1, 2], '21.11.2020', '20:00-21:00', 'party la simona')
        activity_service.update_activity(1, [1, 2, 3], '11.09.2019', '12:00-12:30', 'pizza')
        UndoManager.register_operation(activity_service, UndoHandler.UPDATE_ACTIVITY, 1, [1, 2], '21.11.2020',
                                       '20:00-21:00', 'party la simona')
        UndoManager.undo()
        activities = activity_repo.get_all_activities()
        self.AssertPIDEqual(activities[0], [1, 2])
        self.AssertDateEqual(activities[0], '21.11.2020')

# def test_add_activity():
#     activity_validator = ActivityValidator()
#     activity_repo = ActivityRepository()
#     activity_service = ActivityService(activity_repo, activity_validator)
#     assert activity_repo.get_number_activities() == 0
#
#     activity_service.add_activity(1, [1, 2], '16.11.2020', '18:40', 'Seminar')
#     assert activity_repo.get_number_activities() == 1
#
#     try:
#         activity_service.add_activity(1, [1, 2], '16.11.2020', '18:40', 'Seminar')
#         assert False
#     except ValueError:
#         assert True
