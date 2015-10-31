
class Node:
    """docstring for ClassName"""
    def __init__(self, id, maxDur, addr, notWith=""):
        #super(Node, self).__init__()
        self.id = id.encode('ascii','ignore')
        self.maxDur = int(maxDur)
        self.addr = addr.encode('ascii','ignore')
        if notWith:
            self.notWith = list(notWith.split(','))
        else:
            self.notWith = ''

    def setId(self, id):
        if id:
            self.id = id.encode('ascii','ignore')

    def setAddr(self, addr):
        if addr:
            self.addr = addr.encode('ascii','ignore')

    def setMaxDur(self, maxDur):
        if maxDur:
            self.maxDur = int(maxDur)

    def setNotWith(self, notWith):
        if notWith:
            self.notWith = list(notWith.split(','))
        else:
            self.notWith = ''

    def setNode(self, id='', maxDur='', addr='', notWith=''):
        if id:
            self.id = id.encode('ascii','ignore')
        if addr:
            self.addr = addr.encode('ascii','ignore')
        if maxDur:
            self.maxDur = int(maxDur)
        if notWith:
            self.notWith = list(notWith.split(','))
        else:
            self.notWith = ''

    def getId(self):
        return self.id

    def getMaxDur(self):
        return self.maxDur

    def getAddr(self):
        return self.addr

    def getNotWith(self):
        return self.notWith

    def getNode(self):
        return {
                'id':self.id,
                'addr':self.addr,
                'maxDur':self.maxDur,
                'notWith':self.notWith
                }

