def lerp(v1, v2, t):
    if isinstance(v1, Vector):
        v1 = v1.vector
    if isinstance(v2, Vector):
        v2 = v2.vector
    if hasattr(v1,  '__len__'):
        if len(v1) != len(v2):
            raise ValueError("unable to lerp between vector with different length")
        return (v1[i] + ((v2[i] - v1[i]) * t) for i in range(0, len(v1)))
    else:
        return v1 + (v2 - v1) * t

def gradience(values, keys, t):
    i = -1
    while i + 1 < len(keys) and keys[i + 1] < t:
        i += 1
    if i < 0:
        return values[0]
    elif i >= len(keys):
        return values[len(keys) - 1]
    else:
        return lerp(values[i], values[i + 1], (t - keys[i]) / (keys[i + 1] - keys[i]))

class Gradient:

    def __init__(self, values, keys):
        self.values = values
        self.keys = keys

    def __call__(self, t):
        i = -1
        while i + 1 < len(self.keys) and self.keys[i + 1] < t:
            i += 1
        if i < 0:
            return self.values[0]
        elif i >= len(self.keys):
            return self.values[len(self.keys) - 1]
        else:
            return lerp(self.values[i], self.values[i + 1], (t - self.keys[i]) / (self.keys[i + 1] - self.keys[i]))

from .Types import Vector, Transform, TransformationMatrix, RotateOverTime, TransformOverTime