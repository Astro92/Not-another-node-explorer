from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

rpc_connection = AuthServiceProxy('http://%s:%s@MY_NODE_ADDRESS:8332'%('BITCOIN_NODE_ADMIN', 'BITCOIN_NODE_PASSWORD'),timeout=120)

class Login(object):
    '''Login credentials for the Bitcoin-RPC'''
    def __init__(self):
        self.login = rpc_connection
