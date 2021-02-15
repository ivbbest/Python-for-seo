#Ранее в ДЗ мы писали парсер, аналог Screaming Frog. Делали это с помощью функций.
#Нужно переписать этот парсер в стиле ООП и чтобы он представлялся сайту от имени
# Гугл Бота. Оценка за задание - 50 баллов.

from requests_html import HTMLSession
import random
from reppy.robots import Robots
from time import time, sleep


class GoogleCrawler:

    def __init__(self, url):
        self.url_start = url
        self.agents = []
        self.session = HTMLSession()
        self.set_all_agents()

        self.fieldnames = ['ad_title', 'ad_date', 'ad_price',
                           'ad_photo', 'ad_link', 'ad_city']
        print('Crawler Initialized')

    def get_random_headers(self):
        print('get_random_headers')
        return {'User-Agent': random.choice(self.agents)}

    def set_all_agents(self):
        with open('ua.txt', 'r', encoding='utf-8') as f:
            self.agents = [x.strip() for x in f if x.strip()]

    def run(self):

        domain = self.url_start.split('//')[1]
        print(domain)

        robots_url = self.url_start + '/robots.txt'

        robots = Robots.fetch(robots_url)
        self.session = HTMLSession()

        bad_parts = ['.jpg', '.png', 'cdn-cgi', 'summernote', '#', 'utm', 'tag', 'static']

        uniq_set_url = set()

        uniq_set_url.add(self.url_start)

        result = set()
        result.add(self.url_start)

        while uniq_set_url:

            url = uniq_set_url.pop()

            try:
                t1 = time()
                headers = self.get_random_headers()
                response = self.session.get(url, headers=headers)
                t2 = time()
            except Exception as e:
                print(e, type(e), url)
                continue

            links = response.html.absolute_links

            for link in links:

                if link not in result:


                    if not robots.allowed(link, '*'):
                        continue
                                       
                    if not link.startswith('http'):
                        continue

                    if domain not in link:
                        continue

                    if any([x in link for x in bad_parts]):
                        continue
                        
                    uniq_set_url.add(link)

                result.add(link)

            print(response, f'time: {round(t2 - t1, 2)}', url)

        print(result)

if __name__ == '__main__':
    url = input('Enter url: ')
    crawl = GoogleCrawler(url)
    crawl.run()
