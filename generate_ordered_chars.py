# generate a file containing the utf-8 char codes in sorted order based on the brightness of the character

import freetype as ft

# only works for mac right now
FONT_DIRECTORY = "/System/Library/Fonts/"
CHAR_WIDTH = 19

face = ft.Face(FONT_DIRECTORY + "Monaco.ttf", 0)
chars = face.get_chars()
weights = []
for char_code, glyph_idx in chars:
    face.load_glyph(glyph_idx)
    glyph = face.glyph.get_glyph()
    bitmap = glyph.to_bitmap(ft.FT_RENDER_MODE_NORMAL, 0).bitmap
    brightness, width = sum(bitmap.buffer), bitmap.width
    if width != CHAR_WIDTH:
        continue
    entry = (brightness, char_code)
    weights.append(entry)

weights.sort(key=lambda x: x[0])
with open("ordered_chars.txt", "w+") as f:
    for brightness, char_code in weights:
        s = f"{char_code}\n"
        f.write(s)
