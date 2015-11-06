# bitcoin-blockchain-parser
This Python 3 library provides a parser for the raw data stored by bitcoind. 

## Features
- Returns blocks in an unordered fashion or in the main chain order
- Detects outputs types
- Detects addresses in outputs
- Interprets scripts

## Example

```python
import sys
from blockchain_parser.blockchain import Blockchain

# Instanciate the Blockchain by giving the path to the directory 
# containing the .blk files created by bitcoind
blockchain = Blockchain(sys.argv[1])
for block in blockchain.get_unordered_blocks():
    for tx in block.transactions:
        for no, output in enumerate(tx.outputs):
            print("tx=%s outputno=%d type=%s value=%s" % (tx.hash, no, output.type, output.value))
```

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



