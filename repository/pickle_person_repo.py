from repository.person import PersonRepository
from domain.person import Person
import pickle
import os


class PicklePersonRepo(PersonRepository):

    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name
        self.load()

    def save(self):
        data = []
        with open(self.file_name, 'wb') as file:
            for person in self.get_all_people():
                data.append(person.__dict__)
            pickle.dump(data, file)

    def load(self):
        if os.path.exists(self.file_name) and os.path.getsize(self.file_name) > 0:
            with open(self.file_name, 'rb') as file:
                reader = pickle.load(file)
                for row in reader:
                    super().save_person(Person(int(row['_id']), row['_name'], row['_phone_number']))

    def save_person(self, new_person):
        super().save_person(new_person)
        self.save()

    def remove_person(self, pid_remove):
        super().remove_person(pid_remove)
        self.save()

    def update_person(self, pid_to_update, new_inf):
        super().update_person(pid_to_update, new_inf)
        self.save()
