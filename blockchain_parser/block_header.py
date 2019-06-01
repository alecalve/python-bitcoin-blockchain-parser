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

import struct
from datetime import datetime
from bitcoin.core import CBlockHeader

from .utils import format_hash


class BlockHeader(object):
    """Represents a block header"""

    def __init__(self, raw_hex):
        self._hex = raw_hex[:80]
        self._version, self._previous_block_hash, self._merkle_root,\
        self._timestamp, self._bits, self._nonce = struct.unpack("<I32s32sIII", self._hex)
        self._previous_block_hash, self._merkle_root = format_hash(self._previous_block_hash), format_hash(self._merkle_root)
        self._difficulty = CBlockHeader.calc_difficulty(self._bits)

    def __repr__(self):
        return "BlockHeader(previous_block_hash=%s)" % self.previous_block_hash

    @classmethod
    def from_hex(cls, raw_hex):
        """Builds a BlockHeader object from its bytes representation"""
        return cls(raw_hex)
    
    # GETTER Functions
    @property
    def version(self):
        """Return the block's version"""
        return self._version
    @property
    def previous_block_hash(self):
        """Return the hash of the previous block"""
        return self._previous_block_hash
    @property
    def merkle_root(self):
        """Returns the block's merkle root"""
        return self._merkle_root
    @property
    def timestamp(self, utc = False):
        """Returns the timestamp of the block as a UTC datetime object"""
        if utc == True:
            return datetime.utcfromtimestamp(self._timestamp)
        return self._timestamp
    @property
    def bits(self):
        """Returns the bits (difficulty target) of the block"""
        return self._bits
    @property
    def nonce(self):
        """Returns the block's nonce"""
        return self._nonce
    @property
    def difficulty(self):
        """Returns the block's difficulty target as a float"""
        return self._difficulty
