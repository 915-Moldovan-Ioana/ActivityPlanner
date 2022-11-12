from domain.activity import Activity
from iterable.iterable_repo import Methods


class ActivityService:
    def __init__(self, activity_repo, validator):
        self.__validator = validator
        self.__activity_repo = activity_repo

    def add_activity(self, aid, pid_list, date, time, description):
        """
        This function adds an activity to the agenda.
        :param aid: Activity id.
        :param pid_list: Activity list of participants.
        :param date: Activity date.
        :param time: Activity time.
        :param description: Activity description.
        :return:
        """
        activity = Activity(aid, pid_list, date, time, description)
        self.__validator.validate(activity)
        self.__activity_repo.save_activity(activity)

    def remove_activity(self, aid):
        """
        This function removes an existing activity form the agenda.
        :param aid: Activity id.
        :return:
        """
        self.__activity_repo.remove_activity(aid)

    def update_activity(self, aid, pid_list, date, time, description):
        """
        This function updates the activity info.
        :param aid: Activity id.
        :param pid_list: New list of participants.
        :param date: New date.
        :param time: New time.
        :param description: New description.
        :return:
        """
        activity = Activity(aid, pid_list, date, time, description)
        self.__validator.validate(activity)
        self.__activity_repo.update_activity(aid, activity)

    def find_activity_for_undo(self, aid):
        return self.__activity_repo.find_activity_for_undo(aid)

    def list_activities(self):
        """
        This function returns the list of activities so they can be listed later on.
        :return: list of activities
        """
        return self.__activity_repo.get_all_activities()

    def search_by_date(self, date):
        """
        This function searches activities whose date match with the given one.
        :param date: the date of the searched activities
        :return:list of activities whose date match with the given one
        """
        activities_list = self.__activity_repo.get_all_activities()
        searched_activities = Methods.global_filter(activities_list, lambda activity: activity.date == date)
        sorted_searched_activities = Methods.comb_sort(searched_activities, self.relation_sort_by_time)
        return sorted_searched_activities
        # return self.__activity_repo.search_by_date(date)

    def search_by_description(self, description):
        """
        This function searches activities whose description match with the given one.
        :param description: the description of the searched activities
        :return: list of activities whose description match with the given one
        """
        activities_list = self.__activity_repo.get_all_activities()
        searched_activities = [activity for activity in activities_list if description in activity.description.lower()]
        return searched_activities
        # return self.__activity_repo.search_by_description(description)

    def split_time(self, given_time):
        time = given_time.strip()
        tokens = time.split('-')
        [hour, minute] = tokens[0].split(':')
        return [hour, minute]

    def relation_sort_by_time(self, x, y):
        x = self.split_time(x.time)
        y = self.split_time(y.time)
        if x[0] == y[0]:
            return x[1] > y[1]
        return x[0] > y[0]

    def sort_activities_by_time(self, activities):
        sorted_list = activities
        Methods.comb_sort(sorted_list, self.relation_sort_by_time)
        # n = len(sorted_list)
        # for i in range(n):
        #     for j in range(n-i-1):
        #         time = self.split_time(sorted_list[j].time)
        #         next_time = self.split_time(sorted_list[j+1].time)
        #         if time[0] > next_time[0]:
        #             sorted_list[j], sorted_list[j+1] = sorted_list[j+1], sorted_list[j]
        #         elif time[0] == next_time[0]:
        #             if time[1] > next_time[1]:
        #                 sorted_list[j], sorted_list[j + 1] = sorted_list[j + 1], sorted_list[j]
        return sorted_list

    def busiest_days(self):
        all_dates = []
        dates = []
        activities = self.__activity_repo.get_all_activities()
        for activity in activities:
            if activity.date not in all_dates:
                date_to_append = {'date': activity.date, 'busy_time': 0}
                dates.append(date_to_append)
                all_dates.append(activity.date)
        for activity in activities:
            for dict in dates:
                if activity.date == dict['date']:
                    dict['busy_time'] += self.__activity_repo.get_busy_time(activity)
        return dates

    def activity_with(self, person_id):
        # final_list = []
        # activities = self.__activity_repo.get_all_activities()
        # for activity in activities:
        #     if person_id in activity.pid:
        #         final_list.append(activity)
        # return final_list
        activities_list = self.__activity_repo.get_all_activities()
        searched_activities = Methods.global_filter(activities_list, lambda activity: person_id in activity.pid)
        return searched_activities
