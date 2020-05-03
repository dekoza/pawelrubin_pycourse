import hashlib
import os
import sys
from collections import defaultdict


def sha512(fname):
    hash_sha512 = hashlib.sha512()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha512.update(chunk)
    return hash_sha512.hexdigest()


def repchecker(dirpath):
    def helper(p, file_dict=defaultdict(list)):
        for dirpath, dirnames, filenames in os.walk(p):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                file_dict[(os.stat(filename).st_size, sha512(filepath))] += [
                    filepath
                ]
            for dirname in dirnames:
                file_dict = {
                    **file_dict,
                    **helper(os.path.join(dirpath, dirname), file_dict),
                }
        return file_dict

    for same_files in helper(dirpath).values():
        if len(same_files) > 1:
            print("---------------------------------")
            for file in same_files:
                print(file)

    print("---------------------------------")


if __name__ == "__main__":
    try:
        path = sys.argv[1]

        repchecker(path)

    except IndexError:
        print("path is required")
