import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import string
from utils.utility_functions import read_config, call_rand_image, \
    get_position, reshape_watermark, resize_image
import random
import pandas as pd
import imutils



STRING_CHARS = string.ascii_letters+string.digits


def text_on_img(text="Vaibhav Thakur", size=12, fnt=None):

    # Draw a text on an Image, saves it, show it


    fnt = ImageFont.truetype(fnt, size)
    # create image
    image = Image.new(mode="RGBA", size=(int(size/2)*len(text+3), size+50),
                      color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    # draw text
    draw.text((0, 0), text, font=fnt, fill=(255,255,255))
    # save file
    return image
    # show file
    #os.system(filename)


def concat(im1,im2):

    return cv2.hconcat([im1, im2])


def bring_string(string_characters=STRING_CHARS):

    string_length = random.randint(15, 22)
    random_string_list = [random.choice(string_characters) for i
                     in range(string_length)]
    break_index = random.randint(0, string_length)

    return random_string_list[0:break_index], random_string_list[break_index:]




def create_watermark(im_size):
    print(os.getcwd())

    config = read_config()

    font_path = os.path.join(config['root'],
                             config['watermark_input']['font_input'])
    font_list = os.listdir(font_path)
    font_file = call_rand_image(font_path, font_list)


    random_string_prefix, random_string_suffix = bring_string(STRING_CHARS)

    h, w = im_size

    watermark_height_seq = np.arange(.06, .14, .2)

    if h > w:
        heigth_watermark = round(h * (np.random.choice(watermark_height_seq, 1)[0]))
    else:
        heigth_watermark = round(w * (np.random.choice(watermark_height_seq, 1)[0]))

    logo_path = os.path.join(config['root'],
                             config['watermark_input']['logo_input'])

    logo_list = os.listdir(logo_path)

    logo_file = call_rand_image(logo_path, logo_list)



    if random_string_prefix != []:

        len_first_part = len(random_string_prefix )
        string_prefix = "".join(random_string_prefix)
        watermark_prefix = text_on_img(text=string_prefix,size=heigth_watermark,
                                       fnt=font_file)

    elif random_string_suffix != []:

        len_second_part = len(random_string_suffix)
        string_suffix = "".join(random_string_suffix)
        watermark_suffix = text_on_img(text=string_suffix,
                                       size=heigth_watermark,
                                       fnt=font_file)

    # Height of watermark image here second element in PIL is height for CV
    #_, w_watermark = watermark_prefix.size()[1]


    # Resizing logo to fit with text images
    logo_file_resized = resize_image(logo_file,
                                     height= watermark_prefix.size()[1])

    if random_string_prefix != []:

       temp_image = concat(watermark_prefix,logo_file_resized)

       if random_string_suffix != [] :

           temp_image = concat(temp_image,watermark_suffix)

    elif random_string_suffix != []:

        temp_image = concat(logo_file_resized, watermark_suffix)

    else:
        print('No Watermark to build')

    if h>w:
      return  cv2.rotate(temp_image, cv2.ROTATE_90_CLOCKWISE)

    else :
      return  temp_image



def im_to_watermark(watermark_im, raw_image, alpha=.28, correct_method=False):


    wh, ww = watermark_im.shape[:2]

    if correct_method:
        (B, G, R, A) = cv2.split(watermark_im)
        B = cv2.bitwise_and(B, B, mask=A)
        G = cv2.bitwise_and(G, G, mask=A)
        R = cv2.bitwise_and(R, R, mask=A)
        watermark_im = cv2.merge([B, G, R, A])

    (h, w) = raw_image.shape[:2]

    image = np.dstack([raw_image, np.ones((h, w), dtype="uint8") * 255])

    overlay = np.zeros((h, w, 4), dtype="uint8")

    ext_h, ext_w, start_coordinates = get_position(size_im = (h, w),
                                                   size_watermark= (wh, ww))

    watermark_resized, start_h_coord, start_w_coord = reshape_watermark(
        (h, w), ext_h, ext_w, start_coordinates, watermark_im
        )
    new_size = watermark_resized.shape[:2]

    overlay[start_coordinates[0]:start_coordinates[0]+new_size[0],
    start_coordinates[1]:start_coordinates[1] + new_size[1]] = watermark_resized



    #overlay[h - wH - 10:h - 10, w - wW - 10:w - 10] = watermark

    output = image.copy()
    cv2.addWeighted(overlay, alpha, output, 1.0, 0, output)

    return output


































