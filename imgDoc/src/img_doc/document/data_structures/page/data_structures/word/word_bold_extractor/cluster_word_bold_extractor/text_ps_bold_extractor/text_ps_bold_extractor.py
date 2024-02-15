from ..base_cluster_word_bold_extractor import BaseClusterWordBoldExtractor
from  img_doc.data_structures import Word
from typing import List
from PIL import Image, ImageDraw, ImageFont

import numpy as np

PERMISSIBLE_H_BBOX = 5  # that height bbox after which it makes no sense сrop bbox
PERMISSIBLE_W_BBOX = 3
PS_WIDTH = {'А': 0.87,
 'Б': 0.675,
 'В': 0.742,
 'Г': 0.661,
 'Д': 0.852,
 'Е': 0.582,
 'Ж': 0.8,
 'З': 0.833,
 'И': 0.706,
 'Й': 0.779,
 'К': 0.675,
 'Л': 0.678,
 'М': 0.738,
 'Н': 0.658,
 'О': 0.676,
 'П': 0.663,
 'Р': 0.72,
 'С': 0.778,
 'Т': 0.638,
 'У': 0.706,
 'Ф': 0.767,
 'Х': 0.765,
 'Ц': 0.666,
 'Ч': 0.663,
 'Ш': 0.985,
 'Щ': 1.024,
 'Ъ': 0.714,
 'Ы': 0.754,
 'Ь': 0.707,
 'Э': 0.807,
 'Ю': 0.881,
 'Я': 0.691,
 'а': 0.706,
 'б': 0.821,
 'в': 0.748,
 'г': 0.725,
 'д': 0.817,
 'е': 0.878,
 'ж': 0.665,
 'з': 0.863,
 'и': 0.728,
 'й': 0.746,
 'к': 0.624,
 'л': 0.67,
 'м': 0.772,
 'н': 0.709,
 'о': 0.755,
 'п': 0.697,
 'р': 0.774,
 'с': 0.804,
 'т': 0.76,
 'у': 0.809,
 'ф': 0.748,
 'х': 0.832,
 'ц': 0.709,
 'ч': 0.706,
 'ш': 0.665,
 'щ': 0.683,
 'ъ': 0.607,
 'ы': 0.731,
 'ь': 0.764,
 'э': 0.822,
 'ю': 0.73,
 'я': 0.657,
 '0': 0.723,
 '1': 0.57,
 '2': 0.671,
 '3': 0.655,
 '4': 0.785,
 '5': 0.598,
 '6': 0.78,
 '7': 0.737,
 '8': 0.671,
 '9': 0.786,
 'a': 0.706,
 'b': 0.753,
 'c': 0.804,
 'd': 0.758,
 'e': 0.878,
 'f': 0.685,
 'g': 0.699,
 'h': 0.732,
 'i': 0.637,
 'j': 0.559,
 'k': 0.77,
 'l': 0.746,
 'm': 0.762,
 'n': 0.749,
 'o': 0.755,
 'p': 0.774,
 'q': 0.698,
 'r': 0.647,
 's': 0.691,
 't': 0.607,
 'u': 0.724,
 'v': 0.837,
 'w': 0.834,
 'x': 0.832,
 'y': 0.809,
 'z': 0.673,
 'A': 0.87,
 'B': 0.742,
 'C': 0.778,
 'D': 0.73,
 'E': 0.582,
 'F': 0.569,
 'G': 0.775,
 'H': 0.658,
 'I': 0.61,
 'J': 0.494,
 'K': 0.686,
 'L': 0.598,
 'M': 0.738,
 'N': 0.809,
 'O': 0.676,
 'P': 0.72,
 'Q': 0.708,
 'R': 0.67,
 'S': 0.78,
 'T': 0.638,
 'U': 0.763,
 'V': 0.845,
 'W': 0.929,
 'X': 0.765,
 'Y': 0.719,
 'Z': 0.619,
 '!': 0.592,
 '"': 0.555,
 '#': 0.704,
 '$': 0.85,
 '%': 0.893,
 '&': 0.815,
 "'": 0.543,
 '(': 0.773,
 ')': 0.719,
 '*': 1.073,
 '+': 0.536,
 ',': 0.402,
 '-': 0.642,
 '.': 0.199,
 '/': 0.733,
 ':': 0.192,
 ';': 0.305,
 '<': 0.581,
 '=': 0.26,
 '>': 0.591,
 '?': 0.669,
 '@': 1.038,
 '[': 0.776,
 '\\': 0.723,
 ']': 0.729,
 '^': 0.727,
 '_': 0.275,
 '`': 0.868,
 '{': 0.695,
 '|': 0.686,
 '}': 0.707,
 '~': 0.492}

class TextPsBoldExtractor(BaseClusterWordBoldExtractor):
    def extract(self, words: List[Word], gray_img: np.ndarray):
        for word in words:
            bold_val = self.evaluation_words(word.segment.get_segment_from_img(gray_img), word.text)
            word.set_bold(bold_val)
        bold_vals = self.clusterize(np.array([word.bold for word in words])).tolist()
        for bold, word in zip(bold_vals, words):
            word.bold = int(bold)
      
    def evaluation_words(self, image: np.ndarray, text: str) -> float:
        ps_width_text = 0
        for char_ in text:
            if char_ in PS_WIDTH.keys():
                ps_width_text += PS_WIDTH[char_]
            else:
                ps_width_text += 1
        ps_width_text = ps_width_text/len(text)

        base_line_image = self._get_base_line_image(image)  # baseline - main font area
        s_img = 1 - self._get_rid_spaces(base_line_image)  # removing spaces from a string

        p_img = base_line_image[:, :-1] - base_line_image[:, 1:]
        p_img[abs(p_img) > 0] = 1.
        p_img[p_img < 0] = 0.
        
        p = p_img.sum()
        s = s_img.sum()

        if p > s:
            evaluation = 1.
        else:
            evaluation = p/s * ps_width_text
        return evaluation
    
    def _get_rid_spaces(self, image: np.ndarray) -> np.ndarray:
        x = image.mean(0)
        not_space = x < 0.95
        if len(not_space) > PERMISSIBLE_W_BBOX:
            return image
        return image[:, not_space]

    def _get_base_line_image(self, image: np.ndarray) -> np.ndarray:
        h = image.shape[0]
        if h < PERMISSIBLE_H_BBOX:
            return image
        mean_ = image.mean(1)
        delta_mean = abs(mean_[:-1] - mean_[1:])

        max1 = 0
        max2 = 0
        argmax1 = 0
        argmax2 = 0
        for i, delta_mean_i in enumerate(delta_mean):
            if delta_mean_i <= max2:
                continue
            if delta_mean_i > max1:
                max2 = max1
                argmax2 = argmax1
                max1 = delta_mean_i
                argmax1 = i
            else:
                max2 = delta_mean_i
                argmax2 = i
        h_min = min(argmax1, argmax2)
        h_max = min(max(argmax1, argmax2) + 1, h)
        if h_max-h_min < PERMISSIBLE_H_BBOX:
            return image
        return image[h_min:h_max, :]
    
    def create_width_from_tff(self, path_ttf_bold, path_ttf_regular, size=20):
        reg = ImageFont.truetype(path_ttf_regular, size=size)
        bold = ImageFont.truetype(path_ttf_bold, size=size)
        alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя"+\
                   "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"+\
                   "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

        width = size
        height = size
        json_width  = dict()
        for i in range(len(alphabet)):
            char_ = alphabet[i]
            img_r = Image.new('RGB', (width, height), color=(255, 255, 255))
            imgDraw = ImageDraw.Draw(img_r)
            imgDraw.text((round(size/8), -round(size/8)), char_, font=reg, fill=(0, 0, 0))
            
            img_b = Image.new('RGB', (width, height), color=(255, 255, 255))
            imgDraw = ImageDraw.Draw(img_b)
            imgDraw.text((10, -10), char_, font=bold, fill=(0, 0, 0))
            ar = 256-np.array(img_r) 
            ab = 256-np.array(img_b)
            bs = ar.sum()/ab.sum()
            pr = ar[:,:-1,:]-ar[:,1:,:]
            pb = ab[:,:-1,:]-ab[:,1:,:]
            bp = pb.sum()/pr.sum()

            json_width[char_] = bs/bp
        return json_width