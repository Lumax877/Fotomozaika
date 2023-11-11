from PIL import Image
import random
import os
import glob

path = "venv/generatedimages/script_v1"


def generate_images(number, resolution, picpath):
    for i in range(0, number):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        image = Image.new('RGB', resolution, color)

        image.save(f"{picpath}/image_{i}_{color}.png")


def check(dirpath):
    files = glob.glob(os.path.join(dirpath, '*'))

    for file_path in files:
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error: {str(e)}")


check(path)
generate_images(100, (100, 100), path)
