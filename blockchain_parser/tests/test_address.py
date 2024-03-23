# Copyright (C) 2015-2016 The bitcoin-blockchain-parser developers
#
# This file is part of bitcoin-blockchain-parser.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of bitcoin-blockchain-parser, including this file, may be copied,
# modified, propagated, or distributed except according to the terms contained
# in the LICENSE file.

import unittest
from binascii import a2b_hex

from blockchain_parser.address import Address


class TestUtils(unittest.TestCase):
    def test_from_public_key(self):
        public_key = "0450863AD64A87AE8A2FE83C1AF1A8403CB53F53E486D8511DAD8A" \
                     "04887E5B23522CD470243453A299FA9E77237716103ABC11A1DF38" \
                     "855ED6F2EE187E9C582BA6"
        hex_pk = a2b_hex(public_key)
        address = Address.from_public_key(hex_pk)
        self.assertEqual(address.address, "16UwLL9Risc3QfPqBUvKofHmBQ7wMtjvM")
        address_hash = "010966776006953D5567439E5E39F86A0D273BEE"
        self.assertEqual(address.hash, a2b_hex(address_hash))

    def test_from_ripemd160(self):
        ripemd160 = "010966776006953D5567439E5E39F86A0D273BEE"
        address = Address.from_ripemd160(a2b_hex(ripemd160))
        self.assertEqual(address.address, "16UwLL9Risc3QfPqBUvKofHmBQ7wMtjvM")

    def test_from_bech32(self):
        # Example sourced from https://en.bitcoin.it/wiki/Bech32
        bech32 = "751e76e8199196d454941c45d1b3a323f1433bd6"
        address = Address.from_bech32(a2b_hex(bech32), segwit_version=0)
        self.assertEqual(address.address, "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4")

    def test_from_bech32m(self):
        # https://blockstream.info/tx/33e794d097969002ee05d336686fc03c9e15a597c1b9827669460fac98799036?expand
        # Second output
        bech32m = "a37c3903c8d0db6512e2b40b0dffa05e5a3ab73603ce8c9c4b7771e5412328f9"
        address = Address.from_bech32m(a2b_hex(bech32m), segwit_version=1)
        self.assertEqual(address.address, "bc1p5d7rjq7g6rdk2yhzks9smlaqtedr4dekq08ge8ztwac72sfr9rusxg3297")
