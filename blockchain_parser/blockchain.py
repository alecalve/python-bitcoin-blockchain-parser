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
        """ Yields blocks in sequential order according to height.
            Also sets the height property
        """

        last_blk = None
        global_blks=dict()
        blk_files =  get_files(self.path)

        # Blocks are not written in sequence into the block files.
        # Thus, it's possible that 'block n' is in file 2 and 'block n+1' is n file 50.
        # This means, instead of simply iterating over the files, we have to find the genesis block first
        # and then we have to look for the next block and if we can't find it in our little cache, load a bunch of
        # blocks from the next file(s) until we find the correct block.


        while len(blk_files) >0 or len(global_blks)>0:
            reload = True
            if last_blk is None:
                last_blk = global_blks.pop("0"*64,None)
                if last_blk is not None:
                    reload=False
                    last_blk.height=0
            else:
                b = global_blks.pop(last_blk.hash,None)
                if b is not None:
                    reload = False
                    b.height = last_blk.height + 1
                    last_blk = b

            if reload and len(blk_files) >0:
                blks = [Block(raw_block) for raw_block in get_blocks(blk_files.pop(0))]
                for blk in blks:
                    global_blks[blk.header.previous_block_hash] = blk
                reload=False
            elif reload and len(blk_files) ==0:
                # This means, we can't find the next consecutive block, but we also have no files left to look into
                # so the search is over, even if there are still blocks in global_blks
                break
            else:
                yield last_blk








