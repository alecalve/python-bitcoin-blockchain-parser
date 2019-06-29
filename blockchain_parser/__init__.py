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


__version__ = "0.1.4"


class BlockchainType():
    def __init__(self, symbol, block_delim, p2pkh_addr_version, p2sh_addr_version):
        self.symbol = symbol
        self.block_delim = block_delim
        self.p2pkh_addr_version = p2pkh_addr_version
        self.p2sh_addr_version = p2sh_addr_version


BITCOIN = BlockchainType('btc', b'\xf9\xbe\xb4\xd9', b'\x00', b'\x05')

DASH = BlockchainType('dash', b"\xbf\x0c\x6b\xbd", b'\x4c', b'\x10')

DIGIBYTE = BlockchainType('zec', b'\xfa\xc3\xb6\xda', b'\x1e', b'\x05')

DOGECOIN = BlockchainType('doge', b'\xc0\xc0\xc0\xc0', b'\x1e', b'\x16')

LITECOIN = BlockchainType('ltc', b"\xfb\xc0\xb6\xdb", b'\x30', b'\x05')

MONACOIN = BlockchainType('mona', b"\xfb\xc0\xb6\xdb", b'\x32', b'\x05')

ZCASH = BlockchainType('zec', b'\x24\xe9\x27\x64', b'\x1c\xb8', b'\x1c\xbd')
