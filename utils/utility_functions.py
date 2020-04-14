import os
import json
from random import randint
import math
import cv2
from zipfile import ZipFile


ROOT = "../../../vaibhavthakur/PycharmProjects"

def read_config(ROOT="/Users/vaibhavthakur/PycharmProjects"):

    with open(os.path.join(ROOT,"Image Treatment/config/input_config.json"),'r+') as config:

        return json.load(config)


def call_rand_image(path, list_images):

    rand_pick = randint(0, len(list_images) - 1)
    image_pick = list_images[rand_pick]

    with open(os.path.join(path, image_pick)) as file :
        return file

def resize_image(image, width = None, height = None,
                     inter = cv2.INTER_AREA):

    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]
    print(h, w)
    print(image.shape)

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


def get_position(size_im, size_watermark):

    hi, wi = size_im
    hw, ww = size_watermark

    pos = randint(1, 9)

    margin_size = (round(hi*0.025),
                  round(wi*0.025))


    pos_idx_height  = math.floor(hi/3)*(
        math.floor(pos/3)-1 if pos % 3 == 0 else math.floor(pos/3))

    pos_idx_width = math.floor(wi/3)*(2 if pos % 3 == 0 else (pos % 3)-1)

    add_jitter_h = randint(0,10)
    add_jitter_w = randint(0,12)

    extended_h = add_jitter_h + margin_size[0] + pos_idx_height + hw
    extended_w = add_jitter_w + margin_size[1] + pos_idx_width + ww
    start_coords = (margin_size[0]+add_jitter_h+pos_idx_height,
                  margin_size[1]+add_jitter_w+pos_idx_width)

    return(extended_h,
           extended_w,
           start_coords)



def reshape_watermark(size_im,extended_h, extended_w, start_coords,
                      watermark_img):


    hi,wi = size_im

    extended_h, extended_w, start_coords = (extended_h, extended_w,
                                            start_coords)

    start_h = start_coords[0]
    start_w = start_coords[1]

    hw, ww = watermark_img.shape

    if extended_h < hi & extended_w < wi :
        resized_watermark =  watermark_img

    elif extended_h > hi & extended_w > wi:

        new_height = hi - extended_h
        new_width = wi - extended_h

        resized_watermark = cv2.resize(watermark_img, (new_width, new_height),
                                       interpolation=cv2.INTER_AREA)

    elif extended_h > hi & extended_w < wi:

        new_height = hi - extended_h

        resized_watermark = resize_image(watermark_img, height=new_height)

    elif extended_h < hi & extended_w > wi:

        new_width = wi - extended_h
        resized_watermark = resize_image(watermark_img, width=new_width)


    return resized_watermark.shape, start_h, start_w


















