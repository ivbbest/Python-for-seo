from pprint import pprint
from requests_html import HTMLSession


keyword = input('Введите ключевое слово: ') 	#str

session = HTMLSession() 	#<class 'requests_html.HTMLSession'>

resp = session.get(
	f'https://www.google.com/search?q={keyword}&num=100&hl=en')	 #<class 'requests_html.HTMLResponse'>

links = resp.html.xpath('//div[@class="r"]/a[1]/@href')	 #list

domains = [x.split('/')[2] for x in links if 'http' in x]		 #list

similar_elements = resp.html.xpath('//div[@class="card-section"]//p') 	#list
similar_keys = [el.text.strip() for el in similar_elements]	 #list


print('*'*50)
pprint(links)
print('*'*50)
pprint(domains)
print('*'*50)
pprint(similar_keys)
print('*'*50)