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
