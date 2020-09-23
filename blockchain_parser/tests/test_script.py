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
from blockchain_parser.script import Script


class TestScript(unittest.TestCase):
    def test_op_return_script(self):
        case1 = "6a"
        script = Script.from_hex(a2b_hex(case1))
        self.assertEqual("OP_RETURN", script.value)
        self.assertFalse(script.is_pubkey())
        self.assertFalse(script.is_multisig())
        self.assertFalse(script.is_p2sh())
        self.assertFalse(script.is_p2wpkh())
        self.assertFalse(script.is_p2wsh())
        self.assertFalse(script.is_pubkeyhash())
        self.assertFalse(script.is_unknown())
        self.assertTrue(script.is_return())

    def test_unknown_script(self):
        case = "40"
        script = Script.from_hex(a2b_hex(case))
        self.assertEqual("INVALID_SCRIPT", script.value)
        self.assertFalse(script.is_pubkey())
        self.assertFalse(script.is_multisig())
        self.assertFalse(script.is_p2sh())
        self.assertFalse(script.is_p2wpkh())
        self.assertFalse(script.is_p2wsh())
        self.assertFalse(script.is_pubkeyhash())
        self.assertTrue(script.is_unknown())
        self.assertFalse(script.is_return())

        case = ""
        script = Script.from_hex(a2b_hex(case))
        self.assertEqual("", script.value)
        self.assertFalse(script.is_pubkey())
        self.assertFalse(script.is_multisig())
        self.assertFalse(script.is_p2sh())
        self.assertFalse(script.is_p2wpkh())
        self.assertFalse(script.is_p2wsh())
        self.assertFalse(script.is_pubkeyhash())
        self.assertTrue(script.is_unknown())
        self.assertFalse(script.is_return())

    def test_multisig_script(self):
        case = "514104cc71eb30d653c0c3163990c47b976f3fb3f37cccdcbedb169a1dfef58bbfbfaff7d8a473e7e2e6d317b87bafe8bde97e3cf8f065dec022b51d11fcdd0d348ac4410461cbdcc5409fb4b4d42b51d33381354d80e550078cb532a34bfa2fcfdeb7d76519aecc62770f5b0e4ef8551946d8a540911abe3e7854a26f39f58b25c15342af52ae"
        script = Script.from_hex(a2b_hex(case))
        self.assertFalse(script.is_pubkey())
        self.assertTrue(script.is_multisig())
        self.assertFalse(script.is_p2sh())
        self.assertFalse(script.is_p2wpkh())
        self.assertFalse(script.is_p2wsh())
        self.assertFalse(script.is_pubkeyhash())
        self.assertFalse(script.is_unknown())
        self.assertFalse(script.is_return())

    def test_p2sh_script(self):
        case = "a91428ad3e63dcae36e5010527578e2eef0e9eeaf3e487"
        script = Script.from_hex(a2b_hex(case))
        self.assertFalse(script.is_pubkey())
        self.assertFalse(script.is_multisig())
        self.assertTrue(script.is_p2sh())
        self.assertFalse(script.is_p2wpkh())
        self.assertFalse(script.is_p2wsh())
        self.assertFalse(script.is_pubkeyhash())
        self.assertFalse(script.is_unknown())
        self.assertFalse(script.is_return())

    def test_p2wpkh_script(self):
        case = "0014c958269b5b6469b6e4b87de1062028ad3bb83cc2"
        script = Script.from_hex(a2b_hex(case))
        self.assertFalse(script.is_pubkey())
        self.assertFalse(script.is_multisig())
        self.assertFalse(script.is_p2sh())
        self.assertTrue(script.is_p2wpkh())
        self.assertFalse(script.is_p2wsh())
        self.assertFalse(script.is_pubkeyhash())
        self.assertFalse(script.is_unknown())
        self.assertFalse(script.is_return())

    def test_p2wsh_script(self):
        case = "0020701a8d401c84fb13e6baf169d59684e17abd9fa216c8cc5b9fc63d622ff8c58d"
        script = Script.from_hex(a2b_hex(case))
        self.assertFalse(script.is_p2sh())
        self.assertFalse(script.is_multisig())
        self.assertFalse(script.is_p2sh())
        self.assertFalse(script.is_p2wpkh())
        self.assertTrue(script.is_p2wsh())
        self.assertFalse(script.is_pubkeyhash())
        self.assertFalse(script.is_unknown())
        self.assertFalse(script.is_return())

    def test_pubkeyhash_script(self):
        case = "76a914e9629ef6f5b82564a9b2ecae6c288c56fb33710888ac"
        script = Script.from_hex(a2b_hex(case))
        self.assertFalse(script.is_pubkey())
        self.assertFalse(script.is_multisig())
        self.assertFalse(script.is_p2sh())
        self.assertFalse(script.is_p2wpkh())
        self.assertFalse(script.is_p2wsh())
        self.assertTrue(script.is_pubkeyhash())
        self.assertFalse(script.is_unknown())
        self.assertFalse(script.is_return())

    def test_pubkey_script(self):
        script = Script.from_hex(a2b_hex("4104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac"))
        self.assertTrue(script.is_pubkey())
        self.assertFalse(script.is_multisig())
        self.assertFalse(script.is_p2sh())
        self.assertFalse(script.is_p2wpkh())
        self.assertFalse(script.is_p2wsh())
        self.assertFalse(script.is_pubkeyhash())
        self.assertFalse(script.is_unknown())
        self.assertFalse(script.is_return())
