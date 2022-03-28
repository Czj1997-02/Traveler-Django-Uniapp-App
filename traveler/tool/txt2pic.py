import os

import PIL
import re
from PIL import Image, ImageFont, ImageDraw


def txt2pic(txt, okpath):
    '''加载用户名头像'''
    filepath = os.path.dirname(__file__) + os.sep + \
        '..' + os.sep + okpath
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    txtlong = 0
    for i in txt:
        if '\u4e00' <= i <= '\u9fff':
            txtlong = txtlong+2
        else:
            txtlong = txtlong+1

    fontSize = int(350/txtlong*2)
    if fontSize > 180:
        fontSize = 180
        # r'media\img\portraits
    image_path = os.path.dirname(__file__) + os.sep + '..' + os.sep + \
        'media' + os.sep + 'portrait' + os.sep + 'background.jpg'
    im = Image.open(image_path)
    dr = ImageDraw.Draw(im)
    fontPath = os.path.dirname(__file__) + os.sep + '..' + os.sep + \
        'media' + os.sep + 'portrait' + os.sep + 'simsun.ttc'
    # fontSize=100
    font = ImageFont.truetype(fontPath, fontSize)
    begin = int(320-fontSize*txtlong/4)
    over = int(320-fontSize/2)

    dr.text((begin, over), txt, font=font, fill="black")
    # dr.text((210,450), txt, font=font, fill="purple")

    okrule = okpath + os.sep + txt + '.jpg'
    full_path = os.path.dirname(__file__) + os.sep + \
        '..' + os.sep + okpath + os.sep + txt + '.jpg'
    im.save(full_path)
    im.close()
    return okrule
