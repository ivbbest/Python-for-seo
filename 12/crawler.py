# На гугл диске в папке код с занятий в папке 12_less лежит файл crawler.py
# Это парсер, аналог Screaming Frog, который был написан нами на встрече. 
# Доработать его так, чтобы в момент прерывания парсинга он сохранял состояние 
# и в момент следующего запуска спрашивал: желаем ли мы продолжить сканировать 
# старый сайт с прошлого места, или хотим начать сканирование нового сайта.

from time import time
from requests_html import HTMLSession
from reppy.robots import Robots

from deco import time_decorator

import sys

session = HTMLSession()

while True:


    domain = input('Введите домен для краулинга: ')
    first_link = f'http://{domain}/'

    prepared_response = session.get(first_link)
    first_link = prepared_response.url
    domain = first_link.split('/')[2]

    robots_link = f'https://{domain}/robots.txt'

    crawled_links = set()

    links_to_crawl = set()
    links_to_crawl.add(first_link)

    robots = Robots.fetch(robots_link)

    file_results = open('checking_results.txt', 'w', encoding='utf-8')

    while True:

        try:

            if len(links_to_crawl) == 0:
                break
            url = links_to_crawl.pop()

            t1 = time()
            response = time_decorator(session.get)(url)
            t2 = time()

            crawled_links.add(url)
        
            bad_parts = ['cdn-cgi', '.jpg', '.gif']

            for link in response.html.absolute_links:
                if domain not in link:
                    continue
                if not robots.allowed(link, '*'):
                    continue
                if any(x in link for x in bad_parts):
                    continue
                if link in crawled_links:
                    continue
                links_to_crawl.add(link)

            result = f'[{round(t2-t1, 2)} sec] [OK] {url}'
            print(result)

            file_results.write(result+'\n')
            file_results.flush()

        except KeyboardInterrupt:

            print('Пауза')
            status = input('Продолжим? (y/n)\n')
            if status.lower() == 'y':
                continue
            elif status.lower() == 'n':

                #будем ли вообще дальше работать с парсером
                
                status_next = input('Начнем работу с новым доменом? (y/n)\n')
                if status_next.lower() == 'y':
                    break
                else:
                    sys.exit(0)
            else:
                raise Exception('Invalid input')