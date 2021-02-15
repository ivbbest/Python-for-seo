import re
from uuid import uuid4
from urllib.parse import unquote
from requests_html import HTMLSession


def get_images_from_google(keyword):
    url = f'https://www.google.com/search?q={keyword}&tbm=isch'

    with HTMLSession() as session:
        response = session.get(url)

    expr = re.compile(r',\[\"(.*)\",')
    matches = re.findall(expr, response.text)
    img_types = {'.jpg', '.png', '.webp', '.gif'}
    images = []
    for match in matches:
        if not any(tp in match for tp in img_types):
            continue
        img = match.split('?')[0]
        images.append(unquote(img))
    return images


def save_image(img_url):

    try:
        with HTMLSession() as session:
            response = session.get(img_url, timeout=4)
        assert response.status_code == 200
    except Exception as e:
        print(e, type(e))
        return

    image_name = img_url.split('/')[-1]
    img_path = f'images/{image_name}'

    with open(img_path, 'wb') as f:
        f.write(response.content)

    print(f'[SAVED] {img_url}')


def main():
    key = input('Enter keyword: ')
    images = get_images_from_google(key)

    for img in images:
        save_image(img)

    print(images)
    print('All Done!')


if __name__ == '__main__':
    main()
