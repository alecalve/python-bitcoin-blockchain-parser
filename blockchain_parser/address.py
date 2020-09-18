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

from bitcoin import base58
from bitcoin.bech32 import CBech32Data
from .utils import btc_ripemd160, double_sha256


class Address(object):
    """Represents a bitcoin address"""

    def __init__(self, hash, public_key, address, type, segwit_version):
        self._hash = hash
        self.public_key = public_key
        self._address = address
        self.type = type
        self._segwit_version = segwit_version

    def __repr__(self):
        return "Address(addr=%s)" % self.address

    @classmethod
    def from_public_key(cls, public_key):
        """Constructs an Address object from a public key"""
        return cls(None, public_key, None, "normal", None)

    @classmethod
    def from_ripemd160(cls, hash, type="normal"):
        """Constructs an Address object from a RIPEMD-160 hash, it may be a
        normal address or a P2SH address, the latter is indicated by setting
        type to 'p2sh'"""
        return cls(hash, None, None, type, None)

    @classmethod
    def from_bech32(cls, hash, segwit_version):
        """Constructs an Address object from a bech32 hash."""
        return cls(hash, None, None, "bech32", segwit_version)

    @property
    def hash(self):
        """Returns the RIPEMD-160 hash corresponding to this address"""
        if self.public_key is not None and self._hash is None:
            self._hash = btc_ripemd160(self.public_key)

        return self._hash

    @property
    def address(self):
        """Returns the encoded representation of this address.
        If SegWit, it's encoded using bech32, otherwise using base58
        """
        if self._address is None:
            if self.type != "bech32":
                version = b'\x00' if self.type == "normal" else b'\x05'
                checksum = double_sha256(version + self.hash)

                self._address = base58.encode(version + self.hash + checksum[:4])
            else:
                bech_encoded = CBech32Data.from_bytes(self._segwit_version, self._hash)
                self._address = str(bech_encoded)
        return self._address

    def is_p2sh(self):
        return self.type == "p2sh"
