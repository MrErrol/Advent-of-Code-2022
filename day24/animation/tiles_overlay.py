import os

from PIL import Image

_this_dir = os.path.dirname(__file__)


def merge_images(im1, im2):
    bg = Image.open(im1).convert("RGBA")
    fg = Image.open(im2).convert("RGBA")
    x, y = ((bg.width - fg.width) // 2, (bg.height - fg.height) // 2)
    bg.paste(fg, (x, y), fg)
    return bg
    # convert to 8 bits (pallete mode)
    return bg.convert("P")


if __name__ == "__main__":
    result_image = merge_images(
        os.path.join(_this_dir, "tiles", "dirt.png"), os.path.join(_this_dir, "tiles", "halfling_new.png")
    )
    result_image.save(r"elf.png")
