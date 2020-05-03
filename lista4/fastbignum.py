from cmath import exp
from math import pi

from thetimer import Timer


def omega(k, n):
    return exp(-2j * k * pi / n)


def dft(x, n):
    return [
        sum(x[i] * omega(i * k, n) if i < len(x) else 0 for i in range(n))
        for k in range(n)
    ]


def idft(x, n):
    return [
        int(
            round(
                sum(
                    x[i] * omega(-i * k, n) if i < len(x) else 0
                    for i in range(n)
                ).real
            )
            / n
        )
        for k in range(n)
    ]


class FastBigNum:
    def __init__(self, num: str):
        self.num = [int(x) for x in num]
        self.n = len(num)

    def __mul__(self, other):
        X = dft(self.num + [0 for _ in range(self.n)], 2 * self.n)
        Y = dft(other.num + [0 for _ in range(self.n)], 2 * self.n)
        Z = [x * y for x, y in zip(X, Y)]
        Z = idft(Z, 2 * self.n)[:-1]
        return FastBigNum(str(sum(z * 10 ** i for i, z in enumerate(Z[::-1]))))

    def __str__(self):
        return "".join(map(str, self.num))


def main():
    x = 192830192840123019283019232352523523523534234235235335235256243524
    y = 124093184091129312983019223523523523523523523523523543578697346457

    a = FastBigNum(f"{x}")
    b = FastBigNum(f"{y}")

    with Timer() as t1:
        print(x * y)

    with Timer() as t2:
        print(a * b)

    print(f"standard mul   {t1.time}")
    print(f"FastBigNum mul {t2.time}")


if __name__ == "__main__":
    main()
