from copy import copy
from he_sim.ciphertexts.ciphertext import Ciphertext
from he_sim.benchmark import counter_benchmark


class CKKS(Ciphertext):
    """Simulation of a CKKS ciphertext with batching."""

    def __init__(self, data, poly_mod_degree=8192, scale=2 ** 40, replicated=True):
        self._check_parameters(data)
        self._data = copy(data)
        self._slots = poly_mod_degree // 2
        self._scale_data(scale)
        self._scale = scale
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

    def decrypt(self):
        decrypted = [d / self._scale for d in self._data]
        return decrypted

    def copy(self):
        new = CKKS(self.decrypt(), self._slots * 2, self._scale)
        return new

    def _plaintext(self, data, replicated=True):
        # scale
        pt = copy(data)
        for i in range(len(pt)):
            pt[i] *= self._scale
        # replicate
        if replicated:
            pt = pt * (self._slots // len(pt) + 1)
            pt = pt[: self._slots]
        return pt

    def _check_other(self, other):
        if isinstance(other, list):
            if len(other) > self._slots:
                raise ValueError(f"Plaintext vector is bigger than {self._slots}")
            other = self._plaintext(other)

        elif isinstance(other, CKKS):
            if self._slots != other._slots:
                raise ValueError(
                    f"Polymoduls degrees doesn't match {self._slots * 2} != {other._slots * 2}"
                )
            if self._scale != other._scale:
                raise ValueError(
                    f"Scales doesn't match {self._scale} != {other._scale}"
                )
            other = other._data
        else:
            raise TypeError(f"Don't support operations with {type(other)}")
        return other

    def add(self, other):
        new = self.copy()
        return new.add_(other)

    @counter_benchmark
    def add_(self, other):
        other = self._check_other(other)
        for i in range(len(other)):
            self._data[i] += other[i]
        return self

    def sub(self, other):
        new = self.copy()
        return new.sub_(other)

    @counter_benchmark
    def sub_(self, other):
        other = self._check_other(other)
        for i in range(len(other)):
            self._data[i] -= other[i]
        return self

    def mul(self, other):
        new = self.copy()
        return new.mul_(other)

    @counter_benchmark
    def mul_(self, other):
        other = self._check_other(other)
        for i in range(len(other)):
            self._data[i] *= other[i]
            # rescale down
            self._data[i] /= self._scale
        return self

    def negate(self):
        new = self.copy()
        return new.negate_()

    @counter_benchmark
    def negate_(self):
        for i in range(len(self._data)):
            self._data[i] *= -1
        return self

    def rotate(self, rotation):
        new = self.copy()
        return new.rotate_(rotation)

    @counter_benchmark
    def rotate_(self, rotation):
        rotation %= self._slots
        self._data = self._data[rotation:] + self._data[: rotation]
        return self
