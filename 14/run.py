"""
1. Вводим ключевую фразу из консоли.
2. Получаем ТОП-10 Google по запросу.
3. Заходим на страницы всех сайтов из ТОП-10 и скачиваем текст.
4. Анализируем текст и генерируем задание для копирайтера.
5. Отправляем задание на email адрес.
"""

from core import (
    google_scraper, get_text,
    texts_analyzer, COPYWRITER_TASK,
    send_email
)


def tz_on_mail(keyword=None):
    if not keyword:
        keyword = input('Enter key phrase: ')

    links = google_scraper(keyword)
    texts = dict()

    for link in links:
        texts[link] = get_text(link)

    top3 = list(texts.values())[:3]

    keywords_main = texts_analyzer(texts.values())
    keywords_secondary = texts_analyzer(top3)
    len_text = len(get_text(link))*6

    keywords_secondary.difference_update(keywords_main)

    task_text = COPYWRITER_TASK.format(
        keywords_main='\n'.join(keywords_main),
        keywords_secondary='\n'.join(keywords_secondary),
        title=keyword.upper(),
        len_text=len_text
    )

    send_email(task_text, "vladimir.primeltd.su@gmail.com")


if __name__ == '__main__':
    tz_on_mail()
