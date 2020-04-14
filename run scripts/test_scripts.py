import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import string
from utils.utility_functions import read_config, call_rand_image, \
    get_position, reshape_watermark
import random
import pandas as pd
import imutils
from zipfile import ZipFile


def create_watermark():
    print(os.getcwd())

    config = read_config()

    font_path = os.path.join(config['root'],
                             config['watermark_input']['font_input'])
    font_list = os.listdir(font_path)
    font_file = call_rand_image(font_path, font_list)
    print(font_file)

    print(type(font_file))



#create_watermark()

def extract_all():
    config = read_config()

    font_path = os.path.join(config['root'],
                             config['watermark_input']['font_input'])

    list_d = os.listdir(font_path)
    print(list_d)

    for z in list_d:
        with ZipFile(os.path.join(font_path, z), 'r') as zip_file:
            zip_file.extractall(os.path.join(font_path))
            print(z)



#extract_all()

STRING_CHARS = string.ascii_letters+string.digits

def bring_string(string_characters=STRING_CHARS):

    string_length = random.randint(15, 22)
    random_string_list = [random.choice(string_characters) for i
                     in range(string_length)]
    break_index = random.randint(0, string_length)

    return random_string_list[0:break_index], random_string_list[break_index:]

print(bring_string())