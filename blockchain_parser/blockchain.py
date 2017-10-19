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
import mmap
import struct
import stat
import leveldb

from .block import Block
from .index import DBBlockIndex
from .utils import format_hash


# Constant separating blocks in the .blk files
BITCOIN_CONSTANT = b"\xf9\xbe\xb4\xd9"


def get_files(path):
    """
    Given the path to the .bitcoin directory, returns the sorted list of .blk
    files contained in that directory
    """
    if not stat.S_ISDIR(os.stat(path)[stat.ST_MODE]):
        return [path]
    files = os.listdir(path)
    files = [f for f in files if f.startswith("blk") and f.endswith(".dat")]
    files = map(lambda x: os.path.join(path, x), files)
    return sorted(files)


def get_blocks(blockfile):
    """
    Given the name of a .blk file, for every block contained in the file,
    yields its raw hexadecimal value
    """
    with open(blockfile, "rb") as f:
        if os.name == 'nt':
            size = os.path.getsize(f.name)
            raw_data = mmap.mmap(f.fileno(), size, access=mmap.ACCESS_READ)
        else:
            # Unix-only call, will not work on Windows, see python doc.
            raw_data = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
        length = len(raw_data)
        offset = 0
        block_count = 0
        while offset < (length - 4):
            if raw_data[offset:offset+4] == BITCOIN_CONSTANT:
                offset += 4
                size = struct.unpack("<I", raw_data[offset:offset+4])[0]
                offset += 4 + size
                block_count += 1
                yield raw_data[offset-size:offset]
            else:
                offset += 1
        raw_data.close()

def get_block(blockfile, offset):
    """Extracts a single block from the blockfile at the given offset"""
    with open(blockfile, "rb") as f:
        f.seek(offset - 4) # Size is present 4 bytes before the db offset
        size, = struct.unpack("<I", f.read(4))
        return f.read(size)


class Blockchain(object):
    """Represent the blockchain contained in the series of .blk files
    maintained by bitcoind.
    """

    def __init__(self, path):
        self.path = path
        self.blockIndexes = None
        self.indexPath = None

    def get_unordered_blocks(self):
        """Yields the blocks contained in the .blk files as is,
        without ordering them according to height.
        """
        for blk_file in get_files(self.path):
            for raw_block in get_blocks(blk_file):
                yield Block(raw_block)

    def __getBlockIndexes(self, index):
        """There is no method of leveldb to close the db (and release the lock).
        This creates problem during concurrent operations.
        This function also provides caching of indexes.
        """
        if self.indexPath != index:
            db = leveldb.LevelDB(index)
            self.blockIndexes = [DBBlockIndex(format_hash(k[1:]), v)
                    for k, v in db.RangeIter() if k[0] == ord('b')]
            self.blockIndexes.sort(key = lambda x: x.height)
            self.indexPath = index
        return self.blockIndexes

    def get_ordered_blocks(self, index, start=0, end=None):
        """Yields the blocks contained in the .blk files as per
        the heigt extract from the leveldb index present at path
        index maintained by bitcoind.
        """
        blockIndexes = self.__getBlockIndexes(index)

        if end is None:
            end = len(blockIndexes)

        for blkIdx in blockIndexes[start:end]:
            blkFile = os.path.join(self.path, "blk%05d.dat" % blkIdx.nFile)
            yield Block(get_block(blkFile, blkIdx.dataPos), blkIdx.height)
