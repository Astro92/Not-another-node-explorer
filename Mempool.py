from Admin import Login
from Transaction import Transaction
import SQL
import math
import time
import pandas as pd
rpc = Login().login

class Mempool(object):
    '''creates an object of the mempool'''
    def __init__(self):
        self.transactions = rpc.getmempoolinfo()['size'] # number of transactions
        self.size_bytes = rpc.getmempoolinfo()['bytes'] # size in bytes
        self.mempool_txid = rpc.getrawmempool() # raw txid in current mempool

    '''calculates the size of the mempool in MBs'''
    def size_MBs(self):
        temp = self.size_bytes/1000000
        return round(temp,2)
    
    '''calculates the number of blocks in the mempool'''
    def size_blocks(self):
        temp = self.size_bytes/1000000
        if temp < 1:
            return '1 block waiting to be mined'
        else:
            return str(math.ceil(temp)) + ' blocks waiting to be mined'

class MempoolDatabase(object):
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
        self.mempool_store = """ CREATE TABLE IF NOT EXISTS mempool_store (
                                        DateTime text NOT NULL,
                                        a integer NOT NULL,
                                        b integer NOT NULL,
                                        c integer NOT NULL,
                                        d integer NOT NULL,
                                        e integer NOT NULL,
                                        f integer NOT NULL,
                                        g integer NOT NULL,
                                        h integer NOT NULL,
                                        i integer NOT NULL,
                                        j integer NOT NULL,
                                        k integer NOT NULL,
                                        l integer NOT NULL,
                                        m integer NOT NULL,
                                        n integer NOT NULL,
                                        o integer NOT NULL,
                                        p integer NOT NULL,
                                        q integer NOT NULL,
                                        r integer NOT NULL,
                                        s integer NOT NULL,
                                        t integer NOT NULL,
                                        u integer NOT NULL,
                                        v integer NOT NULL,
                                        w integer NOT NULL,
                                        x integer NOT NULL,
                                        y integer NOT NULL,
                                        z integer NOT NULL,
                                        aa integer NOT NULL,
                                        bb integer NOT NULL,
                                        cc integer NOT NULL,
                                        dd integer NOT NULL,
                                        ee integer NOT NULL,
                                        ff integer NOT NULL,
                                        gg integer NOT NULL
                                        ); """
        
        connection = SQL.create_connection(self.mempool_database)
        if connection is not None:
            SQL.create_table(connection, self.mempool_table)
            SQL.create_table(connection,self.mempool_store)
        else:
            print('Error - Cannot connect to mempool.db')

    '''filter and add txid to mempool database'''
    def mempool_add_new(self):
        connection = SQL.create_connection(self.mempool_database)
        mempool_info = Mempool().mempool_txid
        for txid in mempool_info:
            if SQL.select_query(connection,txid) == None: # not in database
                try:
                    info = rpc.getmempoolentry(txid) # get txid info
                    entry = (txid, info['weight'], 
                            info['vsize'], 
                            int(info['fee']*100000000), 
                            round(int(info['fee']*100000000)/info['vsize']), 
                            info['time'], info['bip125-replaceable']
                            )
                    SQL_command = '''INSERT INTO mempool (txid,Weight,Vsize,Fee,FeePerByte,Time,RBFcompatable) VALUES (?,?,?,?,?,?,?)'''
                    SQL.execute_command(connection,SQL_command,entry) # add txid to database
                except:
                    pass
            else:
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
                connection.commit()
            else:
                pass
        connection.close()

    '''starts the database'''
    def start_database(self):
        self.mempool_add_new()
        self.mempool_remove_old()
    
    #Organisation of transaction

if __name__ == '__main__':
    print('this is a module, should not be executed directly')