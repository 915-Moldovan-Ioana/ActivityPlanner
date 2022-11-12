class StoreException(Exception):
    pass


class ActivityRepositoryError(StoreException):
    pass


class ActivityServiceError(StoreException):
    pass


class ActivityValidatorException(StoreException):
    pass


class ActivityValidator:

    def split_date(self, date):
        date = date.strip()
        tokens = date.split('.')
        year = tokens[0]
        month = tokens[1]
        day = tokens[2]
        return year, month, day

    def validate(self, activity):
        list_of_errors = ''
        if activity.aid < 0:
            list_of_errors += 'Invalid activity ID. ID cannot be negative.'
        date = activity.date
        day, month, year = self.split_date(date)
        if int(year) > 2050:
            list_of_errors += 'Please make a plan for maximum year 2050.'
        if int(month) > 12 or int(month) < 0:
            list_of_errors += 'Month should be between 1 and 12.'
        if int(day) > 31 or int(day) < 0:
            list_of_errors += 'Day should be between 1 and 31.'
        if len(list_of_errors) != 0:
            raise ActivityValidatorException(list_of_errors)
