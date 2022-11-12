# Person: person_id, name, phone_number
# from validator.person_validator import PersonValidatorException


class Person:
    def __init__(self, person_id, name, phone_number):
        self._id = person_id
        self._name = name
        self._phone_number = phone_number

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value):
        # if value == '':
        #     raise PersonValidatorException('The phone number cannot be empty.')
        self._phone_number = value

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self) -> str:
        return '{0}. {1}, {2}'.format(self._id, self._name, self._phone_number)

    def __getitem__(self, key):
        return getattr(self, key)
