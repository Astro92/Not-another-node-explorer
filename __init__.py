from Block import Block
from Mempool import Mempool,MempoolDatabase
from Transaction import Transaction
from Network import Network
from datetime import datetime

def block_explorer():
    while True:
        request = input('transaction, block height, block hash, or mempool: ')
        try:
            request_int = int(request)
            block_hash = Block().block_hash(request_int)
            print('Block Hash: ' + block_hash)
            print('Block subsidy: ' + str(Block().block_subsidy(block_hash)))
            print('Block Time: ' + str(Block().block_time(block_hash)))
            print('Total transactions: ' + str(Block().block_txns(block_hash)))
            print('Block Vweight: ' + str(Block().block_Vweight(block_hash)))
            print('Block weight: ' + str(Block().block_weight(block_hash)))
        except:
            try:
                print('Block subsidy: ' + str(Block().block_subsidy(request)))
                print('Block Time: ' + str(Block().block_time(request)))
                print('Total transactions: ' + str(Block().block_txns(request)))
                print('Block Vweight: ' + str(Block().block_Vweight(request)))
                print('Block weight: ' + str(Block().block_weight(request)))
            except:
                try:
                    print(Transaction(request).transaction_size)
                    print(Transaction(request).transaction_vsize)
                    print(Transaction(request).transaction_fee())
                    print(Transaction(request).transaction_sats_per_byte())
                    print(Transaction(request).transaction_type())
                    print(Transaction(request).age())
                    print(Transaction(request).conformations())
                except:
                    try:
                        if request == 'mempool':
                            print(str(Mempool().transactions) + ' transactions waiting to be mined')
                            print(str(Mempool().size_MBs()) + ' MBs in mempool')
                            print(str(Mempool().size_blocks()))
                        else:
                            pass
                    except:
                        print('incorrect input, please enter a transaction, block height, block hash, or mempool-info')

def main():
    while True:
        try:
            MempoolDatabase().start_database()
            print('loop at',datetime.now().strftime("%H:%M:%S"))
        except:
            pass

if __name__ == '__main__':
    main()

