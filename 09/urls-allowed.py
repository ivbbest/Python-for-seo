import urllib.robotparser

url_list = ['https://habr.com/ru/search/?q=python',
            'https://habr.com/ru/company/southbridge/blog/489628/',
            'https://habr.com/ru/company/skyeng/blog/487764/',
            'https://habr.com/register/',
            'https://habr.com/ru/users/gbougakov/',
            'https://habr.com/ru/search/?q=django',
            'https://habr.com/ru/post/486998/']

rp = urllib.robotparser.RobotFileParser()
rp.set_url('https://habr.com/robots.txt')
rp.read()

print('\nСтраницы разрешенные для индексации из списка:\n')

for url in url_list:
        if (rp.can_fetch('Googlebot',url)) and (rp.can_fetch('*',url))\
            and (rp.can_fetch('Yandex',url)) and (rp.can_fetch('Slurp',url)):

            print(url)