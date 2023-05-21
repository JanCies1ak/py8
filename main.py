import tkinter as tk
import sqlite3
from tkinter import ttk
from typing import Literal

from screeninfo import get_monitors

final_grades = [2, 3, 3.5, 4, 4.5, 5, -1]


class Student:
    """
    Class that represent student.
    Stores: mail, first and last names, grades for project, lists, homeworks, final grade and status.
    """
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
            raise ValueError("Incorrect data size.")

        if project < -1 or project > 40:
            raise ValueError("Incorrect project grade.")

        for grade in lists:
            if grade < -1 or grade > 20:
                raise ValueError("Incorrect list grade.")

        for grade in home_works:
            if grade < -1 or grade > 100:
                raise ValueError("Incorrect homework grade.")

        if final not in final_grades:
            raise ValueError("Incorrect final grade.")

        if final != -1 and (project == -1 or -1 in lists or -1 in home_works):
            raise ValueError("Final grade cannot be put before other grades are set.")

        self.mail = mail
        self.first_name = first_name
        self.last_name = last_name
        self.project = project
        self.lists = lists
        self.home_works = home_works
        self.final = final
        self.status = status

    @staticmethod
    def grade_from_str(s: str, t: type(float) | type(int) = type(int)) -> int | float:
        """
        Gives a grade from given str.
        Empty string will be converted into -1.
        :param s: input from user
        :param t: type of the grade.
        :return: grade
        """
        if s == "":
            return -1
        else:
            return t(s)

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

    def get_grades(self) -> tuple[int | str | float]:
        return tuple([self.mail,
                      self.project if self.project != -1 else "_",
                      *(lst if lst != -1 else "_" for lst in self.lists),
                      *(hw if hw != -1 else "_" for hw in self.home_works),
                      self.final if self.final != -1 else "_"])


class DBController:
    database = None
    students = None

    def connect(self) -> sqlite3.dbapi2.Connection:
        return sqlite3.connect(self.database)

    def __init__(self, db: str):
        self.database = db

        connection = self.connect()
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
        connection.execute(query)
        self.students = list()
        query = "SELECT * FROM student"
        res = connection.execute(query)
        studs = res.fetchall()
        connection.close()
        for student in studs:
            self.students.append(Student.from_iterable(student))

    def __getitem__(self, mail: str) -> Student | None:
        if mail not in self:
            return None
        for stud in self.students:
            if stud.mail == mail:
                return stud

    def __contains__(self, mail: str) -> bool:
        for stud in self.students:
            if stud.mail == mail:
                return True
        return False

    def __add__(self, new: Student):
        if new.mail in self:
            return
        connection = self.connect()
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
        connection.execute(query, new.to_list())
        connection.commit()
        connection.close()
        self.students.append(new)

    def __delitem__(self, mail: str):
        if mail not in self:
            return
        query = "DELETE FROM student WHERE mail = ?"
        connection = self.connect()
        connection.execute(query, [mail])
        connection.commit()
        connection.close()

        stud = self[mail]
        self.students.remove(stud)
        return

    def __setitem__(self, mail: str, new_values: Student):
        if mail not in self:
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
        connection = self.connect()
        connection.execute(query, student_values)
        connection.commit()
        connection.close()

        stud = self[mail]
        stud.first_name = new_values.first_name
        stud.last_name = new_values.last_name
        stud.project = new_values.project
        stud.lists = new_values.lists
        stud.home_works = new_values.home_works
        stud.final = new_values.final
        stud.status = new_values.status


database = DBController("students.db")

root = tk.Tk()
root.title("Students")
screen_width = get_monitors()[0].width
screen_height = get_monitors()[0].height
root.geometry(f"{screen_width // 2}x{int(screen_height / 1.6)}")

treeview = ttk.Treeview(root)
treeview["columns"] = ("mail", "f_name", "l_name", "final", "status")
treeview.column("#0", width=0)
treeview.heading("mail", text="Mail")
treeview.heading("f_name", text="First name")
treeview.heading("l_name", text="Last name")
treeview.heading("final", text="Final grade")
treeview.heading("status", text="Status")


class EntryFrame(tk.Frame):
    """
    Frame with label and entry.
    Used to set label to the left of entry and to reduce code length (~3 times).
    """
    entry = None
    label = None

    def __init__(self,
                 master: tk.Misc | None,
                 *,
                 label: str,
                 width: int,
                 borderwidth: str | float = 0,
                 relief: Literal["raised", "sunken", "flat", "ridge", "solid", "groove"] = "flat"):
        super(EntryFrame, self).__init__(master, borderwidth=borderwidth, relief=relief)
        self.entry = tk.Entry(self, width=width)
        self.label = tk.Label(self, text=label)

    def pack(self):
        self.label.pack(side="left", padx=5, pady=5)
        self.entry.pack(side="right", padx=5, pady=5, before=self.label)
        super(EntryFrame, self).pack(anchor="e")

    def get(self):
        return self.entry.get()


def open_details_window(event):
    """
    Open a new window when program starts.
    Window will have information about all students: grades, first and last name, final grade and status.
    When you will click 2 times on student a new window will appear with all grades of this student.
    :param event: not used
    """
    selected_item = treeview.focus()
    if selected_item:
        item_data = treeview.item(selected_item)
        values = item_data['values']
        stud = database[values[0]]

        new_window = tk.Toplevel(root)
        new_window.title(f"{stud.first_name} {stud.last_name}'s grades")
        grade_tree = ttk.Treeview(new_window)

        grade_tree["columns"] = ("id", "mail"
                                       "project",
                                 "l_1", "l_2", "l_3",
                                 "h_1", "h_2", "h_3", "h_4", "h_5", "h_6", "h_7", "h_8", "h_9", "h_10",
                                 "final")
        grade_tree.column("#0", width=0)
        grade_tree.heading("#1", text="Mail")
        grade_tree.column("#1", width=300)

        grade_tree.heading("#2", text="Project")
        grade_tree.column("#2", width=100)

        grade_tree.heading("#3", text="l_1")
        grade_tree.column("#3", width=50)
        grade_tree.heading("#4", text="l_2")
        grade_tree.column("#4", width=50)
        grade_tree.heading("#5", text="l_3")
        grade_tree.column("#5", width=50)

        grade_tree.heading("#6", text="h_1")
        grade_tree.column("#6", width=50)
        grade_tree.heading("#7", text="h_2")
        grade_tree.column("#7", width=50)
        grade_tree.heading("#8", text="h_3")
        grade_tree.column("#8", width=50)
        grade_tree.heading("#9", text="h_4")
        grade_tree.column("#9", width=50)
        grade_tree.heading("#10", text="h_5")
        grade_tree.column("#10", width=50)
        grade_tree.heading("#11", text="h_6")
        grade_tree.column("#11", width=50)
        grade_tree.heading("#12", text="h_7")
        grade_tree.column("#12", width=50)
        grade_tree.heading("#13", text="h_8")
        grade_tree.column("#13", width=50)
        grade_tree.heading("#14", text="h_9")
        grade_tree.column("#14", width=50)
        grade_tree.heading("#15", text="h_10")
        grade_tree.column("#15", width=50)

        grade_tree.heading("#16", text="Final")
        grade_tree.column("#16", width=70)

        grade_tree.insert("", "end", values=stud.get_grades())
        grade_tree.pack()


def load_data():
    students = database.students

    treeview.delete(*treeview.get_children())
    for stud in students:
        treeview.insert("", "end", values=(stud.mail,
                                           stud.first_name,
                                           stud.last_name,
                                           stud.final if stud.final != -1 else '_',
                                           stud.status))


def open_delete_window():
    new_window = tk.Toplevel(root)
    new_window.title("Delete student")

    mail_label = ttk.Label(new_window, text="Mail:")
    mail_label.pack()
    mail_entry = ttk.Entry(new_window, width=60)
    mail_entry.pack()

    def delete():
        _mail = mail_entry.get()
        database.__delitem__(_mail)
        load_data()
        new_window.destroy()

    button = tk.Button(new_window, text="Delete", command=delete)
    button.config(borderwidth=3)
    button.pack(anchor='w')


def open_add_window():
    new_window = tk.Toplevel(root)
    new_window.title("Add student")

    mail_frame = EntryFrame(new_window, label="Mail:", width=60)
    mail_frame.pack()

    f_name_frame = EntryFrame(new_window, label="First name:", width=60)
    f_name_frame.pack()

    l_name_frame = EntryFrame(new_window, label="Last name:", width=60)
    l_name_frame.pack()

    project_frame = EntryFrame(new_window, label="Project:", width=60)
    project_frame.pack()

    list_frames = []
    for i in range(0, 3):
        frame = EntryFrame(new_window, label=f"List {i + 1}", width=60)
        frame.pack()
        list_frames.append(frame)

    homework_frames = []
    for i in range(0, 10):
        frame = EntryFrame(new_window, label=f"Homework {i + 1}", width=60)
        frame.pack()
        homework_frames.append(frame)

    final_frame = EntryFrame(new_window, label="Final:", width=60)
    final_frame.pack()

    status_frame = EntryFrame(new_window, label="Status:", width=60)
    status_frame.pack()

    def add():
        try:
            mail = mail_frame.get()
            if mail == "":
                raise ValueError("Mail cannot be empty.")

            f_name = f_name_frame.get()
            if f_name == "":
                raise ValueError("First name cannot be empty")

            l_name = l_name_frame.get()
            if l_name == "":
                raise ValueError("Last name cannot be empty")

            project = Student.grade_from_str(project_frame.get())

            lists = []
            for list_entry in list_frames:
                lists.append(Student.grade_from_str(list_entry.get()))

            homeworks = []
            for homework_entry in homework_frames:
                homeworks.append(Student.grade_from_str(homework_entry.get()))
            final = Student.grade_from_str(final_frame.get(), float)
            status = status_frame.get()
            if status == "":
                status = "None"

            new_student = Student(mail, f_name, l_name, project, lists, homeworks, final, status)

            database.__add__(new_student)
            load_data()
            new_window.destroy()
        except ValueError as ve:
            print(ve)

    button = tk.Button(new_window, text="Add", command=add, width=20)
    button.pack(anchor='w', pady=10, padx=10)


def open_update_window():
    new_window = tk.Toplevel(root)
    new_window.title("Update student")

    mail_frame = EntryFrame(new_window, label="Mail:", width=60, borderwidth=2, relief="ridge")
    mail_frame.pack()

    f_name_frame = EntryFrame(new_window, label="First name:", width=60)
    f_name_frame.pack()

    l_name_frame = EntryFrame(new_window, label="Last name:", width=60)
    l_name_frame.pack()

    project_frame = EntryFrame(new_window, label="Project:", width=60)
    project_frame.pack()

    list_frames = []
    for i in range(0, 3):
        frame = EntryFrame(new_window, label=f"List {i + 1}", width=60)
        frame.pack()
        list_frames.append(frame)

    homework_frames = []
    for i in range(0, 10):
        frame = EntryFrame(new_window, label=f"Homework {i + 1}", width=60)
        frame.pack()
        homework_frames.append(frame)

    final_frame = EntryFrame(new_window, label="Final:", width=60)
    final_frame.pack()

    status_frame = EntryFrame(new_window, label="Status:", width=60)
    status_frame.pack()

    def update():
        try:
            mail = mail_frame.get()
            if mail == "":
                raise ValueError("Mail cannot be empty.")

            if mail not in database:
                raise KeyError("Student with given mail not exist.")

            student = database[mail]

            f_name = f_name_frame.get()
            if f_name == "":
                f_name = student.first_name

            l_name = l_name_frame.get()
            if l_name == "":
                l_name = student.last_name

            project = Student.grade_from_str(project_frame.get())

            lists = []
            for j in range(0, 3):
                list_grade = list_frames[j].get()
                if list_grade == "":
                    list_grade = student.lists[j]
                else:
                    list_grade = Student.grade_from_str(list_grade, int)
                lists.append(list_grade)

            homeworks = []
            for j in range(0, 10):
                homework_grade = homework_frames[j].get()
                if homework_grade == "":
                    homework_grade = student.home_works[i]
                else:
                    homework_grade = Student.grade_from_str(homework_grade, int)
                homeworks.append(homework_grade)

            final = final_frame.get()
            if final == "":
                final = student.final
            else:
                final = Student.grade_from_str(final, int)

            status = status_frame.get()
            if status == "":
                status = student.status

            new_student = Student(mail, f_name, l_name, project, lists, homeworks, final, status)

            database[mail] = new_student
            load_data()
            new_window.destroy()
        except ValueError as ve:
            print(ve)
        except KeyError as ie:
            print(ie)

    button = tk.Button(new_window, text="Update", command=update, width=20)
    button.pack(anchor='w', pady=10, padx=10)


delete_button = tk.Button(root, text="Delete student", command=open_delete_window)
delete_button.config(background='red', font=("Helvetica", 9, 'bold'))

add_button = tk.Button(root, text="Add student", command=open_add_window)

update_button = tk.Button(root, text="Update student", command=open_update_window)

treeview.pack(side='top')
add_button.pack(side='left', padx=5, pady=5)
update_button.pack(side="left", padx=5, pady=5)
delete_button.pack(side='left', padx=5, pady=5)

treeview.bind("<Double-1>", open_details_window)

load_data()

root.resizable(width=False, height=False)
root.mainloop()
