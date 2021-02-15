import random
from time import sleep
from requests_html import HTMLSession
from core.seoscore import *


website = 'https://py4you.com/'

domain = website.split('/')[2]

results_format = 'Keyword\tUrl\tPosition\tTitle\tDescription\n'


with open('keywords.txt', 'r', encoding='utf-8') as f:
    keys_to_scan = [line.strip() for line in f]


with open('positions.csv', 'r', encoding='utf-8') as f:
    keys_scanned = set([line.split('\t')[0] for line in f])


r_file = open('positions.csv', 'a', encoding='utf-8')

# r_file.write(results_format)


session = HTMLSession()


for key in keys_to_scan:


    if key in keys_scanned:
        continue

    # engine_link = f'https://www.google.com/search?q={key}&num=100&hl=en'
    engine_link = f'https://www.bing.com/search?q={key}&count=20'

    resp = session.get(engine_link)
    

    # html_snipets = resp.html.xpath('//div[@class="g"]')
    html_snipets = resp.html.xpath('//li[@class="b_algo"]')
    position = link = title = description = 'not-found'
    top3 = []
    my_seo_score = top3_seo_score = 0

    for n, html_item in enumerate(html_snipets, start=1):
        # href = html_item.xpath('//div[@class="r"]/a[1]/@href')[0]
        href = html_item.xpath('//h2/a/@href')[0]
        # print(n, html_item, href)
       	if (n>=1) and (n<=3):
       		top3.append(href) 
        if domain in href:
            link = href
            # title = html_item.xpath('//h3/text()')[0]
            title = html_item.xpath('//h2')[0].text
            # description = html_item.xpath('//span[@class="st"]')[0].text
            description = html_item.xpath('//div[@class="b_caption"]/p')[0].text
            position = n
            # print(position, title, description)
            my_seo_score = seo_score(link, key)
        
        
	# print(position, title, description)
    if len(top3) > 0:
    	print(f'{key}\n{top3}')
    	top3_seo_score = round((seo_score(top3[0], key) + seo_score(top3[1], key) + seo_score(top3[2], key))/3)
    	print(top3_seo_score)

    key_result = f'{key}\t{link}\t{position}\t{title}\t{description}\n'

    r_file.write(key_result)

    request_random_timeout = random.randint(5, 15)

    print(f'[OK] {key} | sleep: {request_random_timeout} sec')

    sleep(request_random_timeout)
