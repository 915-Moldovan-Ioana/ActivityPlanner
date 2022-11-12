from domain.activity import Activity
from validator.activity_validator import ActivityRepositoryError
from iterable.iterable_repo import Iterable


class ActivityRepository:
    def __init__(self):
        self.__activity_list = Iterable()

    @property
    def activity_list(self):
        return self.__activity_list

    @activity_list.setter
    def activity_list(self, new_activity_list):
        if isinstance(new_activity_list, list) is False:
            raise ActivityRepositoryError('The list of activities was assigned an invalid data type.\n')
        for activity in new_activity_list:
            if isinstance(activity, Activity) is False:
                raise ActivityRepositoryError('The list does not contain activities.\n')
        self.__activity_list = new_activity_list

    def check_activity_existence(self, searched_aid):
        aid_list = [activity.aid for activity in self.__activity_list]
        return searched_aid in aid_list

    def create_interval(self, time):
        time_s = time.strip()
        start_time, end_time = time_s.split('-')
        start_hour, start_minute = start_time.split(':')
        end_hour, end_minute = end_time.split(':')
        start_time = float(start_hour + '.' + start_minute)
        end_time = float(end_hour + '.' + end_minute)
        return start_time, end_time

    def save_activity(self, new_activity):
        if self.check_activity_existence(new_activity.aid) is True:
            raise ActivityRepositoryError('An activity with the same ID already exists in the agenda.\n')

        for activity in self.__activity_list:
            if activity.date == new_activity.date:
                start_old, end_old = self.create_interval(activity.time)
                start_new, end_new = self.create_interval(new_activity.time)
                if (start_old < start_new < end_old) or (start_old < end_new < end_old) or (
                        start_new < start_old and end_new > end_old):
                    raise ActivityRepositoryError('Only one activity can be performed at a given time.\n')
        self.__activity_list.append(new_activity)

    def find_activity(self, searched_aid):
        for activity in self.__activity_list:
            if activity.aid == searched_aid:
                return activity
        return None

    def find_activity_for_undo(self, aid):
        for activity in self.__activity_list:
            if activity.aid == aid:
                return [activity.aid, activity.pid, activity.date, activity.time, activity.description]
        return None

    def remove_activity(self, aid_remove):
        activity = self.find_activity(aid_remove)
        if activity is None:
            raise ActivityRepositoryError('The activity you are trying to remove does not exist in the agenda.\n')
        self.__activity_list.remove(activity)

    def update_activity(self, aid_to_update, new_inf):
        activity_to_update = self.find_activity(aid_to_update)
        if activity_to_update is None:
            raise ActivityRepositoryError('The activity you want to update does not exist in the agenda.\n')
        activity_to_update.pid = new_inf.pid
        activity_to_update.date = new_inf.date
        activity_to_update.time = new_inf.time
        activity_to_update.description = new_inf.description

    def get_busy_time(self, activity_add):
        start_time, end_time = self.create_interval(activity_add.time)
        if (start_time - int(start_time)) > (end_time - int(end_time)):
            if end_time < start_time:
                busy_time = int(24 - start_time + end_time) + 0.6 - (
                            start_time - int(start_time)) + (end_time - int(end_time))
            else:
                busy_time = int(end_time - start_time) + (0.6 - (
                            start_time - int(start_time)) + end_time - int(end_time))
        else:
            if end_time < start_time:
                busy_time = 24 + start_time - end_time
            else:
                busy_time = end_time - start_time
        return busy_time

    def search_by_description(self, description):
        activities = self.get_all_activities()
        searched_activities = [activity for activity in activities if description in activity.description]
        return searched_activities

    def search_by_date(self, date):
        activities = self.get_all_activities()
        searched_activities = [activity for activity in activities if date in activity.date]
        return searched_activities

    def get_all_activities(self):
        return self.__activity_list

    def get_number_activities(self):
        return len(self.__activity_list)

    def __len__(self):
        return len(self.__activity_list)
