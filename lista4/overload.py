import math
from inspect import getfullargspec
from typing import Callable, Dict, Tuple, List


class Overload:
    functions: Dict[Tuple[str, int], Callable] = {}

    def __init__(self, function: Callable):
        Overload.functions[
            (function.__name__, len(getfullargspec(function).args))
        ] = function
        self.function = function

    def __call__(self, *args, **kwargs):
        return self.functions[(self.function.__name__, len(args))](*args, **kwargs)


def overload(function: Callable):
    return Overload(function)


if __name__ == "__main__":

    @overload
    def norm(x, y):
        return math.sqrt(x * x + y * y)

    @overload
    def norm(x, y, z):
        return abs(x) + abs(y) + abs(z)

    @overload
    def norm(x):
        return 1

    print(f"norm(2,4) = {norm(2,4)}")
    print(f"norm(2,3,4) = {norm(2,3,4)}")
