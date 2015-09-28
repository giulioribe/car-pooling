
class Node:
    """docstring for ClassName"""
    def __init__(self, id, dur, addr, notWith=""):
        #super(Node, self).__init__()
        self.id = id.encode('ascii','ignore')
        self.dur = dur
        self.addr = addr.encode('ascii','ignore')
        self.notWith = list(notWith.split(','))

    def setId(self, id):
        if id:
            self.id = id.encode('ascii','ignore')

    def setAddr(self, addr):
        if addr:
            self.addr = addr.encode('ascii','ignore')

    def setDur(self, dur):
        if dur:
            self.dur = dur

    def setNotWith(self, notWith):
        if notWith:
            self.notWith = list(notWith.split(','))

    def setNode(self, id='', dur='', addr='', notWith=''):
        if id:
            self.id = id.encode('ascii','ignore')
        if addr:
            self.addr = addr.encode('ascii','ignore')
        if dur:
            self.dur = dur
        if notWith:
            self.notWith = list(notWith.split(','))

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

