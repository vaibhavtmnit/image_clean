import os
import json
from random import randint
import math


ROOT = "../../../vaibhavthakur/PycharmProjects"

def read_config(ROOT):

    with open(os.path.join(ROOT,"Image Treatment/config/input_config.json"),'r+') as config:

        return json.load(config)


def call_rand_image(path,list_images):

    rand_pick = randint(0, len(list_images) - 1)
    image_pick = list_images[rand_pick]
    return os.path.join(path, image_pick)


def load_resize_logo(logo_path, width = None, height = None,
                     inter = cv2.INTER_AREA):

    image = cv2.imread(logo_path)

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

def get_position(size_im,size_watermark):

    hi, wi = size_im
    hw, ww = size_watermark

    pos = randint(1, 9)

    margin_size = (round(hi*0.025),
                  round(wi*0.025))


    pos_idx_height  = math.floor(hi/3)*math.floor(pos/3)

    pos_idx_width = math.floor(wi/3)*( 2 if pos//3 == 0 else (pos//3)-1)

    add_jitter_h = randint(0,10)
    add_jitter_w = randint(0,12)

    extended_h = add_jitter_h + margin_size[0] + pos_idx_height + hw
    extended_w = add_jitter_w + margin_size[1] +pos_idx_width + ww

    if extended_h < hi & extended_w < wi :
        # Apply watermark
    else :
        # do resize





