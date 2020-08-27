# author: zhaofeng-shu33
# usage: python background_mask.py img_name
# purporse: change white background to transparent state
import argparse
from PIL import Image


def background_mask(img_name, threshold, bg):
    try:
        img = Image.open(img_name)
    except FileNotFoundError as e:
        raise e
    if img.mode == 'CMYK':
        img = img.convert('RGB')
    has_alpha = (img.mode == 'RGBA')
    if not has_alpha:
        red, green, blue = img.split()
        alpha = Image.new(mode='L', size=red.size)
    else:
        red, green, blue, alpha = img.split()
    pixels = alpha.load()
    width, height = red.size
    for i in range(0, width):
        for j in range(0, height):
            r = abs(  red.getpixel((i, j)) - bg[0])
            g = abs(green.getpixel((i, j)) - bg[1])
            b = abs( blue.getpixel((i, j)) - bg[2])
            if r <= threshold and g <= threshold and b <= threshold:
                pixels[i, j] = 0
            else:
                pixels[i, j] = 255
    img.putalpha(alpha)
    img.save(img_name.split('.')[0] + '_mask.png')

def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('img_name', help='input image name')
    parser.add_argument('--threshold', type=int, default=15,
            help='threshold for transparency mask, 0 for exact match')
    parser.add_argument('--background', type=int, default=(255, 255, 255),
            nargs=3, metavar=('r', 'g', 'b'), help='background color')
    args = parser.parse_args()
    background_mask(args.img_name, args.threshold, args.background)
 
if __name__ == '__main__':
    _main()
