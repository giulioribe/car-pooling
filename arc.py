
class Arc(object):
    """docstring for Arc"""
    def __init__(self, id_i, id_f, dur, dist):
        #super(Arc, self).__init__()
        self.id_i = id_i.encode('ascii','ignore')
        self.id_f = id_f.encode('ascii','ignore')
        self.dur = int(dur)
        self.dist = int(dist)

    def setId_i(self, id_i):
        if id_i:
            self.id_i = id_i.encode('ascii','ignore')

    def setId_f(self, id_f):
        if id_f:
            self.id_f = id_f.encode('ascii','ignore')

    def setDur(self, dur):
        if dur:
            self.dur = int(dur)

    def setDist(self, dist):
        if dist:
            self.dist = int(dist)

    def setArc(self, id_i='', id_f='', dur='', dist=''):
        if id_i:
            self.id_i = id_i.encode('ascii','ignore')
        if id_f:
            self.id_f = id_f.encode('ascii','ignore')
        if dur:
            self.dur = int(dur)
        if dist:
            self.dist = int(dist)

    def  getId_i(self):
        return self.id_i

    def  getId_f(self):
        return self.id_f

    def getDur(self):
        return self.dur

    def getDist(self):
        return self.dist

    def getArc(self):
        return {
                'id_i':self.id_i,
                'id_f':self.id_f,
                'dur':self.dur,
                'dist':self.dist
                }






