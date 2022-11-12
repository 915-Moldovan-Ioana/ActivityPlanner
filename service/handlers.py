from enum import Enum


def add_activity_handler(activity_service, activity_id):
    activity_service.remove_activity(activity_id)


def delete_activity_handler(activity_service, activity_id, activity_pid, activity_date, activity_time,
                            activity_description):
    activity_service.add_activity(activity_id, activity_pid, activity_date, activity_time, activity_description)


def update_activity_handler(activity_service, activity_id, activity_pid, activity_date, activity_time,
                            activity_description):
    activity_service.update_activity(activity_id, activity_pid, activity_date, activity_time, activity_description)


def add_person_handler(person_service, person_id):
    person_service.remove_person(person_id)


def delete_person_handler(person_service, person_id, person_name, person_phone_number):
    person_service.add_person(person_id, person_name, person_phone_number)


def update_person_handler(person_service, person_id, person_name, person_phone_number):
    person_service.update_person(person_id, person_name, person_phone_number)


class UndoHandler(Enum):
    ADD_ACTIVITY = add_activity_handler
    DELETE_ACTIVITY = delete_activity_handler
    UPDATE_ACTIVITY = update_activity_handler
    ADD_PERSON = add_person_handler
    DELETE_PERSON = delete_person_handler
    UPDATE_PERSON = update_person_handler
