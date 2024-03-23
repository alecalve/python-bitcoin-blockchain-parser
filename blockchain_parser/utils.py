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

import hashlib
import struct

from ripemd import ripemd160

def btc_ripemd160(data):
    """Computes ripemd160(sha256(data))"""

    h1 = hashlib.sha256(data).digest()
    r160 = ripemd160.new()
    r160.update(h1)
    return r160.digest()


def double_sha256(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def format_hash(hash_):
    return hash_[::-1].hex()


def decode_uint32(data):
    assert(len(data) == 4)
    return struct.unpack("<I", data)[0]


def decode_uint64(data):
    assert(len(data) == 8)
    return struct.unpack("<Q", data)[0]


def decode_compactsize(data):
    assert(len(data) > 0)
    size = int(data[0])
    assert(size <= 255)

    if size < 253:
        return size, 1

    if size == 253:
        format_ = '<H'
    elif size == 254:
        format_ = '<I'
    elif size == 255:
        format_ = '<Q'
    else:
        # Should never be reached
        assert 0, "unknown format_ for size : %s" % size

    size = struct.calcsize(format_)
    return struct.unpack(format_, data[1:size+1])[0], size + 1


def decode_varint(raw_hex):
    """
    Reads the weird format of VarInt present in src/serialize.h of bitcoin core
    and being used for storing data in the leveldb.
    This is not the VARINT format described for general bitcoin serialization
    use.
    """
    n = 0
    pos = 0
    while True:
        try:
            data = raw_hex[pos]
        except IndexError as e:
            print("IndexError caught on raw_hex: ", raw_hex, e)
            raise e
        pos += 1
        n = (n << 7) | (data & 0x7f)
        if data & 0x80 == 0:
            return n, pos
        n += 1


def decompress_txout_amt(amount_compressed_int):
    # (this function stolen from https://github.com/sr-gi/bitcoin_tools and modified to remove bug)
    # No need to do any work if it's zero.
    if amount_compressed_int == 0:
        return 0

    # The decompressed amount is either of the following two equations:
    # x = 1 + 10*(9*n + d - 1) + e
    # x = 1 + 10*(n - 1)       + 9
    amount_compressed_int -= 1

    # The decompressed amount is now one of the following two equations:
    # x = 10*(9*n + d - 1) + e
    # x = 10*(n - 1)       + 9
    exponent = amount_compressed_int % 10
    
    # integer division
    amount_compressed_int //= 10

    # The decompressed amount is now one of the following two equations:
    # x = 9*n + d - 1  | where e < 9
    # x = n - 1        | where e = 9
    n = 0
    if exponent < 9:
        lastDigit = amount_compressed_int%9 + 1
        # integer division
        amount_compressed_int //= 9
        n = amount_compressed_int*10 + lastDigit
    else:
        n = amount_compressed_int + 1

    # Apply the exponent.
    return n * 10**exponent


def compress_txout_amt(n):
    """ Compresses the Satoshi amount of a UTXO to be stored in the LevelDB. Code is a port from the Bitcoin Core C++
    source:
        https://github.com/bitcoin/bitcoin/blob/v0.13.2/src/compressor.cpp#L133#L160
    :param n: Satoshi amount to be compressed.
    :type n: int
    :return: The compressed amount of Satoshis.
    :rtype: int
    (this function stolen from https://github.com/sr-gi/bitcoin_tools and modified to remove bug)
    """

    if n == 0:
        return 0
    e = 0
    while ((n % 10) == 0) and e < 9:
        n //= 10
        e += 1

    if e < 9:
        d = (n % 10)
        assert (1 <= d <= 9)
        n //= 10
        return 1 + (n * 9 + d - 1) * 10 + e
    else:
        return 1 + (n - 1) * 10 + 9
