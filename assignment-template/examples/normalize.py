from math import sqrt


def normalize(values: list[float]) -> list[float]:
    """Return a vector with unit Euclidean norm."""
    length = sqrt(sum(value ** 2 for value in values))
    if length == 0:
        raise ValueError("Zero vector")
    return [value / length for value in values]


print(normalize([3.0, 4.0]))  # [0.6, 0.8]
