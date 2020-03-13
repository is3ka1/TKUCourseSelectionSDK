import re

import requests
from parsel import Selector


class TKUCourseSelector:
    captcha_pattern = re.compile('^\[("[0-9a-z]{40}",?){6}\]$')
    captcha_mapping = {
        'b6589fc6ab0dc82cf12099d1c2d40ab994e8410c': '0',
        '356a192b7913b04c54574d18c28d46e6395428ab': '1',
        'da4b9237bacccdf19c0760cab7aec4a8359010b0': '2',
        '77de68daecd823babbb58edb1c8e14d7106e83bb': '3',
        '1b6453892473a467d07372d45eb05abc2031647a': '4',
        'ac3478d69a3c81fa62e60f5c3696165a4e5e6ac4': '5',
        'c1dfd96eea8cc2b62785275bca38ac261256e278': '6',
        '902ba3cda1883801594b6e1b452790cc53948fda': '7',
        'fe5dbbcea5ce7e2988b8c69bcfdfde8904aabc1f': '8',
        '0ade7c2cf97f75d009975f4d720d1fa6c19f4897': '9'
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers['User-Agent'] = (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:73.0) Gecko/20100101 Firefox/73.0')
        self.last_page = None

    @staticmethod
    def get_captcha_code(text: str):
        assert __class__.captcha_pattern.match(text) is not None, "captcha not match!"
        return ''.join(map(__class__.captcha_mapping.get, eval(text)))

    @staticmethod
    def get_hidden_arg(html: str):
        sel = Selector(html)
        return {
            prop: sel.css(f'#{prop}::attr("value")').get()
            for prop in ('__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION')
        }

    def login(self, student_num: str, passwd: str) -> requests.Response:
        login_page = self.session.get(
            'https://www.ais.tku.edu.tw/EleCos/login.aspx?ReturnUrl=%2felecos%2f')
        captcha_page = self.session.post(
            'https://www.ais.tku.edu.tw/EleCos/Handler1.ashx')

        post_data = self.get_hidden_arg(login_page.text)
        post_data.update({
            '__EVENTTARGET': 'btnLogin',
            'txtCONFM': self.get_captcha_code(captcha_page.text),
            'txtStuNo': student_num,
            'txtPSWD': passwd
        })

        login_resp = self.session.post(
            'https://www.ais.tku.edu.tw/EleCos/login.aspx?ReturnUrl=%2felecos%2f', data=post_data)
        assert login_resp.history and login_resp.history[0].status_code == 302, "Login failed QWQ"

        self.last_page = login_resp
        return login_resp

    def _action(self, course_id: str, action: str) -> requests.Response:
        post_data = self.get_hidden_arg(self.last_page.text)
        post_data.update({
            '__EVENTTARGET': action,
            'txtCosEleSeq': course_id
        })

        self.last_page = resp = self.session.post(
            'https://www.ais.tku.edu.tw/EleCos/action.aspx', data=post_data)
        assert resp.status_code == 200 and resp.history == [], f"action({action}) failed!"
        
        return self.last_page

    def course_info(self, course_id: str) -> requests.Response:
        return self._action(course_id, 'btnOffer')

    def add_course(self, course_id: str) -> requests.Response:
        return self._action(course_id, 'btnAdd')

    def del_course(self, course_id: str) -> requests.Response:
        return self._action(course_id, 'btnDel')


if __name__ == "__main__":
    course_selector = TKUCourseSelector()
    resp = course_selector.login('Student Number', 'Password')
    info_resp = course_selector.course_info('Course ID')
    add_resp = course_selector.add_course('Course ID')
    del_resp = course_selector.del_course('Course ID')
