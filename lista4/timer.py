import time
from typing import Callable


class Timer:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.end_time = time.time()

    @property
    def time(self):
        return self.end_time - self.start_time


def timer(function: Callable):
    """ Prints an execution time of a function."""

    def add_timer():
        with Timer() as t:
            function()
        print(f"{function.__name__} execution time: {t.time}s")

    return add_timer


if __name__ == "__main__":

    @timer
    def test_timer():
        time.sleep(1)

    test_timer()
