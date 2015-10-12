import json
import requests
import collections
import random
import math
import sys
import webbrowser
import googlemaps
import copy
from operator import attrgetter
from euristiche import Euristiche
from node import Node
from arc import Arc
from weppy import App, request
from weppy.tools import service

app = App(__name__)
key_googleMaps = 'AIzaSyB27xz94JVRPsuX4qJMMiZpGVoQiQITFb8'
key_googleMaps2 = 'AIzaSyDEeQ7ybauE3th_3d-GQZQcvGI-UxKOFF8'
isTest = False

def createNode(dati_dict):
    node_dict = collections.OrderedDict()
    # la destionazione ha sempre id=0
    node_dict['0'] = (Node(
        id='0',
        dur=dati_dict['time_to_arrive'],
        addr=dati_dict['place_to_arrive'])
    )

    #for i, user in enumerate(dati_dict['users']):
    for user in dati_dict['users']:
        node_dict[str(user['id'])] = Node(
            id=user['id'],
            dur=user['max_duration'],
            addr=user['address'],
            notWith=user['not_with'])
    return node_dict

def createArc(google_dict, node_dict_o, node_dict_d, arc_dict, equals):
    if equals:
        node_dict_d.insert(0, '0')

    print "node_dict_o", node_dict_o
    print "node_dict_d", node_dict_d
    print "google_dict['origin_addresses']", google_dict['origin_addresses']
    print "google_dict['destination_addresses'])", google_dict['destination_addresses']

    for i in range(len(google_dict['origin_addresses'])):
        for y in range(len(google_dict['destination_addresses'])):
            dur = google_dict['rows'][i]['elements'][y]['duration']['value']
            dist = google_dict['rows'][i]['elements'][y]['distance']['value']
            if dur > 0 and dist > 0:
                """
                # tolto per eliminare ordine archi
                if (arc_dict[keys_list[i+1]]['0'].getDur() >
                        arc_dict[keys_list[y]]['0'].getDur()):
                """
                if not (node_dict_o[i] in arc_dict):
                    arc_dict[node_dict_o[i]] = dict()
                arc_dict[node_dict_o[i]][node_dict_d[y]] = Arc(
                    id_i=node_dict_o[i],
                    id_f=node_dict_d[y],
                    dur=int(dur*1000),
                    dist=dist)
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
    return dataOut

def googleMapsRequest(node_dict, arc_dict):
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    params = dict(
        origins='',
        destinations='',
        mode='driving',
        language='it-IT',
        units='metric',
        key=key_googleMaps
    )
    origins_tmp = list()
    destinations_tmp = list()
    node_origins_tmp = list()
    node_destinations_tmp = list()
    # il ciclo for parte dal primo nodo dopo la destionazione cioe' 0
    for x, key in enumerate(node_dict.keys()[1:]):
        origins_tmp.append(node_dict[key])
        node_origins_tmp.append(node_dict[key].getId())
        for y in range(1,len(node_dict)):
            # -2 perche' x parte da 0 e il ciclo for non conta la destinazione
            # TODO questa if non e' meglio inserirla al di fuori del ciclo for
            # cosi' da evitare un continuo ciclo?
            if (len(origins_tmp) >= 9) or (x == (len(node_dict)-2)):
                # appendo la chiave del j-esimo elemento di node_dict
                destinations_tmp.append(node_dict[node_dict.items()[y][0]])
                # appendo l'id del j-esimo nodo
                node_destinations_tmp.append(node_dict[node_dict.items()[y][0]].getId())
                if (len(destinations_tmp) >= 9) or (y == (len(node_dict)-1)):
                    googleParams = getGoogleParams(node_dict, origins_tmp, destinations_tmp)
                    params['origins'] = googleParams[0]
                    params['destinations'] = googleParams[1]
                    if isTest:
                        with open('googleMapsTest.json', 'r') as data_file:
                            google_dict = json.load(data_file)
                    else:
                        resp = requests.get(url=url, params=params)
                        google_dict = json.loads(resp.text)

                    arc_dict = createArc(google_dict, node_origins_tmp, node_destinations_tmp, arc_dict, x+1 == y)
                    destinations_tmp = list()
                    node_destinations_tmp = list()
                    if y == (len(node_dict)-1):
                        origins_tmp = list()
                        node_origins_tmp = list()
    return arc_dict


def getGoogleParams(node_dict, nodeOrigins, nodeDestinations):
    origins = ''
    destinations = ''
    if nodeOrigins == nodeDestinations:
        destinations += node_dict['0'].getAddr() + "|"
    for node in nodeOrigins:
        origins += node.getAddr() + "|"
    for node in nodeDestinations:
        destinations += node.getAddr() + "|"
    origins = origins[:-1]
    destinations = destinations[:-1]
    return (origins, destinations)


def viewMarkers(node_dict):
    gmaps = googlemaps.Client(key=key_googleMaps)
    geocode_results = dict()
    for key in node_dict:
        result = gmaps.geocode(node_dict[key].getAddr())
        lat = str(result[0]['geometry']['location']['lat'])
        lng = str(result[0]['geometry']['location']['lng'])
        geocode_results[key] = (lat,lng)
    url = 'http://giulioribe.github.io/car-pooling/maps.html?'
    params = dict(
        dataM='',
        dataD=''
    )
    for key in geocode_results:
        if key == '0':
            params['dataD'] += geocode_results[key][0] + '_' + \
                geocode_results[key][1]
        else:
            params['dataM'] += node_dict[key].getId() + '_' + \
                node_dict[key].getId() + '_' + geocode_results[key][0] + \
                '_' + geocode_results[key][1] + '|'
    params['dataM'] = params['dataM'][:-1]
    resp = requests.get(url=url, params=params)
    webbrowser.open_new(resp.url)
    return geocode_results

def viewDirection(node_dict, geocode_results, cars_list):
    url = 'http://giulioribe.github.io/car-pooling/directions.html?'
    params = dict(
        dataM='',
        dataD=node_dict['0'].getAddr()
    )
    for cars in cars_list:
        for car in cars:
            if car != '0':
                params['dataM'] += node_dict[car].getId() + '_' + \
                    node_dict[car].getId() + '_' + node_dict[car].getAddr() + '|'
        params['dataM'] = params['dataM'][:-1]
        resp = requests.get(url=url, params=params)
        webbrowser.open_new(resp.url)
        params['dataM'] = ''

def saveNode(node_dict):
    with open('nodeDict.txt', 'w') as outfile:
        for key in node_dict:
            outfile.writelines(node_dict)
    pass

def loadNode(node_dict):
    pass

def saveArc(arc_dict):
    pass

def loadArc(arc_dict):
    pass

def printNode(node_dict):
    for node in node_dict:
        print (node_dict[node].getId(),
            node_dict[node].getDur(),
            node_dict[node].getAddr(),
            node_dict[node].getNotWith())

def printArc(arc_dict):
    for arc in arc_dict:
        for a in arc_dict[arc]:
            print (arc_dict[arc][a].getId_i(),
                arc_dict[arc][a].getId_f(),
                arc_dict[arc][a].getDur(),
                arc_dict[arc][a].getDist())

@app.expose("/")
@service.json
def home():
    # TODO aumentare il numero di nodi per avere se la greedy fa sempre macchine da 5 persone
    if isTest:
        with open('requestTest.json', 'r') as data_file:
            dati_dict = json.load(data_file)
        node_dict = createNode(dati_dict)
    else:
        with open('request.json', 'w') as outfile:
            json.dump(request.vars, outfile, indent=4)
        node_dict = createNode(request.vars)

    arc_dict = collections.OrderedDict()
    arc_dict = googleMapsRequest(node_dict, arc_dict)
    print "\n-->NODI"
    printNode(node_dict)

    #geocode_results = viewMarkers(node_dict)
    print "\n-->ARCHI"
    printArc((arc_dict))

    greedy = Euristiche(node_dict, arc_dict)
    (cars_list, dur_list, dist) = greedy.greedy()
    print "\n-->Greedy"
    print "cars_list:", cars_list
    print "dur_list:", dur_list
    print "dist:", dist
    print "Amm", greedy.ammissibileMinDur(greedy)
    cars_greedy_list = copy.deepcopy(greedy.getCars())

    dataOut = updateDataOutput(initDataOuttput(), 'greedy', cars_list,
        dur_list, dist, node_dict['0'].getDur())

    #viewDirection(node_dict, geocode_results, cars_list)

    grasp = Euristiche(node_dict, arc_dict)
    (cars_list, dur_list, dist) = grasp.grasp()
    print "\n-->Grasp"
    print "cars_list:", cars_list
    print "dur_list:", dur_list
    print "dist:", dist
    print "Amm", grasp.ammissibileMinDur(grasp)
    dataOut = updateDataOutput(dataOut, 'grasp', cars_list, dur_list, dist,
        node_dict['0'].getDur())

    #viewDirection(node_dict, geocode_results, cars_list)

    arcToDest_dict = dict()
    for key in arc_dict.keys():
        arcToDest_dict[key] = arc_dict[key]['0']
    penality = sorted(arcToDest_dict.values(), key=attrgetter('dist'),
                    reverse=True)[0].getDist()

    path = Euristiche(node_dict, arc_dict)
    localSearch_list = list()
    localSearch_list.append(copy.deepcopy(greedy))
    for i in range(math.factorial(len(node_dict)/2)):
        g = Euristiche(node_dict, arc_dict)
        g.grasp()
        if not (g in localSearch_list):
            localSearch_list.append(g)
    path_completo = path.initPath(localSearch_list, 3, penality/2)
    print "\n-->Path"
    print "cars_list:", path_completo[0][0]
    print "dur_list:", path_completo[0][1]
    print "dist:", path_completo[0][2]
    dataOut = updateDataOutput(dataOut, 'path', path_completo[0][0],
        path_completo[0][1], path_completo[0][2], node_dict['0'].getDur())
    print "\n-->Path Reverse"
    print "cars_list:", path_completo[1][0]
    print "dur_list:", path_completo[1][1]
    print "dist:", path_completo[1][2]
    dataOut = updateDataOutput(dataOut, 'pathReverse', path_completo[1][0],
        path_completo[1][1], path_completo[1][2], node_dict['0'].getDur())

    #viewDirection(node_dict, geocode_results, cars_list)

    tabu = Euristiche(node_dict, arc_dict)
    (cars_list, dur_list, dist) = tabu.tabu(greedy, greedy, 0, 0, list(), penality/2)
    print "\n-->Tabu"
    print "cars_list:", cars_list
    print "dur_list:", dur_list
    print "dist:", dist

    dataOut = updateDataOutput(dataOut, 'tabu', cars_list, dur_list, dist,
        node_dict['0'].getDur())

    with open('response.json', 'w') as outfile:
        json.dump(dataOut, outfile, indent=4)

    #return dict(status="OK", data="Sono tanto stupido")

    return dataOut


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            isTest = True
    app.run(host="0.0.0.0")
    #app.run()
