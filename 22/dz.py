import numpy
from PIL import Image, ImageOps


def img_reverse(your_img_file):
    img_open = Image.open(your_img_file)
    im_file_mirrored = ImageOps.mirror(img_open)
    im_file_mirrored.save(f'reversed/{your_img_file[7:]}')


def concat_horizontally(img_frst_rev, img_scnd_rev):
    img_open_first = Image.open(img_frst_rev)
    img_open_second = Image.open(img_scnd_rev)

    if img_open_first.height >= img_open_second.height:
        small_img = img_open_second
        biggest_image = img_open_first
    else:
        small_img = img_open_first
        biggest_image = img_open_second

    result_pixels = []
    for line in numpy.array(small_img):
        new_line = []
        for pix in line:
            b = int(pix[2]) + 100
            b = b if b <= 255 else 255
            new_pix = [pix[0], pix[1], b]
            new_line.append(numpy.asarray(new_pix, dtype=numpy.uint8))
        result_pixels.append(numpy.asarray(new_line))

    result_pixels = numpy.asarray(result_pixels)

    small_img = Image.fromarray(result_pixels, 'RGB')

    new_height = small_img.height
    new_width = int((new_height / biggest_image.height) * biggest_image.width)
    resized_biggest_image = biggest_image.resize((new_width, new_height))

    destination_img = Image.new('RGB', (resized_biggest_image.width + small_img.width, new_height))
    destination_img.paste(small_img, (0, 0))
    destination_img.paste(resized_biggest_image, (small_img.width, 0))

    result_path = f'concatenated/{img_frst_rev[9:].split(".")[0]}_and_{img_scnd_rev[9:]}'
    destination_img.save(result_path)


def main():
    img_file_first = 'images/img1.jpg'
    img_file_second = 'images/img3.jpg'
    img_first_reversed = 'reversed/img1.jpg'
    img_second_reversed = 'reversed/img3.jpg'
    img_reverse(img_file_first)
    img_reverse(img_file_second)
    concat_horizontally(img_first_reversed, img_second_reversed)


if __name__ == '__main__':
    main()
