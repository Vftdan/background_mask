# author: zhaofeng-shu33
# usage: python background_mask.py img_name
# purporse: change white background to transparent state
import argparse
from PIL import Image


def rect_contour(width, height):
    left, bottom, top, right = 0, height - 1, 0, width - 1
    if right - left > 0 and bottom - top > 0:
        # ltr, top
        for x in range(left, right):
            yield (x, top)
        # ttb, right
        for y in range(top, bottom):
            yield (right, y)
        # rtl, bottom
        for x in range(right, left, -1):
            yield (x, bottom)
        # btt, left
        for y in range(bottom, top, -1):
            yield (left, y)
        return
    if right == left:
        for y in range(top, bottom + 1):
            yield (right, y)
    elif bottom == top:
        for x in range(left, right + 1):
            yield (x, top)

def four_neighbours(x, y):
    for d in (-1, +1):
        yield (x + d, y)
        yield (x, y + d)

def background_mask(img_name, threshold, bg, cont):
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
    q = set(rect_contour(width, height))
    visited = tuple([False] * (height + 1) for _ in range(width + 1))
    for i in range(width):
        visited[i][-1] = True
    for j in range(height):
        visited[-1][j] = True
    for i in range(width):
        for j in range(height):
            pixels[i, j] = 255
    while len(q):
        i, j = q.pop()
        if visited[i][j]:
            continue
        visited[i][j] = True
        r = abs(  red.getpixel((i, j)) - bg[0])
        g = abs(green.getpixel((i, j)) - bg[1])
        b = abs( blue.getpixel((i, j)) - bg[2])
        if r <= threshold and g <= threshold and b <= threshold:
            pixels[i, j] = 0
            q.update(four_neighbours(i, j))
        else:
            if not cont:
                q.update(four_neighbours(i, j))
    img.putalpha(alpha)
    img.save(img_name.split('.')[0] + '_mask.png')

def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('img_name', help='input image name')
    parser.add_argument('--threshold', type=int, default=15,
            help='threshold for transparency mask, 0 for exact match')
    parser.add_argument('--background', type=int, default=(255, 255, 255),
            nargs=3, metavar=('r', 'g', 'b'), help='background color')
    parser.add_argument('--continuous', action='store_true',
            help='delete only near edges')
    args = parser.parse_args()
    background_mask(args.img_name, args.threshold, args.background,
        args.continuous)
 
if __name__ == '__main__':
    _main()
