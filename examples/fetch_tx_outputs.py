import os
import sys
from blockchain_parser.blockchain import Blockchain

# Instantiate the Blockchain by giving the path to the directory
# containing the .blk files created by bitcoind
blockchain = Blockchain(os.path.expanduser('/bitcoin-data/blocks'))
print("block_height,block.header_timestamp,tx.hash,no,output.type,address,output_value")
for block in blockchain.get_ordered_blocks(os.path.expanduser('/bitcoin-data/blocks/index'),start=int(sys.argv[1]), end=int(sys.argv[2])):
    for tx in block.transactions:
        for no, output in enumerate(tx.outputs):
            try:
                print("%s,%s,%s,%d,%s,%s,%s" % (block.height,block.header.timestamp,tx.hash, no, output.type, output.addresses[0].address if output.addresses else output.addresses , output.value))
            except Exception:
                print("%s,%s,%s,%d,%s,%s,%s" % (block.height,block.header.timestamp,tx.hash, no, "no","no", output.value))
