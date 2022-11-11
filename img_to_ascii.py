#!/bin/python3

import argparse
from PIL import Image
import numpy as np


def get_sorted_weights():
    with open("ordered_chars.txt", "r") as f:
        lines = []
        for line in f.readlines():
            char_code = int(line)
            ch = chr(char_code)
            lines.append(ch)
        return lines


def get_pixels(img_path, resize=1.0):
    with open(img_path, "rb") as fin:
        img = Image.open(fin).convert("RGBA")
        w, h = img.size
        img.thumbnail((h * resize, w * resize), Image.ANTIALIAS)
        return np.asarray(img)


def format_color(text, r, g, b):
    ENDING_SEQ = "\x1b[0m"
    start = f"\u001b[38;2;{r};{g};{b}m"
    return start + text + ENDING_SEQ

def get_as_ascii(img_path, scale):
    DENSITY = get_sorted_weights()
    DENSITY_LEN = len(DENSITY)
    lines = []
    pixels = get_pixels(img_path, resize=scale)
    for row in pixels:
        line = ""
        for pixel in row:
            r, g, b, a = pixel.astype(np.uint16) / 255
            brightness = (r + g + b) / 3 * a
            idx = round(brightness * (DENSITY_LEN - 1))
            ch = DENSITY[idx]
            line += format_color(ch + "\t".expandtabs(1), *pixel[:3])
        lines.append(line)

    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert an image into an ASCII representation with scalable resolution"
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="path to input image",
        dest="path",
        nargs="?",
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=1.0,
        required=False,
        help="rescale factor of the output resolution",
        dest="scale",
        nargs="?",
    )
    args = vars(parser.parse_args())
    img_path = args["path"]
    scale = args["scale"]
    art = get_as_ascii(img_path, scale=scale)
    print(art)
