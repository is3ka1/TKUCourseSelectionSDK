from datetime import datetime
from getpass import getpass

from course_selection import TKUCourseSelector

stud_no, passwd = input('Student Number: '), getpass()

num = 0
while True:
    try:
        course_selector = TKUCourseSelector()
        resp = course_selector.login(stud_no, passwd)
        while True:
            course_selector.add_course('3193')
            num += 1
            print(f'[{datetime.now().isoformat()}] [action#{num}] Add course 3193')

    except AssertionError as error:
        print(f'[{datetime.now().isoformat()}] {error}')
