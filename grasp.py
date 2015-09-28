
def grasp(node_dict, arc_dict):
    """
    per ogni chiave del dizionario estraggo i nodi e li inserisco in un
    dizionario che contiene solo nodi verso la destinazione
    """
    arcToDest_dict = dict()
    for key in arc_dict.keys():
        arcToDest_dict[key] = arc_dict[key][0]
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
            mindur = node_dict[car].getDur()
            cars_list.append(list())
            dur_list.append(list())
            dist_list.append(list())
            nauto += 1
            cars_list[nauto].append(car)
        else:
            find = False
        # prendo la lista di archi dal nodo di partenza
        arc_list = arc_dict[car]
        # crea lista degli archi papabili
        arc_list_pope = list()
        # ordina la lista di archi in ordine crescente
        for arc in sorted(arc_list, key=attrgetter('dist')):
            if (arc.getId_f() in arcToDest_dict and
                    arc_dict[car][0].getDist() >= arc.getDist() and
                    checkNotWith(cars_list, nauto, node_dict, arc.getId_f()) and
                    minDuration(dur, arc.getDur(), mindur)):
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
            if mindur > node_dict[car].getDur():
                mindur = node_dict[car].getDur()
            cars_list[nauto].append(car)
            arcToDest_dict.pop(car)
            if len(cars_list[nauto]) < 5:
                find = True

    # aggiungo alla lista la distanza e la durata verso il nodo finale
    for i, car in enumerate(cars_list):
        dur_list[i].append(arc_dict[car[-1]][0].getDur())
        dist_list[i].append(arc_dict[car[-1]][0].getDist())
    # per ogni lista all'interno di dist_list sommo tutte le distanze
    dist = sum(map(sum, dist_list))
    return (cars_list, dur_list, dist)