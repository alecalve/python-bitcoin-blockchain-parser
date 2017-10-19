# bitcoin-blockchain-parser [![Build Status](https://travis-ci.org/alecalve/python-bitcoin-blockchain-parser.svg?branch=master)](https://travis-ci.org/alecalve/python-bitcoin-blockchain-parser) [![Coverage Status](https://coveralls.io/repos/alecalve/python-bitcoin-blockchain-parser/badge.svg?branch=master&service=github)](https://coveralls.io/github/alecalve/python-bitcoin-blockchain-parser?branch=master)
This Python 3 library provides a parser for the raw data stored by bitcoind. 

## Features
- Detects outputs types
- Detects addresses in outputs
- Interprets scripts

## Examples

```python
import sys
from blockchain_parser.blockchain import Blockchain

# Instantiate the Blockchain by giving the path to the directory 
# containing the .blk files created by bitcoind
blockchain = Blockchain(sys.argv[1])
for block in blockchain.get_unordered_blocks():
    for tx in block.transactions:
        for no, output in enumerate(tx.outputs):
            print("tx=%s outputno=%d type=%s value=%s" % (tx.hash, no, output.type, output.value))

# To get the blocks ordered by height, you need to provide the path of the
# `index` directory (LevelDB index) being maintained by bitcoind. It contains
# .ldb files and is present inside the `blocks` directory
for block in blockchain.get_ordered_blocks(sys.argv[1] + '/index', end=1000):
    print("height=%d block=%s" % (block.height, block.hash))
```

More examples are available in the examples directory.

## Installing

Requirements : python-bitcoinlib, coverage for tests

To install, just run
```
python setup.py install
```

## Tests

Run the test suite by lauching
```
./tests.sh
```



