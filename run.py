import json
import requests
import collections
import random
import sys
import webbrowser
import googlemaps
import copy
import time
import os
import time
import winsound
from lockfile import LockFile
from operator import attrgetter
from euristiche import Euristiche
from node import Node
from arc import Arc
from weppy import App, request
from weppy.tools import service

app = App(__name__)
key_googleMaps2 = 'AIzaSyB27xz94JVRPsuX4qJMMiZpGVoQiQITFb8'
key_googleMaps = 'AIzaSyDEeQ7ybauE3th_3d-GQZQcvGI-UxKOFF8'
key_googleMaps3 = 'AIzaSyC549poFoVcUz3BsDOJ9XpO7CniNTDC6b4'
isTest = False
isBenchmark = False
isLoop = False
ncycle = 1

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

def createArc(google_dict, node_dict_o, node_dict_d, arc_dict):
    if node_dict_o == node_dict_d:
        node_dict_d.insert(0, '0')
    """
    print "node_dict_o", node_dict_o
    print "node_dict_d", node_dict_d
    print "google_dict['origin_addresses']", google_dict['origin_addresses']
    print "google_dict['destination_addresses'])", google_dict['destination_addresses']
    """
    for i in range(len(google_dict['origin_addresses'])):
        for y in range(len(google_dict['destination_addresses'])):
            dur = google_dict['rows'][i]['elements'][y]['duration']['value']
            dist = google_dict['rows'][i]['elements'][y]['distance']['value']
            #print "##########", node_dict_o[i], node_dict_d[y]
            if node_dict_o[i] != node_dict_d[y]:
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

def googleMapsRequest(node_dict):
    arc_dict = collections.OrderedDict()
    timeGoogle = 0
    timesleep = 10
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
        # -2 perche' x parte da 0 e il ciclo for non conta la destinazione
        if (len(origins_tmp) >= 9) or (x == (len(node_dict)-2)):
            for y in range(1,len(node_dict)):
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
                        print "Sto effettuando le richiesete a Google Maps, attendi..."
                        resp = requests.get(url=url, params=params)
                        google_dict = json.loads(resp.text)
                        # metto in pausa l'applicazione per dieci secondi per aggirare
                        # i limiti delle Google Maps Api
                        time.sleep(timesleep)
                        timeGoogle += timesleep
                    arc_dict = createArc(google_dict, node_origins_tmp, node_destinations_tmp, arc_dict)
                    destinations_tmp = list()
                    node_destinations_tmp = list()
                    if y == (len(node_dict)-1):
                        origins_tmp = list()
                        node_origins_tmp = list()
    return (arc_dict, timeGoogle)


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
            idNode = node_dict[key].getId()
            maxDur = str(node_dict[key].getDur())
            addr = node_dict[key].getAddr()
            notWith = ','.join(node_dict[key].getNotWith())
            outfile.write(idNode + "#" + maxDur  + "#" + addr + "#" + notWith)
            outfile.write("\n")
        outfile.flush()
        os.fsync(outfile)
        print "Ho salvato i nodi nel file 'nodeDict.txt'"
        return True
    return False

def loadNode(filename):
    node_dict = collections.OrderedDict()
    with open('nodeDict.txt', 'r') as inputfile:
        for line in inputfile:
            # prima eseguo rstrip, poi split
            line_tmp = line.rstrip('\n').split('#')
            #print line_tmp
            # la destionazione ha sempre id=0
            node_dict[line_tmp[0]] = (Node(
                id=line_tmp[0],
                dur=long(line_tmp[1]),
                addr=line_tmp[2],
                notWith=line_tmp[3])
            )
    return node_dict

def saveArc(arc_dict):
    with open('arcDict.txt', 'w') as outfile:
        for key1 in arc_dict:
            for key2 in arc_dict[key1]:
                id_i = arc_dict[key1][key2].getId_i()
                id_f = arc_dict[key1][key2].getId_f()
                dur = str(arc_dict[key1][key2].getDur())
                dist = str(arc_dict[key1][key2].getDist())
                outfile.write(id_i + "#" + id_f  + "#" + dur + "#" + dist + '\n')
        outfile.flush()
        os.fsync(outfile)
        print "Ho salvato gli archi nel file 'arcDict.txt'"
        return True
    return False

def loadArc(filename):
    arc_dict = collections.OrderedDict()
    with open('arcDict.txt', 'r') as inputfile:
        for line in inputfile:
            # prima eseguo rstrip, poi split
            line_tmp = line.rstrip('\n').split('#')
            if not (line_tmp[0] in arc_dict):
                arc_dict[line_tmp[0]] = dict()
            arc_dict[line_tmp[0]][line_tmp[1]] = Arc(
                id_i=line_tmp[0],
                id_f=line_tmp[1],
                dur=int(line_tmp[2]),
                dist=int(line_tmp[3])
            )
    return arc_dict


def floatToStringWithComma(num):
    return str(num).replace('.', ',')


def saveBenchmark(filename, durata, maxDist, randomizeDog, node_dict,
        arc_dict, greedy, grasp, path, pathReverse, tabu):
    separetor = ';'
    n_arc = 0
    for key in arc_dict:
        n_arc += len(arc_dict[key])
    """
    invece di verificare la distanza non e' meglio valutare il tempo di esecuzione
    visto che la distanza risulta sempre uguale
    """
    if path.getExecutionTime() > pathReverse.getExecutionTime():
        pathVSpathReverse = '1'
    else:
        pathVSpathReverse = '0'
    line = floatToStringWithComma(durata) + separetor + str(len(node_dict)) + \
        separetor + str(n_arc) + separetor + str(maxDist) + separetor + \
        floatToStringWithComma(greedy.getExecutionTime()) + separetor + str(len(greedy.getCars())) + \
        separetor + str(greedy.getDist()) + separetor  + str(randomizeDog) + \
        separetor + floatToStringWithComma(grasp.getExecutionTime()) + separetor + \
        str(len(grasp.getCars())) + separetor + str(grasp.getDist()) + \
        separetor + floatToStringWithComma(path.getExecutionTime()) + separetor + \
        str(randomizeDog) + separetor + str(len(path.getCars())) + separetor + \
        str(path.getDist()) + separetor + floatToStringWithComma(pathReverse.getExecutionTime()) + \
        separetor + str(randomizeDog) + separetor + \
        str(len(pathReverse.getCars())) + separetor + \
        str(pathReverse.getDist()) + separetor + pathVSpathReverse + \
        separetor + floatToStringWithComma(tabu.getExecutionTime()) + separetor + \
        str(len(tabu.getCars())) + separetor + str(tabu.getDist()) + '\n'

    with LockFile(filename):
        with open(filename, "a") as file:
            file.write(line)
            file.flush()
            os.fsync(file)

    print "\nEsecuzione salvata nel file '" + filename + "'"


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

def printInfo(typeEur, eur):
    print "\n-->" + typeEur
    print "cars_list:", eur.getCars()
    print "dur_list:", eur.getDur()
    print "dist:", eur.getDist()
    print "CPU execution time: ", eur.getExecutionTime()


@app.expose("/")
@service.json
def home():
    for i in range(ncycle):
        if isLoop:
            print "\nCiclo numero:", i+1
        startP = time.clock()
        if isTest:
            with open('requestTest.json', 'r') as data_file:
                dati_dict = json.load(data_file)
            node_dict = createNode(dati_dict)
        elif isBenchmark:
            node_dict = loadNode('nodeDict.txt')
        else:
            with open('request.json', 'w') as outfile:
                json.dump(request.vars, outfile, indent=4)
            node_dict = createNode(request.vars)
        if isBenchmark:
            arc_dict = loadArc('arcDict.txt')
        else:
            (arc_dict, timeGoogle) = googleMapsRequest(node_dict)

        if not isLoop:
            print "\n-->NODI"
            printNode(node_dict)
            print "len(node_dict)", len(node_dict)
        if not isBenchmark and not isTest:
            saveNode(node_dict)

        #geocode_results = viewMarkers(node_dict)

        if not isLoop:
            print "\n-->ARCHI"
            printArc((arc_dict))
            n_arc = 0
            for key in arc_dict:
                n_arc += len(arc_dict[key])
            print "len(arc_dict)", len(arc_dict), n_arc
        if not isBenchmark and not isTest:
            saveArc(arc_dict)

        start_time = time.clock()
        greedy = Euristiche(node_dict, arc_dict)
        (cars_list, dur_list, dist) = greedy.greedy()
        greedy.setExecutionTime(time.clock() - start_time)
        if not isLoop:
            printInfo('Greedy', greedy)
        cars_greedy_list = copy.deepcopy(greedy.getCars())

        dataOut = updateDataOutput(initDataOuttput(), 'greedy', cars_list,
            dur_list, dist, node_dict['0'].getDur())

        #viewDirection(node_dict, geocode_results, cars_list)

        start_time = time.clock()
        grasp = Euristiche(node_dict, arc_dict)
        (cars_list, dur_list, dist) = grasp.grasp()
        grasp.setExecutionTime(time.clock() - start_time)
        if not isLoop:
            printInfo('Grasp', grasp)
        dataOut = updateDataOutput(dataOut, 'grasp', cars_list, dur_list, dist,
            node_dict['0'].getDur())

        #viewDirection(node_dict, geocode_results, cars_list)

        arcToDest_dict = dict()
        for key in arc_dict.keys():
            arcToDest_dict[key] = arc_dict[key]['0']
        penality = sorted(arcToDest_dict.values(), key=attrgetter('dist'),
            reverse=True)[0].getDist()

        randomizeDog = 5
        start_time = time.clock()
        path = Euristiche(node_dict, arc_dict)
        localSearch_list_path = path.preparePath(copy.deepcopy(greedy), randomizeDog)
        localSearch_list_pathReverse = copy.deepcopy(localSearch_list_path)

        (cars_list, dur_list, dist) = path.initPath(localSearch_list_path, randomizeDog, penality/2)
        path.setExecutionTime(time.clock() - start_time)
        if not isLoop:
            printInfo('Path', path)
        dataOut = updateDataOutput(dataOut, 'path', cars_list, dur_list, dist,
            node_dict['0'].getDur())

        start_time = time.clock()
        pathReverse = Euristiche(node_dict, arc_dict)

        #localSearch_list_pathReverse = pathReverse.preparePath(copy.deepcopy(greedy), randomizeDog)
        (cars_list, dur_list, dist) = pathReverse.initPath(localSearch_list_pathReverse, randomizeDog, penality/2)
        pathReverse.setExecutionTime(time.clock() - start_time)
        if not isLoop:
            printInfo('Path Reverse', pathReverse)
        dataOut = updateDataOutput(dataOut, 'pathReverse', cars_list, dur_list, dist,
            node_dict['0'].getDur())

        #viewDirection(node_dict, geocode_results, cars_list)

        start_time = time.clock()
        tabu = Euristiche(node_dict, arc_dict)
        (cars_list, dur_list, dist) = tabu.tabu(greedy, greedy, 0, 0, list(), penality/2)
        tabu.setExecutionTime(time.clock() - start_time)
        if not isLoop:
            printInfo('Tabu', tabu)
        dataOut = updateDataOutput(dataOut, 'tabu', cars_list, dur_list, dist,
            node_dict['0'].getDur())

        with open('response.json', 'w') as outfile:
            json.dump(dataOut, outfile, indent=4)

        durata = time.clock() - startP
        if not isBenchmark and not isTest:
            durata -= timeGoogle
        saveBenchmark('benchmark.txt', durata, penality, randomizeDog,
            node_dict, arc_dict, greedy, grasp, path, pathReverse, tabu)
    winsound.Beep(2500, 2000)
    #return dict(status="OK", data="Sono tanto stupido")
    return dataOut


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '-t':
            isTest = True
            if len(sys.argv) > 2 and sys.argv[2] == '-l':
                isLoop = True
                try:
                    ncycle = int(sys.argv[3])
                except Exception:
                    ncycle = 100
                print "\nEseguo il programma in modalita' TEST LOOP, numero cicli", (ncycle), "...\n"
            else:
                print "\nEseguo il programma in modalita' TEST, numero cicli", (ncycle), "...\n"
        if sys.argv[1] == '-b':
            isBenchmark = True
            if len(sys.argv) > 2 and sys.argv[2] == '-l':
                isLoop = True
                try:
                    ncycle = int(sys.argv[3])
                except Exception:
                    ncycle = 100
                print "\nEseguo il programma in modalita' BENCHMARK LOOP, numero cicli", (ncycle), "...\n"
            else:
                print "\nEseguo il programma in modalita' BENCHMARK...\n"

        app.run()
    else:
        app.run(host="0.0.0.0")
