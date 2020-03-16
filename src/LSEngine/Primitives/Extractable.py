from abc import ABC, abstractmethod
import random

class IExtractable(ABC):

    @abstractmethod
    def get_value(self):
        pass

class RandomValue(IExtractable):

    def __init__(self, min_val, max_val):
        if type(min_val) != type(max_val):
            raise TypeError("type mismatch between min value and max value.")
        self.min = min_val
        self.max = max_val
        if type(self.min) == int:
            self.func = lambda: random.randint(self.min, self.max)
        elif type(self.min) == float:
            self.func = lambda: random.uniform(self.min, self.max)

    def get_value(self):
        return self.func()

class Value(IExtractable):

    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value