from PIL.Image import Image, Resampling


def resize_to_max_dimension(input_image: Image, max_dimension: int) -> Image:
    largest_dimension = max(input_image.width, input_image.height)
    scale = largest_dimension / max_dimension

    new_size = int(input_image.width / scale), int(input_image.height / scale)

    return input_image.resize(new_size, resample=Resampling.BILINEAR)
