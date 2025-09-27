import os

# This import is needed even though it is not called directly
# noinspection PyUnresolvedReferences
import pillow_avif
from PIL import Image

from processor.util.constants import ROOT_PATH
from processor.util.image_adjustments import resize_to_max_dimension

INPUT_DIRECTORY = os.path.join(ROOT_PATH, "input", "plates")
OUTPUT_DIRECTORY = os.path.join(ROOT_PATH, "images", "plates")
HIGH_QUALITY = 50
LOW_QUALITY = 50
HI_MAX_DIMENSION = 4000
LOW_MAX_DIMENSION = 500


def process_plate_image(input_path: str):
    if not input_path.lower().endswith(".jpg"):
        print(f"ERROR: {input_path} is not a jpg file. Cannot process.")
        return

    plate_name = os.path.basename(input_path).split(".")[0]
    output_path = os.path.join(OUTPUT_DIRECTORY, plate_name)
    
    # Check if both output files already exist
    hi_output = os.path.join(output_path, "plate-hi.avif")
    low_output = os.path.join(output_path, "plate.avif")
    
    if os.path.exists(hi_output) and os.path.exists(low_output):
        print(f"Skipping {input_path} - output files already exist")
        return
        
    print(f"Processing {input_path}...")
    os.makedirs(output_path, exist_ok=True)

    input_image = Image.open(input_path)

    # Save the high quality image with no resizing
    hi_image = resize_to_max_dimension(input_image, HI_MAX_DIMENSION)
    hi_image.save(hi_output, "AVIF", quality=HIGH_QUALITY)

    # Resize the image for the low quality gallery
    low_image = resize_to_max_dimension(input_image, LOW_MAX_DIMENSION)
    low_image.save(low_output, "AVIF", quality=LOW_QUALITY)

    print(f"Finished processing {input_path}")


def process_plats_input():
    for item in os.listdir(INPUT_DIRECTORY):
        item_path = os.path.join(INPUT_DIRECTORY, item)
        if os.path.isfile(item_path):
            process_plate_image(item_path)
        else:
            print(f"ERROR!!!!!!! Ignoring item {item_path}")
