import os
import sys


def to_lower(path):
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filename = os.path.join(dirpath, filename)
            os.rename(filename, filename.lower())
        for dirname in dirnames:
            dirname = os.path.join(dirpath, dirname)
            os.rename(dirname, dirname.lower())
            to_lower(dirname)


if __name__ == "__main__":
    try:
        to_lower(sys.argv[1])

    except IndexError:
        print("path is required")
