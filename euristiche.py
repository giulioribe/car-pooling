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
                (cars_list, dur_list, dist) = self.tabu(target, localSearch_list[i], list(), 0)
            else:
                (cars_list_tmp, dur_list_tmp, dist_tmp) = self.tabu(target, localSearch_list[i], list(), 0)
                if dist_tmp < dist:
                    cars_list = cars_list_tmp
                    dur_list = dur_list_tmp
                    dist = dist_tmp

        self.cars_list = cars_list
        self.dur_list = dur_list
        self.dist = dist
        return (cars_list, dur_list, dist)

    def tabu(self, target, grasp, tabu_list, iteration):
    	# Creo matrici di supporto
        maxRig = max(len(target.cars_list), len(grasp.cars_list))
        maxCol = 5
        # boolean controllo di aver eseguito correttamente lo swap
        swap_done = False
    	while not swap_done:
	        # Ricerca mossa valida e scambio
	        # Restore euristiche passate inizialmente nel caso di mosse non ammissibili
	        target_tmp = target
	        grasp_tmp = grasp
	        # boolean controllo di aver trovato una mossa possibile (una differenza)
	        found = False
	        for x in maxRig:
	            for y in maxCol:
	                if found and grasp_tmp.cars_list[x][y] == value_tmp_target:
	                    grasp_tmp.cars_list[x][y] = value_tmp_grasp
	                    swap_done = True
	                    break
	                if not found and target_tmp.cars_list[x][y] != grasp_tmp.cars_list[x][y]:
	                	if not ((grasp_tmp.cars_list[x][y],target_tmp.cars_list[x][y]) in tabu_list):
		                    found = True
		                    value_tmp_grasp = grasp_tmp.cars_list[x][y]
		                    value_tmp_target = target_tmp.cars_list[x][y]
		                    grasp_tmp.cars_list[x][y] = target_tmp.cars_list[x][y]
	            if swap_done:
	                break

	        # riordine delle macchine ricalcolando anche le partenze
	        grasp_tmp = self.reorder(grasp_tmp)
	        # verifica ammissibilità: notwith, durata
	        if not self.ammissibile(grasp_tmp):
	        	swap_done = False
	        else:
		        # aggiunta mossa a tabu_list
		        tabu_list.append((value_tmp_target, value_tmp_grasp))
		        # esco dal while perchè trovata la mossa che va bene

	        # condizione di uscita se non trovo mosse valide
	        if x == maxRig and y == maxCol
	        	break

        if swap_done and self.controllo_stop(target_tmp, grasp_tmp, iteration):
        	return (grasp_tmp.cars_list, grasp_tmp.dur_list, grasp_tmp.dist)
        else
    		return self.tabu(target_tmp, grasp_tmp, tabu_list, iteration += 1)



    def reorder(self, eur):
        # prendo ogni macchina e devo riordinarla
        lista_durate = eur.dur_list
        lista_macchine = eur.cars_list

        for car in eur.cars_list:
        	car_tmp_list = list()
        	for id in car:
        		car_tmp_list.append((id, self.arc_dict[id][0].getDist()))
       		sorted(car_tmp_list, key=itemgetter(1), reverse=True)
       		lista_macchine.append([x for x,_ in car_tmp_list])
       		# devo ricalcolare anche le partenze
       		dur_tmp_list = list()
       		for i in range(len(car)):
       			if i != len(car):
       				dur_tmp_list.append(arc_dict[car[i]][car[i+1]].getDist())
       			else:
       				dur_tmp_list.append(arc_dict[car[i]][0].getDist())
       		lista_durate.append(dur_tmp_list)

       	eur.cars_list = lista_macchine
       	eur.dur_list = lista_durate
        # calcolo del costo
        eur = self.update_cost(eur)
        return eur


    def update_cost(self, eur):
    	# ricalcolo del costo dell'euristica e update del valore
        eur.dist = sum(map(sum, eur.dist_list))
        return eur


    def ammissibile(self, eur):
        # controllo notWith, max_dur
        # teoricamente avendo già riordinato non dovremmo aver problemi di archi orientati sbagliati
        for car in eur.cars_list:
        	for id in car:
	        	if not (self.checkNotWith(eur.cars_list, eur.cars_list.index(car), self.node_dict, id) and
	                        self.minDuration(dur, self.arc_dict[][].getDur(), mindur)):
	        		return False
        return True

    def controllo_stop(self, target, grasp, iteration):
    	# se la grasp è diventata identica alla target
    	# se ho già fatto #nodi / 2 iterazioni mi fermo
    	# anche perchè in teoria non dovremmo arrivare esattamente alla target ma ad una euristica simile
        if target.cars_list == grasp.cars_list or (iteration > (len(node_dict) / 2)):
        	return True
        else:
        	return False