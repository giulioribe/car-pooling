
class Arc(object):
    """docstring for Arc"""
    def __init__(self, id_i, id_f, duration, distance):
        #super(Arc, self).__init__()
        self.id_i = id_i
        self.id_f = id_f
        self.duration = duration
        self.distance = distance

    def setId_i(self, id_i):
        if id_i:
            self.id_i = id_i

    def setId_f(self, id_f):
        if id_f:
            self.id_f = id_f

    def setDuration(self, duration):
        if duration:
            self.duration = duration

    def setDistance(self, distance):
        if distance:
            self.distance = distance

    def setArc(self, id_i='', id_f='', duration='', distance=''):
        if id_i:
            self.id_i = id_i
        if id_f:
            self.id_f = id_f
        if duration:
            self.duration = duration
        if distance:
            self.distance = distance

    def  getId_i(self):
        return self.id_i

    def  getId_f(self):
        return self.id_f

    def getDuration(self):
        return self.duration

    def getDistance(self):
        return self.distance

    def getArc(self):
        return {
                'id_i':self.id_i,
                'id_f':self.id_f,
                'duration':self.duration,
                'distance':self.distance
                }






