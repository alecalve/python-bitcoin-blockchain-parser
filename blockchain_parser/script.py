# Copyright (C) 2015 The bitcoin-blockchain-parser developers
#
# This file is part of bitcoin-blockchain-parser.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-bitcoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

from bitcoin.core.script import CScript, CScriptInvalidError
from binascii import b2a_hex

class Script(object):
    """Represents a bitcoin script contained in an input or output"""

    def __init__(self, raw_hex):
        self.hex = raw_hex
        self._script = None
        self._type = None
        self._value = None
        self._operations = None
        self._addresses = None

    @classmethod
    def from_hex(cls, hex_):
        return cls(hex_)

    def __repr__(self):
        return "Script(%s)" % self.value

    @property
    def script(self):
        """Returns the underlying CScript object"""
        if self._script is None:
            self._script = CScript(self.hex)

        return self._script

    @property
    def operations(self):
        """Returns the list of operations done by this script,
        an operation is one of :
           - a CScriptOP
           - bytes data pushed to the stack
           - an int pushed to the stack
        If the script is invalid (some coinbase scripts are), a list containing
        one operation (INVALID_SCRIPT) is returned
        """
        if self._operations is None:
            # Some coinbase scripts are garbage, they could not be valid
            try:
                self._operations = list(self.script)
            except CScriptInvalidError:
                self._operations = ["INVALID_SCRIPT"]

        return self._operations

    @property
    def value(self):
        """Returns a string representation of the script"""
        if self._value is None:
            representations = []
            for operation in self.operations:
                if type(operation) == bytes:
                    representations.append(b2a_hex(operation).decode("ascii"))
                else:
                    representations.append(str(operation))
            self._value = " ".join(representations)

        return self._value
