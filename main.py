from repository.activity import ActivityRepository
from repository.file_activity_repo import FileActivityRepo
from repository.pickle_activity_repo import PickleActivityRepo
from repository.pickle_person_repo import PicklePersonRepo
from repository.person import PersonRepository
from repository.file_person_repo import FilePersonRepository
from service.activity_service import ActivityService
from service.person_service import PersonService
from tests.person_tests import PersonTest
from tests.activity_tests import ActivityTest
from ui.console import Console
from validator.activity_validator import ActivityValidator
from validator.person_validator import PersonValidator
import configparser


if __name__ == '__main__':
    PersonTest()
    ActivityTest()
    person_validator = PersonValidator()
    activity_validator = ActivityValidator()
    config = configparser.ConfigParser()
    config.read('settings.properties')
    m_dict = dict(config.items('DEFAULT'))
    repo_type = m_dict['repository'].strip()
    tokens = repo_type.split('\n')
    person = tokens[1].split(' = ')
    activity = tokens[2].split(' = ')
    person_file = person[1].strip("'")
    activity_file = activity[1].strip("'")
    if tokens[0] == 'inmemory':
        person_repo = PersonRepository()
        activity_repo = ActivityRepository()
    elif tokens[0] == 'binary':
        person_repo = PicklePersonRepo(person_file)
        activity_repo = PickleActivityRepo(activity_file)
    else:
        person_repo = FilePersonRepository(person_file)
        activity_repo = FileActivityRepo(activity_file)

    person_service = PersonService(person_repo, person_validator)
    activity_service = ActivityService(activity_repo, activity_validator)
    console = Console(person_service, activity_service)
    console.run_console()
