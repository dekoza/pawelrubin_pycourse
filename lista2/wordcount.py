import os
import sys

if __name__ == "__main__":
    try:
        filename = sys.argv[1]

        with open(filename, "r") as file:
            print(f"liczba bajtów: {os.stat(filename).st_size}")
            lines = list(file)
            print(f"liczba słów: {sum(len(line.split()) for line in lines)}")
            print(f"liczba linii: {len(lines)}")
            print(f"maksymalna długość linii: {max(len(line) for line in lines)}")
    except IndexError:
        print("Podaj plik wejściowy...")
