import requests
import json

if __name__ == "__main__":
    test = ''
    if test:
        print True
    else:
        print False
    test_dict = {('1,0'):"aaaaaa", ('2,0'): "bbbbbbb", ('1,2'):"cccccc"}
    print test_dict
    key = '1'
    for k in test_dict.keys():
        k1,k2 = k.split(',')
        if k1 == key:
            print test_dict[k]

    lista = [[1,2,3], [4,5]]
    print lista.index([4,5])
    """
    url = 'http://localhost:8000/'
    with open('requestTest.json', 'r') as inputfile:
        data = json.load(inputfile)
        resp = requests.post(url, data=json.dumps(data), headers = {'content-type': 'application/json'})
    """

    a = 5
    a -= 2
    print a
