# generate a file containing the utf-8 char codes in sorted order based on the brightness of the character

import argparse
import freetype as ft

def load_weights(font_path, char_width):
    face = ft.Face(font_path, 0)
    chars = face.get_chars()
    weights = []
    for char_code, glyph_idx in chars:
        face.load_glyph(glyph_idx)
        glyph = face.glyph.get_glyph()
        bitmap = glyph.to_bitmap(ft.FT_RENDER_MODE_NORMAL, 0).bitmap
        brightness, width = sum(bitmap.buffer), bitmap.width
        if width != char_width:
            continue
        entry = (brightness, char_code)
        weights.append(entry)
    weights.sort(key=lambda x: x[0])
    return weights


def write_weights_to_file(weights):
    with open("ordered_chars.txt", "w+") as f:
        for brightness, char_code in weights:
            s = f"{char_code}\n"
            f.write(s)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="path to input font",
        dest="path",
        nargs="?",
    )
    parser.add_argument(
        "--width",
        type=int,
        required=False,
        default=19,
        help="desired width of each character",
        dest="width",
        nargs="?",
    )
    args = vars(parser.parse_args())
    font_path = args["path"]
    char_width = args["width"]
    weights = load_weights(font_path, char_width)
    write_weights_to_file(weights)