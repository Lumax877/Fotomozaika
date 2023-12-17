import os
import re
import numpy as np
import cv2
from skimage import color

def rgb_to_lab(rgb):
    return color.rgb2lab([[rgb]])[0][0]

def extract_color_from_tile_filename(filename):
    match = re.match(r'image_(\d+)_(\d+)_(\d+)_(\d+)', filename)
    if match:
        return tuple(map(int, match.groups()[1:]))
    return None

def calculate_average_color(region):
    avg_color = np.mean(region, axis=(0, 1))
    return tuple(map(int, avg_color))

def color_difference(color1, color2):
    lab1 = rgb_to_lab(color1)
    lab2 = rgb_to_lab(color2)
    return np.linalg.norm(lab1 - lab2)

def find_most_similar_tile(target_color, tile_filenames):
    min_difference = float('inf')
    most_similar_tile = None

    for tile_filename in tile_filenames:
        tile_color = extract_color_from_tile_filename(tile_filename)
        difference = color_difference(target_color, tile_color)

        if difference < min_difference:
            min_difference = difference
            most_similar_tile = tile_filename

    return most_similar_tile

def mosaic_from_tiles(input_image_path, tiles_folder, output_path, tile_size=100):
    original_image = cv2.imread(input_image_path)
    original_h, original_w, _ = original_image.shape

    mosaic_image = np.ones_like(original_image) * 255

    tile_filenames = os.listdir(tiles_folder)

    for y in range(0, original_h, tile_size):
        for x in range(0, original_w, tile_size):
            region = original_image[y:y+tile_size, x:x+tile_size, :]

            target_color = calculate_average_color(region)

            most_similar_tile_filename = find_most_similar_tile(target_color, tile_filenames)

            most_similar_tile_path = os.path.join(tiles_folder, most_similar_tile_filename)
            most_similar_tile = cv2.imread(most_similar_tile_path)
            mosaic_image[y:y+tile_size, x:x+tile_size, :] = most_similar_tile
            print(x*y)

    cv2.imwrite(output_path, mosaic_image)

mosaic_from_tiles(
    input_image_path="venv/generatedimages/some_input_images/bridge.jpg",
    tiles_folder="venv/generatedimages/script_v1",
    output_path="venv/generatedimages/some_input_images/bridgemosaic10k.jpg"
)
