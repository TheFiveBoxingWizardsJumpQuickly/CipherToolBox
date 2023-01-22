import os
import colorsys
import urllib.request
from PIL import Image, ImageDraw
from operator import itemgetter


SATURATION = 0.4  # 0.4
BRIGHTNESS = 0.3  # 0.3

#  Functions


def setBGColor(input_file_path):
    img = Image.open(input_file_path).convert("RGBA")
    img_filter = Image.new(
        'RGBA', (int(img.size[0]), int(img.size[1]*0.8)), '#000000FF')
    img.paste(
        im=img_filter,
        box=(int(img.size[0]), int(img.size[1]*0.1)),
        mask=img_filter
    )
    usedColors = sorted(img.getcolors(
        img.size[0] * img.size[1]), key=itemgetter(0), reverse=True)
    # print(usedColors[1])
    frequent_color = usedColors[1][1]
    frequent_color_hsv = colorsys.rgb_to_hsv(
        frequent_color[0]/255, frequent_color[1]/255, frequent_color[2]/255)
    bg_color_rgb = colorsys.hsv_to_rgb(
        frequent_color_hsv[0], SATURATION, BRIGHTNESS)

    return (int(bg_color_rgb[0]*255), int(bg_color_rgb[1]*255), int(bg_color_rgb[2]*255))


def setImages(canvas, input_file_path, canvas_size):
    img = Image.open(input_file_path).convert("RGBA")
    w, h = img.size
    multiplier = canvas_size[0] / w

    new_w, new_h = canvas_size[0],  int(h * canvas_size[0] / w)
    position = (0, int((canvas_size[1] - new_h) / 2))
    img = img.resize((new_w, new_h), Image.LANCZOS)
    canvas.paste(
        im=img,
        box=position,
        mask=img
    )


def make_wallpaper(input_dir, output_dir, filename):
    canvas_w = 1080
    canvas_h = 2400

    canvas_size = [canvas_w, canvas_h]
    input_file_path = os.path.join(input_dir, filename)
    output_file_path = os.path.join(output_dir, filename)
    bg_color = setBGColor(input_file_path)
    canvas = Image.new('RGBA', canvas_size, bg_color)

    setImages(canvas, input_file_path, canvas_size)
    canvas.save(output_file_path)
