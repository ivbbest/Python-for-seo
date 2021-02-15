url = 'https://appleiwatch.name/how-to-install-appstore-on-iphone/'
title = 'Как создать учетную запись в AppStore на iPhone и скачивать приложения?'
description = '''AppStore – это магазин приложений для устройств компании 
			     Apple (iPhone, iPad, Apple Watch и другие). 
			     Без App Store не будет работать ни одно приложение, 
			     так как их будет неоткуда скачивать.'''
h1 = 'Как установить AppStore на iPhone и как им пользоваться?'
keyword = 'iPhone'

len_url = len(url)
len_title = len(title)
len_description = len(description)
len_h1 = len(h1)

print(f'\nДля страницы {url} узнаем количество символов и слов в мета\n')

print(f'В url {len_url} символов, в title {len_title} символ, в description {len_description} знаков, а в h1 {len_h1} знаков\n')

word_url = url.count('-')+url.count('.') + 2
word_title = title.count(' ') + 1
word_description = description.count(' ') + 1
word_h1 = h1.count(' ') + 1

print(f'В url {word_url} слов, в title {word_title} слов, в description {word_description} слов, а в h1 {word_h1} слов\n')

keyword_in_title = title.lower().count(keyword.lower())
keyword_in_description = description.lower().count(keyword.lower())
keyword_in_h1 = h1.lower().count(keyword.lower())

density_title = round((keyword_in_title/word_title)*100)
density_description = round((keyword_in_description/word_description)*100)
density_h1 = round((keyword_in_h1/word_h1)*100)

print(f'Узнаем сколько раз используется ключевое слов {keyword} в мета-тегах:\n')
print(f'В title {keyword_in_title} раз, в description {keyword_in_description} раз, в h1 {keyword_in_h1} раз\n')


print(f'А теперь узнаем плотность ключевого слова {keyword} в мета-тегах:\n')
print(f'В title {density_title}%, в description {density_description}%, в h1 {density_h1}%')