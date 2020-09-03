from Admin import Login
rpc = Login().login

class Network(object):
    '''Bitcoin network statistics'''
    def __init__(self):
        self.difficulty = rpc.getdifficulty()