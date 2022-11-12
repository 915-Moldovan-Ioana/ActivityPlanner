from repository.activity import ActivityRepository
from domain.activity import Activity
import pickle
import os


class PickleActivityRepo(ActivityRepository):

    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name
        self.load()

    def save(self):
        data = []
        with open(self.file_name, 'wb') as file:
            for activity in self.get_all_activities():
                data.append(activity.__dict__)
            pickle.dump(data, file)

    def load(self):
        if os.path.exists(self.file_name) and os.path.getsize(self.file_name) > 0:
            with open(self.file_name, 'rb') as file:
                reader = pickle.load(file)
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
