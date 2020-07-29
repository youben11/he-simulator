import pytest
import numpy as np
import torch as th
from he_sim.algorithms.conv2d import ckks_conv2d


def almost_equal(vec1, vec2, m_pow_ten):
    if len(vec1) != len(vec2):
        return False
    upper_bound = pow(10, -m_pow_ten)
    for v1, v2 in zip(vec1, vec2):
        if abs(v1 - v2) > upper_bound:
            return False
    return True


def torch_conv2d(matrix: np.ndarray, kernel: np.ndarray, stride) -> np.ndarray:
    x = th.from_numpy(matrix.astype("float32")).unsqueeze(0).unsqueeze(0)
    k = th.from_numpy(kernel.astype("float32")).unsqueeze(0).unsqueeze(0)
    result = th.nn.functional.conv2d(
        input=x, weight=k, stride=stride, padding=0, dilation=1
    )
    return np.array(result.squeeze(0).squeeze(0).tolist())


@pytest.mark.parametrize(
    "matrix_shape",
    [
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (28, 28),
        (7, 3),
        (8, 4),
        (9, 11),
        (11, 7),
    ],
)
@pytest.mark.parametrize(
    "kernel_shape",
    [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (5, 3),
        (3, 5),
        (2, 4),
        (4, 2),
    ],
)
@pytest.mark.parametrize("stride", [1, 2, 3, 4, 5])
def test_conv(matrix_shape, kernel_shape, stride):
    x_h, x_w = matrix_shape
    k_h, k_w = kernel_shape
    if k_h > x_h or k_w > x_w:
        return

    matrix = np.random.randn(*matrix_shape)
    kernel = np.random.randn(*kernel_shape)
    expected = torch_conv2d(matrix, kernel, stride).flatten().tolist()
    result = ckks_conv2d(matrix, kernel, stride)[: len(expected)]
    assert almost_equal(result, expected, 3)


# TODO: test replication / test operations cost
