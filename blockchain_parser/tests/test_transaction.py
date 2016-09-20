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
from binascii import a2b_hex
from blockchain_parser.transaction import Transaction


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
        noncompliant = "blockchain_parser/tests/bip69_false.txt"
        with open(os.path.join(os.getcwd(), noncompliant)) as f:
            data = a2b_hex(f.read().strip())

        tx = Transaction(data)
        self.assertFalse(tx.uses_bip69())

        compliant = "blockchain_parser/tests/bip69_true.txt"
        with open(os.path.join(os.getcwd(), compliant)) as f:
            data = a2b_hex(f.read().strip())

        tx = Transaction(data)
        self.assertTrue(tx.uses_bip69())
