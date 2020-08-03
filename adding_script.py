import datetime
import re

import click

from course_selection import TKUCourseSelector
from data_parsing import parse_data


@click.command()
@click.option('--studid', prompt='Student ID', envvar='STUDID')
@click.option('--password', prompt=True, hide_input=True, envvar='PASSWD')
@click.argument('script', type=click.File('r'))
def cli(studid, password, script):
    while True:
        try:
            course_selector = TKUCourseSelector()
            course_selector.login(studid, password)
        except AssertionError as error:
            click.echo(f'[{datetime.now().isoformat()}] {error}')

    command_pattern = re.compile('(?P<operation>[+-]{1}) *(?P<course_id>\d{4})')

    for command in script:
        match = command_pattern.match(command)
        if match:
            operation = match.group('operation')
            course_id = match.group('course_id')

            if operation == '+':
                func = course_selector.add_course
            elif operation == '-':
                func = course_selector.del_course

            try:
                resp = func(course_id)
            except AssertionError as error:
                click.echo(f'[{datetime.now().isoformat()}] {error}')

            click.echo(f"course_id: {course_id}\nmsg: {parse_data(resp.text)['msg']}\n")

        else:
            click.echo('Invalid input\n')

if __name__ == "__main__":
    cli()
