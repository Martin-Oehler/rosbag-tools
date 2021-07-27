"""A method to extract camera data from ROS messages into a NumPy tensors."""
import io

import cv2
import numpy as np
from PIL import Image


def encoding_to_dtype_with_channels(encoding):
    if encoding == "rgb8" or encoding == "bgr8":
        return "uint8", 3
    if encoding == "8UC1" or encoding == "mono8":
        return "uint8", 1
    if encoding == "32FC1":
        return "float32", 1


def numpy_image(data: any, dims: tuple) -> np.ndarray:
    """
    Return a NumPy tensor from image data.

    Args:
        data: the image data to convert to a NumPy tensor
        dims: the height and width of the image

    Returns:
        an RGB or RGBA NumPy tensor of the image data

    """
    # try to create an RGBA tensor from the image data
    try:
        return np.array(data, dtype='uint8').reshape((*dims, 4))
    # try to create an RGB tensor from the image data
    except ValueError:
        try:
            return np.array(data, dtype='uint8').reshape((*dims, 3))
        except ValueError:
            return np.array(data, dtype='uint8').reshape((*dims, 1))


def get_camera_image(data: bytes, dims: tuple) -> np.ndarray:
    """
    Get an image from binary ROS data.

    Args:
        data: the binary data to extract an image from
        dims: the expected dimensions of the image

    Returns:
        an uncompressed NumPy tensor with the 8-bit RGB pixel data

    """
    try:
        # open the compressed image using Pillow
        with Image.open(io.BytesIO(data)) as rgb_image:
            return numpy_image(rgb_image, dims)
    # if an OS error happens, the image is raw data
    except OSError:
        return numpy_image(list(data), dims)


def get_camera_image_with_encoding(encoding: str, data: bytes, dims: tuple) -> np.ndarray:
    """
    Get an image from binary ROS data.

    Args:
        data: the binary data to extract an image from
        dims: the expected dimensions of the image

    Returns:
        an uncompressed NumPy tensor with the 8-bit RGB pixel data

    """
    try:
        # open the compressed image using Pillow
        with Image.open(io.BytesIO(data)) as rgb_image:
            return get_np_image_with_encoding(encoding, rgb_image, dims)
    # if an OS error happens, the image is raw data
    except OSError:
        return get_np_image_with_encoding(encoding, list(data), dims)


def get_np_image_with_encoding(encoding: str, data: any, dims: tuple) -> np.ndarray:
    dtype, channels = encoding_to_dtype_with_channels(encoding)
    array = np.array(data, dtype=dtype).reshape((*dims, channels))
    if dtype == "uint8" and channels == 1:
        array = cv2.cvtColor(array, cv2.COLOR_GRAY2RGB)
    return array



# explicitly define the outward facing API of this module
__all__ = [
    get_camera_image.__name__,
    numpy_image.__name__,
]
