from PIL import Image, ImageOps
from math import ceil
from os import listdir
from os.path import isfile, join
from datetime import datetime
from rich.progress import track
from rich import print


def valid_images(all_files):
    ext = ['.JPG', '.JPEG', '.PNG']
    valid = []
    for image in all_files:
        if image[-4:].upper() in ext:
            if image[:7] == "Collage":
                pass
            else:
                valid.append(image)
    return valid


def get_all_images():
    mypath = input("Enter image path: ")
    return valid_images([f for f in listdir(mypath) if isfile(join(mypath, f))])


def get_avg_size(listofimages):
    h, w = 0, 0
    for proc, p in zip(track(range(len(listofimages)), description="Getting Average..."), listofimages):
        im = Image.open(p)
        width, height = im.size
        h += height
        w += width
    #     print('Process image {0} and height-weight is {1} '.format(p, im.size))
    # print('Calculate average w-h: {0} ~ {1}'.format(w //len(listofimages), h//len(listofimages)))
    return w//len(listofimages), h//len(listofimages)


def _convert_in_same_size(width, height, listofimages):
    newsize = (width, height)
    for proc, p in zip(track(range(len(listofimages)), description="Converting images..."), listofimages):
        images = Image.open(p)
        w, h = images.size
        if w != width and h != height:
            images = images.resize(newsize)
            images.save(p)
            # print('Saved image {0} and size is {1}'.format(p, newsize))


def _create_collage_frame(frame_width, images_per_row, padding, listofimages):
    img_width, img_height = Image.open(listofimages[0]).size
    sf = (frame_width-(images_per_row-1)*padding) / (images_per_row*img_width)
    scaled_img_width = ceil(img_width*sf)
    scaled_img_height = ceil(img_height*sf)

    number_of_rows = ceil(len(listofimages)/images_per_row)
    frame_height = ceil(sf*img_height*number_of_rows)

    new_im = Image.new('RGB', (frame_width, frame_height))
    i, j = 0, 0

    for num, im in enumerate(listofimages):
        if num % images_per_row == 0:
            i = 0
        im = Image.open(im)
        im.thumbnail((scaled_img_width, scaled_img_height))
        im_br = ImageOps.expand(im, border=20, fill=((103, 201, 60)))
        y_cord = (j//images_per_row)*scaled_img_height
        new_im.paste(im_br, (i, y_cord))
        i = (i+scaled_img_width)+padding
        j += 1
    # new_im.show()
    dt = datetime.now().strftime('%Y%m%d_') + \
        str(datetime.now().microsecond)[-3:]

    new_im.save(f"Collage_{dt}.jpg", quality=80,
                optimize=True, progressive=True)


# progress bar

if __name__ == "__main__":

    listofimages = get_all_images()
    get_width, get_height = get_avg_size(listofimages)
    _convert_in_same_size(get_width, get_height, listofimages)
    _create_collage_frame(get_width*3, 3, 4, listofimages)
    print("Collage [bold magenta]Done![/bold magenta]")
