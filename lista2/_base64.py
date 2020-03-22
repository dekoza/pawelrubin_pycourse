BASE64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def encode(source: str) -> str:
    bitstring = "".join("{:08b}".format(ord(c)) for c in source)
    bitstring += "0" * abs(len(bitstring) % -6)
    sextets = [bitstring[n : n + 6] for n in range(0, len(bitstring) - 5, 6)]
    return "".join(BASE64[int(b, 2)] for b in sextets) + "=" * abs(len(sextets) % -3)


def decode(encoded: str) -> str:
    bitstring = "".join("{:06b}".format(BASE64.index(c)) for c in encoded if c != "=")
    octets = [bitstring[n : n + 8] for n in range(0, len(bitstring) - 7, 8)]
    return "".join(chr(int(oct, 2)) for oct in octets)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--encode", action="store_true")
    group.add_argument("--decode", action="store_true")
    parser.add_argument("inputfile")
    parser.add_argument("outputfile")

    args = parser.parse_args()

    with open(args.inputfile) as inputf, open(args.outputfile, "w") as outputf:
        if args.encode:
            outputf.write(encode(inputf.read()))
        else:
            outputf.write(decode(inputf.read()))
