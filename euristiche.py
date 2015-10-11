import json
import requests
import collections
import random
import copy
from operator import itemgetter, attrgetter


class Euristiche(object):
    """docstring for Euristiche"""
    def __init__(self, node_dict, arc_dict, cars_list=None, dur_list=None, dist=None):
        #super(Euristiche, self).__init__()
        self.node_dict = node_dict
        self.arc_dict = arc_dict
        if cars_list:
            self.cars_list = cars_list
        else:
            self.cars_list = list()
        if dur_list:
            self.dur_list = dur_list
        else:
            self.dur_list = list()
        if dist:
            self.dist = dist
        else:
            self.dist = list()

    def setCars(self, cars_list):
        self.cars_list = cars_list

    def setDur(self, dur_list):
        self.dur_list = dur_list

    def setDist(self, dist):
        self.dist = dist

    def getNode(self):
        return self.node_dict

    def getArc(self):
        return self.arc_dict

    def getCars(self):
        return self.cars_list

    def getDur(self):
        return self.dur_list

    def getDist(self):
        return self.dist


    def checkNotWith(self, cars_list, nauto, newper):
        for car in cars_list[nauto]:
            if (newper in self.node_dict[car].getNotWith() or
                    car in self.node_dict[newper].getNotWith()):
                return False
        return True


    # minduration(car, arc_dict[car[-1]]['0'])
    def minDuration(self, car, dur):
        # scorro ogni elemento
        for i in range(len(car)):
            sumdur = 0
            # per ogni elemento riparto da se stesso e scorro la lista dei passeggeri
            for k in range(i,len(car)):
                # se non sono in fondo allora sommo il costo del passaggio da una persona all'altra
                if k != len(car)-1:
                    sumdur += self.arc_dict[car[k]][car[k+1]].getDur() # e' getDur per avere la durata dell'arco?
                if self.node_dict[car[i]].getDur() != 0:
                    # se sono in fondo, e in ogni caso ad ogni iterazione, controllo l'ammissibilia'
                    if (sumdur + dur) > self.node_dict[car[i]].getDur():
                        return False
        return True


    def minDurationGreedy(self, car, nodeNew):
        # scorro ogni elemento
        for i in range(len(car)):
            sumdur = 0
            # per ogni elemento riparto da se stesso e scorro la lista dei passeggeri
            for k in range(i,len(car)):
                # se non sono in fondo allora sommo il costo del passaggio da una persona all'altra
                if k != len(car)-1:
                    sumdur += self.arc_dict[car[k]][car[k+1]].getDur() # e' getDur per avere la durata dell'arco?
                # se sono in fondo, e in ogni caso ad ogni iterazione, controllo l'ammissibilia'
                else:
                    sumdur += self.arc_dict[car[k]][nodeNew.getId()].getDur() + self.arc_dict[nodeNew.getId()]['0'].getDur()
                if self.node_dict[car[i]].getDur() != 0:
                    if sumdur > self.node_dict[car[i]].getDur():
                        return False
        return True


    def greedy(self):
        """
        per ogni chiave del dizionario estraggo i nodi e li inserisco in un
        dizionario che contiene solo nodi verso la destinazione
        """
        arcToDest_dict = dict()
        for key in self.arc_dict.keys():
            arcToDest_dict[key] = self.arc_dict[key]['0']
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
            arc_start = self.arc_dict[car]
            #arc_list = list()
            #for key in arc_start.keys():
            #    arc_list.append(arc_start[key])
            #for a in arc_list:
            #    print a.getId_i(), a.getId_f(), a.getDist()
            #print "------------------"
            #for a in sorted(arc_list, key=attrgetter('dist')):
            #    print a.getId_i(), a.getId_f(), a.getDist()
            #print "------------------"
            # ordina la lista di archi in ordine crescente
            #for arc in sorted(arc_list, key=attrgetter('dist')):
            for arc in sorted(arc_start.values(), key=attrgetter('dist')):

                """
                if self.arc_dict[car]['0'].getDist() >= arc.getDist():
                    print "0"
                if self.checkNotWith(cars_list, nauto, arc.getId_f()):
                    print '1'
                if self.minDuration(cars_list[nauto], arc.getDur()):
                    print '2'
                """

                if (arc.getId_f() in arcToDest_dict and
                        self.arc_dict[car]['0'].getDist() >= arc.getDist() and
                        self.checkNotWith(cars_list, nauto, arc.getId_f()) and
                        self.minDurationGreedy(cars_list[nauto], self.node_dict[arc.getId_f()])):
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
            dur_list[i].append(self.arc_dict[car[-1]]['0'].getDur())
            dist_list[i].append(self.arc_dict[car[-1]]['0'].getDist())
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
            arcToDest_dict[key] = self.arc_dict[key]['0']
        """
        creo una lista di liste dove ogni lista contiene il percorso di una
        macchina
        """
        nIteration = 3
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
                car_pope = list()
                ordered_arc = sorted(arcToDest_dict.values(),
                        key=attrgetter('dist'),
                        reverse=True)
                for e in range(nIteration):
                    if e <= (len(ordered_arc)-1):
                        car_pope.append(ordered_arc.pop(e))
                car = (random.choice(car_pope)).getId_i()
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
            #arc_list = self.arc_dict[car]
            arc_start = self.arc_dict[car]
            # crea lista degli archi papabili
            #arc_list_pope = list()
            arc_list_pope = list()
            # ordina la lista di archi in ordine crescente
            for arc in sorted(arc_start.values(), key=attrgetter('dist')):
                if (arc.getId_f() in arcToDest_dict and
                        self.arc_dict[car]['0'].getDist() >= arc.getDist() and
                        self.checkNotWith(cars_list, nauto, arc.getId_f()) and
                        self.minDurationGreedy(cars_list[nauto], self.node_dict[arc.getId_f()])):
                    arc_list_pope.append(arc)
                # devo fare il break solo quando ne ho trovati tre
                if len(arc_list_pope) >= nIteration:
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
            dur_list[i].append(self.arc_dict[car[-1]]['0'].getDur())
            dist_list[i].append(self.arc_dict[car[-1]]['0'].getDist())
        # per ogni lista all'interno di dist_list sommo tutte le distanze
        dist = sum(map(sum, dist_list))
        self.setCars(cars_list)
        self.setDur(dur_list)
        self.setDist(dist)
        return (cars_list, dur_list, dist)


    def initPath(self, localSearch_list, k):
        sorted_ls = sorted(localSearch_list, key=attrgetter('dist'))
        target = sorted_ls.pop(0)
        path_list = list()
        path_list_reverse = list()
        if k > len(sorted_ls):
            k = len(sorted_ls)
        for i in range(k):
            path_list.append(self.path(target, sorted_ls[i], 0))
            print "Sono nel ciclo for, iteration", i
            path_list_reverse.append(self.path(sorted_ls[i], target, 0))
        best_path = sorted(path_list, key=itemgetter(2)).pop(0)
        self.setCars(best_path[0])
        self.setDur(best_path[1])
        self.setDist(best_path[2])

        best_path_revers = sorted(path_list, key=itemgetter(2)).pop(0)
        self.setCars(best_path_revers[0])
        self.setDur(best_path_revers[1])
        self.setDist(best_path_revers[2])
        return (best_path, best_path_revers)


    def path(self, target, grasp, iteration):
        # Creo matrici di supporto
        maxRig = max(len(target.cars_list), len(grasp.cars_list))
        maxCol = 5
        path_list = list()
        # boolean controllo di aver eseguito correttamente lo swap
        swap_done = False
        grasp_tmp_pope = list()
        done_all = False
        while not done_all:
            while not swap_done:
                # Ricerca mossa valida e scambio
                # Restore euristiche passate inizialmente nel caso di mosse non ammissibili
                grasp_tmp_pope.append(copy.deepcopy(grasp))
                # boolean controllo di aver trovato una mossa possibile (una differenza)
                found = False
                for x in range(maxRig):
                    if x >= len(grasp_tmp_pope[-1].cars_list):
                        grasp_tmp_pope[-1].cars_list.append(list())
                    if x >= len(target.cars_list):
                        target.cars_list.append(list())
                    for y in range(maxCol):
                        if y >= len(grasp_tmp_pope[-1].cars_list[x]):
                            grasp_tmp_pope[-1].cars_list[x].append(-1)
                        if y >= len(target.cars_list[x]):
                            target.cars_list[x].append(-1)
                        if found and grasp_tmp_pope[-1].cars_list[x][y] == value_tmp_target:
                            grasp_tmp_pope[-1].cars_list[x][y] = value_tmp_grasp
                            swap_done = True
                            break
                        if not found and target.cars_list[x][y] != grasp_tmp_pope[-1].cars_list[x][y]:
                            if not ((grasp_tmp_pope[-1].cars_list[x][y],target.cars_list[x][y]) in path_list):
                                found = True
                                value_tmp_grasp = grasp_tmp_pope[-1].cars_list[x][y]
                                value_tmp_target = target.cars_list[x][y]
                                grasp_tmp_pope[-1].cars_list[x][y] = target.cars_list[x][y]
                        # esco dal while perche' trovata la mossa che va bene
                        # condizione di uscita se non trovo mosse valide
                        if x == maxRig and y == maxCol:
                            done_all = True
                            break
                    if swap_done or done_all:
                        break

                if done_all:
                    break
                tmp_c_l = list()
                k = 0
                #print "prima trip", grasp_tmp_pope[-1].cars_list
                for trip in grasp_tmp_pope[-1].cars_list:
                    if trip.count(-1) != len(trip):
                        tmp_c_l.append(list())
                        for e in trip:
                            if e > 0:
                                tmp_c_l[k].append(e)
                        k += 1
                #print "dopo  trip", tmp_c_l
                grasp_tmp_pope[-1].setCars(tmp_c_l)
                # riordine delle macchine ricalcolando anche le partenze
                grasp_tmp_pope[-1] = copy.deepcopy(self.reorder(grasp_tmp_pope[-1]))

                # verifica ammissibilita': notwith, durata
                if not self.ammissibile(grasp_tmp_pope[-1]):
                    swap_done = False
                elif found:
                    # aggiunta mossa a path_list
                    path_list.append((value_tmp_target, value_tmp_grasp))

        grasp_tmp_pope.pop(-1)
        grasp_tmp_pope_ordered = sorted(grasp_tmp_pope, key=attrgetter('dist'),
            reverse=True)
        grasp_ok = grasp_tmp_pope_ordered.pop(0)

        if done_all or self.controllo_stop(target, grasp_ok, iteration):
            return (grasp_ok.getCars(), grasp_ok.getDur(), grasp_ok.getDist())
        else:
            iteration += 1
            return self.tabu(target, grasp_ok, iteration)


    def tabu(self, best_solution, actual_solution, iteration, global_iteration, tabu_list, penality):
        global_iteration += 1
        # list di scambi tabu
        solutions_list = list()
        cars = actual_solution.getCars()
        actual_dist = actual_solution.getDist()
        # swapCar
        for x in range(len(cars)):
            for y in range(len(cars[x])):
                if x != len(cars):
                    for x1 in range(x+1, len(cars)):
                        for y1 in range(len(cars[x1])):
                            totDist = 0
                            if not self.ammissibileNotWith(actual_solution):
                                totDist -= penality
                                #print "-1"
                            if not self.ammissibileMinDur(actual_solution):
                                totDist -= penality
                                #print "-2"
                            totDist -= self.ammissibileCard(actual_solution)*penality
                            cars_tmp_list = copy.deepcopy(cars)

                            #print cars_tmp_list

                            value_tmp = cars_tmp_list[x1][y1]
                            cars_tmp_list[x1][y1] = cars_tmp_list[x][y]
                            cars_tmp_list[x][y] = value_tmp

                            eur = Euristiche(self.node_dict, self.arc_dict)
                            eur.setCars(cars_tmp_list)
                            eur = self.reorder(eur)
                            if not self.ammissibileNotWith(eur):
                                totDist += penality
                            if not self.ammissibileMinDur(eur):
                                totDist += penality
                            totDist += self.ammissibileCard(eur)*penality

                            # il reorder va effettuato prima perche' altrimenti
                            # ho problemi nei vari calcoli dell'ammissibilita'
                            #eur = self.reorder(eur)
                            eur.setDist(eur.getDist() + totDist)
                            mossa = (cars_tmp_list[x1][y1], cars_tmp_list[x][y], True)
                            delta = eur.getDist() - actual_dist
                            solutions_list.append((eur, mossa, delta))

        # Stack
        for x in range(len(cars)):
            for y in range(len(cars[x])):
                for x1 in range(x, len(cars)):
                    if x != x1:
                        totDist = 0
                        if not self.ammissibileNotWith(actual_solution):
                            totDist -= penality
                        if not self.ammissibileMinDur(actual_solution):
                            totDist -= penality
                        totDist -= self.ammissibileCard(actual_solution)*penality
                        cars_tmp_list = copy.deepcopy(cars)
                        car_tmp = cars_tmp_list[x].pop(y)
                        cars_tmp_list[x1].append(car_tmp)
                        if len(cars_tmp_list[x]) == 0:
                            cars_tmp_list.pop(x)
                        eur = Euristiche(self.node_dict, self.arc_dict)
                        eur.setCars(cars_tmp_list)
                        eur = self.reorder(eur)
                        if not self.ammissibileNotWith(eur):
                            totDist += penality
                        if not self.ammissibileMinDur(eur):
                            totDist += penality
                        totDist += self.ammissibileCard(eur)*penality

                        # il reorder va sempre effettuato prima
                        #eur = self.reorder(eur)
                        eur.setDist(eur.getDist() + totDist)
                        mossa = (cars[x][y], x, False)
                        delta = eur.getDist() - actual_dist
                        solutions_list.append((eur, mossa, delta))

                # New car
                cars_tmp_list = copy.deepcopy(cars)
                if len(cars_tmp_list[x]) > 1:
                    totDist = 0
                    if not self.ammissibileNotWith(actual_solution):
                        totDist -= penality
                    if not self.ammissibileMinDur(actual_solution):
                        totDist -= penality
                    totDist -= self.ammissibileCard(actual_solution)*penality
                    car_tmp = cars_tmp_list[x].pop(y)
                    cars_tmp_list.append(list())
                    cars_tmp_list[-1].append(car_tmp)
                    eur = Euristiche(self.node_dict, self.arc_dict)
                    eur.setCars(cars_tmp_list)
                    if not self.ammissibileNotWith(eur):
                        totDist += penality
                    if not self.ammissibileMinDur(eur):
                        totDist += penality
                    totDist += self.ammissibileCard(eur)*penality
                    eur = self.reorder(eur)
                    eur.setDist(eur.getDist() + totDist)
                    mossa = (cars[x][y], x, False)
                    delta = eur.getDist() - actual_dist
                    solutions_list.append((eur, mossa, delta))


        solutions_list = sorted(solutions_list, key=itemgetter(2))
        if len(tabu_list) > 0:
            if solutions_list[0][1] == tabu_list[-1]:
                solutions_list.pop(0)
        best_delta_solution = copy.deepcopy(solutions_list[0][0])
        # Criterio di aspirazione
        if solutions_list[0][1] in tabu_list:
            tabu_list.pop(solutions_list[0][1])
            tabu_list.append(solutions_list[0][1])
        if best_delta_solution.getDist() < best_solution.getDist():
            best_solution = best_delta_solution
            iteration = 0
        else:
            iteration += 1
        """
        print "\n"
        print "iteration", iteration
        for i, sol in enumerate(solutions_list):
            print i, "\t", sol[0].getCars(), "\t\t", sol[2]
        """
        if iteration >= 30 or global_iteration >= 50:
            #print "iteration", iteration
            return (best_delta_solution.getCars(), best_delta_solution.getDur(), best_delta_solution.getDist())
        else:
            return self.tabu(best_solution, best_delta_solution, iteration, global_iteration, tabu_list, penality)


    def reorder(self, eur):
        # prendo ogni macchina e devo riordinarla
        lista_macchine = list()
        for z, car in enumerate(eur.cars_list):
            lista_macchine.append(list())
            car_tmp_list = list()
            for id in car:
                car_tmp_list.append((id, self.arc_dict[id]['0'].getDist()))
            # riordiniamo dal piu' distante al piu' vicinio e ne prendo l'id
            car_tmp_list = sorted(car_tmp_list, key=itemgetter(1), reverse=True)
            choose_first = car_tmp_list.pop(0)[0]
            car_tmp_next = list()
            for id in [i[0] for i in car_tmp_list]:
                car_tmp_next.append((id, self.arc_dict[choose_first][id].getDist()))
            choose_next = sorted(car_tmp_next, key=itemgetter(1))
            lista_macchine[z].append(choose_first)
            for x,_ in car_tmp_list:
                lista_macchine[z].append(x)
        # devo ricalcolare anche le partenze
        lista_durate = list()
        lista_dist = list()
        for z, car in enumerate(lista_macchine):
            lista_dist.append(list())
            lista_durate.append(list())
            for i in range(len(car)):
                if i != len(car)-1:
                    lista_durate[z].append(self.arc_dict[car[i]][car[i+1]].getDur())
                    lista_dist[z].append(self.arc_dict[car[i]][car[i+1]].getDist())
                else:
                    lista_durate[z].append(self.arc_dict[car[i]]['0'].getDur())
                    lista_dist[z].append(self.arc_dict[car[i]]['0'].getDist())

        eur.setCars(lista_macchine)
        eur.setDur(lista_durate)
        # calcolo del costo
        eur.setDist(sum(map(sum, lista_dist)))
        return eur


    def ammissibile(self, eur):
        # controllo notWith, max_dur
        # teoricamente avendo gia' riordinato non dovremmo aver problemi di archi orientati sbagliati
        for car in eur.cars_list:
            for i in range(len(car)):
                if i != len(car)-1:
                    if not (self.checkNotWith(eur.cars_list, eur.cars_list.index(car), car[i+1]) and
                            self.minDuration(car, self.arc_dict[car[i]][car[i+1]].getDur())):
                        return False
                else:
                    if not (self.checkNotWith(eur.cars_list, eur.cars_list.index(car), '0') and
                            self.minDuration(car, self.arc_dict[car[i]]['0'].getDur())):
                        return False
        return True


    def ammissibileNotWith(self, eur):
        #print "self.node_dict", self.node_dict.keys()
        #print "eur.cars_list", eur.cars_list
        for car in eur.cars_list:
            for user in car:
                if not self.checkNotWith(eur.cars_list, eur.cars_list.index(car), user):
                    return False
        return True


    """
    def ammissibileMinDur(self, eur):
        # controllo notWith, max_dur
        # teoricamente avendo gia' riordinato non dovremmo aver problemi di archi orientati sbagliati
        for car in eur.cars_list:
            dur = 0
            mindur = 0
            for i in range(len(car)):
                if mindur == 0 and self.node_dict[car[i]].getDur() > 0:
                    mindur = self.node_dict[car[i]].getDur()
                if  mindur > 0 and self.node_dict[car[i]].getDur() > 0:
                    mindur = min(mindur, self.node_dict[car[i]].getDur())
                if i != len(car)-1:
                    if not self.minDuration(dur, self.arc_dict[car[i]][car[i+1]].getDur(), mindur):
                        return False
                    dur += self.arc_dict[car[i]][car[i+1]].getDur()
                else:
                    if not self.minDuration(dur, self.arc_dict[car[i]]['0'].getDur(), mindur):
                        return False
                    dur += self.arc_dict[car[i]]['0'].getDur()
        return True
    """
    def ammissibileMinDur(self, eur):
        for car in eur.cars_list:
            if not self.minDuration(car, self.arc_dict[car[-1]]['0'].getDur()):
                print "Auto stronza", car
                return False
        return True


    def ammissibileCard(self, eur):
        maxPapaia = 0
        for car in eur.cars_list:
            n = len(car)
            if n > 5:
                maxPapaia += (n - 5)
        return maxPapaia


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
