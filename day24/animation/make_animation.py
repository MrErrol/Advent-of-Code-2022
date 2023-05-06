import os
import glob
from typing import List
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from day24.solution import Position, Valley, PathSeeker

_this_dir = os.path.dirname(__file__)
_tiles_folder = os.path.join(_this_dir, "tiles")


WALL = plt.imread(os.path.join(_tiles_folder, "wall_flat.png"))
DIRT = plt.imread(os.path.join(_tiles_folder, "dirt.png"))
ELF = plt.imread(os.path.join(_tiles_folder, "elf.png"))
CLOUD = plt.imread(os.path.join(_tiles_folder, "blizzard.png"))


assert WALL.shape == DIRT.shape


def make_symbol_map_from_seeker(seeker: PathSeeker) -> List[List[List[str]]]:
    tile_mapping = [
        [[blizzard.raw_dir for blizzard in seeker.valley._map[Position(x=x, y=y)]] for x in range(seeker.valley.width)]
        for y in range(seeker.valley.height)
    ]
    tile_mapping = [[["#"]] + row + [["#"]] for row in tile_mapping]
    tile_mapping = (
        [[["#"] for _ in range(seeker.valley.width + 2)]]
        + tile_mapping
        + [[["#"] for _ in range(seeker.valley.width + 2)]]
    )
    tile_mapping[0][seeker.start.x + 1] = []
    tile_mapping[-1][seeker.destination.x + 1] = []
    for option in seeker.positions:
        tile_mapping[option.y + 1][option.x + 1] = ["@"]

    return tile_mapping


def tile_to_bitmap(symbols: List[str]) -> np.ndarray:
    symbols = set(symbols)
    if symbols == {"#"}:
        return WALL
    elif symbols == {"@"}:
        return ELF
    elif len(symbols):
        # blizzard case
        return CLOUD
    # just ground
    return DIRT


def make_bitmap_from_seeker(seeker: PathSeeker) -> np.ndarray:
    tile_mapping = make_symbol_map_from_seeker(seeker)
    tile_bitmaps = np.vstack([np.hstack([tile_to_bitmap(tile) for tile in row]) for row in tile_mapping])
    return tile_bitmaps


with open(os.path.join("..", "test_input.txt"), "+r") as file:
    raw_map = file.read().split("\n")

start = Position(y=-1, x=raw_map[0].index(".") - 1)
destination = Position(y=len(raw_map) - 2, x=raw_map[-1].index(".") - 1)
valley = Valley(raw_map=raw_map)
seeker = PathSeeker(valley=valley, start=start, destination=destination)

os.makedirs("screenshots", exist_ok=True)
while True:
    bitmaps = make_bitmap_from_seeker(seeker)
    fig = plt.figure(figsize=(valley.width + 2, valley.height + 2))
    ax = plt.Axes(fig, [0.0, 0.0, 1.0, 1.0])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(bitmaps)
    # fig.savefig(filename, dpi=data.shape[0])
    plt.savefig(os.path.join("screenshots", f"{seeker.valley.iteration:06}.png"))
    if seeker.destination_found():
        break
    seeker.make_search_step()

# combining slides to gif file
# Create the frames
frames = []
imgs = glob.glob(os.path.join("screenshots", "*.png"))
imgs.sort()
for i in imgs:
    new_frame = Image.open(i)
    frames.append(new_frame)

# Save into a GIF file that loops forever
frames[0].save(
    "going_there.gif",
    format="GIF",
    append_images=frames[1:] + frames[-1:] + frames[-1:],
    optimize=True,
    save_all=True,
    duration=400,
    loop=0,
)
