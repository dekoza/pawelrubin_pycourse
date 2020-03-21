import math
import random
import statistics


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
    factors = []
    for p in [p for p in range(2, int(math.sqrt(n))) if is_prime(p)]:
        a = 0
        while n % p == 0:
            n /= p
            a += 1
        if a > 0:
            factors.append((p, a))
    return factors


def fraczero(n):
    zeros = 0
    while n > 0:
        n //= 5
        zeros += n
    return zeros


def random_vector():
    vector = [random.randint(1, 100) for i in range(20)]
    print(f"random vector: {vector}")
    print(f"mean: {statistics.mean(vector)}")
    print(f"min, max: {min(vector)}, {max(vector)}")
    print(f"second min, max: {sorted(vector)[1]}, {sorted(vector)[-2]}")
    print(f"even count: {sum(1 for i in vector if i % 2 == 0)}")


def roman_to_arabic(roman):
    roman_numerals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    arabic = 0
    for i, r in enumerate(roman):
        if i == len(roman) - 1 or roman_numerals[r] >= roman_numerals[roman[i + 1]]:
            arabic += roman_numerals[r]
        else:
            arabic -= roman_numerals[r]

    return arabic


def sequence_matcher(pattern, sequences):
    pattern_dict = {i: c for i, c in enumerate(pattern) if c != "*"}
    return [
        s
        for s in sequences
        if all(s[i] == c for i, c in pattern_dict.items()) and len(pattern) == len(s)
    ]


def sequence_matcher_better(pattern, sequences):
    return [
        s
        for s in sequences
        if all(s[i] == c for i, c in enumerate(pattern) if c != "*")
        and len(pattern) == len(s)
    ]
