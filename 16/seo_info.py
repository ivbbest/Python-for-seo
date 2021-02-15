# Написать 5 классов, с атрибутами и методами на свое усмотрение: Website, Page, SearchEngine, Text, Title.
# Некоторые классы могут наследоваться один от другого, некоторые могут не наследоваться ни от кого.

from requests_html import HTMLSession
from reppy.robots import Robots


class Text:

    def __init__(self, language, the_text):

        self.language = language
        self.the_text = the_text

    def __len__(self, other):

        length = (self, other)
        return length

    def _what_string(self):

        text_test = self.the_text
        if str(text_test).isalnum():
            return 'alnum'
        elif str(text_test).isdigit():
            return 'digit'
        elif str(text_test).isalpha():
            return 'alpha'


class SearchEngine:

    def __init__(self, url):

        self.session = HTMLSession()
        self.resp = self.session.get(url)

    def description(self):

        try:
            description1 = self.resp.html.xpath('//meta[@name="description"]/@content')[0]

        except Exception as e:
            print('Description not found on the page', e)
            description1 = ''

        return description1

    def h1(self):

        try:
            h11 = self.resp.html.xpath('//h1')[0].text

        except Exception as e:
            print('H1 not found on the page', e)
            h11 = ''

        return h11

    def title(self):

        try:
            title1 = self.resp.html.xpath('//title')[0].text

        except Exception as e:
            print('Title not found on the page', e)
            title1 = ''

        return title1


class Title(SearchEngine, Text):

    def test_quality_title(self):

        len_title = len(self.title())

        if 50 < len_title < 75:
            return f'Нормальный тайтл = {len_title}'
        elif 76 < len_title < 90:
            return 'Возможно стоит скорректировать тайтл = {len_title}'
        else:
            return 'Очень плохой тайтл = {len_title}'

    def __len__(self, other):
        length = (self, other)
        return length

    def __lt__(self, other):
        return (len(self.title())) < (len(other.title()))

    def __le__(self, other):
        return (len(self.title())) <= (len(other.title()))

    def __eq__(self, other):
        return (len(self.title())) == (len(other.title()))

    def __ne__(self, other):
        return (len(self.title())) != (len(other.title()))

    def __ge__(self, other):
        return (len(self.title())) >= (len(other.title()))


class Page(SearchEngine, Text):

    def what_coding(self):

        coding_page = self.resp.encoding
        return coding_page

    def fetch_in_robots(self):

        domain = str(self.resp.url).split('/')[2]
        robots_link = f'https://{domain}/robots.txt'
        robots = Robots.fetch(robots_link)
        flag = robots.allowed(self.resp.url, '*')

        return flag

    def code_answer(self):

        code1 = self.session.get(self.resp.url)

        return code1


class Website(Page):

    pass
