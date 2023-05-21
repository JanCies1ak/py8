This is a GUI to manage students in database.
Database used here is sqlite3.
Student format is:
<lt>
    <li>e-mail</li>
    <li>first name</li>
    <li>last name</li>
    <li>project grade 
        (0-40, or -1 for empty)
    </li>
    <li>3 grades for list with tasks
        (0-20, or -1 for empty)
    </li>
    <li>10 grades for homeworks
        (0-100, or -1 for empty)
    </li>
    <li>final grade 
        (2, 3, 3.5, 4, 4.5, 5, or -1 for empty)
    </li>
    <li>status</li>
</lt>
<p>At the beginning you will see a window with short student info:
their e-mails, first and last names, final grades and statuses.
To check all grades you need to double-click on student you want.</p>
<p>To add student you need to click button "Add student". After this
you will need to enter all student data and click "Add" button. 
You can skip grades and status. They would be automatically filed 
(grades with -1 and status withNone)</p>
<p>To delete student you need click button "Delete student". After this
you will need to enter all student mail and click "Delete" button.</p>
<p>To add student you need to click button "Update student". After this
you will need to enter all student data and click "Update" button. 
You can skip names, grades and status. They would be automatically 
filed with old data.</p>
