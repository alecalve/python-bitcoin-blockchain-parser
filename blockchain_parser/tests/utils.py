import os
from binascii import a2b_hex

dir_path = os.path.dirname(os.path.realpath(__file__))


def read_test_data(filename):
    with open(os.path.join(dir_path, "data/", filename)) as f:
        return a2b_hex(f.read().strip())