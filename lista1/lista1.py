import math
import operator


def print_triangle(triangle):
    triangle_str = "\n"
    for i, row in enumerate(triangle):
        padding = (len(triangle) - i) * 2 * " "
        triangle_str += padding + "   ".join(map(str, row)) + padding + "\n"
    triangle_str += (len(triangle) * 4 + 1) * "."
    print(triangle_str)


def pascal_triangle(n):
    return [row := [1]] + [
        row := [1] + [n + m for n, m in zip(row, row[1:])] + [1] for i in range(n)
    ]


def is_prime(n):
    return all(n % i > 0 for i in range(2, int(math.sqrt(n) + 1)))


def primes(n):
    return [i for i in range(2, n) if is_prime(i)]


def make_unique(l):
    return list(dict.fromkeys(l))


def prime_factors(n):
        
