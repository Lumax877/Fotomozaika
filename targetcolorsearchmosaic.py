from PIL import Image
import os
import random
from skimage import color
import numpy as np

# very slow due to tile color calculation

def rgb_to_lab(rgb):
    return color.rgb2lab([[rgb]])[0][0]

def calculate_average_color(region):
    width, height = region.size
    r, g, b = 0, 0, 0

    for y in range(height):
        for x in range(width):
            pixel_color = region.getpixel((x, y))
            r += pixel_color[0]
            g += pixel_color[1]
            b += pixel_color[2]

    total_pixels = width * height
    avg_color = (r // total_pixels, g // total_pixels, b // total_pixels)
    return avg_color

def color_difference(color1, color2):
    lab1 = rgb_to_lab(color1)
    lab2 = rgb_to_lab(color2)
    return np.linalg.norm(lab1 - lab2)

def find_most_similar_tile(target_color, tile_images):
    min_difference = float('inf')
    most_similar_tile = None

    for tile_path in tile_images:
        tile_image = Image.open(tile_path)
        tile_color = calculate_average_color(tile_image)

        difference = color_difference(target_color, tile_color)

        if difference < min_difference:
            min_difference = difference
            most_similar_tile = tile_image

    return most_similar_tile

def random_tile_mosaic(input_image_path, tiles_folder, output_path, tile_size=100):
    original_image = Image.open(input_image_path)
    original_w, original_h = original_image.size

    mosaic_image = Image.new('RGB', (original_w, original_h), (255, 255, 255))
    tile_images = [os.path.join(tiles_folder, filename) for filename in os.listdir(tiles_folder)]

    for y in range(0, original_h, tile_size):
        for x in range(0, original_w, tile_size):
            region = original_image.crop((x, y, x + tile_size, y + tile_size))
            target_color = calculate_average_color(region)
            print(y*x)

            most_similar_tile = find_most_similar_tile(target_color, tile_images)

            mosaic_image.paste(most_similar_tile, (x, y))


    mosaic_image.save(output_path)

random_tile_mosaic(
    input_image_path="venv/generatedimages/some_input_images/sea1000x1000.jpg",
    tiles_folder="venv/generatedimages/script_v1",
    output_path="venv/generatedimages/some_input_images/seamosaic.jpg"
)

