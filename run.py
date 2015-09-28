import json
import requests
import collections
import random
from operator import attrgetter
from node import Node
from arc import Arc
from weppy import App, request
from weppy.tools import service

app = App(__name__)
key = 'AIzaSyB27xz94JVRPsuX4qJMMiZpGVoQiQITFb8'


def createNode(dati_dict):
    node_dict = collections.OrderedDict()
    # la destionazione ha sempre id=0
    node_dict['0'] = (Node(
        ### TODO: id controllare se il JSON restituisce  int o str
        id='0',
        dur=dati_dict['time_to_arrive'],
        addr=dati_dict['place_to_arrive'])
    )

    #for i, user in enumerate(dati_dict['users']):
    for user in dati_dict['users']:
        node_dict[user['id']] = Node(
            ### TODO: id controllare se il JSON restituisce  int o str
            id=user['id'],
            dur=user['max_duration'],
            addr=user['address'],
            notWith=user['not_with'])
    return node_dict

def createArc(google_dict, node_dict):
    arc_dict = collections.OrderedDict()
    #arc_dict = dict()
    '''
    posso usare questo metodo per inserire i nodi perche' la lista dei
    sorgenti e di destinazione di Google Maps sono nello stesso ordine ma
    traslati di uno perche nella prima posizione della lista dei nodi di
    destinazione c'e' la destionazione di tutti i nodi
    '''
    #for i in range(len(google_dict['origin_addresses'])):
    for i, key in enumerate(node_dict.keys()):
        if key != '0':
            arc_dict[key] = list()
            arc_dict[key].append(Arc(
                ### TODO: id controllare se il JSON restituisce  int o str
                id_i=key,
                # id_f=0 perche' il nodo di destionazione e' 0
                id_f='0',
                # -1 perche' gli indirizzi non hanno il nodo destinazione in
                # prima posizione
                # prendo il nodo in posizione 0 (destinazione uguale per tutti)
                # perche' recupero tutti i valori verso la destinazione
                dur=int(google_dict['rows'][i-1]['elements'][0]['duration']['value']*1000),
                dist=google_dict['rows'][i-1]['elements'][0]['distance']['value'])
            )
    keys_list = node_dict.keys()
    for i in range(len(google_dict['origin_addresses'])):
        # il ciclo parte da 1 perche' nella prima posizione c'e' la
        # destinazione di tutti
        for y in range(1, len(google_dict['destination_addresses'])):
            dur = google_dict['rows'][i]['elements'][y]['duration']['value']
            dist = google_dict['rows'][i]['elements'][y]['distance']['value']
            if dur > 0 and dist > 0:
                if (arc_dict[keys_list[i+1]][0].getDur() >
                        arc_dict[keys_list[y]][0].getDur()):
                    arc_dict[keys_list[i+1]].append(Arc(
                        ### TODO: id controllare se il JSON restituisce  int o str
                        id_i=keys_list[i+1],
                        # id_f=0 perche' il nodo di destionazione e' 0
                        id_f=keys_list[y],
                        # prendo il nodo in posizione 0 (destinazione uguale
                        # per tutti) perche' recupero tutti i valori verso
                        # la destinazione
                        dur=int(dur*1000),
                        dist=dist)
                    )
    return arc_dict

def checkNotWith(cars_list, nauto, node_dict, newper):
    for car in cars_list[nauto]:
        if (newper in node_dict[car].getNotWith() or
                car in node_dict[newper].getNotWith()):
            return False
    return True

def minDuration(dur, newdur, mindur):
    if newdur == 0 or dur == 0:
        return True
    elif (dur+newdur) > mindur:
        return False
    return True

def updateAddress(node_dict, google_dict):
    for i, key in enumerate(node_dict):
        node_dict[key].setAddr(google_dict['destination_addresses'][i])

def greedy(node_dict, arc_dict):
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
        # ordina la lista di archi in ordine crescente
        for arc in sorted(arc_list, key=attrgetter('dist')):
            if (arc.getId_f() in arcToDest_dict and
                    arc_dict[car][0].getDist() >= arc.getDist() and
                    checkNotWith(cars_list, nauto, node_dict, arc.getId_f()) and
                    minDuration(dur, arc.getDur(), mindur)):
                car = arc.getId_f()
                dur += arc.getDur()
                dur_list[nauto].append(arc.getDur())
                dist_list[nauto].append(arc.getDist())
                if mindur > node_dict[car].getDur():
                    mindur = node_dict[car].getDur()
                cars_list[nauto].append(car)
                arcToDest_dict.pop(car)
                if len(cars_list[nauto]) < 5:
                    find = True
                break
    # aggiungo alla lista la distanza e la durata verso il nodo finale
    for i, car in enumerate(cars_list):
        dur_list[i].append(arc_dict[car[-1]][0].getDur())
        dist_list[i].append(arc_dict[car[-1]][0].getDist())
    # per ogni lista all'interno di dist_list sommo tutte le distanze
    dist = sum(map(sum, dist_list))
    return (cars_list, dur_list, dist)

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

def initDataOuttput():
    dataOut = dict()
    dataOut['euristiche'] = dict()
    dataOut['euristiche']['name'] = ''
    dataOut['euristiche']['results'] = dict()
    return dataOut

def updateDataOutput(dataOut, eur_type, cars_list, dur_list, dist, timeEnd):
    if dataOut['euristiche']['name']:
        dataOut['euristiche']['name'] += ','
    dataOut['euristiche']['name'] += eur_type
    dataOut['euristiche']['results'][eur_type] = dict()
    dataOut['euristiche']['results'][eur_type]['cars'] = list()
    for i, (cars, dur) in enumerate(zip(cars_list, dur_list)):
        tmpEnd = timeEnd
        dataOut['euristiche']['results'][eur_type]['cars'].append(dict())
        dataOut['euristiche']['results'][eur_type]['cars'][i]['id'] = ','.join(cars)
        dataOut['euristiche']['results'][eur_type]['cars'][i]['partenze'] = ''
        for d in reversed(dur):
            tmpEnd = tmpEnd - d
            if not dataOut['euristiche']['results'][eur_type]['cars'][i]['partenze']:
                dataOut['euristiche']['results'][eur_type]['cars'][i]['partenze'] = str(tmpEnd)
            else:
                dataOut['euristiche']['results'][eur_type]['cars'][i]['partenze'] = (str(tmpEnd) +
                ',' + dataOut['euristiche']['results'][eur_type]['cars'][i]['partenze'])
    dataOut['euristiche']['results'][eur_type]['costo'] = str(dist)

def googleMapsRequest(node_dict):
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    params = dict(
        origins='',
        destinations='',
        mode='driving',#transit
        language='it-IT',
        units='metric',
        key='AIzaSyB27xz94JVRPsuX4qJMMiZpGVoQiQITFb8'
    )
    params['destinations'] = node_dict['0'].getAddr() + "|"
    for key in node_dict:
        if key != '0':
            params['origins'] += node_dict[key].getAddr() + "|"
            params['destinations'] += node_dict[key].getAddr() + "|"
    params['origins'] = params['origins'][:-1]
    params['destinations'] = params['destinations'][:-1]
    resp = requests.get(url=url, params=params)
    google_dict = json.loads(resp.text)
    with open('googleMaps.json', 'w') as outfile:
        json.dump(google_dict, outfile, indent=4)
    return google_dict

def printNode(node_dict):
    for node in node_dict:
        print (node_dict[node].getId(),
            node_dict[node].getDur(),
            node_dict[node].getAddr(),
            node_dict[node].getNotWith())

def printArc(arc_dict):
    for arc in arc_dict:
        for a in arc_dict[arc]:
            print (a.getId_i(),
                a.getId_f(),
                a.getDur(),
                a.getDist())

@app.expose("/")
@service.json
def home():
    #with open('dati.json', 'r') as data_file:
    #    dati_dict = json.load(data_file)
    #node_dict = createNode(dati_dict)
    with open('dati2.json', 'w') as outfile:
        json.dump(request.vars, outfile, indent=4)
    node_dict = createNode(request.vars)

    printNode(node_dict)

    google_dict = googleMapsRequest(node_dict)
    arc_dict = createArc(google_dict, node_dict)

    print "----------------------------"
    printArc((arc_dict))
    print "----------------------------"

    (cars_list, dur_list, dist) = greedy(node_dict, arc_dict)
    print "-->Greedy"
    print "cars_list:",cars_list
    print "dur_list:", dur_list
    print "dist:", dist

    dataOut = initDataOuttput()
    updateDataOutput(dataOut, 'greedy', cars_list, dur_list, dist, node_dict['0'].getDur())

    (cars_list, dur_list, dist) = grasp(node_dict, arc_dict)
    print "-->Grasp"
    print "cars_list:",cars_list
    print "dur_list:", dur_list
    print "dist:", dist
    updateDataOutput(dataOut, 'grasp', cars_list, dur_list, dist, node_dict['0'].getDur())
    #return dict(status="OK", data="Sono tanto stupido")
    return dataOut


@app.expose("/test")
@service.json
def test():
    print '############'
    print request.vars
    for r in request.vars:
        print r, ":", request.vars[r]
    print '############'

    with open('dati.json', 'r') as data_file:
        dati_dict = json.load(data_file)
    node_dict = createNode(dati_dict)
    for node in node_dict:
        print (node_dict[node].getId(),
            node_dict[node].getDur(),
            node_dict[node].getAddr(),
            node_dict[node].getNotWith())

    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    params = dict(
        origins='',
        destinations='',
        mode='driving',#transit
        language='it-IT',
        units='metric',
        key='AIzaSyB27xz94JVRPsuX4qJMMiZpGVoQiQITFb8'
    )

    params['destinations'] = node_dict['0'].getAddr() + "|"
    for key in node_dict:
        if key != '0':
            params['origins'] += node_dict[key].getAddr() + "|"
            params['destinations'] += node_dict[key].getAddr() + "|"

    params['origins'] = params['origins'][:-1]
    params['destinations'] = params['destinations'][:-1]

    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    with open('googleMaps.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)
    return dict(status="OK", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
    #app.run()
