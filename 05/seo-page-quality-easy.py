from requests_html import HTMLSession
import string   #чтобы убрать знаки пунктуации испортирую данную библиотеку

#чтобы исключить знаки пунктации в мета-тегах использую метод punctuation

def remove_punctuation(temp_value):

    value_meta = ''

    for c in temp_value:
        if c not in string.punctuation:
            value_meta += c

    return value_meta

#определим качество плотности ключа в мета-тегах
#используем следующий принцип: 6-9% - 100 баллов,
#4-5% и 9-10% - 80 баллов, 2-3% и 11-12% - 60 баллов, остальное - 0 баллов

def quality_density_meta(density_meta):

    if (density_meta >= 6) and (density_meta <= 9):
        quality_density = 100
    elif (density_meta >= 4 and density_meta <= 5)\
         or (density_meta > 9 and density_meta <= 10):
        quality_density = 80
    elif (density_meta >= 2 and density_meta <= 3)\
         or (density_meta >= 11 and density_meta <= 12):
        quality_density = 60
    else:
        quality_density = 0

    return quality_density

url = ''
keyword = ''

url = input('\nEnter URL: ')
keyword = input('Enter Keyword: ')


with HTMLSession() as session:
    resp = session.get(url)



try:
    title_tmp = resp.html.xpath('//title')[0].text
    title = remove_punctuation(title_tmp)

except Exception as e:
    print('Title not found on the page', e)
    title = ''

try:
    description_tmp = resp.html.xpath('//meta[@name="description"]/@content')[0]
    description = remove_punctuation(description_tmp)
 
except Exception as e:
    print('Description not found on the page', e)
    description = ''

try:
    h1_tmp = resp.html.xpath('//h1')[0].text
    h1 = remove_punctuation(h1_tmp)
            
except Exception as e:
    print('H1 not found on the page', e)
    h1 = ''

print('*'*50)
print('TITLE:', title)
print('*'*50)
print('DESCRIPTION:', description)
print('*'*50)
print('H1:', h1)
print('*'*50)


# Вычисление основных параметров страницы

len_url = len(url)
len_title = len(title)
len_description = len(description)
len_h1 = len(h1)

# print(f'\nДля страницы {url} узнаем количество символов и слов в мета\n')

# print(f'В url {len_url} символов, в title {len_title} символ,' 
#       f'в h1 {len_h1} знаков, в description {len_description} знаков\n')

#подсчет количества слов

word_url = url.count('-')+url.count('.') + 2
word_title = title.count(' ') + 1
word_description = description.count(' ') + 1
word_h1 = h1.count(' ') + 1

# print(f'В url {word_url} слов, в title {word_title} слов, '
#       f'в description {word_description} слов, а в h1 {word_h1} слов\n')

#подсчет сколько раз встречается ключ в мета-тегах

keyword_in_title = title.lower().count(keyword.lower())
keyword_in_description = description.lower().count(keyword.lower())
keyword_in_h1 = h1.lower().count(keyword.lower())

#анализ плотности ключа в мета-тегах

density_title = int(round((keyword_in_title/word_title)*100))
density_description = int(round((keyword_in_description/word_description)*100))
density_h1 = int(round((keyword_in_h1/word_h1)*100))


#здесь определим качество плотности ключа в мета-тегах

quality_density_title = quality_density_meta(density_title)
quality_density_description = quality_density_meta(density_description)
quality_density_h1 = quality_density_meta(density_h1)

# print(f'Узнаем сколько раз используется ключевое слов {keyword} в мета-тегах:\n')
# print(f'В title {keyword_in_title} раз, в h1 {keyword_in_h1} раз, '
#       f'в description {keyword_in_description} раз\n')


# print(f'А теперь узнаем плотность ключевого слова {keyword} в мета-тегах:\n')
# print(f'В title {density_title}%, в description {density_description}%,' 
#       f'в h1 {density_h1}%')

#словарь, в котором чем дальше от начала ключ, тем больше вычитаем из Quality

rating = {0: 0, 1: 3, 2: 7, 3: 14, 4: 20, 5: 30, 6: 40, 7: 55, 8: 65, 9: 80, 10: 90}

#подсчет индекса ключа в мета-тегах и quality: максимум 100 баллов в 1 
#если нет ключа, то 0 баллов

try:
    index_key_in_title = title.lower().split().index(keyword.lower())
    quality_index_in_title = 100 - rating[index_key_in_title]
except Exception as e:
    quality_index_in_title = 0

try:
    index_key_in_descr = description.lower().split().index(keyword.lower())
    quality_index_in_descr = 100 - rating[index_key_in_descr]
except Exception as e:
    quality_index_in_descr = 0

try:
    index_key_in_h1 = h1.lower().split().index(keyword.lower())
    quality_index_in_h1 = 100 - rating[index_key_in_h1]
except Exception as e:
    quality_index_in_h1 = 0

# print('\nЗначение для Quality в зависимости от индекса ключа в мета:\n')
# print(quality_index_in_title)
# print(quality_index_in_descr)
# print(quality_index_in_h1)


# print(quality_density_title)
# print(quality_density_description)
# print(quality_density_h1)

#считаем среднее арифметические 6 показателей для SEO Page Quality и print

seo_page_quality = round((quality_index_in_title + quality_index_in_descr 
                    + quality_index_in_h1 + quality_density_title 
                    + quality_density_description + quality_density_h1)/6)
print(f'\nSEO Page Quality is {seo_page_quality}%')