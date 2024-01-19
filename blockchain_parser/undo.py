# Copyright (C) 2015-2020 The bitcoin-blockchain-parser developers
#
# This file is part of bitcoin-blockchain-parser.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of bitcoin-blockchain-parser, including this file, may be copied,
# modified, propagated, or distributed except according to the terms contained
# in the LICENSE file.

from .utils import decode_varint, decode_compactsize, decompress_txout_amt

def decompress_script(raw_hex):
    script_type = raw_hex[0]
    compressed_script = raw_hex[1:]

    # def decompress_script(compressed_script, script_type):
    """ Takes CScript as stored in leveldb and returns it in uncompressed form
    (de)compression scheme is defined in bitcoin/src/compressor.cpp
    :param compressed_script: raw script bytes hexlified (data in decode_utxo)
    :type compressed_script: str
    :param script_type: first byte of script data (out_type in decode_utxo)
    :type script_type: int
    :return: the decompressed CScript
    :rtype: str
    (this code adapted from https://github.com/sr-gi/bitcoin_tools)
    """

    if script_type == 0:
        if len(compressed_script) != 20:
            raise Exception("Compressed script has wrong size")
        script = OutputScript.P2PKH(compressed_script, hash160=True)

    elif script_type == 1:
        if len(compressed_script) != 20:
            raise Exception("Compressed script has wrong size")
        script = OutputScript.P2SH(compressed_script)

    elif script_type in [2, 3]:
        if len(compressed_script) != 33:
            raise Exception("Compressed script has wrong size")
        script = OutputScript.P2PK(compressed_script)

    elif script_type in [4, 5]:
        if len(compressed_script) != 33:
            raise Exception("Compressed script has wrong size")
        prefix = format(script_type - 2, '02')
        script = OutputScript.P2PK(get_uncompressed_pk(prefix + compressed_script[2:]))

    else:
        assert len(compressed_script) / 2 == script_type - NSPECIALSCRIPTS
        script = OutputScript.from_hex(compressed_script)

    return script.content


class BlockUndo(object):
    """
    Represents a block of spent transaction outputs (coins), as encoded 
    in the undo rev*.dat files
    """
    def __init__(self, raw_hex):
        self._raw_hex = raw_hex
        self.spends = []
        num_txs, pos = decode_compactsize(raw_hex)
        # print("found %d" % num_txs + " transactions")
        for i in range(num_txs):
            # print("calling SpentOutput with raw_hex %s", raw_hex)
            txn = SpentTransaction(raw_hex=raw_hex[pos:])
            self.spends.append(txn)
            # print("found transaction #%d length %d hex: " % (i, txn.len), raw_hex[pos:pos+txn.len].hex())
            pos += txn.len


class SpentTransaction(object):
    """Represents the script portion of a spent Transaction output"""
    def __init__(self, raw_hex=None):
        self._raw_hex = raw_hex
        self.outputs = []
        # print("decoding compactsize for hex: ",  raw_hex.hex())
        self.output_len, pos = decode_compactsize(raw_hex)
        # print("found %d" % self.output_len + " outputs")
        for i in range(self.output_len):
            output = SpentOutput(raw_hex=raw_hex[pos:])
            self.outputs.append(output)
            # print("found output #%d length %d hex: " % (i, output.len), raw_hex[pos:pos+output.len].hex())
            pos += output.len
        self.len = pos

    @classmethod
    def from_hex(cls, hex_):
        return cls(hex_)


class SpentOutput(object):
    """Represents a spent Transaction output"""

    def __init__(self, raw_hex=None):
        # print("decoding output: ", raw_hex.hex())
        self._raw_hex = raw_hex
        pos = 0
        # self.version = raw_hex[pos]
        # pos += 1

        # decode height code
        height_code, height_code_len = decode_varint(raw_hex[pos:])
        # print("found height code : ", height_code, height_code_len)
        if height_code % 2 == 1:
            self.is_coinbase = True
            height_code -= 1
        else:
            self.is_coinbase = False
        self.height = height_code // 2

        # print("found height: ", self.height)

        # skip byte reserved only for backwards compatibility, should always be 0x00
        pos += height_code_len + 1

        # decode compressed txout amount
        compressed_amt, compressed_amt_len = decode_varint(raw_hex[pos:])
        self.amt = decompress_txout_amt(compressed_amt)
        pos += compressed_amt_len

        # get script
        script_hex, script_pub_key_compressed_len = SpentScriptPubKey.extract_from_hex(raw_hex[pos:])
        self.script_pub_key_compressed = SpentScriptPubKey(script_hex)
        self.len = pos + self.script_pub_key_compressed.len

    @classmethod
    def from_hex(cls, hex_):
        return cls(hex_)

    
    @property
    def script(self):
        if not self.script:
            self.script = decompress_script(self.script_pub_key_compressed)
        return self.script



class SpentScriptPubKey(object):
    """Represents the script portion of a spent Transaction output"""
    def __init__(self, raw_hex=None):
        self._raw_hex = raw_hex
        self.len = len(raw_hex)
        # self.script_hex = raw_hex[1:]

    @classmethod
    def from_hex(cls, hex_):
        return cls(hex_)

    @classmethod
    def extract_from_hex(cls, raw_hex):
        """
        docstring
        """
        if raw_hex[0] in (0x00, 0x01):
            return (raw_hex[:21], 21)
        elif raw_hex[0] in (0x02, 0x03):
            return (raw_hex[:33], 33)
        elif raw_hex[0] in (0x04, 0x05):
            # print("found strange script type: ", raw_hex[0])
            return (raw_hex[:33], 33)
        else:
            # print("found strange script type: ", raw_hex[0])
            # print("decoding compactsize for raw hex: ", raw_hex.hex())
            script_len_code, script_len_code_len = decode_varint(raw_hex)
            # print("script_len_code, script_len_code_len: (%s, %s)" % (script_len_code, script_len_code_len))
            real_script_len = script_len_code - 6
            # print("real_script_len: %d" % real_script_len)
            return (raw_hex[:script_len_code_len+real_script_len], real_script_len)

    @property
    def script(self):
        if not self.script:
            self.script = decompress_script(self._raw_hex)
        return self.script
