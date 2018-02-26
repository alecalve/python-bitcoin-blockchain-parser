import unittest
from binascii import a2b_hex
from datetime import datetime

from blockchain_parser.index import DBBlockIndex

class TestDBIndex(unittest.TestCase):
    def test_from_hex(self):
        key_str = "0000000000000000169cdec8dcfa2e408f59e0d50b1a228f65d8f5480f" \
                  "990000"
        value_str = "88927193a7021d8160804aaa89fc0185b6e81e02000000fb759231e1" \
                    "fa5f80c3508e3a59ebf301930257d04aa492070000000000000000c1" \
                    "1c6bc67af8264be7979db45043f5f5c1e8d2060082af4ce7957658a2" \
                    "2147e30bf97f54747b1b187d1eac41"

        value_hex = a2b_hex(value_str)
        idx = DBBlockIndex(key_str, value_hex)

        self.assertEqual(idx.hash, "0000000000000000169cdec8dcfa2e408f59e0d50b1a228f65d8f5480f990000")
        self.assertEqual(idx.height, 332802)
        self.assertEqual(idx.status, 29)
        self.assertEqual(idx.n_tx, 352)
        self.assertEqual(idx.nFile, 202)
        self.assertEqual(idx.dataPos, 90357377)
        self.assertEqual(idx.undoPos, 13497502)
        self.assertEqual(idx.version, 2)
        self.assertEqual(idx.nounce, 1101799037)
        self.assertEqual(idx.prevHash, "00000000000000000792a44ad057029301f3eb593a8e50c3805ffae1319275fb")
        self.assertEqual(idx.merkelroot, "e34721a2587695e74caf820006d2e8c1f5f54350b49d97e74b26f87ac66b1cc1")
