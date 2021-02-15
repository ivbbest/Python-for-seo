# Доделал парсер доменов, работает асинхронно, пишет в файл тоже асинхронно. 
# Скорость работы при 50 потоках 1 тысячу доменов в 2 минуты.
# В чём фишка и зачем это надо: берём в ахрефсе все исходящие с Nyt.com, например, 
# парсим на доступность. Доступные проверяем на трафик, он уже есть в ахрефсе в таблице. 
# Проверяем в вебархиве, если ок - забираем, восстанавливаем и получаем PBN для ссылок
# с трафиком за 20$, либо для своих других целей. Вторым этапом конечно надо парсить 
# по доменам веб-архив, хотя бы заголовки, чтобы китай и редиректы отсечь сразу. Получится почти на автомате. 
# Есть проблема, что r01 банит после 10 тыс. запросов, но я думаю это решается через 
# прокси, тоже доделаю, потому что надо парсить по несколько сот тысяч.


from requests_html import AsyncHTMLSession
import asyncio
from aiofile import AIOFile, Writer

# дописать работу через прокси, т.к. после 10000 запросов банит

DOMAINS = list()
domains_dict = dict()
LINKS_QUEUE = asyncio.Queue()
SCANNED_LINKS = set()

with open('domain1.txt', 'r', encoding='utf-8') as file_source:
    for line in file_source:
        line = line.strip()
        DOMAINS.append(line)
        LINKS_QUEUE.put_nowait(line)

async def domain_cheker(coro_num):

    while True:
        if LINKS_QUEUE.qsize() == 0:
            await asyncio.sleep(4)
            if LINKS_QUEUE.qsize() == 0:
                break
            continue

        domain = await LINKS_QUEUE.get()
        base_url = f'https://r01.ru/domain/whois/check_website.php?sitename={domain}' # r01.ru
        asession = AsyncHTMLSession()
        request = await asession.get(base_url)
        if (request.html.find('span', containing='не зарегистрирован')) == []: # r01.ru
            print(f'[Домен зарегистрирован {coro_num}]', domain)
            domains_dict[domain] = "зарегистрирован" # можно записывать в словарь зарегистрированные, а можно не записывать
            string_rezult_deny = f'{domain}; занят\n'
            async with AIOFile("rezult.txt", 'a', encoding='utf-8') as afp:
                await afp.write(string_rezult_deny)
                await afp.fsync()
        else:
            print(f'[Домен не зарегистрирован {coro_num}]', domain)
            domains_dict[domain] = "домен свободен"
            string_rezult_allow = f'{domain}; свободен\n'

            async with AIOFile("rezult.txt", 'a', encoding='utf-8') as afp:
                await afp.write(string_rezult_allow)
                await afp.fsync()

async def main():

    thread = 50
    tasks = [domain_cheker(i) for i in range(thread)]

    await asyncio.gather(*tasks)

def writer():
    file_rezult = open('rezult.txt', 'w', encoding='utf-8')
    for dom, status in domains_dict.items():
        file_rezult.writelines(dom+'; '+status+'\n')

if __name__ == '__main__':
    asyncio.run(main())