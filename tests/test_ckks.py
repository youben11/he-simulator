from he_sim.ciphertexts import CKKS
import pytest


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
