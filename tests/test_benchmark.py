from he_sim.ciphertexts import CKKS
from he_sim import benchmark


def some_ckks_ops():
    ct = CKKS([1, 2, 3])
    ct.add(ct)
    ct.mul(ct)
    ct.add_(ct)
    ct.mul_(ct)


def test_ops_counter():
    benchmark.reset()
    some_ckks_ops()
    assert benchmark.OPS_COUNTER["CKKS"]["add"] == 2
    assert benchmark.OPS_COUNTER["CKKS"]["mul"] == 2


def test_context_manager(capsys):
    with benchmark.ops_counter():
        some_ckks_ops()
        ct = CKKS([1, 2, 3])
        ct.rotate(1)

    captured = capsys.readouterr()
    expected_out = """========= CKKS =========
add: 2
mul: 2
rotate: 1
"""
    assert captured.out == expected_out
