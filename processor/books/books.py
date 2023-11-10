import os

# This import is needed even though it is not called directly
# noinspection PyUnresolvedReferences
import pillow_avif
from PIL import Image

from processor.util import ALREADY_PROCESSED_UTIL
from processor.util.constants import ROOT_PATH
from processor.util.image_adjustments import resize_to_max_dimension

INPUT_DIRECTORY = os.path.join(ROOT_PATH, "input", "books")
OUTPUT_DIRECTORY = os.path.join(ROOT_PATH, "images", "books")
HIGH_QUALITY = 40
LOW_QUALITY = 40
HI_MAX_DIMENSION = 2000
LOW_MAX_DIMENSION = 550


def process_book_image(input_path: str):
    if ALREADY_PROCESSED_UTIL.is_already_processed(input_path):
        print(f"Skipping {input_path} as already processed")
        return

    if not input_path.lower().endswith(".jpg"):
        print(f"ERROR: {input_path} is not a jpg file. Cannot process.")
        return

    print(f"Processing {input_path}...")

    hi_gallery = os.path.join(OUTPUT_DIRECTORY, os.path.basename(os.path.dirname(input_path)), "gallery", "hi")
    low_gallery = os.path.join(OUTPUT_DIRECTORY, os.path.basename(os.path.dirname(input_path)), "gallery", "low")
    file_name = os.path.basename(input_path).split(".")[0]

    input_image = Image.open(input_path)

    # Save the high quality image with no resizing
    hi_image = resize_to_max_dimension(input_image, HI_MAX_DIMENSION)
    hi_image.save(os.path.join(hi_gallery, f"{file_name}.avif"), "AVIF", quality=HIGH_QUALITY)

    # Resize the image for the low quality gallery
    low_image = resize_to_max_dimension(input_image, LOW_MAX_DIMENSION)
    low_image.save(os.path.join(low_gallery, f"{file_name}.avif"), "AVIF", quality=LOW_QUALITY)

    ALREADY_PROCESSED_UTIL.record_file_processed(input_path)

    print(f"Finished processing {input_path}")


def process_book_directory(input_path: str):
    os.makedirs(os.path.join(OUTPUT_DIRECTORY, os.path.basename(input_path), "gallery", "hi"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIRECTORY, os.path.basename(input_path), "gallery", "low"), exist_ok=True)

    for item in os.listdir(input_path):
        item_path = os.path.join(input_path, item)
        if os.path.isfile(item_path):
            process_book_image(item_path)
        else:
            print(f"Ignoring item {item_path}")


def process_books_input():
    for item in os.listdir(INPUT_DIRECTORY):
        item_path = os.path.join(INPUT_DIRECTORY, item)
        if os.path.isdir(item_path):
            process_book_directory(item_path)
        else:
            print(f"Ignoring item {item_path}")
