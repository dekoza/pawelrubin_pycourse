import secrets


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


def get_prime(bits):
    lower_bound = 6074001000 << (bits - 33)
    upper_bound = (1 << bits) - 1
    p = secrets.randbelow(upper_bound - lower_bound) + lower_bound
    while not miller_rabin(p):
        p = secrets.randbelow(upper_bound - lower_bound) + lower_bound
    return p
