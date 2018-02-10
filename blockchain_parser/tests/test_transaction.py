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


dir_path = os.path.dirname(os.path.realpath(__file__))


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
        noncompliant = "bip69_false.txt"
        with open(os.path.join(dir_path, noncompliant)) as f:
            data = a2b_hex(f.read().strip())

        tx = Transaction(data)
        self.assertFalse(tx.uses_bip69())

        compliant = "bip69_true.txt"
        with open(os.path.join(dir_path, compliant)) as f:
            data = a2b_hex(f.read().strip())

        tx = Transaction(data)
        self.assertTrue(tx.uses_bip69())

    def test_segwit(self):
        example_tx = "segwit.txt"
        with open(os.path.join(dir_path, example_tx)) as f:
            data = a2b_hex(f.read().strip())

        tx = Transaction(data)
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
