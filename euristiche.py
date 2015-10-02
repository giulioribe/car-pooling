import json
import requests
import collections
import random
from operator import itemgetter, attrgetter


class Euristiche(object):
    """docstring for Euristiche"""
    def __init__(self, node_dict, arc_dict):
        #super(Euristiche, self).__init__()
        self.node_dict = node_dict
        self.arc_dict = arc_dict
        self.cars_list = list()
        self.dur_list = list()
        self.dist = int()

    def setCars(self, cars_list):
        self.cars_list = cars_list

    def setDur(self, dur_list):
        self.dur_list = dur_list

    def setDist(self, dist):
        self.dist = dist

    def getCars(self):
        return self.cars_list

    def getDur(self):
        return self.dur_list

    def getDist(self):
        return self.dist

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
        self.setCars(cars_list)
        self.setDur(dur_list)
        self.setDist(dist)
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
                if len(arc_list_pope) >= 3:
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
        self.setCars(cars_list)
        self.setDur(dur_list)
        self.setDist(dist)
        return (cars_list, dur_list, dist)


    def initTabu(self, localSearch_list, k):
        print "Sono in initTabu"
        target = sorted(localSearch_list, key=attrgetter('dist')).pop(0)
        tabu_list = list()
        for i in range(k):
            #tabu_tmp = self.tabu(target, localSearch_list[i], list(), 0)
            tabu_list.append(self.tabu(target, localSearch_list[i], list(), 0))
            print "initTabu -------------> ", tabu_list[0][0]
        best_tabu = sorted(tabu_list, key=itemgetter(2)).pop(0)
        self.setCars(best_tabu[0])
        self.setDur(best_tabu[1])
        self.setDist(best_tabu[2])
        return best_tabu


    def tabu(self, target, grasp, tabu_list, iteration):
        print "Sono in Tabu"
        print "grasp", grasp.cars_list
        # Creo matrici di supporto
        maxRig = max(len(target.cars_list), len(grasp.cars_list))
        maxCol = 5
        # boolean controllo di aver eseguito correttamente lo swap
        swap_done = False
        while not swap_done:
            print "Sono nel ciclo while Tabu", iteration
            # Ricerca mossa valida e scambio
            # Restore euristiche passate inizialmente nel caso di mosse non ammissibili
            grasp_tmp = grasp
            # boolean controllo di aver trovato una mossa possibile (una differenza)
            found = False
            for x in range(maxRig):
                if x >= len(grasp_tmp.cars_list):
                    grasp_tmp.cars_list.append(list())
                if x >= len(target.cars_list):
                    target.cars_list.append(list())
                for y in range(maxCol):
                    if y >= len(grasp_tmp.cars_list[x]):
                        grasp_tmp.cars_list[x].append(-1)
                    if y >= len(target.cars_list[x]):
                        target.cars_list[x].append(-1)
                    if found and grasp_tmp.cars_list[x][y] == value_tmp_target:
                        grasp_tmp.cars_list[x][y] = value_tmp_grasp
                        swap_done = True
                        break
                    if not found and target.cars_list[x][y] != grasp_tmp.cars_list[x][y]:
                        if not ((grasp_tmp.cars_list[x][y],target.cars_list[x][y]) in tabu_list):
                            found = True
                            value_tmp_grasp = grasp_tmp.cars_list[x][y]
                            value_tmp_target = target.cars_list[x][y]
                            grasp_tmp.cars_list[x][y] = target.cars_list[x][y]

                if swap_done:
                    break
            tmp_c_l = list()
            print "sono stronzo1", grasp_tmp.cars_list
            k = 0
            for trip in grasp_tmp.cars_list:
                if sum(map(int, trip)) > 0:
                    tmp_c_l.append(list())
                    for e in trip:
                        if e > 0:
                            tmp_c_l[k].append(e)
                    k += 1
                    #grasp_tmp.cars_list[k] = tmp_c_l


            grasp_tmp2 = Euristiche(grasp_tmp.node_dict, grasp_tmp.node_dict)
            grasp_tmp2.setCars(tmp_c_l)
            grasp_tmp2.setDur(grasp_tmp.getDur())
            grasp_tmp2.setDist(grasp_tmp.getDist())


            print "sono stronzo2", grasp_tmp2.cars_list
            # riordine delle macchine ricalcolando anche le partenze
            grasp_tmp2 = self.reorder(grasp_tmp2)
            # verifica ammissibilita': notwith, durata
            if not self.ammissibile(grasp_tmp2):
                swap_done = False
            else:
                # aggiunta mossa a tabu_list
                tabu_list.append((value_tmp_target, value_tmp_grasp))
                # esco dal while perche' trovata la mossa che va bene

            # condizione di uscita se non trovo mosse valide
            if x == maxRig and y == maxCol:
                break
            if swap_done or self.controllo_stop(target, grasp_tmp, iteration):
                return (grasp_tmp2.getCars(), grasp_tmp2.getDur(), grasp_tmp2.getDist())
            else:
                iteration += 1
                return self.tabu(target, grasp_tmp2, tabu_list, iteration)


    def reorder(self, eur):
        # prendo ogni macchina e devo riordinarla
        lista_macchine = list()
        print "dentro reorder", eur.cars_list
        for car in eur.cars_list:
            car_tmp_list = list()
            for id in car:
                car_tmp_list.append((id, self.arc_dict[id][0].getDist()))
            # riordiniamo dal piu' distante al piu' vicinio
            car_tmp_list = sorted(car_tmp_list, key=itemgetter(1), reverse=True)
            lista_macchine.append([x for x,_ in car_tmp_list])
            # devo ricalcolare anche le partenze
        lista_durate = list()
        lista_dist = list()
        for z, car in enumerate(lista_macchine):
            lista_dist.append(list())
            lista_durate.append(list())
            for i in range(len(car)):
                if i != len(car)-1:
                    for y in range(len(self.arc_dict[car[i]])):
                        if self.arc_dict[car[i]][y].getId_f() == car[i+1]:
                            lista_durate[z].append(self.arc_dict[car[i]][y].getDur())
                            lista_dist[z].append(self.arc_dict[car[i]][y].getDist())
                            break
                else:
                    lista_durate[z].append(self.arc_dict[car[i]][0].getDur())
                    lista_dist[z].append(self.arc_dict[car[i]][0].getDist())

        eur.cars_list = lista_macchine
        eur.dur_list = lista_durate
        # calcolo del costo
        eur.dist = sum(map(sum, lista_dist))
        return eur


    def ammissibile(self, eur):
        # controllo notWith, max_dur
        # teoricamente avendo gia' riordinato non dovremmo aver problemi di archi orientati sbagliati
        for car in eur.cars_list:
            dur = 0
            mindur = self.node_dict[car[0]].getDur()
            for i in range(len(car)):
                if mindur > self.node_dict[car[i]].getDur():
                    mindur = self.node_dict[car[i]].getDur()
                if i != len(car)-1:
                    for y in range(len(self.arc_dict[car[i]])):
                        if self.arc_dict[car[i]][y].getId_f() == car[i+1]:
                            if not (self.checkNotWith(eur.cars_list, eur.cars_list.index(car), self.node_dict, car[i+1]) and
                                        self.minDuration(dur, self.arc_dict[car[i]][y].getDur(), mindur)):
                                return False
                            dur += self.arc_dict[car[i]][y].getDur()
                            break
                else:
                    if not (self.checkNotWith(eur.cars_list, eur.cars_list.index(car), self.node_dict, '0') and
                                self.minDuration(dur, self.arc_dict[car[i]][0].getDur(), mindur)):
                        return False
                    dur += self.arc_dict[car[i]][0].getDur()
        return True

    def controllo_stop(self, target, grasp, iteration):
        # se la grasp e' diventata identica alla target
        # se ho gia' fatto #nodi / 2 iterazioni mi fermo
        # anche perche' in teoria non dovremmo arrivare esattamente alla
        # target ma ad una euristica simile
        if (target.cars_list == grasp.cars_list or
                (iteration > (len(self.node_dict) / 2))):
            return True
        else:
            return False
