from requests_html import HTMLSession
import string   #чтобы убрать знаки пунктуации экспортирую данную библиотеку

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

def calc_density_meta(density_meta):

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

def quality_density(url,keyword):

    title = my_title(url)
    description = my_description(url)
    h1 = my_h1(url)

    # Вычисление основных параметров страницы

    # len_url = len(url)
    # len_title = len(title)
    # len_description = len(description)
    # len_h1 = len(h1)

    # подсчет количества слов

    # word_url = url.count('-') + url.count('.') + 2
    word_title = title.count(' ') + 1
    word_description = description.count(' ') + 1
    word_h1 = h1.count(' ') + 1

    # подсчет сколько раз встречается ключ в мета-тегах

    keyword_in_title = title.lower().count(keyword.lower())
    keyword_in_description = description.lower().count(keyword.lower())
    keyword_in_h1 = h1.lower().count(keyword.lower())

    # анализ плотности ключа в мета-тегах

    density_title = int(round((keyword_in_title / word_title) * 100))
    density_description = int(round((keyword_in_description / word_description) * 100))
    density_h1 = int(round((keyword_in_h1 / word_h1) * 100))

    # здесь определим качество плотности ключа в мета-тегах

    quality_density_title = calc_density_meta(density_title)
    quality_density_description = calc_density_meta(density_description)
    quality_density_h1 = calc_density_meta(density_h1)

    final_quality_density = round((quality_density_title + quality_density_description + quality_density_h1)/3)

    return final_quality_density

def quality_index_meta(url, keyword):
    # словарь, в котором чем дальше от начала ключ, тем больше вычитаем из Quality

    rating = {0: 0, 1: 3, 2: 7, 3: 14, 4: 20, 5: 30, 6: 40, 7: 55, 8: 65, 9: 80, 10: 90}

    # подсчет индекса ключа в мета-тегах и quality: максимум 100 баллов в 1
    # если нет ключа, то 0 баллов

    try:
        index_key_in_title = my_title(url).lower().split().index(keyword.lower())
        quality_index_in_title = 100 - rating[index_key_in_title]
    except Exception as e:
        quality_index_in_title = 0

    try:
        index_key_in_descr = my_description(url).lower().split().index(keyword.lower())
        quality_index_in_descr = 100 - rating[index_key_in_descr]
    except Exception as e:
        quality_index_in_descr = 0

    try:
        index_key_in_h1 = my_h1(url).lower().split().index(keyword.lower())
        quality_index_in_h1 = 100 - rating[index_key_in_h1]
    except Exception as e:
        quality_index_in_h1 = 0

    final_quality_index = round((quality_index_in_title + quality_index_in_descr + quality_index_in_h1)/3)

    return final_quality_index


#далее каждый из мета-тегов отдельно считываю черех функцию
#добавил 1 в конце мета в функциях, чтобы не было проблем с local/global


def my_title(url):

    with HTMLSession() as session:
        resp = session.get(url)

    try:
        title_tmp = resp.html.xpath('//title')[0].text
        title1 = remove_punctuation(title_tmp)

    except Exception as e:
        print('Title not found on the page', e)
        title1 = ''

    return title1


def my_description(url):

    with HTMLSession() as session:
        resp = session.get(url)

    try:
        description_tmp = resp.html.xpath('//meta[@name="description"]/@content')[0]
        description1 = remove_punctuation(description_tmp)
     
    except Exception as e:
        print('Description not found on the page', e)
        description1 = ''

    return description1


def my_h1(url):

    with HTMLSession() as session:
        resp = session.get(url)

    try:
        h1_tmp = resp.html.xpath('//h1')[0].text
        h11 = remove_punctuation(h1_tmp)
                
    except Exception as e:
        print('H1 not found on the page', e)
        h11 = ''

    return h11

def seo_score(url, keyword):

    score = round((quality_density(url,keyword) + quality_index_meta(url, keyword))/2)
    return score

# while True:
#
#     url = input('\nEnter URL: ')
#     if url == 'exit':
#         break
#
#     keyword = input('Enter Keyword: ')
#
#     if keyword == 'exit':
#         break
#
#     #считаем среднее арифметические 6 показателей для SEO Page Quality и print
#
#     seo_page_quality = seo_score(url, keyword)
#
#     print(f'\nSEO Page Quality is {seo_page_quality}%')