import json
import requests
import collections
import random
import math
from operator import attrgetter
from euristiche import Euristiche
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

def updateAddress(node_dict, google_dict):
    for i, key in enumerate(node_dict):
        node_dict[key].setAddr(google_dict['destination_addresses'][i])

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
    ### TEST
    with open('requestTest.json', 'r') as data_file:
        dati_dict = json.load(data_file)
    node_dict = createNode(dati_dict)
    with open('googleMapsTest.json', 'r') as data_file:
        google_dict = json.load(data_file)
    ### END TEST
    #with open('request.json', 'w') as outfile:
    #    json.dump(request.vars, outfile, indent=4)
    #node_dict = createNode(request.vars)

    printNode(node_dict)

    #google_dict = googleMapsRequest(node_dict)
    arc_dict = createArc(google_dict, node_dict)

    print "----------------------------"
    printArc((arc_dict))
    print "----------------------------"
    greedy = Euristiche(node_dict, arc_dict)
    (cars_list, dur_list, dist) = greedy.greedy()
    print "-->Greedy"
    print "cars_list:", cars_list
    print "dur_list:", dur_list
    print "dist:", dist

    dataOut = initDataOuttput()

    updateDataOutput(dataOut, 'greedy', cars_list, dur_list, dist, node_dict['0'].getDur())

    grasp = Euristiche(node_dict, arc_dict)
    (cars_list, dur_list, dist) = grasp.grasp()
    print "-->Grasp"
    print "cars_list:", cars_list
    print "dur_list:", dur_list
    print "dist:", dist
    updateDataOutput(dataOut, 'grasp', cars_list, dur_list, dist, node_dict['0'].getDur())

    tabu = Euristiche(node_dict, arc_dict)
    localSearch_list = list()
    localSearch_list.append(greedy)
    for i in range(math.factorial(len(node_dict)/2)):
        g = Euristiche(node_dict, arc_dict)
        g.grasp()
        if not (g in localSearch_list):
            localSearch_list.append(g)

    (cars_list, dur_list, dist) = tabu.initTabu(localSearch_list, 3)
    print "-->Tabu"
    print "cars_list:", cars_list
    print "dur_list:", dur_list
    print "dist:", dist
    updateDataOutput(dataOut, 'tabu', cars_list, dur_list, dist, node_dict['0'].getDur())

    with open('response.json', 'w') as outfile:
        json.dump(dataOut, outfile, indent=4)

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
