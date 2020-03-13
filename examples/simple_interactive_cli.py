import re
from getpass import getpass

from course_selection import TKUCourseSelector
from data_parsing import parse_data


course_selector = TKUCourseSelector()
course_selector.login(input('Student Number: '), getpass())

command_pattern = re.compile('(?P<operation>[+-]{1}) *(?P<course_id>\d{4})')

print('''
Interactive command line ...
input `+` or `-` and some space or not then input a course id to do a operation on TKU course selection
Example:
    `+ 3193` 
    `- 3193`
''')

while True:
    command = input('command: ')
    match = command_pattern.match(command)
    if match:
        operation = match.group('operation')
        course_id = match.group('course_id')

        if operation == '+':
            func = course_selector.add_course
        elif operation == '-':
            func = course_selector.del_course

        resp = func(course_id)
        print(f"course_id: {course_id}\nmsg: {parse_data(resp.text)['msg']}\n")

    else:
        print('Invalid input\n')
