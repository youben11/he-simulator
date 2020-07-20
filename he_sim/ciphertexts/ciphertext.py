import abc


class Ciphertext(abc.ABC):
    """Define common operations for ciphertexts"""

    @abc.abstractmethod
    def add(self, other):
        pass

    @abc.abstractmethod
    def sub(self, other):
        pass

    @abc.abstractmethod
    def mul(self, other):
        pass

    @abc.abstractmethod
    def negate(self, other):
        pass

    @abc.abstractmethod
    def add_(self, other):
        pass

    @abc.abstractmethod
    def sub_(self, other):
        pass

    @abc.abstractmethod
    def mul_(self, other):
        pass

    @abc.abstractmethod
    def negate_(self, other):
        pass

    @abc.abstractmethod
    def rotate(self, rotation):
        pass

    @abc.abstractmethod
    def rotate_(self, rotation):
        pass

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.sub(other)

    def __mul__(self, other):
        return self.mul(other)

    def __iadd__(self, other):
        return self.add_(other)

    def __isub__(self, other):
        return self.sub_(other)

    def __imul__(self, other):
        return self.mul_(other)
