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
from datetime import datetime, timedelta
import winsound
from lockfile import LockFile
from operator import attrgetter
from euristiche import Euristiche
from node import Node
from arc import Arc

key_googleMaps3 = 'AIzaSyB27xz94JVRPsuX4qJMMiZpGVoQiQITFb8'
key_googleMaps2 = 'AIzaSyDEeQ7ybauE3th_3d-GQZQcvGI-UxKOFF8'
key_googleMaps = 'AIzaSyC549poFoVcUz3BsDOJ9XpO7CniNTDC6b4'
isTest = False
isBenchmark = False
isLoop = False
ncycle = 1

def createNode(dati_dict):
    node_dict = collections.OrderedDict()
    # la destionazione ha sempre id=0
    node_dict['0'] = (Node(
        id='0',
        maxDur=dati_dict['time_to_arrive'],
        addr=dati_dict['place_to_arrive'])
    )

    #for i, user in enumerate(dati_dict['users']):
    for user in dati_dict['users']:
        node_dict[str(user['id'])] = Node(
            id=user['id'],
            maxDur=user['max_duration'],
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


def initDataOutput():
    dataOut = dict()
    dataOut['euristiche'] = dict()
    dataOut['euristiche']['name'] = ''
    dataOut['euristiche']['results'] = dict()
    return dataOut


def updateDataOutput(dataOut, eur_type, cars_list, dur_list, dur, timeEnd):
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
    dataOut['euristiche']['results'][eur_type]['costo'] = str(dur)
    return dataOut


def googleMapsRequest(node_dict):
    arc_dict = collections.OrderedDict()
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
                    arc_dict = createArc(google_dict, node_origins_tmp, node_destinations_tmp, arc_dict)
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
            idNode = node_dict[key].getId()
            maxDur = str(node_dict[key].getMaxDur())
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
                maxDur=long(line_tmp[1]),
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
    if path.getExecutionTime() > pathReverse.getExecutionTime():
        pathVSpathReverse = '1'
    else:
        pathVSpathReverse = '0'
    line = floatToStringWithComma(durata) + separetor + str(len(node_dict)) + \
        separetor + str(n_arc) + separetor + str(maxDist) + separetor + \
        floatToStringWithComma(greedy.getExecutionTime()) + separetor + str(len(greedy.getCars())) + \
        separetor + str(greedy.getDur()) + separetor  + str(randomizeDog) + \
        separetor + floatToStringWithComma(grasp.getExecutionTime()) + separetor + \
        str(len(grasp.getCars())) + separetor + str(grasp.getDur()) + \
        separetor + floatToStringWithComma(path.getExecutionTime()) + separetor + \
        str(randomizeDog) + separetor + str(len(path.getCars())) + separetor + \
        str(path.getDur()) + separetor + floatToStringWithComma(pathReverse.getExecutionTime()) + \
        separetor + str(randomizeDog) + separetor + \
        str(len(pathReverse.getCars())) + separetor + \
        str(pathReverse.getDur()) + separetor + pathVSpathReverse + \
        separetor + floatToStringWithComma(tabu.getExecutionTime()) + separetor + \
        str(len(tabu.getCars())) + separetor + str(tabu.getDur()) + '\n'

    with LockFile(filename):
        with open(filename, "a") as file:
            file.write(line)
            file.flush()
            os.fsync(file)
    print "\nEsecuzione salvata nel file '" + filename + "'"


def printNode(node_dict):
    for node in node_dict:
        print (node_dict[node].getId(),
            node_dict[node].getMaxDur(),
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
    print "Lista ID auto:", eur.getCars()
    #print "Lista partenze in millisecondi:", eur.getDurList()
    print "Durata totale di tutte le auto (H:M:S):", timedelta(milliseconds=eur.getDur())
    print "CPU execution time: ", eur.getExecutionTime()


def initMain():
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
        arc_dict = googleMapsRequest(node_dict)

    if not isLoop:
        print "\n-->NODI"
        printNode(node_dict)
    print "len(node_dict)", len(node_dict)
    if not isLoop:
        print "\n-->ARCHI"
        printArc((arc_dict))
    n_arc = 0
    for key in arc_dict:
        n_arc += len(arc_dict[key])
    print "len(arc_dict)", len(arc_dict), n_arc
    if not isBenchmark and not isTest:
        saveNode(node_dict)
        saveArc(arc_dict)

    return (node_dict, arc_dict)


def main():
    calcEndTime = False
    (node_dict, arc_dict) = initMain()
    #geocode_results = viewMarkers(node_dict)

    #node_dict = loadNode('nodeDict.txt')
    #arc_dict = googleMapsRequest(node_dict)

    for i in range(ncycle):
        if isLoop:
            print "\nCiclo numero:", i+1
        startP = time.clock()

        start_time = time.clock()
        greedy = Euristiche(node_dict, arc_dict)
        (cars_list, dur_list, dur) = greedy.greedy()
        greedy.setExecutionTime(time.clock() - start_time)
        if not isLoop:
            printInfo('Greedy', greedy)
        cars_greedy_list = copy.deepcopy(greedy.getCars())

        dataOut = updateDataOutput(initDataOutput(), 'greedy', cars_list,
            dur_list, dur, node_dict['0'].getMaxDur())

        #viewDirection(node_dict, geocode_results, cars_list)

        start_time = time.clock()
        grasp = Euristiche(node_dict, arc_dict)
        (cars_list, dur_list, dur) = grasp.grasp()
        grasp.setExecutionTime(time.clock() - start_time)
        if not isLoop:
            printInfo('Grasp', grasp)
        dataOut = updateDataOutput(dataOut, 'grasp', cars_list, dur_list, dur,
            node_dict['0'].getMaxDur())

        #viewDirection(node_dict, geocode_results, cars_list)

        arcToDest_dict = dict()
        for key in arc_dict.keys():
            arcToDest_dict[key] = arc_dict[key]['0']
        penality = sorted(arcToDest_dict.values(), key=attrgetter('dur'),
            reverse=True)[0].getDur()

        randomizeDog = 5

        tmp_time_path = time.clock()
        path = Euristiche(node_dict, arc_dict)
        localSearch_list_path = path.preparePath(copy.deepcopy(greedy), randomizeDog)
        tmp_time_path = time.clock() - tmp_time_path
        # Effettuo subito la copia per non rischiare di usare una lista modificata
        tmp_time_path_reverse = time.clock()
        localSearch_list_pathReverse = copy.deepcopy(localSearch_list_path)
        tmp_time_path_reverse = time.clock() - tmp_time_path_reverse
        """
        Il tempo parte da qua e non da 'path = Euristiche(node_dict, arc_dict)'
        perche' prima effettuo anche la copia per la localSearch_list_pathReverse
        e quindi le due tempistiche non sarebbero veritiere
        """
        start_time = time.clock()
        (cars_list, dur_list, dur) = path.initPath(localSearch_list_path, randomizeDog, penality/2)
        path.setExecutionTime((time.clock() - start_time) + tmp_time_path)
        if not isLoop:
            printInfo('Path', path)
        dataOut = updateDataOutput(dataOut, 'path', cars_list, dur_list, dur,
            node_dict['0'].getMaxDur())

        pathReverse = Euristiche(node_dict, arc_dict)
        # Stesso discorso di della path
        start_time = time.clock()
        (cars_list, dur_list, dur) = pathReverse.initPath(localSearch_list_pathReverse, randomizeDog, penality/2)
        pathReverse.setExecutionTime((time.clock() - start_time) + tmp_time_path_reverse)
        if not isLoop:
            printInfo('Path Reverse', pathReverse)
        dataOut = updateDataOutput(dataOut, 'pathReverse', cars_list, dur_list, dur,
            node_dict['0'].getMaxDur())

        #viewDirection(node_dict, geocode_results, cars_list)

        start_time = time.clock()
        tabu = Euristiche(node_dict, arc_dict)
        (cars_list, dur_list, dur) = tabu.tabu(greedy, greedy, 0, 0, list(), penality/2)
        tabu.setExecutionTime(time.clock() - start_time)
        if not isLoop:
            printInfo('Tabu', tabu)
        dataOut = updateDataOutput(dataOut, 'tabu', cars_list, dur_list, dur,
            node_dict['0'].getMaxDur())

        with open('response.json', 'w') as outfile:
            json.dump(dataOut, outfile, indent=4)

        durata = time.clock() - startP
        if isBenchmark:
            saveBenchmark('benchmark.txt', durata, penality, randomizeDog,
                node_dict, arc_dict, greedy, grasp, path, pathReverse, tabu)

        if ncycle > 1 and i < (ncycle-1):
            # da decidere se e' meglio effettuare il calcolo ogni volta
            if not calcEndTime:
                calcEndTime = True
                totalTime = durata * ncycle
                endExec = datetime.now() + timedelta(seconds=totalTime)
            print "\nLa fine dell'esecuzione e' prevista per le", '{:%H:%M:%S}'.format(endExec)
        elif i == (ncycle-1):
            print "\n### ESECUZIONE TERMINATA ###"

    winsound.Beep(2500, 1500)
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
                    ncycle = 50
                print "\nEseguo il programma in modalita' TEST LOOP, numero cicli:", (ncycle), "...\n"
            else:
                print "\nEseguo il programma in modalita' TEST...\n"
            main()
        elif sys.argv[1] == '-b':
            isBenchmark = True
            if len(sys.argv) > 2 and sys.argv[2] == '-l':
                isLoop = True
                try:
                    ncycle = int(sys.argv[3])
                except Exception:
                    ncycle = 50
                print "\nEseguo il programma in modalita' BENCHMARK LOOP, numero cicli", (ncycle), "...\n"
            else:
                print "\nEseguo il programma in modalita' BENCHMARK...\n"
            main()
        else:
            print "Eseguire il programma con una delle seguenti modalita':"
            print "'python main.py -t' per la modalita' test"
            print "'python main.py -t -l n' per la modalita' test in modalita' loop dove n e' il numero di iterazioni"
            print "'python main.py -b' per la modalita' benchmark"
            print "'python main.py -b -l n' per la modalita' benchmark in modalita' loop dove n e' il numero di iterazioni"

    else:
        print "Eseguire il programma con una delle seguenti modalita':"
        print "'python main.py -t' per la modalita' test"
        print "'python main.py -t -l n' per la modalita' test in modalita' loop dove n e' il numero di iterazioni"
        print "'python main.py -b' per la modalita' benchmark"
        print "'python main.py -b -l n' per la modalita' benchmark in modalita' loop dove n e' il numero di iterazioni"
