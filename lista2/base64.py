BASE64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def encode(source: str) -> str:
    bitstring = "".join(format(ord(c), "b").zfill(8) for c in source)
    bitstring += "0" * (6 - len(bitstring) % 6)
    sextets = [bitstring[n : n + 6] for n in range(0, len(bitstring) - 5, 6)]
    return "".join(BASE64[int(b, 2)] for b in sextets)


def decode(encoded: str) -> str:
    bitstring = "".join(format(BASE64.index(c), "b").zfill(6) for c in encoded)
    bitstring += "0" * (8 - len(bitstring) % 8)
    octets = [bitstring[n : n + 8] for n in range(0, len(bitstring) - 7, 8)]
    return "".join(chr(int(oct, 2)) for oct in octets)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--encode", action="store_true")
    group.add_argument("--decode", action="store_true")
    parser.add_argument("text")

    args = parser.parse_args()

    if args.encode:
        print(encode(args.text))
    else:
        print(decode(args.text))
