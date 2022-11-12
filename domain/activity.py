# Activity: activity_id, person_id - list, date, time, description
from validator.activity_validator import ActivityValidatorException


class Activity:
    def __init__(self, activity_id, pid_list, date, time, description):
        self._aid = activity_id
        self._pid = pid_list
        self._date = date
        self._time = time
        self._description = description

    @property
    def aid(self):
        return self._aid

    @aid.setter
    def aid(self, value):
        self._aid = value

    @property
    def pid(self):
        return self._pid

    @pid.setter
    def pid(self, value):
        if isinstance(value, list) is False:
            raise ActivityValidatorException("The participants' ids must be a list.")
        self._pid = value

    # @property
    # def year(self):
    #     return self.__date['year']
    #
    # @year.setter
    # def year(self, value):
    #     if value < 0:
    #         raise ActivityValidatorException('Year cannot be negative.')
    #     self.__date['year'] = value
    #
    # @property
    # def month(self):
    #     return self.__date['month']
    #
    # @month.setter
    # def month(self, value):
    #     if not (1 <= int(value) <= 12):
    #         raise ActivityValidatorException('Month must be between 1 and 12.')
    #
    # @property
    # def day(self):
    #     return self.__date['day']
    #
    # @day.setter
    # def day(self, value):
    #     if not (1 <= int(value) <= 31):
    #         raise ActivityValidatorException('Day must be between 1 and 31.')

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if value == '':
            raise ActivityValidatorException('Description cannot be empty.')
        self._description = value

    def __eq__(self, other):
        return self.aid == other.aid

    def __str__(self) -> str:
        return '{0}. {1} performed with members having the IDs {2} on {3}, at {4}.'.format(self._aid,
                                                                                           self._description,
                                                                                           self._pid, self._date,
                                                                                           self._time)

    def __getitem__(self, key):
        return getattr(self, key)
