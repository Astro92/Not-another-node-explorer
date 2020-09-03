from Admin import Login
from datetime import datetime
import numpy as np
rpc = Login().login

class Transaction(object):
    '''contains details of the transactions'''
    def __init__(self,txid):
    #   attributes generated for all transactions
        self.txid = txid # retreives txid
        self.txid_raw = rpc.getrawtransaction(txid) # this might become redundent
        self.txid_info = rpc.decoderawtransaction(self.txid_raw) # this might become redundent
        self.transaction_size = rpc.getrawtransaction(txid, True)['size'] # retreives txid size - uses new RPC call
        self.transaction_vsize = rpc.getrawtransaction(txid, True)['vsize'] # retreives txid vsize - uses new RPC call
    
    def transaction_fee(self):
    #   calculates total fee paid in satoshis    
        Vout_values = []
        Vin_txids = []
        Vin_position = []
        parent_input_value = 0
        for vout in self.txid_info['vout']:
            Vout_values.append(vout['value'])
        vout_total = np.sum(Vout_values) # total output value of UTXO
        for vin in self.txid_info['vin']:
            Vin_txids.append(vin['txid'])
            Vin_position.append(vin['vout'])
        for vin_txid, vin_position in zip(Vin_txids, Vin_position):
            parent_input_value += rpc.decoderawtransaction(rpc.getrawtransaction(vin_txid))['vout'][vin_position]['value']
        fee_total = (parent_input_value - vout_total) * 100000000
        return(fee_total)
    
    def transaction_sats_per_byte(self):
    #   calculates total fee paid in satoshis_per_byte
        Vout_values = []
        Vin_txids = []
        Vin_position = []
        parent_input_value = 0
        for vout in self.txid_info['vout']:
            Vout_values.append(vout['value'])
        vout_total = np.sum(Vout_values) # total output value of UTXO
        for vin in self.txid_info['vin']:
            Vin_txids.append(vin['txid'])
            Vin_position.append(vin['vout'])
        for vin_txid, vin_position in zip(Vin_txids, Vin_position):
            parent_input_value += rpc.decoderawtransaction(rpc.getrawtransaction(vin_txid))['vout'][vin_position]['value']
        fee_total = (parent_input_value - vout_total) * 100000000
        sats_per_vbyte = round(fee_total / self.transaction_vsize,1)
        return sats_per_vbyte
    
    
    def transaction_type(self):
    #   determines the type of transaction script per UTXO generated in the transaction  
        scripts = []
        for script_type in self.txid_info['vout']:
            if script_type['scriptPubKey']['type'] == 'pubkeyhash': 
                scripts.append('P2PKH legacy transaction')
            elif script_type['scriptPubKey']['type'] == 'scripthash':
                scripts.append('P2SH compatability transaction')
            elif script_type['scriptPubKey']['type'] == 'witness_v0_keyhash':
                scripts.append('P2WPHK native segwit transaction')
        return scripts
    
    
    def age(self):
    #   calculates the age of the trasaction either in the mempool or block conformation
        try:
            mempool_entry = rpc.getmempoolentry(self.txid)['time']
            return mempool_entry, datetime.fromtimestamp(mempool_entry).strftime("%d %B %Y, %H:%M")
        except:
            transaction_age = rpc.getrawtransaction(self.txid, True)['blocktime']
            return transaction_age, datetime.fromtimestamp(transaction_age).strftime("%d %B %Y, %H:%M")
        else:    
            return 'Not in mempool'
    
    
    def conformations(self):
    #   caluclates the number of conformations, and the block has it was confirmed in
        try:
            rpc.getmempoolentry(self.txid)['time']
            return 'Not confirmed'
        except:
            number_of_confs = rpc.getrawtransaction(self.txid, True)['confirmations'] 
            block_hash = rpc.getrawtransaction(self.txid, True)['blockhash']
            return number_of_confs, block_hash
        else:    
            return 'Not in mempool'