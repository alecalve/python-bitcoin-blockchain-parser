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
from datetime import datetime

from .utils import read_test_data
from blockchain_parser.block import Block


class TestBlock(unittest.TestCase):
    def test_from_hex(self):
        block_hex = read_test_data("genesis_block.txt")
        block = Block.from_hex(block_hex)
        self.assertEqual(1, block.n_transactions)
        block_hash = "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1" \
                     "b60a8ce26f"
        self.assertEqual(block_hash, block.hash)
        self.assertEqual(486604799, block.header.bits)
        merkle_root = "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127" \
                      "b7afdeda33b"
        self.assertEqual(merkle_root, block.header.merkle_root)
        self.assertEqual(2083236893, block.header.nonce)
        self.assertEqual(1, block.header.version)
        self.assertEqual(1, block.header.difficulty)
        self.assertEqual(285, block.size)
        self.assertEqual(datetime.utcfromtimestamp(1231006505),
                         block.header.timestamp)
        self.assertEqual("0" * 64, block.header.previous_block_hash)

        for tx in block.transactions:
            self.assertEqual(1, tx.version)
            tx_hash = "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127" \
                      "b7afdeda33b"
            self.assertEqual(tx_hash, tx.hash)
            self.assertEqual(204, tx.size)
            self.assertEqual(0, tx.locktime)
            self.assertEqual(0xffffffff, tx.inputs[0].transaction_index)
            self.assertEqual(0xffffffff, tx.inputs[0].sequence_number)
            self.assertTrue("ffff001d" in tx.inputs[0].script.value)
            self.assertEqual("0" * 64, tx.inputs[0].transaction_hash)
            self.assertEqual(50 * 100000000, tx.outputs[0].value)
