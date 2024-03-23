import os
import sys
from blockchain_parser.blockchain import Blockchain
from blockchain_parser.transaction import Transaction


# Instantiate the Blockchain by giving the path to the directory
# containing the .blk files created by bitcoind
blockchain = Blockchain(os.path.expanduser('/bitcoin-data/blocks'))
print("block_height,block_header_timestamp,tx_hash,no,input_transaction_hash,input_transaction_index")
for block in blockchain.get_ordered_blocks(os.path.expanduser('/bitcoin-data/blocks/index'),start=int(sys.argv[1]), end=int(sys.argv[2]), cache='index-cache.pickle'):
    for tx in block.transactions:
        for no, input in enumerate(tx.inputs):
            print("%s,%s,%s,%s,%s,%s" % (block.height,block.header.timestamp,tx.hash, no,(input.transaction_hash),input.transaction_index))
