#Написать краулер, который пролазит по всему сайту и найдет на сайте все url адреса открытые 
#для индексации гуглботу, чтобы урлы сохранялись в файл.


from typing import Set, Any, Union

from requests_html import HTMLSession

from reppy.robots import Robots
from time import time, sleep
import csv

url_start = input('Enter url: ')
domain = url_start.split('//')[1]
print(domain)

robots_url = url_start + '/robots.txt'

robots = Robots.fetch(robots_url)
session = HTMLSession()

bad_parts = ['.jpg', '.png', 'cdn-cgi', 'summernote', '#', 'utm', 'tag', 'static']

uniq_set_url = set()

uniq_set_url.add(url_start)

result = set()
result.add(url_start)

while uniq_set_url:

    url = uniq_set_url.pop()

    try:
        t1 = time()
        response = session.get(url)
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

with open('result-url.csv','w',encoding='utf-8', newline='') as file2:
    file_writer = csv.writer(file2, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
    for line_data in result:
        file_writer.writerow(line_data)