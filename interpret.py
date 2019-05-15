import json

file = '/Users/suhyunkim/git/Pasion/json/model1-5-14-mse.json'

with open(file, 'r') as f:
    json_obj = json.load(f)
    for obj in json_obj:
        # print(obj) #key
        print(json_obj['val_dsc'])  # val
