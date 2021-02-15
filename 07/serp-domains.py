import random
from time import sleep
from pprint import pprint
from requests_html import HTMLSession


keywords = (
    'buy essays online',
    'buy essay',
    'write my essay',
    'write history essay'
)

session = HTMLSession()

SERP = {}

for key in keywords:
    print(f'Send request to Google: [{key}]')
    resp = session.get(f'https://www.google.com/search?q={key}&num=100&hl=en')
    links = resp.html.xpath('//div[@class="r"]/a[1]/@href')
    SERP[key] = [x.split('/')[2] for x in links if 'http' in x]
    sleep_seconds = random.randint(1, 10)
    print(f'Sleep: {sleep_seconds}')
    sleep(sleep_seconds)

pprint(SERP)

serp_set = []
general_domain = []
tmp_domains = []

#из словаря делается двумерный список, а из него уже одномерный

for domains in SERP.values():
    for dom in domains: 
        serp_set.append(dom)

#уникальный отсортированный список доменов и печается

serp_set = set(serp_set)
serp_set = list(serp_set)
serp_set.sort()
print('\n\nPrint unique domen:\n\n', serp_set)


#отдельным списком те домены, которые есть в каждом серпе, каждого ключа и печать

for domains in SERP.values():
    tmp_domains.append(domains)

general_domain = set(tmp_domains[0])
for i in range(1, len(tmp_domains)):
    general_domain.intersection_update(set(tmp_domains[i]))

general_domain = list(general_domain)
general_domain.sort()

print('\n\nPrint intersection domen in list:\n\n', general_domain)