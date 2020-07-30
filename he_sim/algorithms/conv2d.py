import numpy as np
from typing import Tuple
from math import ceil, log2
from skimage.util.shape import view_as_windows
from he_sim.ciphertexts import CKKS


def memory_strided_im2col(
    x: np.ndarray, kernel_shape: Tuple[int, int], stride: int
) -> np.ndarray:
    x_h, x_w = x.shape
    k_h, k_w = kernel_shape
    # always assuming padding =0
    out_h, out_w = (
        (x_h - k_h) // stride + 1,
        (x_w - k_w) // stride + 1,
    )
    windows = view_as_windows(x, kernel_shape, step=stride)
    return windows.reshape(out_h * out_w, k_h * k_w)


def padded_memory_strided_im2col(
    x: np.ndarray, kernel: np.ndarray, stride: int
) -> Tuple[np.ndarray, np.ndarray]:
    x = memory_strided_im2col(x, kernel.shape, stride)
    # compute padding
    next_power2 = pow(2, ceil(log2(kernel.size)))
    pad_width = next_power2 - kernel.size
    # pad/flatten matrix and kernel
    padded_x = np.pad(x, ((0, 0), (0, pad_width)))
    padded_x = padded_x.T.flatten()
    padded_kernel = np.pad(kernel.flatten(), (0, pad_width))
    return padded_x, padded_kernel


def ckks_conv2d(
    matrix: np.ndarray,
    kernel: np.ndarray,
    stride=1,
    poly_mod_degree=4096,
    scale=2 ** 10,
):
    # encode matrix and kernel
    x, k = padded_memory_strided_im2col(matrix, kernel, stride)
    x, k = x.tolist(), k.tolist()
    chunk_size = len(x) // len(k)
    chunk_nb = len(k)
    # encryption
    ct = CKKS(x, poly_mod_degree, scale, replicated=True)
    # replicating chunks of the kernel [k[i] * chunk_size for i in chunk_nb]
    replicated_kernel = [k[i] for i in range(chunk_nb) for j in range(chunk_size)]
    assert len(x) == len(replicated_kernel)
    # element-wise multiplication
    ct *= replicated_kernel
    # rotate and sum
    next_rotation = 2 ** ceil(log2(len(kernel)))
    while next_rotation >= 1:
        # element-wise sum
        ct += ct.rotate(next_rotation * chunk_size)
        next_rotation //= 2
    # return decrypted result
    return ct.decrypt()
