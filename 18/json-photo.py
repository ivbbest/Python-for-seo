import json
from requests_html import HTMLSession

with HTMLSession() as session:

    resp = session.get("https://jsonplaceholder.typicode.com/albums/1/photos")
    breakpoint()
    photos = json.loads(resp.text)

with open('url_photo.txt', 'w', encoding='utf-8') as file:

    for urlphoto in photos:
        file.write(urlphoto['thumbnailUrl'] + '\n')
        file.write(urlphoto['url'] + '\n')