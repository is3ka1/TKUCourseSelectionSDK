from datetime import datetime
from getpass import getpass

from course_selection import TKUCourseSelector
from data_parsing import parse_data

stud_no, passwd = input('Student Number: '), getpass()

num = 0
course = '0777'
while True:
    try:
        course_selector = TKUCourseSelector()
        resp = course_selector.login(stud_no, passwd)
        while True:
            resp = course_selector.add_course(course)
            num += 1
            print(f'[{datetime.now().isoformat()}] [action#{num}] Add course {course}')
            action_result = parse_data(resp.text)
            print(f"resp: {action_result['msg']}")

    except AssertionError as error:
        print(f'[{datetime.now().isoformat()}] {error}')
