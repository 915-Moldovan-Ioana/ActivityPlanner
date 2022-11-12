class StoreException(Exception):
    pass


class PersonRepositoryError(StoreException):
    pass


class PersonValidatorException(StoreException):
    pass


class PersonValidator:
    def validate(self, person):
        list_of_errors = ''
        if person.id < 0:
            list_of_errors += 'Invalid person ID. The ID cannot be negative.'
        if person.name == '':
            list_of_errors += 'Invalid person name. The name cannot be empty.'
        if person.phone_number == '':
            list_of_errors += 'Invalid phone number. The phone number cannot be empty.'

        if len(list_of_errors) != 0:
            raise PersonValidatorException(list_of_errors)
