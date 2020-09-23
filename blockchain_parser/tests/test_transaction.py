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

import os
import unittest
from binascii import a2b_hex, b2a_hex
from blockchain_parser.transaction import Transaction

from .utils import read_test_data

class TestTransaction(unittest.TestCase):
    def test_rbf(self):
        data = a2b_hex("01000000019222bbb054bb9f94571dfe769af5866835f2a97e8839"
                       "59fa757de4064bed8bca01000000035101b1000000000100000000"
                       "00000000016a01000000")
        tx = Transaction(data)
        self.assertTrue(tx.uses_replace_by_fee())

        coinbase = a2b_hex("01000000010000000000000000000000000000000000000000"
                           "000000000000000000000000ffffffff4203c8e405fabe6d6d"
                           "98b0e98e3809941f1fd8cafe7c8236e27b8d1a776b1835aa54"
                           "8bb84fe5b5f3d7010000000000000002650300aaa757eb0000"
                           "002f736c7573682f0000000001baa98396000000001976a914"
                           "7c154ed1dc59609e3d26abb2df2ea3d587cd8c4188ac000000"
                           "00")
        tx = Transaction(coinbase)
        self.assertTrue(tx.is_coinbase())
        self.assertFalse(tx.uses_replace_by_fee())

    def test_bip69(self):
        non_compliant = read_test_data("bip69_false.txt")
        tx = Transaction(non_compliant)
        self.assertFalse(tx.uses_bip69())

        compliant = read_test_data("bip69_true.txt")
        tx = Transaction(compliant)
        self.assertTrue(tx.uses_bip69())

    def test_bech32_p2wpkh(self):
        tx = Transaction(read_test_data("bech32_p2wpkh.txt"))
        self.assertEqual(["3BBqfnaPbgi5KWECWdFpvryUfw7QatWy37"], [a.address for a in tx.outputs[0].addresses])
        self.assertEqual(["bc1q4z0874xmfxe3xeqknulgnqhukhfjwh5tvjrr2x"], [a.address for a in tx.outputs[1].addresses])

    def test_bech32_p2wsh(self):
        tx = Transaction(read_test_data("bech32_p2wsh.txt"))
        self.assertEqual(["3GMKKFPNUg13VktgihUD8QfXVQRBdoDNDf"], [a.address for a in tx.outputs[0].addresses])
        self.assertEqual(["bc1qday7wsftyv4r6qkpn8907s8fy3kexkny0xwrd8d4wlk06zffzyuqpp629n"], [a.address for a in tx.outputs[1].addresses])

    def test_segwit(self):
        tx = Transaction(read_test_data("segwit.txt"))
        self.assertTrue(tx.is_segwit)
        id = "22116f1d76ab425ddc6d10d184331e70e080dd6275d7aa90237ceb648dc38224"
        self.assertTrue(tx.txid == id)
        h = "1eac09f372a8c13bb7dea6bd66ee71a6bcc469b57b35c1e394ad7eb7c107c507"
        self.assertTrue(tx.hash == h)

        segwit_input = tx.inputs[0]
        self.assertTrue(len(segwit_input.witnesses) == 4)
        self.assertTrue(len(segwit_input.witnesses[0]) == 0)

        wit_1 = "3045022100bc2ba8808127f8a74beed6dfa1b9fe54675c55aab85a61d7" \
                "a74c15b993e67e5f02204dada4e15f0b4e659dae7bf0d0f648010d1f2b" \
                "665f587a35eb6f22e44194952301"

        wit_2 = "3045022100f4c7ec7c2064fe2cc4389733ac0a57d8080a62180a004b02" \
                "a19b89267113a17f022004ee9fdb081359c549ee42ffb58279363563ea" \
                "f0191cd8b2b0ceebf62146b50b01"

        wit_3 = "5221022b003d276bce58bef509bdcd9cf7e156f0eae18e1175815282e6" \
                "5e7da788bb5b21035c58f2f60ecf38c9c8b9d1316b662627ec672f5fd9" \
                "12b1a2cc28d0b9b00575fd2103c96d495bfdd5ba4145e3e046fee45e84" \
                "a8a48ad05bd8dbb395c011a32cf9f88053ae"

        parsed_1 = b2a_hex(segwit_input.witnesses[1]).decode("utf-8")
        parsed_2 = b2a_hex(segwit_input.witnesses[2]).decode("utf-8")
        parsed_3 = b2a_hex(segwit_input.witnesses[3]).decode("utf-8")

        self.assertEqual(parsed_1, wit_1)
        self.assertEqual(parsed_2, wit_2)
        self.assertEqual(parsed_3, wit_3)

    def test_vsize(self):
        segwit_tx = Transaction(read_test_data("size_segwit.txt"))
        non_segwit_tx = Transaction(read_test_data("size_non_segwit.txt"))

        self.assertEqual(non_segwit_tx.vsize, non_segwit_tx.size)
        self.assertEqual(non_segwit_tx.vsize, 189)

        self.assertNotEqual(segwit_tx.vsize, segwit_tx.size)
        self.assertEqual(segwit_tx.vsize, 208)
        self.assertEqual(segwit_tx.size, 373)

    def test_large(self):
        data = read_test_data("large_tx.txt")

        tx = Transaction(data)
        self.assertTrue(
            tx.hash == "29a3efd3ef04f9153d47a990bd7b048a4b2d213daa"
                       "a5fb8ed670fb85f13bdbcf")
        self.assertTrue(tx.size == len(tx.hex))

    def test_incomplete(self):
        data = read_test_data("invalid_tx.txt")

        self.assertRaises(Exception, Transaction, data)

    def test_unknown_scripts(self):
        data = read_test_data("scripts_invalid.txt")
        tx = Transaction(data)

        for output in tx.outputs:
            self.assertEqual([], output.addresses)