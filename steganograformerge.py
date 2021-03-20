import imghdr
import os
import sys
from pathlib import Path
from PIL import Image
from PIL import ExifTags

FILE_PATH = Path(__file__).absolute()
FILE_DIR = Path().absolute()

RED = 0
GREEN = 1
BLUE = 2


def get_images_paths(directory=FILE_DIR):
    """
    """
    images = []
    for img in os.listdir(directory):
        if not os.path.isfile(img):
            continue
        if imghdr.what(img) in ('png', 'jpeg'):
            images.append(img)
    return images


def get_image(image_name, directory=FILE_DIR):
    """
    input: text
    output: Image object
    """
    image_path = os.path.join(directory, image_name)
    img = Image.open(image_path)
    return img


def print_image_properties(image):
    """
    input: Image object
    """
    print(image.filename, ", format:", image.format, ", size:", image.size, ", mode:", image.mode)


def print_images_properties(directory=FILE_DIR):
    """
    """
    for image_path in get_images_paths(directory):
        im = get_image(image_path)
        print_image_properties(im)


def print_tags(exifdata, max_size=200):
    """
    """

    print("Tags in exifdata :")
    for tag_id in exifdata:
        tag = ExifTags.TAGS.get(tag_id)  # see exif_tags_list.txt
        data = exifdata.get(tag_id, tag_id)  # take the number if no value associated
        # do not print image
        # if isinstance(data, bytes):
        #     continue
        # do not print large GPS coord
        size = sys.getsizeof(data)
        if size > max_size:
            print(f"{tag_id:25}: Data too large ({size/1000}ko). tag type: {type(tag)}, data type: {type(data)}")
            continue
        print(f"{tag:25}: {data}, type: {type(data)}")
    print("** End print tags **")


def hide_image(photo, image_to_hide, significant_bits=1):
    """
    photo: Image object
    image: Image object
    text_to_hide: ascii text to encode
    color to choose
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

            nr = ((pr >> significant_bits) << significant_bits) | (ir >> non_significant_bits)
            ng = ((pg >> significant_bits) << significant_bits) | (ig >> non_significant_bits)
            nb = ((pb >> significant_bits) << significant_bits) | (ib >> non_significant_bits)

            if x==0 and y==0:
                print(bin((pr >> significant_bits) << significant_bits))
                print(bin((ir >> non_significant_bits)))
                print(((pr >> significant_bits) << significant_bits) & (ir >> non_significant_bits))
            new_photo.putpixel((x, y), (nr, ng, nb))

    return new_photo
    
    
def save_picture(picture, filename):
    """
    """
    picture.save(filename)


def main():
    get_images_paths()
    print_images_properties()

    photo_name = "Tower.jpg"
    image_name = "text_foobar.jpg"

    photo = get_image(photo_name)
    image = get_image(image_name)

    print("photo")
    data = photo.getdata()
    imgdata = list(data)
    for i in range(5):
        print(imgdata[i * 10:i * 10 + 10])

    print("image")
    data = image.getdata()
    imgdata = list(data)
    for i in range(5):
        print(imgdata[i * 10:i * 10 + 10])

    
    for significant_bits in (1, 2, 3, 4, 5, 6, 7, 8):
        new_photo = hide_image(photo, image, significant_bits)
        sb = str(significant_bits) 
        save_picture(new_photo, "tower_with_text_" + sb + "_sb.jpg")


if __name__ == "__main__":
    main()
