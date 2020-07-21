"""Benchmark algorithms by counting the number of operations performed.
This module use global variables, multiple threads can leave a battlefield here.
"""

import functools


def _default_ops_counter():
    # For every scheme type, count operations such as add and mul
    # and the CKKS dictionary should then looks like below as example
    # "CKKS": {"add": 5, "mul":2}
    return {"CKKS": {}}


OPS_COUNTER = _default_ops_counter()


def reset():
    global OPS_COUNTER
    OPS_COUNTER = _default_ops_counter()


def counter_benchmark(op):
    @functools.wraps(op)
    def wrapper(*args, **kwargs):
        scheme_name = op.__module__.split(".")[-1].upper()
        # inplace methods such as add_ should be counted as addition as well
        op_name = op.__name__.replace("_", "")
        # increment op count for the specific scheme
        scheme_op_count = OPS_COUNTER[scheme_name].get(op_name, 0)
        OPS_COUNTER[scheme_name][op_name] = scheme_op_count + 1
        return op(*args, **kwargs)

    return wrapper


class ops_counter:
    """Context Manager for counting operations.

    Example:

    with ops_counter():
        ct = CKKS([1, 2, 3])
        ct.add(ct)
        ...
    """

    def __init__(self):
        global OPS_COUNTER
        # save old counter and create a new one for this context
        self._old_ops_counter = OPS_COUNTER.copy()
        OPS_COUNTER = _default_ops_counter()

    def __enter__(self):
        pass

    def __exit__(self, *args):
        global OPS_COUNTER
        for scheme_name in OPS_COUNTER.keys():
            print(f"========= {scheme_name} =========")
            for op_name, count in OPS_COUNTER[scheme_name].items():
                print(f"{op_name}: {count}")
        # restore saved counter
        OPS_COUNTER = self._old_ops_counter
