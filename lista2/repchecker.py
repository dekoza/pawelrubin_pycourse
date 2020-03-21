import os
import sys
import hashlib
import pprint

from collections import defaultdict


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def repchecker(path):
    def helper(path, file_dict=defaultdict(list)):
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                file_dict[(os.stat(filename).st_size, md5(filepath))] += [filepath]
            for dirname in dirnames:
                file_dict = {
                    **file_dict,
                    **helper(os.path.join(dirpath, dirname), file_dict),
                }
        return file_dict
    
    for same_files in helper(path).values():
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
