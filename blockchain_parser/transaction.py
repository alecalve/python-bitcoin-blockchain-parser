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

from math import ceil

from .utils import decode_compactsize, decode_uint32, double_sha256, format_hash
from .input import Input
from .output import Output


def bip69_sort(data):
    return list(sorted(data, key=lambda t: (t[0], t[1])))


class Transaction(object):
    """Represents a bitcoin transaction"""

    def __init__(self, raw_hex):
        self._hash = None
        self._txid = None
        self.inputs = None
        self.outputs = None
        self._version = None
        self._locktime = None
        self._size = None
        self.n_inputs = 0
        self.n_outputs = 0
        self.is_segwit = False

        offset = 4

        # adds basic support for segwit transactions
        #   - https://bitcoincore.org/en/segwit_wallet_dev/
        #   - https://en.bitcoin.it/wiki/Protocol_documentation#BlockTransactions
        if b'\x00\x01' == raw_hex[offset:offset + 2]:
            self.is_segwit = True
            offset += 2

        self.n_inputs, varint_size = decode_compactsize(raw_hex[offset:])
        offset += varint_size

        self.inputs = []
        for i in range(self.n_inputs):
            input = Input.from_hex(raw_hex[offset:])
            offset += input.size
            self.inputs.append(input)

        self.n_outputs, varint_size = decode_compactsize(raw_hex[offset:])
        offset += varint_size

        self.outputs = []
        for i in range(self.n_outputs):
            output = Output.from_hex(raw_hex[offset:])
            offset += output.size
            self.outputs.append(output)

        if self.is_segwit:
            self._offset_before_tx_witnesses = offset
            for inp in self.inputs:
                tx_witnesses_n, varint_size = decode_compactsize(raw_hex[offset:])
                offset += varint_size
                for j in range(tx_witnesses_n):
                    component_length, varint_size = decode_compactsize(
                        raw_hex[offset:])
                    offset += varint_size
                    witness = raw_hex[offset:offset + component_length]
                    inp.add_witness(witness)
                    offset += component_length

        self._size = offset + 4
        self.hex = raw_hex[:self._size]

        if self._size != len(self.hex):
            raise Exception("Incomplete transaction!")

    def __repr__(self):
        return "Transaction(%s)" % self.hash

    @classmethod
    def from_hex(cls, hex):
        return cls(hex)

    @property
    def version(self):
        """Returns the transaction's version number"""
        if self._version is None:
            self._version = decode_uint32(self.hex[:4])
        return self._version

    @property
    def locktime(self):
        """Returns the transaction's locktime as an int"""
        if self._locktime is None:
            self._locktime = decode_uint32(self.hex[-4:])
        return self._locktime

    @property
    def hash(self):
        """Returns the transaction's id. Equivalent to the hash for non SegWit transactions,
        it differs from it for SegWit ones. """
        if self._hash is None:
            self._hash = format_hash(double_sha256(self.hex))

        return self._hash

    @property
    def size(self):
        """Returns the transactions size in bytes including the size of the
        witness data if there is any."""
        return self._size

    @property
    def vsize(self):
        """Returns the transaction size in virtual bytes."""
        if not self.is_segwit:
            return self._size
        else:
            # the witness is the last element in a transaction before the
            # 4 byte locktime and self._offset_before_tx_witnesses is the
            # position where the witness starts
            witness_size = self._size - self._offset_before_tx_witnesses - 4

            # size of the transaction without the segwit marker (2 bytes) and
            # the witness
            stripped_size = self._size - (2 + witness_size)
            weight = stripped_size * 3 + self._size

            # vsize is weight / 4 rounded up
            return ceil(weight / 4)

    @property
    def txid(self):
        """Returns the transaction's id. Equivalent to the hash for non SegWit transactions,
        it differs from it for SegWit ones. """
        if self._txid is None:
            # segwit transactions have two transaction ids/hashes, txid and wtxid
            # txid is a hash of all of the legacy transaction fields only
            if self.is_segwit:
                txid_data = self.hex[:4] + self.hex[
                                           6:self._offset_before_tx_witnesses] + self.hex[
                                                                                 -4:]
            else:
                txid_data = self.hex
            self._txid = format_hash(double_sha256(txid_data))

        return self._txid

    def is_coinbase(self):
        """Returns whether the transaction is a coinbase transaction"""
        for input in self.inputs:
            if input.transaction_hash == "0" * 64:
                return True
        return False

    def uses_replace_by_fee(self):
        """Returns whether the transaction opted-in for RBF"""
        # Coinbase transactions may have a sequence number that signals RBF
        # but they cannot use it as it's only enforced for non-coinbase txs
        if self.is_coinbase():
            return False

        # A transactions opts-in for RBF when having an input
        # with a sequence number < MAX_INT - 1
        for input in self.inputs:
            if input.sequence_number < 4294967294:
                return True
        return False

    def uses_bip69(self):
        """Returns whether the transaction complies to BIP-69,
        lexicographical ordering of inputs and outputs"""
        # Quick check
        if self.n_inputs == 1 and self.n_outputs == 1:
            return True

        input_keys = [
            (i.transaction_hash, i.transaction_index)
            for i in self.inputs
        ]

        if bip69_sort(input_keys) != input_keys:
            return False

        output_keys = [(o.value, o.script.value) for o in self.outputs]

        return bip69_sort(output_keys) == output_keys
