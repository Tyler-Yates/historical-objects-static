import os

# This import is needed even though it is not called directly
# noinspection PyUnresolvedReferences
import pillow_avif
from PIL import Image

from processor.util import ALREADY_PROCESSED_UTIL
from processor.util.constants import ROOT_PATH
from processor.util.image_adjustments import resize_to_max_dimension

INPUT_DIRECTORY = os.path.join(ROOT_PATH, "input", "plates")
OUTPUT_DIRECTORY = os.path.join(ROOT_PATH, "images", "plates")
HIGH_QUALITY = 50
LOW_QUALITY = 50
HI_MAX_DIMENSION = 2000
LOW_MAX_DIMENSION = 500


def process_plate_image(input_path: str):
    if ALREADY_PROCESSED_UTIL.is_already_processed(input_path):
        print(f"Skipping {input_path} as already processed")
        return

    if not input_path.lower().endswith(".jpg"):
        print(f"ERROR: {input_path} is not a jpg file. Cannot process.")
        return

    print(f"Processing {input_path}...")

    plate_name = os.path.basename(input_path).split(".")[0]
    output_path = os.path.join(OUTPUT_DIRECTORY, plate_name)
    os.makedirs(output_path, exist_ok=True)

    input_image = Image.open(input_path)

    # Save the high quality image with no resizing
    hi_image = resize_to_max_dimension(input_image, HI_MAX_DIMENSION)
    hi_image.save(os.path.join(output_path, "plate-hi.avif"), "AVIF", quality=HIGH_QUALITY)

    # Resize the image for the low quality gallery
    low_image = resize_to_max_dimension(input_image, LOW_MAX_DIMENSION)
    low_image.save(os.path.join(output_path, "plate.avif"), "AVIF", quality=LOW_QUALITY)

    ALREADY_PROCESSED_UTIL.record_file_processed(input_path)

    print(f"Finished processing {input_path}")


def process_plats_input():
    for item in os.listdir(INPUT_DIRECTORY):
        item_path = os.path.join(INPUT_DIRECTORY, item)
        if os.path.isfile(item_path):
            process_plate_image(item_path)
        else:
            print(f"ERROR!!!!!!! Ignoring item {item_path}")
