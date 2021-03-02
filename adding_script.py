import datetime
import re
from datetime import datetime
from pprint import pformat

import click

from course_selection import TKUCourseSelector
from data_parsing import parse_data

command_pattern = re.compile('(?P<operation>[+-?]{1}) *(?P<course_id>\d{4})')


class Dispatcher:
    def __init__(self):
        self.operators = {}

    def add_op(self, operation):
        def wrap(func):
            self.operators[operation] = func
        return wrap

    def sequence_process(self, course_selector, script, verbose=False):
        num = 0
        for command in script:
            match = command_pattern.match(command)
            if match:
                operation = match.group('operation')
                course_id = match.group('course_id')

                if operation in self.operators:
                    result = self.operators[operation](
                        course_selector, course_id)

                    click.echo(
                        f"[{datetime.now().isoformat()}] [action#{num}] "
                        f"course_id: {course_id}\nmsg: {pformat(result) if verbose else result['msg']}\n"
                    )
                    num += 1
                else:
                    click.echo('Operation not handle!')
            else:
                click.echo('Invalid input\n')


disp = Dispatcher()


@disp.add_op('+')
def add_course(course_selector, course_id) -> dict:
    return parse_data(
        course_selector.add_course(course_id).text)


@disp.add_op('-')
def add_course(course_selector, course_id) -> dict:
    return parse_data(
        course_selector.del_course(course_id).text)


@disp.add_op('?')
def add_course(course_selector, course_id) -> dict:
    return parse_data(
        course_selector.course_info(course_id).text)


def copy_io(backup: list, file):
    for line in file:
        backup.append(line)
        yield line


@click.command()
@click.option('--studid', prompt='Student ID', envvar='STUDID')
@click.option('--password', prompt=True, hide_input=True, envvar='PASSWD')
@click.argument('script', type=click.File('r'), default='course_list.txt')
@click.option('-v', '--verbose', count=True)
@click.option('--loop/--no-loop', default=False)
def cli(studid, password, script, verbose, loop):
    backup_cmds = []
    cmds = copy_io(backup_cmds, script)
    while True:
        try:
            course_selector = TKUCourseSelector()
            course_selector.login(studid, password)
            disp.sequence_process(course_selector, cmds, verbose)
            if loop:
                cmds = backup_cmds
            else:
                break
        except AssertionError as error:
            click.echo(f'[{datetime.now().isoformat()}] {error}')


if __name__ == "__main__":
    cli()
