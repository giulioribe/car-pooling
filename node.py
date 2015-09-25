
class Node:
    """docstring for ClassName"""
    def __init__(self, id, dur, addr, notWith=""):
        #super(Node, self).__init__()
        self.id = id
        self.dur = dur
        self.addr = addr
        self.notWith = list(notWith.split(','))

    def setId(self, id):
        if id:
            self.id = id

    def setAddr(self, addr):
        if addr:
            self.addr = addr

    def setNode(self, id='', dur='', addr='', notWith=''):
        if id:
            self.id = id
        if addr:
            self.addr = addr
        if dur:
            self.dur = dur
        if notWith:
            self.notWith = notWith

    def getId(self):
        return self.id

    def getDur(self):
        return self.dur

    def getAddr(self):
        return self.addr

    def getNotWith(self):
        return self.notWith

    def getNode(self):
        return {
                'id':self.id,
                'addr':self.addr,
                'dur':self.dur,
                'notWith':self.notWith
                }

