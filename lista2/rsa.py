import secrets
from math import gcd


def mod_inv(a, b):
    s = 0
    old_s = 1
    r = b
    old_r = a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s

    return old_s


def miller_rabin(n, k=10):
    if n % 2 == 0:
        return False
    if n in (2, 3, 5, 7):
        return True
    # calculate s and d such that n - 1 = 2^s * d and s maximal
    n_1 = n - 1
    s = 0
    d = n_1
    while (d & 1) == 0:
        s += 1
        d >>= 1

    tested = []
    for _ in range(min(k, n - 2)):
        a = secrets.randbelow(n)
        while a in tested:
            a = secrets.randbelow(n)
        tested.append(a)
        x = pow(a, d, n)
        if x in (1, n_1):
            continue
        composite = True
        for _ in range(s):
            x = pow(x, 2, n)
            if x == 1:
                return False
            if x == n_1:
                composite = False
                break
        if composite:
            return False
    return True


def get_prime(bits: int):
    lower_bound = 1 << (bits - 1)
    upper_bound = (1 << bits) - 1
    p = secrets.randbelow(upper_bound - lower_bound) + lower_bound
    while not miller_rabin(p):
        p = secrets.randbelow(upper_bound - lower_bound) + lower_bound
    return p


def _generate_keys(keysize: int):
    p = get_prime(keysize // 2)
    q = get_prime(keysize // 2)
    m = (p - 1) * (q - 1)

    n = p * q

    d = 2
    while gcd(d, m) != 1:
        d += 1

    e = mod_inv(d, m)

    return (d, n), (e, n)


def encrypt(self, m: int):
    return pow(m, self.e, self.n)


def decrypt(self, c: int):
    return pow(c, self.d, self.n)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--gen-keys", action="store_true")

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--encrypt", action="store_true")
    group.add_argument("--decrypt", action="store_true")

    parser.add_argument_group(group)

    args = parser.parse_args()

    if args.gen_keys:
        print("gen")
    if args.encrypt:
        print("encrypt")
    elif args.decrypt:
        print("decrypt")
