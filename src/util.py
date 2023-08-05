from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.fft import fft2, fftshift, ifft2, ifftshift
from PIL import Image

if TYPE_CHECKING:
    from numpy.typing import NDArray


def homomorphic_filter(image: Image.Image, *, rh=2.5, rl=0.5, cutoff=32) -> NDArray:
    """
    :param image: an image in L mode
    :returns: a 2D NumPy data array (you can `Image.fromarray` if you want)

    https://dsp.stackexchange.com/a/42507/64418
    """

    array = np.asarray(image)

    # Prepare kernel
    # Extremely slow!
    kernel = np.zeros(array.shape)
    rows, cols = kernel.shape
    sigma = cols / cutoff
    for r in range(rows):
        for c in range(cols):
            kernel[r, c] = 1 - np.exp(
                -((r - rows / 2) ** 2 + (c - cols / 2) ** 2) / (2 * sigma**2)
            )
    kernel *= rh - rl
    kernel += rl

    # Filter
    freq = fftshift(fft2(np.log(array + 0.01)))
    result = np.exp(ifft2(ifftshift(kernel * freq)).real)

    # Rescale
    result -= result.min()
    result /= result.max()
    result *= 255
    return result.astype(array.dtype)
