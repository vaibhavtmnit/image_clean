import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import string
from utils.utility_functions import read_config, call_rand_image
import random
import pandas as pd
import imutils



STRING_CHARS = string.ascii_letters+string.digits


def text_on_img(text="Vaibhav Thakur", size=12, fnt):

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





def im_to_watermark(watermark_im, raw_image, alpha=.28, correct_method=False,):


    wh, ww = watermark_im.shape[:2]

    if correct_method:
        (B, G, R, A) = cv2.split(watermark_im)
        B = cv2.bitwise_and(B, B, mask=A)
        G = cv2.bitwise_and(G, G, mask=A)
        R = cv2.bitwise_and(R, R, mask=A)
        watermark_im = cv2.merge([B, G, R, A])

    (h, w) = raw_image.shape[:2]

    image = np.dstack([image, np.ones((h, w), dtype="uint8") * 255])

    overlay = np.zeros((h, w, 4), dtype="uint8")

    if min(h,w)>max(wh,ww):



    elif

    overlay[h - wH - 10:h - 10, w - wW - 10:w - 10] = watermark

    output = image.copy()
    cv2.addWeighted(overlay, alpha, output, 1.0, 0, output)




























