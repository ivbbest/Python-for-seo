# Спарсить картинки, используя функцию get_images_from_google c занятия.
# Взять из спаршенных картинок 2 файла, отзеркалить каждый из них по горизонтали
# и отзеркаленные склеить в одну
# картинку путем горизонтального приклеивания друг к другу.

import re
from urllib.parse import unquote
from requests_html import HTMLSession
import random
import os
from PIL import Image


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

        if len(images) > 15:
            break

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

    num_foto1 = random.randint(0, 15)
    num_foto2 = random.randint(0, 15)

    save_foto1 = images[num_foto1]
    save_foto2 = images[num_foto2]

    save_image(save_foto1)
    save_image(save_foto2)

    list_file = os.listdir(path="images")

    file1 = list_file[0]
    file2 = list_file[1]

    img1 = Image.open(f'images/{file1}')
    img2 = Image.open(f'images/{file2}')

    old_w1, old_h1 = img1.size
    old_w2, old_h2 = img2.size

    img1 = img1.transpose(Image.FLIP_LEFT_RIGHT)
    img2 = img2.transpose(Image.FLIP_LEFT_RIGHT)

    new_image = Image.new('RGB', (max(old_w1, old_w2) + min(old_w1, old_w2), max(old_h1, old_h2)))

    if max(old_w1, old_w2) == old_w1:

        new_image.paste(img1, (0, 0))
        new_image.paste(img2, (max(old_w1, old_w2), 0))

    else:

        new_image.paste(img2, (0, 0))
        new_image.paste(img1, (max(old_w1, old_w2), 0))

    new_image.show()
    new_image.save(f'images/new_image.jpg')

    print(images)
    print('All Done!')

if __name__ == '__main__':
    main()