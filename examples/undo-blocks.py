import os
import plyvel
from blockchain_parser.blockchain import *
from blockchain_parser.output import *
from blockchain_parser.utils import *
from blockchain_parser.blockchain import Blockchain

undo_files = get_undo_files(os.path.expanduser('~/.bitcoin/blocks'))
undo_block_ctr = 0
for i, file_name in enumerate(undo_files):
    print("parsing undo file #%d" % i)
    for j, block_raw in enumerate(get_blocks(file_name)):
        undo_block_ctr += 1
        if j % 1000 == 0 or (i == 1 and j > 9000):
            print("parsing undo block #%d in file #%d block #%d" % (undo_block_ctr, i, j))
        block_undo_current = BlockUndo(block_raw)
