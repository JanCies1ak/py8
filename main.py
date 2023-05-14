import tkinter as tk
import sqlite3
from screeninfo import get_monitors

final_grades = [2, 3, 3.5, 4, 4.5, 5, -1]


class Student:
    mail = None
    first_name = None
    last_name = None
    project = None
    list_entries = None
    home_works = None
    final = None
    status = None

    def __init__(self, mail: str,
                 first_name: str,
                 last_name: str,
                 project: int,
                 lists: list[int],
                 home_works: list[int],
                 final: float,
                 status: str):

        if len(lists) != 3 or len(home_works) != 10:
            raise ValueError("Niepoprawna liczba ocen.")

        if project < -1 or project > 40:
            raise ValueError("Niepoprawna ocena z projektu.")
        for grade in lists:
            if grade < -1 or grade > 20:
                raise ValueError("Niepoprawna ocena z listy z zadaniami.")

        for grade in home_works:
            if grade < -1 or grade > 100:
                raise ValueError("Niepoprawna ocena z pracy domowej.")

        if final not in final_grades:
            raise ValueError("Niepoprawna ocena końcowa.")

        self.mail = mail
        self.first_name = first_name
        self.last_name = last_name
        self.project = project
        self.lists = lists
        self.home_works = home_works
        self.final = final
        self.status = status

    @staticmethod
    def from_iterable(iterable: list[int | str] | set[int | str] | tuple[int | str]):
        if len(iterable) < 19:
            raise ValueError("Niepoprawny format studenta")
        mail = iterable[0]
        first_name = iterable[1]
        last_name = iterable[2]
        project = int(iterable[3])

        lists_str = iterable[4:7]
        lists = []
        for i in range(0, 3):
            lists.append(int(lists_str[i]))

        home_works_str = iterable[7:17]
        home_works = []
        for i in range(0, 10):
            home_works.append(int(home_works_str[i]))

        final = int(iterable[17])
        status = iterable[18]

        return Student(mail, first_name, last_name, project, lists, home_works, final, status)

    @staticmethod
    def from_str(line: str):
        split = line.split(",")
        split[3] = int(split[3])
        split[4] = int(split[4])
        split[5] = int(split[5])
        split[6] = int(split[6])
        split[7] = int(split[7])
        split[8] = int(split[8])
        split[9] = int(split[9])
        split[10] = int(split[10])
        split[11] = int(split[11])
        split[12] = int(split[12])
        split[13] = int(split[13])
        split[14] = int(split[14])
        split[15] = int(split[15])
        split[16] = int(split[16])
        split[17] = int(split[17])
        return Student.from_iterable(split)

    def calculate_final(self):
        if self.final != -1:
            return
        if self.project == -1:
            return
        if -1 in self.lists:
            return
        if -1 in self.home_works:
            return

        average = 0
        for grade in self.home_works:
            average += grade
        average /= 10

        sorted_lists = sorted(self.lists)

        if average >= 60:
            sorted_lists[0] = 20
        if average >= 70:
            sorted_lists[1] = 20
        if average >= 80:
            sorted_lists[2] = 20

        points = self.project + sum(sorted_lists)
        if points < 51:
            self.final = 2
        else:
            self.final = (points / 20).__ceil__()

        self.status = "GRADED"

    def show(self):
        data = [self.first_name, self.last_name, self.project]
        for grade in self.lists:
            data.append(grade)
        for grade in self.home_works:
            data.append(grade)
        data.append(self.final)
        data.append(self.status)
        print(f"{self.mail}: {data}")

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if other is None:
            return False
        if self.mail is None:
            return other.mail is None
        return self.mail == other.mail

    def __ne__(self, other):
        return self.mail != other.mail

    def to_list(self) -> list[int | str]:
        lst = [self.mail, self.first_name, self.last_name, self.project]
        lst += self.lists
        lst += self.home_works
        lst.append(self.final)
        lst.append(self.status)
        return lst

    def __str__(self):
        project = str(self.project) if self.project != -1 else "_"
        lists = []
        for lst in self.lists:
            lists.append(str(lst) if lst != -1 else "_")
        lists = ', '.join(lists)
        home_works = []
        for hwork in self.home_works:
            home_works.append(str(hwork) if hwork != -1 else "_")
        home_works = ', '.join(home_works)
        final = str(self.final) if self.final != -1 else "_"
        line = f'''Student {self.mail}:
    name = {self.first_name} {self.last_name}
    grades:
        project = {project}
        lists = {lists}
        homeworks = {home_works}
        final = {final}
    status = {self.status}'''
        return line


class DBController:
    students = None
    connection = None

    def __init__(self, db: str):
        self.connection = sqlite3.connect(db)
        query = '''CREATE TABLE IF NOT EXISTS student (
                mail TEXT PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                project REAL,
                list_1 INTEGER,
                list_2 INTEGER,
                list_3 INTEGER,
                hw_1 INTEGER,
                hw_2 INTEGER,
                hw_3 INTEGER,
                hw_4 INTEGER,
                hw_5 INTEGER,
                hw_6 INTEGER,
                hw_7 INTEGER,
                hw_8 INTEGER,
                hw_9 INTEGER,
                hw_10 INTEGER,
                final REAL,
                status TEXT
                )'''
        self.connection.execute(query)
        self.students = list()
        query = "SELECT * FROM student"
        res = self.connection.execute(query)
        studs = res.fetchall()
        for student in studs:
            self.students.append(Student.from_iterable(student))

    def __getitem__(self, mail: str) -> Student | None:
        for stud in self.students:
            if stud.mail == mail:
                return stud
        return None

    def __add__(self, new: Student):
        if self[new.mail] is not None:
            return
        query = '''INSERT INTO student (
mail, first_name, last_name, 
project, 
list_1, list_2, list_3,
hw_1, hw_2, hw_3, hw_4, hw_5, hw_6, hw_7, hw_8, hw_9, hw_10,
final, status
)
VALUES (
?, ?, ?,
?,
?, ?, ?, 
?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
?, ?
)'''
        self.connection.execute(query, new.to_list())
        self.connection.commit()
        self.students.append(new)

    def __delitem__(self, mail: str):
        query = "DELETE FROM student WHERE mail = ?"
        self.connection.execute(query, mail)
        self.connection.commit()
        for stud in self.students:
            if stud.mail == mail:
                self.students.remove(stud)
                return

    def __setitem__(self, mail: str, new_values: Student):
        if self[mail] is None:
            return
        student_values = new_values.to_list()[1:19]
        student_values.append(mail)
        query = '''UPDATE student SET
first_name = ?,
last_name = ?,
project = ?,
list_1 = ?, list_2 = ?, list_3 = ?,
hw_1 = ?, hw_2 = ?, hw_3 = ?, hw_4 = ?, hw_5 = ?, hw_6 = ?, hw_7 = ?, hw_8 = ?, hw_9 = ?, hw_10 = ?,
final = ?, status = ? WHERE mail = ?'''
        self.connection.execute(query, student_values)
        self.connection.commit()
        for stud in self.students:
            if stud.mail == mail:
                stud.project = new_values.project
                stud.lists = new_values.lists
                stud.home_works = new_values.home_works
                stud.final = new_values.final
                stud.status = new_values.status


database = DBController("students.db")

# root
root = tk.Tk()
root.title("Students")
screen_width = get_monitors()[0].width
screen_height = get_monitors()[0].height
root.geometry(f"{screen_width // 2}x{int(screen_height / 1.6)}")

# data enter
left_frame = tk.Frame(root, borderwidth=4, relief="ridge", width=screen_width // 4,
                      height=int(screen_height / 1.6))
left_frame.pack(side="left", padx=10, pady=10)
left_frame.pack_propagate(False)


# get, delete
def get():
    """
    Podaje dane studenta z mailem podanym w polu mail_entry.
    """
    student_mail = mail_entry.get()
    student = database[student_mail]
    if student is None:
        student = f"Student z mailem {student_mail} nie istnieje."
    students_label.config(text=str(student))


def get_all():
    """
    Podaje meile wszystkich studentów w bazie danych.
    """
    students_mails = []
    for stud in database.students:
        students_mails.append(stud.mail)
    students_label.config(text='\n'.join(students_mails))


def calculate_finals():
    for student in database.students:
        student.calculate_final()
    students_label.config(text="Oceny końcowe zostały przeliczone.")


def delete():
    """
    Usuwa studenta z mailem podanym w polu mail_entry.
    """
    student_mail = mail_entry.get()
    student = database[student_mail]
    if student is None:
        student = f"Student z mailem {student_mail} nie istnieje."
    else:
        database.__delitem__(student_mail)
        student = "Student został usunięty."
    students_label.config(text=student)


get_frame = tk.Frame(left_frame, borderwidth=2, relief="ridge", width=screen_width // 4 - 20,
                     height=screen_height // 8)
get_frame.pack(padx=5, pady=5)
get_frame.pack_propagate(False)

mail_enter_frame = tk.Frame(get_frame)
mail_enter_frame.pack(anchor='w', padx=5, pady=5)

mail_entry = tk.Entry(mail_enter_frame, width=screen_width // 4)
mail_label = tk.Label(mail_enter_frame, text="mail:")
mail_label.pack(side='left')

get_button = tk.Button(get_frame, text="Get", command=get)
delete_button = tk.Button(get_frame, text="Delete", command=delete)
get_all_button = tk.Button(get_frame, text="Get all mails", command=get_all)
calculate_finals_button = tk.Button(get_frame, text="Calculate finals", command=calculate_finals)

mail_entry.pack(anchor="w", padx=10, pady=10)
get_all_button.pack(anchor='w', padx=10, pady=10, side='left')
get_button.pack(anchor='w', padx=10, pady=10, side='left')

delete_button.pack(padx=10, pady=10, side='right')
delete_button.config(background='yellow')
calculate_finals_button.pack(pady=10, padx=10, side='right')


# update, insert
def update():
    """
    Zmienia dane studenta z mailem, podanym w polu mail_entry.
    Puste dane będą zamieniane na odpowiednie dane studenta, który jest zmieniany.
    """
    mail = mail_entry.get()
    student = database[mail]
    if student is None:
        students_label.config(text=f"Student z mailem {mail} nie istnieje.")
        return

    try:
        can_set_final = True
        name = name_entry.get()
        if name == '':
            first = student.first_name
            last = student.last_name
        else:
            first = name.split(' ')[0]
            last = name.split(' ')[1]

        grade = project_entry.get()
        if grade == '':
            project = student.project
        else:
            project = int(grade)

        if project == -1:
            can_set_final = False

        lists = []
        for i in range(0, 3):
            grade = list_entries[i].get()
            if grade == '':
                lists.append(student.lists[i])
            else:
                lists.append(int(grade))
        if -1 in lists:
            can_set_final = False

        homeworks = []
        for i in range(0, 10):
            grade = homework_entries[i].get()
            if grade == '':
                homeworks.append(student.home_works[i])
            else:
                homeworks.append(int(grade))
        if -1 in homeworks:
            can_set_final = False

        grade = final_entry.get()
        if not can_set_final:
            final = -1
        elif grade == '':
            final = student.final
        else:
            final = float(grade)

        status = status_entry.get()
        if status == '':
            status = student.status
        if first == '' or last == '' or status == '':
            students_label.config(text="Niepoprawne dane")
            return
        new = Student(mail, first, last, project, lists, homeworks, final, status)
        database[mail] = new
        students_label.config(text="Zmieniono:\n" + str(new))
    except ValueError as ve:
        students_label.config(text=str(ve))
    except Exception:
        students_label.config(text="Niepoprawne dane")


def insert():
    """
    Dodaje nowego studenta do bazy danych.
    Puste oceny są zamieniane na -1, pusty status na 'None', natomiast
    pustego imienia wprowadzić się nie da.
    """
    mail = mail_entry.get()
    if database[mail] is not None:
        students_label.config(text=f"Student z mailem {mail} już istnieje.")
        return

    try:
        can_set_final = True
        name = name_entry.get()
        if name == '':
            raise ValueError("Imie nie może być puste.")
        first = name.split(' ')[0]
        last = name.split(' ')[1]
        if first is None or last is None \
                or first == '' or last == '':
            raise ValueError("Imie nie może być puste.")

        grade = project_entry.get()
        if grade == '':
            project = -1
        else:
            project = int(grade)

        if project == -1:
            can_set_final = False

        lists = []
        for i in range(0, 3):
            grade = list_entries[i].get()
            if grade == '':
                lists.append(-1)
            else:
                lists.append(int(grade))
        if -1 in lists:
            can_set_final = False

        homeworks = []
        for i in range(0, 10):
            grade = homework_entries[i].get()
            if grade == '':
                homeworks.append(-1)
            else:
                homeworks.append(int(grade))
        if -1 in homeworks:
            can_set_final = False

        grade = final_entry.get()
        if not can_set_final or grade == '':
            final = -1
        else:
            final = float(grade)

        status = status_entry.get()
        if status == '':
            status = "None"

        new = Student(mail, first, last, project, lists, homeworks, final, status)
        database.__add__(new)
        students_label.config(text="Dodano:\n" + str(new))
    except ValueError as ve:
        students_label.config(text=str(ve))
    except Exception:
        students_label.config(text="Niepoprawne dane")


name_enter_frame = tk.Frame(left_frame)
name_enter_frame.pack(anchor='w', padx=5, pady=5)

grade_enter_frame = tk.Frame(left_frame)
grade_enter_frame.pack(anchor='w', padx=5, pady=5)

status_enter_frame = tk.Frame(left_frame)
status_enter_frame.pack(anchor='w', padx=5, pady=5)

name_entry = tk.Entry(name_enter_frame, width=screen_width // 4)
name_label = tk.Label(name_enter_frame, text="first and last name")
name_label.pack(side='right', padx=5, pady=5)
name_entry.pack()

grade_label = tk.Label(grade_enter_frame, text="Grades:")

project_frame = tk.Frame(grade_enter_frame)
project_frame.pack(anchor='w', padx=5)
project_entry = tk.Entry(project_frame)
project_label = tk.Label(project_frame, text="project")
project_label.pack(side='right')
project_entry.pack(anchor='w')

list_entries = []
for i in range(0, 3):
    list_frame = tk.Frame(grade_enter_frame)
    list_frame.pack(anchor='w', padx=5)
    list_entry = tk.Entry(list_frame)
    list_label = tk.Label(list_frame, text=f"l_{i + 1}")
    list_label.pack(side='right')
    list_entry.pack(anchor='w')
    list_entries.append(list_entry)

homework_entries = []
for i in range(0, 10):
    homework_frame = tk.Frame(grade_enter_frame)
    homework_frame.pack(anchor='w', padx=5)
    homework_entry = tk.Entry(homework_frame)
    homework_label = tk.Label(homework_frame, text=f"h_{i + 1}")
    homework_label.pack(side='right')
    homework_entry.pack(anchor='w')
    homework_entries.append(homework_entry)

final_frame = tk.Frame(grade_enter_frame)
final_frame.pack(anchor='w', padx=5)
final_entry = tk.Entry(final_frame)
final_label = tk.Label(final_frame, text="final")
final_label.pack(side='right')
final_entry.pack(anchor='w')

status_entry = tk.Entry(status_enter_frame, width=screen_width // 4)
status_label = tk.Label(status_enter_frame, text="status")
status_label.pack(side='right', padx=5, pady=5)
status_entry.pack()

update_button = tk.Button(left_frame, text="Update", command=update)
update_button.pack(side='left')
insert_button = tk.Button(left_frame, text="Add", command=insert)
insert_button.pack(side='right')

# data show
right_frame = tk.Frame(root, width=screen_width // 4, height=left_frame["height"],
                       borderwidth=4, relief="ridge")
right_frame.pack(side="right", padx=10, pady=10)
right_frame.pack_propagate(False)

students_label = tk.Label(right_frame, text="Podaj dane studenta")
students_label.pack(anchor='w')

root.resizable(width=False, height=False)
root.mainloop()
