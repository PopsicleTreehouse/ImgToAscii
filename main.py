from PIL import Image
import numpy as np


def get_pixels(img_path, resize=1.0):
    with open(img_path, "rb") as fin:
        img = Image.open(fin)
        w, h = img.size
        rgb = img.convert("RGB")
        rgb.thumbnail((h * resize, w * resize), Image.ANTIALIAS)
        return np.asarray(rgb)


def get_as_ascii(img_path, scale):
    DENSITY = " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@"
    DENSITY_LEN = len(DENSITY)
    lines = []
    pixels = get_pixels(img_path, resize=scale)
    for row in pixels:
        ret = ""
        for pixel in row:
            r, g, b = pixel[:3].astype(np.uint16)
            brightness = (r + g + b) / 3
            scaled = (brightness / 255) * (DENSITY_LEN - 1)
            idx = round(scaled)
            ret += "%-2s" % (DENSITY[idx])
        lines.append(ret)
    return "\n".join(lines)


if __name__ == "__main__":
    print("Enter image path: ")
    img_path = input()
    print("Enter resize multiplier: ")
    scale = float(input())
    art = get_as_ascii(img_path, scale)
    print(art)
