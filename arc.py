
class Arc(object):
    """docstring for Arc"""
    def __init__(self, id_i, id_f, dur, dist):
        #super(Arc, self).__init__()
        self.id_i = id_i
        self.id_f = id_f
        self.dur = dur
        self.dist = dist

    def setId_i(self, id_i):
        if id_i:
            self.id_i = id_i

    def setId_f(self, id_f):
        if id_f:
            self.id_f = id_f

    def setDur(self, dur):
        if dur:
            self.dur = dur

    def setDist(self, dist):
        if dist:
            self.dist = dist

    def setArc(self, id_i='', id_f='', dur='', dist=''):
        if id_i:
            self.id_i = id_i
        if id_f:
            self.id_f = id_f
        if dur:
            self.dur = dur
        if dist:
            self.dist = dist

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






