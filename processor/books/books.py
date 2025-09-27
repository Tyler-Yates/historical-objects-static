import os

# This import is needed even though it is not called directly
# noinspection PyUnresolvedReferences
import pillow_avif
from PIL import Image

from processor.util.constants import ROOT_PATH
from processor.util.image_adjustments import resize_to_max_dimension

INPUT_DIRECTORY = os.path.join(ROOT_PATH, "input", "books")
OUTPUT_DIRECTORY = os.path.join(ROOT_PATH, "images", "books")
HIGH_QUALITY = 40
LOW_QUALITY = 40
HI_MAX_DIMENSION = 2000
LOW_MAX_DIMENSION = 550


def process_book_image(input_path: str):
    if not input_path.lower().endswith(".jpg"):
        print(f"ERROR: {input_path} is not a jpg file. Cannot process.")
        return

    file_name = os.path.basename(input_path).split(".")[0]
    book_name = os.path.basename(os.path.dirname(input_path))

    if file_name == "cover":
        cover_folder = os.path.join(OUTPUT_DIRECTORY, book_name)
        cover_output = os.path.join(cover_folder, f"{file_name}.avif")
        
        if os.path.exists(cover_output):
            print(f"Skipping {input_path} - cover already exists")
            return
            
        print(f"Processing {input_path}...")
        os.makedirs(cover_folder, exist_ok=True)
        
        input_image = Image.open(input_path)
        cover_image = resize_to_max_dimension(input_image, LOW_MAX_DIMENSION)
        cover_image.save(cover_output, "AVIF", quality=HIGH_QUALITY)
    else:
        hi_gallery = os.path.join(OUTPUT_DIRECTORY, book_name, "gallery", "hi")
        low_gallery = os.path.join(OUTPUT_DIRECTORY, book_name, "gallery", "low")
        
        hi_output = os.path.join(hi_gallery, f"{file_name}.avif")
        low_output = os.path.join(low_gallery, f"{file_name}.avif")
        
        if os.path.exists(hi_output) and os.path.exists(low_output):
            print(f"Skipping {input_path} - output files already exist")
            return
            
        print(f"Processing {input_path}...")
        os.makedirs(hi_gallery, exist_ok=True)
        os.makedirs(low_gallery, exist_ok=True)
        
        input_image = Image.open(input_path)
        
        # Save the high quality image with no resizing
        hi_image = resize_to_max_dimension(input_image, HI_MAX_DIMENSION)
        hi_image.save(hi_output, "AVIF", quality=HIGH_QUALITY)

        # Resize the image for the low quality gallery
        low_image = resize_to_max_dimension(input_image, LOW_MAX_DIMENSION)
        low_image.save(low_output, "AVIF", quality=LOW_QUALITY)

    print(f"Finished processing {input_path}")

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
