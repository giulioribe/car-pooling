import json
import requests
import collections
import random
from operator import attrgetter

class Euristiche(object):
    """docstring for Euristiche"""
    def __init__(self, node_dict, arc_dict):
        #super(Euristiche, self).__init__()
        self.node_dict = node_dict
        self.arc_dict = arc_dict
        self.cars_list = list()
        self.dur_list = list()
        self.dist = int()

    def checkNotWith(self, cars_list, nauto, node_dict, newper):
        for car in cars_list[nauto]:
            if (newper in node_dict[car].getNotWith() or
                    car in node_dict[newper].getNotWith()):
                return False
        return True

    def minDuration(self, dur, newdur, mindur):
        if newdur == 0 or dur == 0:
            return True
        elif (dur+newdur) > mindur:
            return False
        return True

    def greedy(self):
        """
        per ogni chiave del dizionario estraggo i nodi e li inserisco in un
        dizionario che contiene solo nodi verso la destinazione
        """
        arcToDest_dict = dict()
        for key in self.arc_dict.keys():
            arcToDest_dict[key] = self.arc_dict[key][0]
        """
        creo una lista di liste dove ogni lista contiene il percorso di una
        macchina
        """
        # imposto a -1 nauto cosi' nel ciclo while la prima volta che aggiungo un
        # valore = 0
        nauto = -1
        cars_list = list()
        dur_list = list()
        dist_list = list()
        find = False
        # finche' ci sono archi verso la destionazione continuo a ciclare
        while len(arcToDest_dict) > 0:
            if not find:
                # ordino il dizionario e prendo l'arco che ha il nodo iniziale
                # piu' distante
                car = sorted(arcToDest_dict.values(),
                        key=attrgetter('dist'),
                        reverse=True)[0].getId_i()
                arcToDest_dict.pop(car)
                dur = 0
                mindur = self.node_dict[car].getDur()
                cars_list.append(list())
                dur_list.append(list())
                dist_list.append(list())
                nauto += 1
                cars_list[nauto].append(car)
            else:
                find = False
            # prendo la lista di archi dal nodo di partenza
            arc_list = self.arc_dict[car]
            # ordina la lista di archi in ordine crescente
            for arc in sorted(arc_list, key=attrgetter('dist')):
                if (arc.getId_f() in arcToDest_dict and
                        self.arc_dict[car][0].getDist() >= arc.getDist() and
                        self.checkNotWith(cars_list, nauto, self.node_dict, arc.getId_f()) and
                        self.minDuration(dur, arc.getDur(), mindur)):
                    car = arc.getId_f()
                    dur += arc.getDur()
                    dur_list[nauto].append(arc.getDur())
                    dist_list[nauto].append(arc.getDist())
                    if mindur > self.node_dict[car].getDur():
                        mindur = self.node_dict[car].getDur()
                    cars_list[nauto].append(car)
                    arcToDest_dict.pop(car)
                    if len(cars_list[nauto]) < 5:
                        find = True
                    break
        # aggiungo alla lista la distanza e la durata verso il nodo finale
        for i, car in enumerate(cars_list):
            dur_list[i].append(self.arc_dict[car[-1]][0].getDur())
            dist_list[i].append(self.arc_dict[car[-1]][0].getDist())
        # per ogni lista all'interno di dist_list sommo tutte le distanze
        dist = sum(map(sum, dist_list))
        self.cars_list = cars_list
        self.dur_list = dur_list
        self.dist = dist
        return (cars_list, dur_list, dist)

    def grasp(self):
        """
        per ogni chiave del dizionario estraggo i nodi e li inserisco in un
        dizionario che contiene solo nodi verso la destinazione
        """
        arcToDest_dict = dict()
        for key in self.arc_dict.keys():
            arcToDest_dict[key] = self.arc_dict[key][0]
        """
        creo una lista di liste dove ogni lista contiene il percorso di una
        macchina
        """
        # imposto a -1 nauto cosi' nel ciclo while la prima volta che aggiungo un
        # valore = 0
        nauto = -1
        cars_list = list()
        dur_list = list()
        dist_list = list()
        find = False
        # finche' ci sono archi verso la destionazione continuo a ciclare
        while len(arcToDest_dict) > 0:
            if not find:
                # ordino il dizionario e prendo l'arco che ha il nodo iniziale
                # piu' distante
                car = sorted(arcToDest_dict.values(),
                        key=attrgetter('dist'),
                        reverse=True)[0].getId_i()
                arcToDest_dict.pop(car)
                dur = 0
                mindur = self.node_dict[car].getDur()
                cars_list.append(list())
                dur_list.append(list())
                dist_list.append(list())
                nauto += 1
                cars_list[nauto].append(car)
            else:
                find = False
            # prendo la lista di archi dal nodo di partenza
            arc_list = self.arc_dict[car]
            # crea lista degli archi papabili
            arc_list_pope = list()
            # ordina la lista di archi in ordine crescente
            for arc in sorted(arc_list, key=attrgetter('dist')):
                if (arc.getId_f() in arcToDest_dict and
                        self.arc_dict[car][0].getDist() >= arc.getDist() and
                        self.checkNotWith(cars_list, nauto, self.node_dict, arc.getId_f()) and
                        self.minDuration(dur, arc.getDur(), mindur)):
                    arc_list_pope.append(arc)
                    # devo fare il break solo quando ne ho trovati tre
                if len(arc_list_pope) > 3:
                    break

            # prendo un elemento a random tra quelli possibili appena estratti
            if len(arc_list_pope) > 0:
                arc_random = random.choice(arc_list_pope)
                car = arc_random.getId_f()
                dur += arc_random.getDur()
                dur_list[nauto].append(arc_random.getDur())
                dist_list[nauto].append(arc_random.getDist())
                if mindur > self.node_dict[car].getDur():
                    mindur = self.node_dict[car].getDur()
                cars_list[nauto].append(car)
                arcToDest_dict.pop(car)
                if len(cars_list[nauto]) < 5:
                    find = True

        # aggiungo alla lista la distanza e la durata verso il nodo finale
        for i, car in enumerate(cars_list):
            dur_list[i].append(self.arc_dict[car[-1]][0].getDur())
            dist_list[i].append(self.arc_dict[car[-1]][0].getDist())
        # per ogni lista all'interno di dist_list sommo tutte le distanze
        dist = sum(map(sum, dist_list))
        self.cars_list = cars_list
        self.dur_list = dur_list
        self.dist = dist
        return (cars_list, dur_list, dist)

    def initTabu(self, localSearch_list, k):
        target = sorted(localSearch_list, key=attrgetter('dist')).pop(0)
        for i in range(k):
            if i == 0:
                (cars_list, dur_list, dist) = self.tabu(target, localSearch_list[i])
            else:
                (cars_list_tmp, dur_list_tmp, dist_tmp) = self.tabu(target, localSearch_list[i])
                if dist_tmp < dist:
                    cars_list = cars_list_tmp
                    dur_list = dur_list_tmp
                    dist = dist_tmp

        self.cars_list = cars_list
        self.dur_list = dur_list
        self.dist = dist
        return (cars_list, dur_list, dist)

    def tabu(self, target, grasp):
        maxRig = max(len(target.cars_list), len(grasp.cars_list))
        maxCol = 5
        found = False
        swap_done = False
        for x in maxRig:
            for y in maxCol:
                if found and grasp.cars_list[x][y] == value_tmp_target:
                    grasp.cars_list[x][y] = value_tmp_grasp
                    swap_done = True
                    break
                if not found and target.cars_list[x][y] != grasp.cars_list[x][y]:
                    found = True
                    value_tmp_grasp = grasp.cars_list[x][y]
                    value_tmp_target = target.cars_list[x][y]
                    grasp.cars_list[x][y] = target.cars_list[x][y]
            if swap_done:
                break

        # riordine delle macchine
        # verifica ammissibilità: notwith, durata
        # calcolo del costo che nel caso non ammissibile è 0
        # aggiunta mossa ad una lista che devo passare già di base (init)
        # teorico check dello stop
