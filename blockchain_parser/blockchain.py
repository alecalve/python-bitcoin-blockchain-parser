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

from .block import Block


# Constant separating blocks in the .blk files
BITCOIN_CONSTANT = b"\xf9\xbe\xb4\xd9"
BITCOIN_GENESIS_BLOCK_HASH = '000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f'

def get_files(path):
    """
    Given the path to the .bitcoin directory, returns the sorted list of .blk
    files contained in that directory
    """
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


class Blockchain(object):
    """Represent the blockchain contained in the series of .blk files
    maintained by bitcoind.
    """

    def __init__(self, path):
        self.path = path

    def get_unordered_blocks(self):
        """Yields the blocks contained in the .blk files as is,
        without ordering them according to height.
        """
        for blk_file in get_files(self.path):
            for raw_block in get_blocks(blk_file):
                yield Block(raw_block)

    def get_ordered_blocks(self):
            """
            yields the blocks contained in the .blk files by their height
            order, however since the blocks are not always ordered in the blockchain
            it stores the blocks that came early while searching for the current one.
            
            meaning you could potentially have several blocks in memory
            depending on the state of the blockchain.
            """
            previous_hash = None
            early_block_pool = {}
            blockchain_generator = self.get_unordered_blocks()
            while True:
                #checking if next block is not already in the early_block_pool
                if len(early_block_pool) != 0:
                    try:
                        wanted_early_block = early_block_pool[previous_hash]
                        del early_block_pool[previous_hash]
                        previous_hash = wanted_early_block.hash
                        yield wanted_early_block
                        continue
                    except KeyError:
                        pass

                #was not in the early_block_pool, reading new block from drive
                current_block = blockchain_generator.next()

                #special case, looking for genesis block
                if previous_hash is None:
                    if current_block.hash == BITCOIN_GENESIS_BLOCK_HASH:
                        previous_hash = current_block.hash
                        yield current_block
                        continue
                    else:
                        early_block_pool[current_block.header.previous_block_hash] = current_block
                #normal case, checking if read block is the next one, goes into the early_block_pool otherwhise
                else:
                    if current_block.header.previous_block_hash == previous_hash:
                        previous_hash = current_block.hash
                        yield current_block
                        continue
                    else:
                        early_block_pool[current_block.header.previous_block_hash] = current_block