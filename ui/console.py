from tkinter import *
from service.handlers import UndoHandler
from service.undo import UndoManager
from validator.activity_validator import ActivityRepositoryError
from validator.person_validator import PersonRepositoryError
from iterable.iterable_repo import Methods


# root = Tk()
# mainFrame = Frame(root)
# mainFrame.pack()
# myLabel = Label(root, text='Welcome to MyAgenda!', bg='black', fg='white')
# myLabel.pack(side=TOP, fill=X)
# buttonPeople = Button(mainFrame, text='Access people.', fg='black')
# buttonActivities = Button(mainFrame, text='Access activities.', fg='blue')
# buttonPeople.pack(side=LEFT)
# buttonActivities.pack(side=LEFT)
# root.mainloop()


class Console:
    def __init__(self, person_service=None, activity_service=None):
        self.__person_service = person_service
        self.__activity_service = activity_service

    def tk_add_activity(self):
        activity = Frame()
        text = Label(activity, text='Add activity:')
        text.grid(row=0)
        aid = Label(activity, text='ID:')
        entry_aid = Entry(activity)
        pid = Label(activity, text='Participants:')
        entry_pid = Entry(activity)
        date = Label(activity, text='Date:')
        entry_date = Entry(activity)
        time = Label(activity, text='Time:')
        entry_time = Entry(activity)
        description = Label(activity, text='Description:')
        entry_descriprion = Entry(activity)
        aid.grid(row=1, sticky=E)
        entry_aid.grid(row=1, column=1)
        pid.grid(row=2, sticky=E)
        entry_pid.grid(row=2, column=1)
        date.grid(row=3, sticky=E)
        entry_date.grid(row=3, column=1)
        time.grid(row=4, sticky=E)
        entry_time.grid(row=4, column=1)
        description.grid(row=5, sticky=E)
        entry_descriprion.grid(row=5, column=1)
        activity.pack()

    def tk_remove_activity(self):
        activity = Frame()
        aid = Label(activity, text='Remove activity with ID:')
        entry_aid = Entry(activity)
        aid.grid(row=1, sticky=E)
        entry_aid.grid(row=1, column=1)
        activity.pack()

    def tk_add_person(self):
        people = Frame()
        text = Label(people, text='Add person:')
        text.grid(row=0)
        pid = Label(people, text='ID:')
        entry_pid = Entry(people)
        get_pid = entry_pid.get()
        name = Label(people, text='Name:')
        entry_name = Entry(people)
        get_name = entry_name.get()
        phone_number = Label(people, text='Phone number:')
        entry_phone_number = Entry(people)
        get_phone_number = entry_phone_number.get()
        print(type(get_pid))
        entry_pid.grid(row=1, column=1)
        name.grid(row=2, sticky=E)
        entry_name.grid(row=2, column=1)
        phone_number.grid(row=3, sticky=E)
        entry_phone_number.grid(row=3, column=1)
        btn_add = Button(people, text='Finish',
                         command=self.__person_service.add_person(int(get_pid), int(get_name), int(get_phone_number)))
        pid.grid(row=1, sticky=E)
        btn_add.grid(row=4)
        people.pack()

    def tk_remove_person(self):
        people = Frame()
        # text = Label(people, text='Remove person:')
        # text.grid(row=0)
        pid = Label(people, text='Remove person with ID:')
        entry_pid = Entry(people)
        pid.grid(row=1, sticky=E)
        entry_pid.grid(row=1, column=1)
        people.pack()

    def tk_layout(self):
        main = Tk()
        title_label = Label(main, text='Welcome to MyAgenda!', bg='black', fg='white')
        title_label.pack(side=TOP, fill=X)
        menu_1 = Label(main, text='What do you want to do?')
        menu_1.pack()
        people = Frame()
        activities = Frame()
        menu_people = Label(people, text='Manage people.')
        menu_people.grid()
        btn_add_person = Button(people, text='Add person', command=self.tk_add_person)
        btn_add_person.grid()
        btn_remove_person = Button(people, text='Remove person', command=self.tk_remove_person)
        btn_remove_person.grid()
        btn_update_person = Button(people, text='Update person')
        btn_update_person.grid()
        btn_list_activities = Button(people, text='List people')
        btn_list_activities.grid()
        btn_statistics_person = Button(people, text='Statistics')
        btn_statistics_person.grid()
        people.pack()
        menu_activities = Label(activities, text='Manage activities.')
        menu_activities.grid()
        btn_add_activity = Button(activities, text='Add activity', command=self.tk_add_activity)
        btn_add_activity.grid()
        btn_remove_activity = Button(activities, text='Remove activity', command=self.tk_remove_activity)
        btn_remove_activity.grid()
        btn_update_activity = Button(activities, text='Update activity')
        btn_update_activity.grid()
        btn_list_activities = Button(activities, text='List activities', command=self.list_ui('activities'))
        btn_list_activities.grid()
        btn_statistics_activity = Button(activities, text='Statistics')
        btn_statistics_activity.grid()
        activities.pack()
        # menu_2 = Label(main, text='Add a person or an activity.')
        # menu_3 = Label(main, text='Remove a person or an activity.')
        # menu_4 = Label(main, text='Update a person or an activity.')
        # menu_5 = Label(main, text='List all people or list al activities.')
        # menu_6 = Label(main, text='Search person by name/phone number or activity by date and time/description.')
        # menu_7 = Label(main, text='Statistics: activities on a given date, busiest days, activities with a person.')
        # menu_8 = Label(main, text='Exit.')
        # menu_1.pack()
        # menu_2.pack()
        # menu_3.pack()
        # menu_4.pack()
        # menu_5.pack()
        # menu_6.pack()
        # menu_7.pack()
        # menu_8.pack()
        main.mainloop()

    def print_menu(self):
        print()
        print('What do you want to do?')
        print('\t Add a person or an activity.')
        print('\t Remove a person or an activity.')
        print('\t Update a person or an activity.')
        print('\t List all people or list al activities.')
        print('\t Search person by name/phone number or activity by date and time/description.')
        print('\t Statistics: activities on a given date, busiest days, activities with a person.')
        print('\t Exit.')

    def add_ui(self, cmd_entity, added_list, added_redo):
        if cmd_entity == 'person':
            pid = input('ID: ')
            name = input('Name: ')
            phone_number = input('Phone number: ')
            try:
                added_list.append(int(pid))
                added_redo.append(int(pid))
                self.__person_service.add_person(int(pid), name, phone_number)
            except PersonRepositoryError as apre:
                print(apre)
        elif cmd_entity == 'activity':
            aid = input('ID: ')
            print('Choose members: ')
            self.list_ui('people')
            people = input('Participants: ')
            p_list = self.split_list(people)
            date = input('Date: ')
            time = input('Time: ')
            description = input('Description: ')
            try:
                added_list.append(int(aid))
                added_redo.append(int(aid))
                self.__activity_service.add_activity(int(aid), p_list, date, time, description)
            except ActivityRepositoryError as are:
                print(are)

    def split_date(self, date):
        date = date.strip()
        tokens = date.split('.')
        year = tokens[0]
        month = tokens[1]
        day = tokens[2]
        return year, month, day

    def remove_ui(self, cmd_entity, removed_list, removed_redo):
        if cmd_entity == 'person':
            pid = input('Which person do you want to remove? (ID)')
            try:
                person_to_remove = self.__person_service.find_person(int(pid))
                removed_list.append(person_to_remove)
                removed_redo.append(person_to_remove)
                self.__person_service.remove_person(int(pid))
            except PersonRepositoryError as rpre:
                print(rpre)
        elif cmd_entity == 'activity':
            aid = input('What activity do you want to remove? (ID)')
            try:
                activity_to_remove = self.__activity_service.find_activity_for_undo(int(aid))
                removed_list.append(activity_to_remove)
                removed_redo.append(activity_to_remove)
                self.__activity_service.remove_activity(int(aid))
            except ActivityRepositoryError as rre:
                print(rre)

    def list_ui(self, cmd_entity):
        if cmd_entity == 'people':
            people = self.__person_service.list_people()
            if people is None:
                print('No people registered.')
            else:
                for person in people:
                    print(person)
        elif cmd_entity == 'activities':
            activities = self.__activity_service.list_activities()
            if activities is None:
                print('No activities registered.')
            else:
                for activity in activities:
                    print(activity)

    def update_ui(self, cmd_entity, updated_list, updated_redo):
        if cmd_entity == 'person':
            pid = input('Which person do you want to update? (ID)')
            name = input('New name: ')
            phone_number = input('New phone number: ')
            person_to_update = self.__person_service.find_person(int(pid))
            updated_list.append(person_to_update)
            updated_redo.append([int(pid), name, phone_number])
            self.__person_service.update_person(int(pid), name, phone_number)
        elif cmd_entity == 'activity':
            aid = input('What activity do you want to update? (ID)')
            print('Choose new members: ')
            self.list_ui('people')
            people = input('New participants(IDs): ')
            p_list = self.split_list(people)
            date = input('New date: ')
            time = input('New time: ')
            description = input('New description: ')
            try:
                updated_list.append(self.__activity_service.find_activity_for_undo(int(aid)))
                updated_redo.append([int(aid), p_list, date, time, description])
                self.__activity_service.update_activity(int(aid), p_list, date, time, description)
            except ActivityRepositoryError as ure:
                print(ure)

    def undo_ui(self, command_list, added_list, removed_list, updated_list, undoed_list):
        try:
            last_command = command_list.pop()
            undoed_list.append(last_command)
            last_command = last_command.strip()
            # try:
            command, entity = last_command.split(' ')
            # except ValueError as ve:
            #     print('You must make another command in order to undo something.')
            if command == 'add':
                if entity == 'person':
                    UndoManager.register_operation(self.__person_service, UndoHandler.ADD_PERSON, added_list.pop())
                elif entity == 'activity':
                    UndoManager.register_operation(self.__activity_service, UndoHandler.ADD_ACTIVITY, added_list.pop())
            elif command == 'remove':
                last_removed = removed_list.pop()
                if entity == 'person':
                    id, name, phone_number = last_removed[0], last_removed[1], last_removed[2]
                    UndoManager.register_operation(self.__person_service, UndoHandler.DELETE_PERSON, id, name,
                                                   phone_number)
                elif entity == 'activity':
                    aid, pid, date, time, description = last_removed[0], last_removed[1], last_removed[2], last_removed[
                        3], last_removed[4]
                    UndoManager.register_operation(self.__activity_service, UndoHandler.DELETE_ACTIVITY, aid, pid, date,
                                                   time, description)
            elif command == 'update':
                last_updated = updated_list.pop()
                if entity == 'person':
                    id, name, phone_number = last_updated[0], last_updated[1], last_updated[2]
                    UndoManager.register_operation(self.__person_service, UndoHandler.UPDATE_PERSON, id, name,
                                                   phone_number)
                elif entity == 'activity':
                    aid, pid, date, time, description = last_updated[0], last_updated[1], last_updated[2], last_updated[
                        3], last_updated[4]
                    UndoManager.register_operation(self.__activity_service, UndoHandler.UPDATE_ACTIVITY, aid, pid, date,
                                                   time, description)
            UndoManager.undo()
        except IndexError as ie:
            print('There are no more commands to undo.')

    def redo_ui(self, undo_command_list, undoed_list, added_redo, removed_redo, updated_redo):
        last_command = undo_command_list.pop()
        if last_command == 'undo':
            what_command = undoed_list.pop()
            what_command = what_command.strip()
            command, entity = what_command.split(' ')
            if command == 'add':
                last_removed = removed_redo.pop()
                if entity == 'person':
                    id, name, phone_number = last_removed[0], last_removed[1], last_removed[2]
                    UndoManager.register_operation(self.__person_service, UndoHandler.DELETE_PERSON, id, name,
                                                   phone_number)
                elif entity == 'activity':
                    aid, pid, date, time, description = last_removed[0], last_removed[1], last_removed[2], last_removed[
                        3], last_removed[4]
                    UndoManager.register_operation(self.__activity_service, UndoHandler.DELETE_ACTIVITY, aid, pid, date,
                                                   time, description)
            elif command == 'remove':
                if entity == 'person':
                    UndoManager.register_operation(self.__person_service, UndoHandler.ADD_PERSON, added_redo.pop())
                elif entity == 'activity':
                    UndoManager.register_operation(self.__activity_service, UndoHandler.ADD_ACTIVITY, added_redo.pop())
            elif command == 'update':
                last_updated = updated_redo.pop()
                if entity == 'person':
                    id, name, phone_number = last_updated[0], last_updated[1], last_updated[2]
                    UndoManager.register_operation(self.__person_service, UndoHandler.UPDATE_PERSON, id, name,
                                                   phone_number)
                elif entity == 'activity':
                    aid, pid, date, time, description = last_updated[0], last_updated[1], last_updated[2], last_updated[
                        3], last_updated[4]
                    UndoManager.register_operation(self.__activity_service, UndoHandler.UPDATE_ACTIVITY, aid, pid, date,
                                                   time, description)
            UndoManager.undo()

    def search_ui(self, cmd_entity):
        command = cmd_entity.strip()
        entity, prop = command.split(' by ')
        if entity == 'person':
            if prop == 'name':
                name = input('Give name: ')
                people = self.__person_service.search_by_name(name)
                if people is None:
                    print('No people registered.')
                else:
                    for person in people:
                        print(person)
            elif prop == 'phone number':
                phone_number = input('Give phone number: ')
                people = self.__person_service.search_by_phone(phone_number)
                if people is None:
                    print('No people registered.')
                else:
                    for person in people:
                        print(person)
        elif entity == 'activity':
            if prop == 'date':
                date = input('Give date: ')
                activities = self.__activity_service.search_by_date(date)
                if activities is None:
                    print('No activities registered.')
                else:
                    for activity in activities:
                        print(activity)
            elif prop == 'description':
                description = input('Give description: ')
                activities = self.__activity_service.search_by_description(description)
                if activities is None:
                    print('No activities registered.')
                else:
                    for activity in activities:
                        print(activity)

    def relation_busy_time(self, x, y):
        return x['busy_time'] < y['busy_time']

    def busiest_days_ui(self):
        sorted_days = self.__activity_service.busiest_days()
        Methods.comb_sort(sorted_days, self.relation_busy_time)
        # n = len(sorted_days)
        # for i in range(n):
        #     for j in range(n - i - 1):
        #         if sorted_days[j]['busy_time'] > sorted_days[j + 1]['busy_time']:
        #             sorted_days[j], sorted_days[j + 1] = sorted_days[j + 1], sorted_days[j]
        for day in sorted_days:
            print('Date: {0}, busy time: {1} hours, free time: {2}.'.format(day['date'], day['busy_time'],
                                                                            24 - day['busy_time']))

    def activities_statistics(self, cmd_entity):
        command = cmd_entity.strip()
        tokens = command.split(' ')
        if tokens[0] == 'on':
            self.activities_date(tokens[1])
        elif tokens[0] == 'with':
            self.activity_with_ui(int(tokens[1]))

    def activity_with_ui(self, person_id):
        activities = self.__activity_service.activity_with(person_id)
        if activities is None:
            print('No activities registered.')
        else:
            for activity in activities:
                print(activity)

    def activities_date(self, date):
        activities = self.__activity_service.search_by_date(date)
        sorted_activities = self.__activity_service.sort_activities_by_time(activities)
        if sorted_activities is None:
            print('No activities registered.')
        else:
            for activity in sorted_activities:
                print(activity)

    def split_list(self, people):
        p_list = []
        people = people.strip()
        tokens = people.split(',')
        for person in tokens:
            p_list.append(int(person))
        return p_list

    def split_command(self, command):
        command = command.strip()
        tokens = command.split(' ', 1)
        command_word = tokens[0].strip()
        command_entity = tokens[1].strip() if len(tokens) == 2 else ''
        return command_word, command_entity

    def run_console(self):
        # self.tk_layout()
        removed_list = []
        removed_redo = []
        added_list = []
        added_redo = []
        updated_list = []
        updated_redo = []
        command_list = []
        undo_command_list = []
        undoed_list = []
        self.__person_service.add_person(1, 'Ioana Moldovan', '0734987665')
        self.__person_service.add_person(2, 'Simona Motoc', '0789663421')
        self.__person_service.add_person(3, 'Anda Pop', '0789997221')
        self.__person_service.add_person(4, 'Cezar Maniu', '0709421443')
        self.__person_service.add_person(5, 'Dan Negru', '0750998211')
        self.__person_service.add_person(6, 'Iulia Marin', '0711345208')
        self.__person_service.add_person(7, 'Ioana Popescu', '0799612008')
        self.__activity_service.add_activity(1, [1, 2], '16.11.2020', '18:40-20:00', 'Seminar')
        self.__activity_service.add_activity(2, [3, 5], '16.11.2020', '10:00-12:00', 'Exam')
        self.__activity_service.add_activity(3, [1, 2, 6], '23.12.2020', '21:20-24:00', 'Christmas party')
        self.__activity_service.add_activity(4, [3, 4], '19.11.2020', '19:30-21:20', 'Movie')
        self.__activity_service.add_activity(5, [1], '16.11.2020', '12:30-13:30', 'Lunch')
        self.__activity_service.add_activity(6, [1, 2, 3, 4], '16.11.2020', '12:10-12:30', 'Break')

        done = False
        while done is not True:
            self.print_menu()
            command = input('Command: ')
            cmd_word, cmd_entity = self.split_command(command)
            if cmd_word == 'add':
                command_list.append(command)
                undo_command_list.append(command)
                self.add_ui(cmd_entity, added_list, added_redo)
            elif cmd_word == 'list':
                self.list_ui(cmd_entity)
            elif cmd_word == 'remove':
                command_list.append(command)
                undo_command_list.append(command)
                self.remove_ui(cmd_entity, removed_list, removed_redo)
            elif cmd_word == 'update':
                command_list.append(command)
                undo_command_list.append(command)
                self.update_ui(cmd_entity, updated_list, updated_redo)
            elif cmd_word == 'search':
                self.search_ui(cmd_entity)
            elif cmd_word == 'activities':
                self.activities_statistics(cmd_entity)
            elif cmd_word == 'busiest':
                self.busiest_days_ui()
            elif cmd_word == 'undo':
                undo_command_list.append(command)
                self.undo_ui(command_list, added_list, removed_list, updated_list, undoed_list)
            elif cmd_word == 'redo':
                command_list.append(command)
                self.redo_ui(undo_command_list, undoed_list, added_redo, removed_redo, updated_redo)
            elif cmd_word == 'exit':
                print('Bye!')
                done = True
            else:
                print('Wrong command!')
