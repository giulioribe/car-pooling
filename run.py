import json
import requests
from node import Node
from arc import Arc
from weppy import App, request
from weppy.tools import service

app = App(__name__)
key = 'AIzaSyB27xz94JVRPsuX4qJMMiZpGVoQiQITFb8'

@app.expose("/")
def home():
    with open('dati.json', 'r') as data_file:
        dati_dict = json.load(data_file)
    node_dict = dict()
    # la destionazione ha sempre id=0
    node_dict[0] = (Node(
        ### TODO: id controllare se il JSON restituisce  int o str
        id=0,
        dur=dati_dict['time_to_arrive'],
        addr=dati_dict['place_to_arrive'])
    )

    for i, user in enumerate(dati_dict['users']):
        node_dict[i+1] = Node(
            ### TODO: id controllare se il JSON restituisce  int o str
            id=user['id'],
            dur=user['max_duration'],
            addr=user['address'],
            notWith=user['not_with'])

    with open('googleMaps.json', 'r') as data_file:
        google_dict = json.load(data_file)
    arc_dict = dict()
    '''
    posso usare questo metodo per inserire i nodi perche' la lista dei
    sorgenti e di destinazione di Google Maps sono nello stesso ordine ma
    traslati di uno perche nella prima posizione della lista dei nodi di
    destinazione c'e' la destionazione di tutti i nodi
    '''
    for i in range(len(google_dict['origin_addresses'])):
        arc_dict[node_dict[i+1].getId()] = list()
        arc_dict[node_dict[i+1].getId()].append(Arc(
            ### TODO: id controllare se il JSON restituisce  int o str
            id_i=node_dict[i+1].getId(),
            # id_f=0 perche' il nodo di destionazione e' 0
            id_f=0,
            # prendo il nodo in posizione 0 (destinazione uguale per tutti)
            # perche' recupero tutti i valori verso la destinazione
            duration=google_dict['rows'][i]['elements'][0]['duration']['value'],
            distance=google_dict['rows'][i]['elements'][0]['distance']['value'])
        )
    for i in range(len(google_dict['origin_addresses'])):
        # il ciclo parte da 1 perche' nella prima posizione c'e' la
        # destinazione di tutti
        for y in range(1, len(google_dict['destination_addresses'])):
            duration = google_dict['rows'][i]['elements'][y]['duration']['value']
            distance = google_dict['rows'][i]['elements'][y]['distance']['value']
            print "i", i, "y", y, "duration", duration
            if duration > 0 and distance > 0:
                arc_dict[node_dict[i+1].getId()].append(Arc(
                    ### TODO: id controllare se il JSON restituisce  int o str
                    id_i=node_dict[i+1].getId(),
                    # id_f=0 perche' il nodo di destionazione e' 0
                    id_f=node_dict[y].getId(),
                    # prendo il nodo in posizione 0 (destinazione uguale per tutti)
                    # perche' recupero tutti i valori verso la destinazione
                    duration=duration,
                    distance=distance)
                )
            else:
                print "NO"

    for node in node_dict:
        print (node_dict[node].getId(),
            node_dict[node].getDur(),
            node_dict[node].getAddr(),
            node_dict[node].getNotWith())
    print '###'
    for arc in arc_dict:
        for a in arc_dict[arc]:
            print type(a)
            print (a.getId_i(),
                a.getId_f(),
                a.getDuration(),
                a.getDistance())
    return "Sono stupido"


@app.expose("/greedy")
@service.json
def greedy():
    print ############
    print request.vars
    for r in request.vars:
        print r, ":", request.vars[r]
    print ############
    dest = 'Via Sagarat, Ferrara'
    nodelist = ['Via A. Volta, Castelguglielmo',
                'Via della Fornace, Ferrara']
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    params = dict(
        origins = '',
        destinations = '',
        mode = 'driving',#transit
        language = 'it-IT',
        units = 'metric',
        key = key
    )

    params['destinations'] = dest + "|"
    for node in nodelist:
        params['origins'] += node + "|"
        params['destinations'] += node + "|"

    params['origins'] = params['origins'][:-1]
    params['destinations'] = params['destinations'][:-1]

    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    with open('GoogleMaps.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)
    return dict(status="OK", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
