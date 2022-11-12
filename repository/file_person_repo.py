from domain.person import Person
from repository.person import PersonRepository
import csv


class FilePersonRepository(PersonRepository):

    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name
        self.load()

    def save(self):
        with open(self.file_name, 'w') as file:
            writer = csv.DictWriter(file, ['_id', '_name', '_phone_number'])
            writer.writeheader()
            for person in self.get_all_people():
                writer.writerow(person.__dict__)

    def load(self):
        with open(self.file_name, 'r') as file:
            reader = csv.DictReader(file)
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
