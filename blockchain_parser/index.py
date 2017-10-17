from struct import unpack

from .utils import format_hash

BLOCK_HAVE_DATA = 8
BLOCK_HAVE_UNDO = 16

def readVarInt(raw_hex):
    """
    Reads the wierd format of VarInt present in src/serialize.h of bitcoin core
    and being used for storing data in the leveldb.
    This is not the VARINT format described for general bitcoin serialization
    use.
    """
    n = 0
    pos = 0
    while True:
        chData = raw_hex[pos]
        pos += 1
        n = (n << 7) | (chData & 0x7f)
        if chData & 0x80 == 0:
            return (n, pos)
        n += 1

class DBBlockIndex():
    def __init__(self, blk_hash, raw_hex):
        self.hash = blk_hash
        pos = 0
        nVersion, i = readVarInt(raw_hex[pos:])
        pos += i
        self.height, i = readVarInt(raw_hex[pos:])
        pos += i
        self.status, i = readVarInt(raw_hex[pos:])
        pos += i
        self.n_tx, i = readVarInt(raw_hex[pos:])
        pos += i
        if self.status & (BLOCK_HAVE_DATA | BLOCK_HAVE_UNDO):
            self.nFile, i = readVarInt(raw_hex[pos:])
            pos += i
        else:
            self.nFile = -1

        if self.status & BLOCK_HAVE_DATA:
            self.dataPos, i = readVarInt(raw_hex[pos:])
            pos += i
        else:
            dataPos = -1
        if self.status & BLOCK_HAVE_UNDO:
            self.undoPos, i = readVarInt(raw_hex[pos:])
            pos += i

        assert(pos + 80 == len(raw_hex))
        self.version, pHashi, mHashi, time, bits, self.nounce = unpack("<I32s32sIII", raw_hex[-80:])
        self.prevHash = format_hash(pHashi)
        self.merkelroot = format_hash(mHashi)

    def __repr__(self):
        return "DBBlockIndex(%s, height=%d, file_no=%d, file_pos=%d)" % (self.hash, self.height, self.nFile, self.dataPos)
