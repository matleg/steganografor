import imghdr
import os
import sys
from pathlib import Path
from PIL import Image
from PIL import ExifTags

FILE_PATH = Path(__file__).absolute()
FILE_DIR = Path().absolute()


def get_image(image_name, directory=FILE_DIR):
    """
    input: text
    output: Image object
    """
    image_path = os.path.join(directory, image_name)
    img = Image.open(image_path)
    return img


def hide_image(photo, image_to_hide, significant_bits=1):
    """
    Hide image in photo
    photo: Image object
    image: Image object
    1 pixel <==> 1 bit  (Not 3, one color only to choose)
    """

    photo_width = photo.size[0]
    photo_height = photo.size[1]
    image_width = image_to_hide.size[0]
    image_height = image_to_hide.size[1]

    if photo_width < image_width or photo_height < image_height:
        raise OverflowError("not enough space in picture, image will not be hidden entirely.")

    non_significant_bits = 8 - significant_bits
    new_photo = photo.copy()
    for x in range(image_width):
        for y in range(image_height):
            pr, pg, pb = photo.getpixel((x, y))
            ir, ig, ib = image_to_hide.getpixel((x, y))

            # example with 3 most significant bits
            # photo : 10101010 -> shift by 3 to right : 10101 -> shift by 3 to left : 10101000
            # image : 11100000 -> shift by (8-3=5) to right : 111
            # merge the two : 10101000 | 00000111 = 10101111

            nr = ((pr >> significant_bits) << significant_bits) | (ir >> non_significant_bits)
            ng = ((pg >> significant_bits) << significant_bits) | (ig >> non_significant_bits)
            nb = ((pb >> significant_bits) << significant_bits) | (ib >> non_significant_bits)

            new_photo.putpixel((x, y), (nr, ng, nb))

    return new_photo


def save_picture(picture, filename):
    picture.save(filename)


def main():

    photo_name = "Tower.jpg"
    image_name = "text_foobar.jpg"

    photo = get_image(photo_name)
    image = get_image(image_name)

    for significant_bits in range(1, 9):
        new_photo = hide_image(photo, image, significant_bits)
        sb = str(significant_bits)
        save_picture(new_photo, "tower_with_text_" + sb + "_sb.jpg")


if __name__ == "__main__":
    main()
