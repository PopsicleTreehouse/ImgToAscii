#!/bin/python3

import argparse
from PIL import Image
import numpy as np


def get_pixels(img_path, resize=1.0):
    with open(img_path, "rb") as fin:
        img = Image.open(fin).convert("RGBA")
        w, h = img.size
        img.thumbnail((h * resize, w * resize), Image.ANTIALIAS)
        return np.asarray(img)


def get_as_ascii(img_path, scale):
    DENSITY = " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@"
    DENSITY_LEN = len(DENSITY)
    lines = []
    pixels = get_pixels(img_path, resize=scale)
    for row in pixels:
        ret = ""
        for pixel in row:
            r, g, b, a = pixel.astype(np.uint16) / 255
            brightness = (r + g + b) / 3 * a
            idx = round(brightness * (DENSITY_LEN - 1))
            ret += "%-2s" % (DENSITY[idx])
        lines.append(ret)
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert an image into an ASCII representation with scalable resolution"
    )
    parser.add_argument(
        "--path",
        nargs=1,
        type=str,
        required=True,
        help="path to input image",
        dest="path",
    )
    parser.add_argument(
        "--scale",
        nargs=1,
        type=float,
        default=1.0,
        required=False,
        help="rescale factor of the output resolution",
        dest="scale",
    )
    args = vars(parser.parse_args())
    img_path = args["path"][0]
    scale = args["scale"][0]
    art = get_as_ascii(img_path, scale=scale)
    print(art)
