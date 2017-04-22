This is a fork of the `bitcoin-blockchain-parser` project found here:
https://github.com/alecalve/python-bitcoin-blockchain-parser

Differences include: Modifications to make parsing work with altcoins such as
Dash, Dogecoin, Litecoin and Feathercoin.

To use with litecoin:

    >>> ltc=Blockchain('/media/chris/3033-6537/litecoin/blocks', b"\xfb\xc0\xb6\xdb")
    >>> next(ltc.get_unordered_blocks())
    Block(12a765e31ffd4059bada1e25190f6e98c99d9714d334efa41a195a7e7e04bfe2)

To use with bitcoin:

    >>> btc=Blockchain('/home/chris/.bitcoin/blocks/')
    >>> next(btc.get_unordered_blocks())
    Block(000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f)

and dash:

    >>> dash=Blockchain('/media/chris/3033-6537/dash/blocks', b"\xbf\x0c\x6b\xbd")
    >>> next(dash.get_unordered_blocks())
    Block(089fc444b06edd0f70d9fda85f9a3b2e22e549b354a1bdb210ce7804c69eb0a4)
