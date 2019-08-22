import json

#file = 'model1-mae.json'
file = 'model2-mse.json'

with open(file, 'r') as f:
    json_obj = json.load(f)
    for key, val in json_obj.iteritems():

        print(val) #key
        # print(json_obj['val_mean_absolute_error'])  # val
