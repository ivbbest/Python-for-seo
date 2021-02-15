from requests_html import HTMLSession
import re

url = 'https://habr.com/'

session = HTMLSession()
response = session.get(url)
links_in_url = response.html.absolute_links

# проверяем есть ли в множестве якорные ссылке с # в урле, если нет, то печать
# проверяем, что очередный урл относится к домену habr.com
# если два условия истина, то печать ссылки 

for link in links_in_url:
	if (link.split('/')[2] == 'habr.com') and (not re.search(r'#.*$',link)):
		print(link)