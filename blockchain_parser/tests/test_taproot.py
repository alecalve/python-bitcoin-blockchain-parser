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
#
# The transactions were taken from 
# https://bitcoin.stackexchange.com/questions/110995/how
# -can-i-find-samples-for-p2tr-transactions-on-mainnet
#
# 33e7…9036, the first P2TR transaction
# 3777…35c8, the first transaction with both a P2TR scriptpath and a P2TR keypath input
# 83c8…7d82, with multiple P2TR keypath inputs
# 905e…d530, the first scriptpath 2-of-2 multisig spend
# 2eb8…b272, the first use of the new Tapscript opcode OP_CHECKSIGADD
#
# THESE TRANSACTIONS ARE INCLUDED IN BLK02804.DAT

import os
import sys
sys.path.append('../..')
from blockchain_parser.blockchain import Blockchain


FIRST_TAPROOT = "33e794d097969002ee05d336686fc03c9e15a597c1b9827669460fac98799036"
FIRST_TAPROOT_2X_P2TR = "37777defed8717c581b4c0509329550e344bdc14ac38f71fc050096887e535c8"
MULTIPLE_P2TR_INPUTS = "83c8e0289fecf93b5a284705396f5a652d9886cbd26236b0d647655ad8a37d82"
FIRST_2_OF_2_SPEND = "905ecdf95a84804b192f4dc221cfed4d77959b81ed66013a7e41a6e61e7ed530"
USING_OP_CHECKSIGADD = "2eb8dbaa346d4be4e82fe444c2f0be00654d8cfd8c4a9a61b11aeaab8c00b272"


TAPROOTS = [FIRST_TAPROOT,
            FIRST_TAPROOT_2X_P2TR,
            MULTIPLE_P2TR_INPUTS,
            FIRST_2_OF_2_SPEND,
            USING_OP_CHECKSIGADD]


blockchain = Blockchain(os.path.expanduser('../../blocks'))
for block in blockchain.get_unordered_blocks():
    for tx in block.transactions:
         if tx.txid in TAPROOTS:
            print("{:<15}{}".format("Tx ID: ", tx.txid))
            for tx_input in tx.inputs:
                print("{:<15}{}".format("Input Tx ID: ",tx_input.transaction_hash))
            for tx_output in tx.outputs:
                for addr in tx_output.addresses:
                    print("{:<15}{}".format("Address: ", addr.address))
                print("{:<15}{:,.0f} s".format("Value: ", tx_output.value))
            print("----------------------------------------------------------------")