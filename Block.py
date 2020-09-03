from Admin import Login
rpc = Login().login

class Block(object):

    '''creates a block object'''
    def __init__(self):
        self.bestblock = rpc.getbestblockhash()

    '''gets states for a block'''
    def block_statistics(self,hash):
        block_stats = rpc.getblockstats(hash)
        return block_stats
    
    '''gets hash for a block'''
    def block_hash(self,height):
        block_hash = rpc.getblockhash(height)
        return block_hash
    
    ''' average fee for that block'''
    def block_avgfee(self,hash):
        block_stats = rpc.getblockstats(hash)
        return block_stats['avgfee']

    '''block height'''
    def block_height(self,hash):
        block_stats = rpc.getblockstats(hash)
        return block_stats['height']

    '''UTXO spent in block'''
    def block_UTXOs_in(self,hash):
        block_stats = rpc.getblockstats(hash)
        return block_stats['ins']

    '''block subsidy'''
    def block_subsidy(self,hash):
        block_stats = rpc.getblockstats(hash)
        return block_stats['subsidy']

    '''UTXO output by block'''
    def block_UTXOs_out(self,hash):
        block_stats = rpc.getblockstats(hash)
        return block_stats['outs']

    '''block time'''
    def block_time(self,hash):
        block_stats = rpc.getblockstats(hash)
        return block_stats['time']

    '''block weight in bytes'''
    def block_weight(self,hash):
        block_stats = rpc.getblockstats(hash)
        return block_stats['total_size']
    
    '''block weight in Vbytes'''
    def block_Vweight(self,hash):
        block_stats = rpc.getblockstats(hash)
        return block_stats['total_weight']
    
    '''total fees in block'''
    def block_total_fee(self,hash):
        block_stats = rpc.getblockstats(hash)
        return block_stats['totalfee']
    
    '''totals txns in block'''
    def block_txns(self,hash):
        block_stats = rpc.getblockstats(hash)
        return block_stats['txs']

