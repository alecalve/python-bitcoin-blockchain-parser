# Copyright (C) 2015 The bitcoin-blockchain-parser developers
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
from blockchain_parser.script import Script


class TestScript(unittest.TestCase):
    def test_from_hex(self):
        case1 = "6a"
        script = Script.from_hex(a2b_hex(case1))
        self.assertEqual("OP_RETURN", script.value)

    def test_invalid_script(self):
        case = "40"
        script = Script.from_hex(a2b_hex(case))
        self.assertEqual("INVALID_SCRIPT", script.value)
