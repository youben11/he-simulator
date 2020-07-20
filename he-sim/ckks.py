class CKKS:
    """Simulation of a CKKS ciphertext with batching."""

    def __init__(self, data, poly_mod_degree=8192, scale=2 ** 40, replicated=False):
        self._check_parameters(data)
        self._data = data
        self._slots = poly_mod_degree // 2
        self._scale_data(scale)
        if replicated:
            self._replicate_data()
        else:
            self._fill_with(0)

    def _check_parameters(self, data):
        if not isinstance(data, list):
            raise ValueError("data must be a list of numbers")
        else:
            for elem in data:
                if not isinstance(elem, (int, float)):
                    raise ValueError("data must be a list of numbers")

    def _replicate_data(self):
        self._data = self._data * (self._slots // len(self._data) + 1)
        self._data = self._data[: self._slots]

    def _fill_with(self, elem):
        self._data.extend([elem] * (self._slots - len(self._data)))

    def _scale_data(self, scale):
        for i in range(len(self._data)):
            self._data[i] *= scale
