from Mempool import Mempool
import SQL
from Admin import Login
from Transaction import Transaction
import SQL
import math
import pandas as pd
rpc = Login().login
class MempoolDatabase(object):
    # inherits - __init__() - no. of transactions, size, no. of blocks
    # inherits - size_MBs() - calculates size of mempool in MBs
    # inherits - size_blocks() - calculates number of blocks required to clear mempool
    # inherits - self.mempool_txid - list of all txids in the mempool
    '''create the SQL database for the mempool'''
    def __init__(self):
        self.mempool_database = 'mempool.db'
        self.mempool_table = """ CREATE TABLE IF NOT EXISTS mempool (
                                        txid text NOT NULL,
                                        Weight integer NOT NULL,
                                        Vsize integer NOT NULL,
                                        Fee integer NOT NULL,
                                        FeePerByte integer NOT NULL,
                                        Time integer NOT NULL,
                                        RBFcompatable text NOT NULL
                                        ); """
        connection = SQL.create_connection(self.mempool_database)
        if connection is not None:
            SQL.create_table(connection, self.mempool_table)
        else:
            print('Error - Cannot connect to mempool.db')

    '''filter and add txid to mempool database'''
    def mempool_add_new(self):
        connection = SQL.create_connection(self.mempool_database)
        mempool_info = Mempool().mempool_txid
        for txid in mempool_info:
            if SQL.select_task(connection,txid) == None: # not in database
                try:
                    info = rpc.getmempoolentry(txid) # get txid info
                    entry = (txid, info['weight'], 
                            info['vsize'], 
                            int(info['fee']*100000000), 
                            round(int(info['fee']*100000000)/info['vsize']), 
                            info['time'], info['bip125-replaceable']
                            )
                    add_entry = '''INSERT INTO mempool (txid,Weight,Vsize,Fee,FeePerByte,Time,RBFcompatable) VALUES (?,?,?,?,?,?,?)'''
                    SQL.create_entry(connection,add_entry,entry) # add txid to database
                    #print('transaction - added')
                except:
                    #print('transaction',txid,'has already been mined')
                    pass
            else:
                #print('transaction - already in database')
                pass
        connection.close()
        
    '''remove mined txids from mempool database'''
    def mempool_remove_old(self):
        connection = SQL.create_connection(self.mempool_database)
        info = Mempool().mempool_txid
        df = pd.read_sql_query('SELECT txid FROM mempool;', connection)
        for txid in df['txid']:
            if txid not in info:
                cur = connection.cursor()
                cur.execute('DELETE FROM mempool WHERE txid =?', (txid,))
                #print('transaction ',txid, 'removed')
                connection.commit()
            else:
                pass
        connection.close()

    '''starts the database'''
    def start_database(self):
        self.mempool_add_new()
        self.mempool_remove_old()

if __name__ == '__main__':
    print('this is a module, should not be executed directly')

