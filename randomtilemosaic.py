from PIL import Image
import os
import random

# const tile size and quantity
# const image size (dividable by tile_size)
# random tile (no RGB value parse)
# functional tile paste
# no tile resize
# jpg extension only
# no region calculation
def random_tile_mosaic(input_image_path, tiles_folder, output_path):
    original_image = Image.open(input_image_path)
    original_w, original_h = original_image.size

    mosaic_image = Image.new('RGB', (original_w, original_h), (255,255,255))
    tile_images = []
    for filename in os.listdir(tiles_folder):
        tile_images.append(os.path.join(tiles_folder, filename))

    for y in range(0, original_h, 100):
        for x in range(0, original_w, 100):
            random_tile_path = random.choice(tile_images)
            tile_image = Image.open(random_tile_path)

            region = original_image.crop((x, y, x + 100, y + 100))

            mosaic_image.paste(tile_image, (x,y))

    mosaic_image.save(output_path)
    print("Successfully saved")

random_tile_mosaic(
    input_image_path="venv/generatedimages/some_input_images/black.jpg",
    tiles_folder="venv/generatedimages/script_v1",
    output_path="venv/generatedimages/some_input_images/randomtilemosaic.jpg"
)