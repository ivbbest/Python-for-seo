# КОД НЕ РАБОТАЕТ. ТОЧНЕЕ выдает некорретный результат Скинул показать, как пытался сделать домашку
###################################################################################################
from typing import Set, Any, Union

from requests_html import HTMLSession

import urllib.robotparser
from time import time
from urllib.parse import urlparse

# проверка на разрешение к индексации в роботсе для гуглбота

# def allowed_in_robots(url_def):
#
# 	rp = urllib.robotparser.RobotFileParser()
# 	rp.set_url(url_def + '/robots.txt')
# 	rp.read()
#
# 	if rp.can_fetch('*',url_def):
# 		return True
# 	else:
# 		return False

domain = input('Enter domain: ')

robots_url = domain + '/robots.txt'

rp = urllib.robotparser.RobotFileParser()
rp.set_url(robots_url)
rp.read()

session = HTMLSession()

bad_parts = ['.jpg', '.png', 'cdn-cgi', 'summernote']

uniq_set_url = set()
next_pars_url = set()

uniq_set_url.add(domain)
print(uniq_set_url)

while uniq_set_url:

    url = uniq_set_url.pop()
    print(url)
    next_pars_url.add(url)

    try:
        t1 = time()
        response = session.get(url)
        t2 = time()
    except Exception as e:
        print(e, type(e), url)
        continue

    for link in response.html.absolute_links:

        if not link.startswith('http'):
            continue

        if urlparse(link).netloc not in link:
           continue

        if any([x in link for x in bad_parts]):
            continue

        if link in next_pars_url:
            continue

        if not rp.can_fetch('*', link):
            continue

        uniq_set_url.add(link)

    print(response, f'time: {round(t2 - t1, 2)}', url)

#print(uniq_set_url)