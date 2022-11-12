from domain.activity import Activity
from repository.activity import ActivityRepository
import csv
import os


class FileActivityRepo(ActivityRepository):

    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name
        self.load()

    def save(self):
        with open(self.file_name, 'w') as file:
            writer = csv.DictWriter(file, ['_aid', '_pid', '_date', '_time', '_description'])
            writer.writeheader()
            for activity in self.get_all_activities():
                writer.writerow(activity.__dict__)

    def load(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    super().save_activity(
                        Activity(int(row['_aid']), row['_pid'], row['_date'], row['_time'], row['_description']))

    def save_activity(self, new_activity):
        super().save_activity(new_activity)
        self.save()

    def remove_activity(self, aid_remove):
        super().remove_activity(aid_remove)
        self.save()

    def update_activity(self, aid_to_update, new_inf):
        super().update_activity(aid_to_update, new_inf)
        self.save()
