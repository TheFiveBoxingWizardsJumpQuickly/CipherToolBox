import os
import colorsys
import urllib.request
import random
import threading
from PIL import Image, ImageDraw
from operator import itemgetter


SATURATION = 0.4
BRIGHTNESS = 0.3


def setBGColor(input_file_path, bgcolor_prop):
    if bgcolor_prop == 'Auto':
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

        frequent_color = usedColors[1][1]
        frequent_color_hsv = colorsys.rgb_to_hsv(
            frequent_color[0]/255, frequent_color[1]/255, frequent_color[2]/255)
        bg_color_rgb = colorsys.hsv_to_rgb(
            frequent_color_hsv[0], SATURATION, BRIGHTNESS)

        return (int(bg_color_rgb[0]*255), int(bg_color_rgb[1]*255), int(bg_color_rgb[2]*255), 255)
    elif bgcolor_prop == 'Transparent':
        return (0, 0, 0, 0)
    else:
        r = int(bgcolor_prop[0:2], 16)
        g = int(bgcolor_prop[2:4], 16)
        b = int(bgcolor_prop[4:6], 16)
        return(r, g, b, 255)


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


def delete_output(modified_file_path):
    threading.Timer(300, delete_file, [modified_file_path]).start()


def delete_file(file_path):
    try:
        os.remove(file_path)
    except:
        print(f'Error: Unable to delete {file_path}')


def resize_image(input_dir, output_dir, filename, canvas_w, canvas_h, bgcolor_prop, output_name):
    if output_name == '':
        output_name = os.path.splitext(
            filename)[0]
    final_output_name = os.path.splitext(
        output_name)[0] + '_' + str(random.randint(100000, 999999)) + '.png'

    canvas_w = int(canvas_w)
    canvas_h = int(canvas_h)

    canvas_size = [canvas_w, canvas_h]
    input_file_path = os.path.join(input_dir, filename)
    output_file_path = os.path.join(output_dir, final_output_name)
    bg_color = setBGColor(input_file_path, bgcolor_prop)
    canvas = Image.new('RGBA', canvas_size, bg_color)

    setImages(canvas, input_file_path, canvas_size)
    canvas.save(output_file_path)

    delete_file(input_file_path)
    threading.Thread(target=delete_output, args=(output_file_path,)).start()

    return final_output_name
