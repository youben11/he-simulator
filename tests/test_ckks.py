import pytest
from copy import copy
from he_sim.ciphertexts import CKKS


@pytest.mark.parametrize("data", [[1, 2, 3], [0, 0, 0, 0], [-1, 5, 93.5]])
@pytest.mark.parametrize("poly_mod_degree", [2048, 4096, 8192])
@pytest.mark.parametrize("scale", [2 ** 20, 2 ** 40])
@pytest.mark.parametrize("replicated", [True, False])
def test_encryption_decryption(data, poly_mod_degree, scale, replicated):
    ct = CKKS(data, poly_mod_degree, scale, replicated)
    slots = poly_mod_degree // 2

    if replicated:
        expected_data = (data * (slots // len(data) + 1))[:slots]
    else:
        expected_data = data + [0] * (slots - len(data))

    assert ct.decrypt() == expected_data


@pytest.mark.parametrize("data", [[1, 2, 3], [0, 0, 0, 0], [-1, 5, 93.5]])
@pytest.mark.parametrize("poly_mod_degree", [2048, 4096, 8192])
@pytest.mark.parametrize("scale", [2 ** 20, 2 ** 40])
@pytest.mark.parametrize("replicated", [True, False])
def test_copy(data, poly_mod_degree, scale, replicated):
    ct = CKKS(data, poly_mod_degree, scale, replicated)
    new_ct = ct.copy()

    assert new_ct.decrypt() == ct.decrypt()


@pytest.mark.parametrize("data", [[1, 2, 3], [0, 0, 0, 0], [-1, 5, 93.5]])
@pytest.mark.parametrize(
    "other", [[-1, 0, 2], [0, 1, -1, 73.5], [0, -2, 93.5], [1, 5, 6, 99, -5, 0, 100]]
)
@pytest.mark.parametrize("poly_mod_degree", [2048, 4096, 8192])
@pytest.mark.parametrize("scale", [2 ** 10, 2 ** 20, 2 ** 40])
def test_add(data, other, poly_mod_degree, scale):
    data_copy = copy(data)
    other_copy = copy(other)
    ct = CKKS(data, poly_mod_degree, scale, replicated=True)
    expected = [data[i % len(data)] + other[i % len(other)] for i in range(ct._slots)]
    # add
    result = ct + other
    assert expected == result.decrypt()
    # right add
    result = other + ct
    assert expected == result.decrypt()
    # add inplace
    ct += other
    assert expected == ct.decrypt()
    # data still correct
    assert data_copy == data
    assert other_copy == other


@pytest.mark.parametrize("data", [[1, 2, 3], [0, 0, 0, 0], [-1, 5, 93.5]])
@pytest.mark.parametrize(
    "other", [[-1, 0, 2], [0, 1, -1, 73.5], [0, -2, 93.5], [1, 5, 6, 99, -5, 0, 100]]
)
@pytest.mark.parametrize("poly_mod_degree", [2048, 4096, 8192])
@pytest.mark.parametrize("scale", [2 ** 10, 2 ** 20, 2 ** 40])
def test_sub(data, other, poly_mod_degree, scale):
    data_copy = copy(data)
    other_copy = copy(other)
    ct = CKKS(data, poly_mod_degree, scale, replicated=True)
    expected = [data[i % len(data)] - other[i % len(other)] for i in range(ct._slots)]
    expected_right = [-e for e in expected]
    # sub
    result = ct - other
    assert expected == result.decrypt()
    # right sub
    result = other - ct
    assert expected_right == result.decrypt()
    # sub inplace
    ct -= other
    assert expected == ct.decrypt()
    # data still correct
    assert data_copy == data
    assert other_copy == other


@pytest.mark.parametrize("data", [[1, 2, 3], [0, 0, 0, 0], [-1, 5, 93.5, 73, 81]])
@pytest.mark.parametrize("rotation", [-5, -2, -1, 0, 1, 2, 7])
@pytest.mark.parametrize("poly_mod_degree", [2048, 4096, 8192])
@pytest.mark.parametrize("scale", [2 ** 10])
def test_mul(data, rotation, poly_mod_degree, scale):
    data_copy = copy(data)
    ct = CKKS(data, poly_mod_degree, scale, replicated=True)
    replicated = (data * (ct._slots // len(data) + 1))[: ct._slots]
    expected = replicated[rotation % ct._slots:] + replicated[: rotation % ct._slots]
    # rotate
    result = ct.rotate(rotation)
    assert expected == result.decrypt()
    # rotate inplace
    ct.rotate_(rotation)
    assert expected == ct.decrypt()
    # data still correct
    assert data_copy == data


@pytest.mark.parametrize("data", [[1, 2, 3], [0, 0, 0, 0], [-1, 5, 93.5]])
@pytest.mark.parametrize(
    "other", [[-1, 0, 2], [0, 1, -1, 73.5], [0, -2, 93.5], [1, 5, 6, 99, -5, 0, 100]]
)
@pytest.mark.parametrize("poly_mod_degree", [2048, 4096, 8192])
@pytest.mark.parametrize("scale", [2 ** 10, 2 ** 20, 2 ** 40])
def test_rotation(data, other, poly_mod_degree, scale):
    data_copy = copy(data)
    other_copy = copy(other)
    ct = CKKS(data, poly_mod_degree, scale, replicated=True)
    expected = [data[i % len(data)] * other[i % len(other)] for i in range(ct._slots)]
    # mul
    result = ct * other
    assert expected == result.decrypt()
    # right mul
    result = other * ct
    assert expected == result.decrypt()
    # mul inplace
    ct *= other
    assert expected == ct.decrypt()
    # data still correct
    assert data_copy == data
    assert other_copy == other
