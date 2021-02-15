from time import time
from requests_html import HTMLSession
from reppy.robots import Robots

from deco import time_decorator


session = HTMLSession()


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
        breakpoint()
